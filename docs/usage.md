# 使用手册

## 命令

`blg` 是单命令工具，不需要写 `run`。`python -m djhx_blogger` 是等价入口。

| 参数 | 作用 |
| --- | --- |
| `-o / --origin PATH` | Markdown 源目录 |
| `-t / --target PATH` | 输出父目录，生成到 `PATH/public` |
| `-n / --new-blog PATH` | 创建 `PATH/simple-blog` 示例，已有目录时报错 |
| `-p / --new-post NAME` | 在源目录创建文章，可包含分类路径；默认 `draft: true` |
| `-c / --config-path` | 只打印配置地址，不创建目录、不读取配置 |
| `--config PATH` | 显式指定 TOML 文件；不存在或格式错误时退出 |
| `--archive` | 构建后打包 `public.tar.gz` |
| `-d / --deploy` | 构建、打包、部署，成功后刷新搜索 |
| `-s / --server HOST` | 覆盖 SSH 主机/别名 |
| `-T / --server-target PATH` | 覆盖远程父目录，入口为其下 `blog` |
| `--ssh-user USER`、`--port PORT` | 覆盖 SSH 用户与端口 |
| `--identity-file PATH` | SSH 私钥 |
| `--password` | 交互输入 SSH 密码 |
| `--no-sudo` | 以 SSH 用户权限部署 |
| `--workers N` | 1–32 个工作线程，默认 4 |
| `--no-cache` | 禁用内容缓存，重新转换/处理 |
| `--no-compress` | 原样复制图片 |
| `--no-refresh` | 这次部署跳过搜索刷新 |
| `-v / --verbose` | 输出错误堆栈 |
| `--version`、`--help` | 查看版本/帮助，不进行构建 |

新建动作不能与打包或部署混用。失败使用非零退出码：`1` 为操作失败，`2` 为 Typer 参数语法错误，`3` 为博客已上线但搜索刷新失败。

## 内容发现规则

1. 含 `index.md` 的目录渲染为文章；`INDEX.md` 也统一输出 `index.html`。
2. 没有文章首页的普通目录渲染为分类；分类优先按名称排序，文章按真实时间倒序。
3. 独立 `note.md` 转换成 `note.html`，加入父分类和归档。指向本地 `.md` 的正文链接会改成 `.html`，保留查询参数和锚点。
4. 其他文件作为附件复制。`images/` 及其中的目录仅作为资源，不加入分类列表。
5. 忽略所有以 `.` 开头的条目以及 `LICENSE`、`node_modules`、`__pycache__`。`.git`、`.env` 和编辑器目录不会发布。
6. 拒绝符号链接、Windows junction 和非常规文件，避免泄露博客目录之外的内容或进入循环。
7. 根目录的 `css`、`js`、`archive.html` 为保留名称；每个内容目录的 `index.html` 由生成器所有。输出冲突会明确报错。

输入是 UTF-8，支持 UTF-8 BOM 和 CRLF。构建不会写源文件；新建命令才会写文章。

## 元数据

| 字段 | 格式与用途 |
| --- | --- |
| `title` | 字符串；缺省用文章目录名或 Markdown 文件名 |
| `summary` | 字符串；缺省空；可用 YAML `|` / `>` 写多行文本 |
| `date` | ISO 8601 日期或日期时间；推荐 `2026-10-01T09:30:00+08:00` |
| `draft` | YAML 布尔值 `true` / `false`；缺省 `false` |

日期为空或无效时放在归档的“未注明日期”分组，无效日期会提示。无时区日期按 UTC 排序，不受构建机器所在时区影响；页面保留原始日期文本。`tags`、`featured_image`、`toc` 等旧字段可继续保留，当前不用于页面导航或封面布局。

`draft: true` 会显示“未完成”及文章页提示。它不改变 URL、排序、归档数量或搜索可见性。判断文章是否未完成由作者明确标记，构建器不按长度或关键词自动推断。

```yaml
summary: |
  第一段摘要。
  第二段摘要。
draft: true
```

元信息使用安全 YAML 解析器，拒绝 Python 对象标签和错误类型。YAML 引号会按正常字符串解析，不会出现在标题两端。

## 图片

JPEG、PNG、WebP 支持保守压缩，默认质量 85、最长宽高均为 1920，保持比例、不放大。JPEG 根据 EXIF 调整方向，压缩产物不保留 EXIF；PNG 保留透明度，WebP 保留 alpha。动画和 GIF、TIFF、BMP、ICO 等格式原样复制，SVG 等附件原样复制。

只有候选文件更小时才采用，否则保留原文件。因此尺寸限制是优化目标，而不是在所有输入上强制改变尺寸的保证。原样复制的文件会保留其已有元数据。损坏的待压缩图片或 Pillow 判定的解压炸弹会使构建失败，旧站点不受影响。

高清截图需要完整分辨率时使用 `--no-compress`，或在 `[build]` 调大 `max_width/max_height`。

## 本地浏览

用 HTTP 服务预览，不要直接双击 HTML；默认导航和资源采用从站点根开始的路径。部署到子路径时设置 `site.base_path = "/notes/"`，同时让预览服务器把 `public` 挂载到 `/notes/`。正文里作者写的根路径链接不自动加前缀。

## 常见问题

- **“源目录与输出目录不能重叠”**：把 `-t` 改到源目录之外。
- **“拒绝覆盖非 blogger 输出目录”**：检查 `public` 是否放了用户文件；将旧目录改名保存，使用空的输出位置。旧版生成的标准目录可直接迁移。
- **“输出目录正被另一构建占用”**：等待另一构建结束。如果进程异常终止，确认没有构建仍在运行，再删除输出父目录的 `.blogger-public.lock`。
- **构建失败**：先读错误中的具体文件；加 `-v` 获得堆栈。暂存目录会清理，旧输出保留。
- **搜索没有新文章**：先确认部署已成功，检查搜索的 `BLOG_PATH` 是否指向远程 `blog`，再单独调用刷新接口；退出码 3 不意味着博客部署回滚。
- **SSH 报主机密钥未知或变化**：用正常 SSH 流程独立核实主机指纹后记录到 `known_hosts`，不要绕过校验。

程序库入口 `generate_blog(origin, target, site=SiteConfig(...), options=BuildOptions(...))` 返回 `Node`，其 `destination_path` 是最终目录、`stats` 为耗时、处理/复用文件数等统计。旧 `gen` 模块的元数据、Markdown、图片帮助函数仍可导入；内部全局缓存和进程池已移除。
