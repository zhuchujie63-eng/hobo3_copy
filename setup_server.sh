#!/bin/bash

# 确保脚本以 root 权限运行
if [ "$EUID" -ne 0 ]; then 
  echo "请使用 sudo 运行此脚本 (例如: sudo ./setup_server.sh)"
  exit
fi

echo "正在更新系统软件包..."
apt-get update

echo "正在安装系统依赖 (Python3, pip, ffmpeg, nginx)..."
apt-get install -y python3-pip python3-venv ffmpeg nginx git

# 创建虚拟环境
echo "正在创建 Python 虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
echo "正在安装 Python 依赖..."
source venv/bin/activate
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "警告: 未找到 requirements.txt，跳过依赖安装。"
fi

# 获取当前目录作为应用目录
APP_DIR=$(pwd)
SERVICE_FILE="/etc/systemd/system/hobo3.service"

echo "正在配置 Systemd 服务..."
# 创建 systemd 服务文件
cat > $SERVICE_FILE <<EOF
[Unit]
Description=Hobo3 Flask App
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}"
Environment="MINIMAX_API_KEY=${MINIMAX_API_KEY}"
Environment="MINIMAX_GROUP_ID=${MINIMAX_GROUP_ID}"
# 如果有 .env 文件，可以直接读取，或者在这里硬编码环境变量
# EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd 并启动服务
systemctl daemon-reload
systemctl start hobo3
systemctl enable hobo3

echo "正在配置 Nginx 反向代理..."
NGINX_CONF="/etc/nginx/sites-available/hobo3"
cat > $NGINX_CONF <<EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # 增加超时时间以支持长请求（如视频下载）
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}
EOF

# 启用 Nginx 配置
ln -sf $NGINX_CONF /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试并重启 Nginx
nginx -t && systemctl restart nginx

echo "==========================================="
echo "部署完成！"
echo "您的应用现在应该可以通过服务器的公网 IP 访问了 (端口 80)。"
echo "如果遇到问题，请检查服务状态: sudo systemctl status hobo3"
echo "查看日志: sudo journalctl -u hobo3 -f"
echo "注意：请确保在 $APP_DIR/.env 文件中配置了正确的 API Key。"
echo "==========================================="
