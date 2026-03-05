# 国内云服务器部署指南

由于国外平台（Render/Vercel）存在支付或功能限制，您可以选择购买一台国内云服务器（如阿里云、腾讯云）来部署本项目。这通常更稳定且访问速度更快。

## 第一步：购买云服务器

1. **选择服务商**：推荐阿里云 (Aliyun) 或 腾讯云 (Tencent Cloud)。
2. **选择配置**：
   - **操作系统**：推荐选择 **Ubuntu 20.04 LTS** 或 **Ubuntu 22.04 LTS** (本指南基于 Ubuntu)。
   - **CPU/内存**：最低配置 1核 2GB 内存即可运行，推荐 2核 4GB 以获得更好性能。
   - **带宽**：按量付费或固定带宽（如 3Mbps+）均可。
3. **购买后**：
   - 获取服务器的 **公网 IP 地址**。
   - 设置 `root` 用户的密码。

## 第二步：连接服务器

在您的电脑上（Windows 使用 PowerShell 或 CMD），使用 SSH 连接服务器：

```bash
ssh root@<您的服务器公网IP>
# 例如: ssh root@123.45.67.89
# 输入密码登录
```

## 第三步：上传代码

您可以通过多种方式将代码上传到服务器。

### 方法 A：使用 Git（推荐）

1. 确保您的代码已推送到 GitHub/Gitee。
2. 在服务器上克隆仓库：
   ```bash
   git clone https://github.com/zhuchujie63-eng/hobo3_copy.git
   cd hobo3_copy
   ```

### 方法 B：直接上传文件（如果不使用 Git）

在您的本地电脑项目目录下，使用 `scp` 命令上传（排除虚拟环境和临时文件）：

```bash
# 在本地 PowerShell 中执行
scp -r . root@<服务器IP>:/root/hobo3
```

## 第四步：一键部署

1. 进入项目目录（如果还没进入）：
   ```bash
   cd /root/hobo3  # 或者您的实际目录
   ```

2. 创建 `.env` 文件并填入 API Key：
   ```bash
   nano .env
   ```
   在编辑器中粘贴您的环境变量（参考本地 `.env` 文件）：
   ```
   DEEPSEEK_API_KEY=your_key_here
   MINIMAX_API_KEY=your_key_here
   MINIMAX_GROUP_ID=your_id_here
   ```
   按 `Ctrl+O` 保存，按 `Enter` 确认，按 `Ctrl+X` 退出。

3. 运行部署脚本：
   ```bash
   # 赋予执行权限
   chmod +x setup_server.sh
   
   # 运行脚本
   sudo ./setup_server.sh
   ```

## 第五步：访问网站

脚本执行完成后，打开浏览器访问：`http://<您的服务器公网IP>`

如果无法访问，请检查云服务商的控制台（防火墙/安全组设置），确保 **80 端口** 已开放。

## 常用维护命令

- **重启服务**：`sudo systemctl restart hobo3`
- **查看运行状态**：`sudo systemctl status hobo3`
- **查看应用日志**：`sudo journalctl -u hobo3 -f`
