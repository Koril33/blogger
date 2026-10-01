# 发布流程

## 发布前

1. 更新 `pyproject.toml` 版本及 CHANGELOG；PyPI 已发布版本不可覆盖。
2. `uv sync --group dev` 同步锁文件，执行测试和 Ruff。
3. 导出运行依赖并审计，确认没有误用开发环境或漏掉传递依赖。
4. 对示例与真实博客做完整、增量构建及 HTML/资源验证。
5. `uv build`；只选择当前版本的 wheel/sdist，避免把 dist 中旧版本一起上传。
6. `uv run twine check dist/djhx_blogger-<version>*`，检查 wheel 资源及 sdist 内容；确保不含 token、用户配置、缓存或生成站点。
7. 在隔离工具环境从 wheel 安装，验证 `blg --version`、新建示例和实际构建。

依赖审计示例：

```powershell
uv export --no-dev --no-emit-project --no-hashes -o runtime-requirements.txt
uv run pip-audit -r runtime-requirements.txt --no-deps --disable-pip
```

审计数据以运行时查询结果为准；“没有已知漏洞”不等于安全性的永久保证。发布记录应包含日期和检查范围。

## PyPI token

仓库根的 `pypi-token.txt` 已被 git 忽略。只在发布进程中读取，不输出，不写入命令参数或文档。`scripts/publish.ps1` 从 pyproject 读取当前版本，选择准确的两个构建产物，用 `UV_PUBLISH_TOKEN` 环境变量调用 `uv publish`，结束后恢复原来的环境变量。

```powershell
uv build
uv run twine check dist/djhx_blogger-0.3.1*
powershell -File scripts/publish.ps1
```

脚本不自动更改版本或运行测试；必须先完成验证再发布。上传目标是官方 PyPI，使用账号对本项目授予的 token 权限。

## 用户工具更新

发布后确认官方 PyPI 的版本和 wheel/sdist 摘要，再更新工具：

```powershell
uv tool upgrade djhx-blogger
uv tool list
blg --version
blg --help
```

私有镜像可能尚未同步，可显式使用官方索引和刷新缓存安装准确版本：

```powershell
uv tool install djhx-blogger==0.3.1 --force --refresh --default-index https://pypi.org/simple
```

最后用已安装的 `blg` 构建示例或真实博客，确认运行的是 PyPI 分发包，而不是仓库的可编辑安装。不要升级或重装无关的其他工具。
