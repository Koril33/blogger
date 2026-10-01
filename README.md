# djhx-blogger

把 Markdown 文件夹变成一个可阅读、可搜索的静态博客。`blg` 支持增量构建、图片优化、文章归档、草稿标记，以及经过校验的 SSH 部署。

**Python ≥ 3.10 · Windows / macOS / Linux · 无前端构建工具 · 无 CDN 依赖**

## 开始使用

```powershell
uv tool install djhx-blogger
blg --version
blg --help
```

已有博客：

```powershell
blg -o "C:\Project\blog" -t "C:\Project\blog-output"
python -m http.server 8000 --directory "C:\Project\blog-output\public"
```

浏览器打开 `http://localhost:8000`。`-t` 指定输出的**父目录**，生成结果在其下的 `public/`。源目录和输出目录必须分开。

创建一个示例：

```powershell
blg -n ./demo
blg -o ./demo/simple-blog -t ./output
```

## 文章格式

```text
blog/
├── about/index.md
└── software/
    └── 第一篇文章/
        ├── index.md
        ├── images/example.png
        └── attachment.pdf
```

`index.md` 所在目录是文章；其他内容目录是分类。普通 `.md` 文件也会生成同名 `.html` 页面。附件原样复制，`images/` 只存放资源，不生成分类页。

```markdown
---
title: "第一篇文章"
date: 2026-10-01T09:30:00+08:00
summary: "这篇文章讨论什么。"
draft: true
---

## 开始

正文，支持代码块、表格和 [TOC]。
```

`draft: true` 表示未完成，文章页、分类页和归档都会显示标记。草稿**仍然发布并参与搜索**，不能用它隐藏秘密。写完后改为 `draft: false`，或删除这个字段。旧文章没有标记时按已完成处理。

```powershell
blg -o ./blog -p "software/新文章"
```

新文章默认是草稿，不覆盖已有文章。

## 配置与部署

```powershell
blg -c                          # 查看默认配置路径
blg --config ./config.toml      # 使用指定配置
blg --archive                   # 构建并打包，使用配置中的源/输出路径
blg -d                         # 构建 → 打包 → SSH 部署 → 刷新搜索
uv tool upgrade djhx-blogger
```

配置示例见 [config.example.toml](config.example.toml)。原来的 `[local]`、`[deploy]` 配置和 `-o/-t/-s/-T/-d/-n/-p/-c` 保留；命令行值优先。

远程部署需要 Linux、Python 3.9+、可信的 SSH host key，以及目标目录的写权限。默认 SSH 用户仍为 `koril`，可配置；SSH 默认使用密钥或 agent，密码认证使用 `--password`。SSH 密码和 sudo 密码分开输入。部署按完整 release 切换，保留上一版 `blog.bak`；迁移步骤见 [部署文档](docs/deployment.md)。

## 这次翻修解决了什么

- 构建在独立暂存目录进行，任何转换或图片任务失败都会保留旧站点；重复调用不再受全局进程池影响。
- 文件按内容校验缓存，未变化的 HTML 和图片自动复用，删除的源文件不会残留在新站点。
- 正确读取 YAML、BOM、CRLF、带时区日期、多行摘要与缺省元数据，标题统一使用 `title`。
- 保留图片透明度和动画，处理 JPEG 方向；附件不再误当图片，损坏图片会报错。
- 所有模板元信息默认转义，链接使用 URL 编码；拒绝路径重叠、符号链接、输出冲突和目录穿越。
- 部署校验 SSH 主机、上传摘要和归档成员，先准备新站点再切换，防止命令注入和半成品上线。
- 本地样式与代码高亮，浅色/深色主题，响应式目录、搜索表单、代码复制和键盘可访问性。

## 文档导航

| 文档 | 内容 |
| --- | --- |
| [使用手册](docs/usage.md) | 命令、目录规则、元数据、图片、草稿和故障排查 |
| [配置参考](docs/configuration.md) | 完整配置项、默认值、迁移与优先级 |
| [架构与取舍](docs/architecture.md) | 三个项目的关系、构建事务、缓存、并发和部署协议 |
| [页面设计](docs/design.md) | 排版、主题、响应式与搜索服务的 HTML 约定 |
| [开发指南](docs/development.md) | 模块、测试、检查、调试、扩展方法 |
| [部署与回滚](docs/deployment.md) | SSH、release 布局、旧版迁移、恢复和搜索刷新 |
| [发布流程](docs/releasing.md) | 构建检查、PyPI token、发布与 uv tool 更新 |
| [修复与验证记录](docs/audit.md) | 原问题、修复、验证范围和性能实测 |
| [草稿整理记录](docs/draft-review.md) | 本次补标的文章与判断依据 |
| [版本记录](CHANGELOG.md) | 0.3.1 的改动与兼容说明 |

## 开发

```powershell
uv sync --group dev
uv run pytest
uv run ruff check src tests
uv run ruff format --check src tests
uv build
uv run twine check dist/djhx_blogger-0.3.1*
```

Markdown 正文允许作者编写原始 HTML。输入应来自可信作者；它不是针对不可信多用户投稿的 HTML 清洗服务。其他安全边界见 [架构文档](docs/architecture.md)。

MIT License。
