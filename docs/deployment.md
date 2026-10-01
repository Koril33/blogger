# 部署与回滚

## 前置条件

远程为 Linux/POSIX 环境，安装 Python 3.9+ 和 `mktemp`，SSH 用户能上传到 `/tmp`。配置中的 `deploy.target` 是父目录，站点路径保持 `<target>/blog`。已有 Nginx `root /var/www/djhx.site/blog` 可以继续使用；它需要允许读取 release 目录及目录符号链接。

先用独立 SSH 流程核实服务器指纹并写入 `known_hosts`。新版使用 Paramiko `RejectPolicy`；不会静默接受未知服务器。支持 SSH alias、agent、密钥文件；密码认证通过 `--password`，sudo 密码另行输入。两者也可通过文档规定的环境变量传递，不会存入配置。

```powershell
blg -o "C:\Project\blog" -t "C:\Project\blog-output" -d `
  -s djhx.site -T /var/www/djhx.site --ssh-user koril
```

不需要 sudo 的账户：

```powershell
blg --config ./config.toml -d --no-sudo
```

## 目录结构

```text
<target>/
├── blog -> .blogger/releases/<current-id>
├── blog.bak -> .blogger/releases/<previous-id>
└── .blogger/
    ├── owner
    └── releases/
        ├── <current-id>/
        ├── <previous-id>/
        └── legacy-<id>/       # 旧版目录的迁移备份
```

上传在随机 `/tmp/djhx-blogger.*` 目录完成。客户端先验证归档，再上传归档和 helper；远程校验 SHA-256、展开到全新 release、限制归档类型和路径，并检查 `index.html/archive.html`。文件权限规范为文件 0644、目录 0755。

正常更新通过 `os.replace` 替换 `blog` 符号链接，切换之前用户继续访问旧版。每次更新保留当前与上一 release，旧的托管 release 在成功后清理。`legacy-*` 目录保留给人工核对，不自动删除。

旧版 `blog` 为实体目录时，第一次需要将它移入 `legacy-*` 后设置入口链接，有很短的迁移间隙；切换失败会恢复实体目录。原 `blog.bak` 实体目录也会被保存。目录与链接验证失败时停止操作，不覆盖未知文件。

远程 `.blogger/deploy.lock` 防止同父目录并发切换。进程被强制终止时可能留下 lock 或暂存 release；先确认无部署运行，再人工处理。正常错误会清理 lock 和未上线 release。连接关闭和上传临时目录清理由客户端负责。

## 回滚

先通过 SSH 查看并确认 `blog`、`blog.bak` 的链接和内容。在目标父目录内，用临时链接再原子替换入口，示意命令：

```sh
cd /var/www/djhx.site
readlink blog
readlink blog.bak
ln -s "$(readlink blog.bak)" .blogger-rollback
mv -Tf .blogger-rollback blog
```

目标目录需要相应写权限，必要时使用 sudo。回滚后重新调用搜索刷新，使索引与站点一致。这个过程保留 release 内容；下次发布仍会识别当前入口并保留它作为上一版。

## 搜索刷新

仅在远程切换成功后 GET `search.refresh_url`，默认 30 秒超时。预期响应为 `{"success": true, ...}`。刷新失败时站点已经上线，CLI 返回 3 并说明原因，不重新部署或回滚站点。

```powershell
blg -d --no-refresh
```

搜索服务的 `BLOG_PATH` 应指向 `<target>/blog`。本次搜索兼容修复加入明确页面类型识别，服务代码需要部署到搜索服务才会生效；仅安装新版 `blg` 不会更新 Flask 服务代码。带普通附件或独立 Markdown 页依赖这个修复，旧的标准 index.md + images 布局仍兼容原服务。

新版不会自动修改 Nginx、重启搜索服务或迁移其数据库。
