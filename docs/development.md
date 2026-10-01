# 开发指南

## 环境与检查

```powershell
uv sync --group dev
uv run blg --version
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv build
uv run twine check dist/djhx_blogger-0.3.1*
```

开发依赖保存在 `dev` 组，不进入用户的工具安装。`uv.lock` 纳入版本控制，明确记录直接与传递依赖。`pyproject.toml` 同时声明安全版本下限，确保没有使用本仓库锁文件的 PyPI 用户也获得已修复依赖。

Windows 受限环境可把缓存、环境与 pytest 临时目录放在仓库里：

```powershell
$env:UV_CACHE_DIR = "$PWD/.cache/uv"
$env:UV_PROJECT_ENVIRONMENT = "$PWD/.cache/venv"
uv sync --group dev
uv run pytest --basetemp .cache/pytest -p no:cacheprovider
```

不要把 `--basetemp` 指向用户数据目录：pytest 拥有该目录并可能清空它。

## 模块分工

| 模块 | 责任 |
| --- | --- |
| `cli.py` | Typer 参数、优先级、动作选择、退出码 |
| `config.py` | TOML、站点/构建配置与值检查 |
| `content.py` | YAML、日期、Markdown 渲染与源码摘要 |
| `gen.py` | 树发现、导航/归档、缓存、工作调度、构建提交 |
| `images.py` | 格式判断、保守图片优化 |
| `deploy.py` | 打包、SSH 客户端、上传、刷新搜索 |
| `remote_deploy.py` | 上传至服务器的纯标准库 helper，校验展开与 release 切换 |
| `log_config.py` | 只配置工具自身的日志，不重写 root logger |

库导入不创建线程池、不读配置、不创建用户目录、不配置宿主程序日志。CLI 在命令执行时初始化日志。

## 测试重点

测试检查实际结果与失败边界，不连接生产服务器或刷新线上搜索：

- YAML/BOM/CRLF、多行摘要、安全解析、缺省日期、UTC 排序、正文扩展。
- 草稿三处展示、标题转义、中文/空格 URL、独立 Markdown 和附件。
- 增量复用、同文件变化、输出损坏、删除文件、配置变化。
- 图片失败、源文件在构建中被修改、提交阶段失败时保留旧输出。
- 输出重叠、目录所有权、链接、名称冲突、构建 lock。
- alpha、动画、EXIF 方向、较小文件优先与解压炸弹。
- 可复现归档、路径穿越/链接归档拒绝、SSH host key 策略、shell 参数边界、上传清理。
- 远程摘要/展开失败、首次迁移、重复部署保留数量、切换失败恢复。
- 兼容 CLI、配置优先级、部署失败不刷新、刷新失败退出码 3。

远程真实符号链接测试在无法创建 symlink 的 Windows 主机上跳过，在 Linux CI 执行。同时用 pyfakefs 的 POSIX 模拟覆盖首次迁移、连续切换、保留数量和旧站点/备份恢复。本次本机为 67 通过、2 项真实 symlink 测试跳过。测试 fixture 只使用临时目录；禁止将真实博客或服务器目录作为测试清理目标。

## 修改约定

改变处理逻辑时提高缓存协议或包版本，确保旧输出不会被错误复用；影响模板的配置必须进入渲染指纹，影响图片字节的策略必须进入图片指纹。修改静态资源后它们会在每次构建中重新写出。

新增元数据先在 `content.py` 定义类型和默认值，再在模板中消费，最后补实际输出测试。保留 `.article-content`、文章标题与发布日标签，避免破坏搜索。

修改远程 helper 时保持 Python 3.9+、纯标准库，不依赖服务器安装 blogger。解压过程不能采用不受限制的 `extractall`；只允许普通文件/目录，并在任何旧入口移动前完成全部验证。

## 手工验证

用示例博客和真实博客各构建一次，再运行相同命令检查复用数。HTTP 预览检查首页、含长代码/表格的文章、草稿和归档；分别覆盖桌面与窄屏、浅色与深色。检查代码复制不带按钮文字、目录锚点可跳转、页面没有整体水平溢出。

发布前还需验证 wheel 包含模板/CSS/JS/favicon，在干净工具环境运行 `blg -n` 与构建，避免仅在可编辑安装里有效。
