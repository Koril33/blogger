# 配置参考

`blg -c` 显示 platformdirs 计算的当前用户配置路径。Windows 默认形如 `%LOCALAPPDATA%\djhx\djhx-blogger\config.toml`；macOS/Linux 以命令输出为准。不存在的默认文件视为空配置；指定 `--config` 时文件必须存在。读取配置不会创建文件或文件夹。

优先级：**命令行值 → TOML 值 → 内置默认值**。路径相对当前工作目录解释，跨目录使用建议写绝对路径。未知节、拼错键名、错误类型及无效值都会报错，避免配置错误被静默忽略。

完整可复制模板：[config.example.toml](../config.example.toml)。

| 节 | 字段 | 默认值 / 说明 |
| --- | --- | --- |
| local | origin | 必须显式提供或使用 `-o` |
| local | target | 当前工作目录；最终输出在 `public/` |
| site | title | `DJHX BLOG` |
| site | description | `记录技术、实践与生活。` |
| site | search_url | `https://search.djhx.site/`；空字符串关闭搜索表单 |
| site | about_url | `/about/index.html`；默认页面不存在时自动隐藏，空字符串关闭关于链接 |
| site | footer / footer_url | 备案文案与地址；均可设空 |
| site | base_path | `/`；子路径例如 `/notes/` |
| build | workers | `4`，范围 1–32 |
| build | cache | `true`；内容与输出都通过 SHA-256 校验后复用 |
| build | compress_images | `true` |
| build | image_quality | `85`，范围 1–95 |
| build | max_width / max_height | `1920`；范围 1–32768 |
| deploy | server / target | 部署时必填；target 为远程父目录 |
| deploy | user / port | `koril` / `22` |
| deploy | identity_file | 未配置时交给 SSH agent 和 SSH 配置 |
| deploy | known_hosts | `~/.ssh/known_hosts` 与系统 host keys |
| deploy | sudo | `true`；有写权限的用户可设 `false` |
| deploy | timeout | `120` 秒，连接和远程命令超时 |
| deploy | compression_level | `1`，范围 0–9；JPEG 等已压缩资源使用较低等级节约 CPU |
| search | enabled | `true`；可用 `--no-refresh` 临时关闭 |
| search | refresh_url | `https://search.djhx.site/refresh-db` |
| search | timeout | `30` 秒 |

搜索/备案地址仅接受 HTTP(S)，关于链接允许同站相对路径。`base_path` 不允许 `..`、反斜杠、控制字符或协议相对 URL。

Windows TOML 路径建议使用单引号：

```toml
[local]
origin = 'C:\Project\blog'
target = 'C:\Project\blog-output'
```

密码不写入 TOML，不通过命令行值传递。非交互部署可使用 `DJHX_BLOGGER_SSH_PASSWORD` 和 `DJHX_BLOGGER_SUDO_PASSWORD` 环境变量；优先采用 SSH 密钥和最小权限账户。

## 从 0.2.3 迁移

已有 `[local] origin/target` 和 `[deploy] server/target` 可直接继续使用。原 `target` 的含义和远程 `target/blog` 的入口不变。新版首次输出会写入私有构建清单，后续构建自动增量；打包时排除清单。

原来共用一个密码的 SSH/sudo 认证现已拆开：没有密钥时添加 `--password` 输入 SSH 密码，sudo 会单独提示。建议先运行一次普通构建，再按部署文档核实 SSH 和服务路径。Python 最低要求从声明的 3.9 调整到 3.10；旧版实际无条件导入 `tomllib`，在 3.9/3.10 上无法正常启动，新版对 3.10 使用 `tomli` 兼容。
