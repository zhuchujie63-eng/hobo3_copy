#!/bin/bash

# 确保脚本以 root 权限运行
if [ "$EUID" -ne 0 ]; then 
  echo "请使用 sudo 运行此脚本 (例如: sudo ./update_app.sh)"
  exit
fi

APP_DIR=$(pwd)
echo "正在进入应用目录: $APP_DIR"

# 1. 拉取最新代码
echo "正在拉取最新代码..."
git fetch --all
git reset --hard origin/main

# 2. 更新依赖 (如果有变化)
echo "正在检查依赖更新..."
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "警告: 未找到虚拟环境，跳过依赖更新。"
fi

# 3. 重启服务
echo "正在重启应用服务..."
systemctl restart hobo3

# 4. 检查状态
echo "服务状态检查:"
systemctl status hobo3 --no-pager

echo "==========================================="
echo "更新完成！您的网站已运行最新版本代码。"
echo "==========================================="
