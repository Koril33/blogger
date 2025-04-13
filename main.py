import shutil
import tarfile
from collections import deque
from pathlib import Path
import logging
import sys
import time
from bs4 import BeautifulSoup
from getpass import getpass
from fabric import Config, Connection

# 日志配置
logger = logging.getLogger(__name__)
ch = logging.StreamHandler(sys.stdout)
fmt = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(filename)s :: %(message)s')
ch.setFormatter(fmt)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

ignore_item = ['.git', 'LICENSE']


class Node:
    cache_map = {}
    def __init__(self, source_path, destination_path, node_type):
        # 该节点的源目录路径
        self.source_path = source_path
        # 该节点生成的结果目录路径
        self.destination_path = destination_path
        # 子节点
        self.children = []
        # 节点类型：
        # 1. category 包含多个子目录
        # 2. article 包含一个 index.md 文件和 images 目录
        # 3. leaf index.md 或者 images 目录
        self.node_type = node_type
        # 描述分类或者文章的元信息（比如：文章的标题，简介和日期）
        self.metadata = None

        Node.cache_map[source_path] = self

    def __str__(self):
        return f'path={self.source_path}'


def walk_dir(dir_path_str: str, destination_blog_dir_name: str) -> Node:
    """
    遍历目录，构造树结构
    :param dir_path_str: 存放博客 md 文件的目录的字符串
    :param destination_blog_dir_name: 生成博客目录的名称
    :return: 树结构的根节点
    """

    start = int(time.time() * 1000)
    q = deque()
    dir_path = Path(dir_path_str)
    q.append(dir_path)

    # 生成目录的根路径
    destination_root_dir = dir_path.parent.joinpath(destination_blog_dir_name)
    logger.info(f'源路经: {dir_path}, 目标路径: {destination_root_dir}')

    root = None

    # 层次遍历
    while q:
        item = q.popleft()
        if item.name in ignore_item:
            logger.info(f'略过: {item.name}')
            continue
        if Path.is_dir(item):
            [q.append(e) for e in item.iterdir()]

        # node 类型判定
        node_type = 'leaf'
        if Path.is_dir(item):
            node_type = 'category'
            # 如果目录包含 index.md 则是文章目录节点
            for e in item.iterdir():
                if e.name == 'index.md':
                    node_type = 'article'
                    break

        if not root:
            root = Node(item, destination_root_dir, node_type)
        else:
            cur_node = Node.cache_map[item.parent]
            # 计算相对路径
            relative_path = item.relative_to(dir_path)
            # 构造目标路径
            destination_path = destination_root_dir / relative_path
            if destination_path.name == 'index.md':
                destination_path = destination_path.parent / Path('index.html')
            n = Node(item, destination_path, node_type)
            cur_node.children.append(n)
    end = int(time.time() * 1000)
    logger.info(f'构造树耗时: {end - start} ms')

    return root


def md_to_html(md_file_path: Path) -> str:
    """
    markdown -> html
    :param md_file_path: markdown 文件的路径对象
    :return: html str
    """

    import markdown

    def remove_metadata(content: str) -> str:
        """
        删除文章开头的 YAML 元信息
        :param content: markdown 内容
        """
        lines = content.splitlines()
        if lines and lines[0] == '---':
            for i in range(1, len(lines)):
                if lines[i] == '---':
                    return '\n'.join(lines[i+1:])
        return md_content

    with open(md_file_path, mode='r', encoding='utf-8') as md_file:
        md_content = md_file.read()
        md_content = remove_metadata(md_content)
        return markdown.markdown(
            md_content,
            extensions=[
                'markdown.extensions.toc',
                'markdown.extensions.tables',
                'markdown.extensions.sane_lists',
                'markdown.extensions.fenced_code'
            ]
        )


def gen_article_index(md_file_path: Path, article_name):
    with open('./template/article.html', mode='r', encoding='utf-8') as f:
        bs1 = BeautifulSoup(f, "html.parser")
        bs2 = BeautifulSoup(md_to_html(md_file_path), "html.parser")
        bs1.find('article').append(bs2)
        bs1.find('title').string = f'文章 | {article_name}'
        return bs1.prettify()


def gen_category_index(categories: list, category_name) -> str:
    from jinja2 import Template

    with open('./template/category.html', mode='r', encoding='utf-8') as f:
        template_content = f.read()
        template = Template(template_content)
        html = template.render(categories=categories, category_name=category_name)
        return html


def sort_categories(item):
    """
    对 categories 排序，type = category 排在所有 type = article 前
    category 按照 name 字典顺序 a-z 排序
    article 按照 metadata 的 date 字段（格式：2024-02-03T14:44:42+08:00）降序排列。
    :param item:
    :return:
    """
    from datetime import datetime
    if item['type'] == 'category':
        # 分类优先，按 name 排序
        return 0, item['name'].lower()
    elif item['type'] == 'article':
        # 文章按日期降序排序，优先级次于 category
        # 将日期解析为 datetime 对象，若无日期则排在最后
        date = item['metadata'].get('date')
        parsed_date = datetime.fromisoformat(date) if date else datetime(year=1970, month=1, day=1)
        return 1, -parsed_date.timestamp()


def gen_blog_dir(root: Node):
    """
    根据目录树构造博客目录
    :param root: 树结构根节点
    :return:
    """

    start = int(time.time() * 1000)

    q = deque()
    q.append(root)

    # 清理之前生成的 root destination
    if Path.exists(root.destination_path):
        logger.info(f'存在目标目录: {root.destination_path}，进行删除')
        shutil.rmtree(root.destination_path)

    while q:
        node = q.popleft()
        [q.append(child) for child in node.children]

        # 对三种不同类型的节点分别进行处理

        if node.node_type == 'category' and node.source_path.name != 'images':
            Path.mkdir(node.destination_path, parents=True, exist_ok=True)
            category_index = node.destination_path / Path('index.html')
            categories = []
            for child in node.children:
                if child:
                    if child.node_type == 'article':
                        child.metadata = read_metadata(child.source_path / Path('index.md'))
                    relative_path = child.destination_path.name / Path('index.html')
                    categories.append({
                        'type': child.node_type,
                        'name': child.destination_path.name,
                        'href': relative_path,
                        'metadata': child.metadata,
                    })
            categories.sort(key=sort_categories)
            with open(category_index, mode='w', encoding='utf-8') as f:
                f.write(gen_category_index(categories, node.source_path.name))

        if node.node_type == 'article':
            Path.mkdir(node.destination_path, parents=True, exist_ok=True)

        if node.node_type == 'leaf':
            Path.mkdir(node.destination_path.parent, parents=True, exist_ok=True)
            if node.source_path.name == 'index.md':
                with open(node.destination_path, mode='w', encoding='utf-8') as f:
                    f.write(gen_article_index(node.source_path, node.source_path.parent.name))
            else:
                shutil.copy(node.source_path, node.destination_path)

    end = int(time.time() * 1000)
    logger.info(f'生成目标目录耗时: {end - start} ms')


def cp_resource(dir_path_str: str):
    dir_path = Path(dir_path_str)
    # 拷贝 css
    css_destination_root_dir = dir_path.parent.joinpath('public').joinpath('css')
    shutil.copytree('./css', str(css_destination_root_dir.absolute()))
    # 拷贝 images
    images_destination_root_dir = dir_path.parent.joinpath('public').joinpath('images')
    shutil.copytree('./images', str(images_destination_root_dir.absolute()))

def read_metadata(md_file_path):
    import re
    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则提取元数据
    match = re.match(r'^---\n([\s\S]*?)\n---\n', content)
    if match:
        metadata = match.group(1)
        return parse_metadata(metadata)
    return {}


def parse_metadata(metadata):
    """
    将元数据解析为字典
    title, date, summary
    """
    meta_dict = {}
    for line in metadata.split('\n'):
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            meta_dict[key] = value
    return meta_dict


def compress_dir(blog_path: Path) -> Path:
    """
    将指定目录压缩为 public.tar.gz
    """
    logger.info(f'压缩目录: {blog_path}')
    output_tar = blog_path.parent / 'public.tar.gz'

    with tarfile.open(output_tar, "w:gz") as tar:
        tar.add(str(blog_path), arcname="public")

    logger.info(f'压缩完成: {output_tar}')
    return output_tar

def deploy(server_name: str, local_tar_path: Path, remote_web_root: str = '/var/www/dingjinghui.site/'):
    """
    将 tar.gz 文件部署到远程服务器
    """
    logger.info(f'开始部署 -> 服务器: {server_name}，文件: {local_tar_path}')

    sudo_pass = getpass("[sudo]: ")
    config = Config(overrides={'sudo': {'password': sudo_pass}})
    c = Connection(server_name, config=config)

    remote_home_path = f'/home/{c.user}'
    remote_tar_path = f'{remote_home_path}/{local_tar_path.name}'
    remote_target_path = f'{remote_web_root}blog'

    try:
        # 上传
        c.put(str(local_tar_path), remote=remote_home_path)
        logger.info('上传完成')

        # 删除旧备份
        c.sudo(f'rm -rf {remote_web_root}blog.bak')
        logger.info('旧 blog.bak 删除')

        # 备份 blog
        c.sudo(f'mv {remote_target_path} {remote_target_path}.bak')
        logger.info('blog -> blog.bak')

        # 移动 tar.gz 并解压
        c.sudo(f'mv {remote_tar_path} {remote_web_root}')
        c.sudo(f'tar -xzf {remote_web_root}{local_tar_path.name} -C {remote_web_root}')
        logger.info('解压完成')

        # 清理
        c.sudo(f'rm {remote_web_root}{local_tar_path.name}')
        c.sudo(f'mv {remote_web_root}public {remote_target_path}')
        logger.info('部署完成')

    except Exception as e:
        logger.exception(f"部署失败")
        raise

def main():
    start = time.time()

    blog_dir = Path('/home/koril/Documents/djhx.site/blog')
    public_name = 'public'

    logger.info("开始生成博客文件结构...")
    root_node = walk_dir(str(blog_dir), public_name)
    gen_blog_dir(root_node)
    cp_resource(str(blog_dir))

    tar_path = compress_dir(root_node.destination_path)
    deploy('djhx.site', tar_path)

    end = time.time()
    logger.info(f'任务完成，总耗时: {(end - start) * 1000:.0f} ms')

if __name__ == '__main__':
    main()