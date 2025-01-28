import shutil
from collections import deque
from pathlib import Path

from bs4 import BeautifulSoup


class Node:
    cache_map = {}
    def __init__(self, source_path, destination_path):
        self.source_path = source_path
        self.destination_path = destination_path
        self.children = []
        self.node_type = None
        self.metadata = None
        Node.cache_map[source_path] = self

    def __str__(self):
        return f'path={self.source_path}'


def walk_dir(dir_path_str: str) -> Node:
    """
    遍历目录，构造树结构
    :param dir_path_str: 目标目录
    :return: 树结构的根节点
    """
    q = deque()
    dir_path = Path(dir_path_str)
    q.append(dir_path)
    destination_root_dir = dir_path.parent.joinpath('public')
    root = None
    while q:
        item = q.popleft()
        if Path.is_dir(item):
            [q.append(e) for e in item.iterdir()]

        node_type = 'leaf'
        if Path.is_dir(item):
            node_type = 'category'
            for e in item.iterdir():
                if e.name == 'index.md':
                    node_type = 'article'
                    break


        if not root:
            root = Node(item, destination_root_dir)
            root.node_type = node_type
        else:
            cur_node = Node.cache_map[item.parent]
            # 计算相对路径
            relative_path = item.relative_to(dir_path)
            # 构造目标路径
            destination_path = destination_root_dir / relative_path
            if destination_path.name == 'index.md':
                destination_path = destination_path.parent / Path('index.html')
            n = Node(item, destination_path)
            n.node_type = node_type
            cur_node.children.append(n)

    return root


def md_to_html(md_file_path: Path) -> str:
    import markdown

    with open(md_file_path, mode='r', encoding='utf-8') as md_file:
        return markdown.markdown(
            md_file.read(),
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


def gen_blog_dir(root: Node):
    """
    根据目录树构造博客目录
    :param root: 树结构根节点
    :return:
    """
    q = deque()
    q.append(root)

    # 清理之前生成的 root destination
    if Path.exists(root.destination_path):
        print('存在 root destination 目录，进行删除')
        shutil.rmtree(root.destination_path)

    while q:
        node = q.popleft()
        [q.append(child) for child in node.children]

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


def cp_css(dir_path_str: str):
    dir_path = Path(dir_path_str)
    destination_root_dir = dir_path.parent.joinpath('public').joinpath('css')
    shutil.copytree('./css', str(destination_root_dir.absolute()))


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
    """将元数据解析为字典"""
    meta_dict = {}
    for line in metadata.split('\n'):
        if ':' in line:
            key, value = map(str.strip, line.split(':', 1))
            meta_dict[key] = value
    return meta_dict


def main():
    dir_path_str = '/home/koril/project/djhx.site/blog'
    root_node = walk_dir(dir_path_str)
    gen_blog_dir(root_node)
    cp_css(dir_path_str)


if __name__ == '__main__':
    main()