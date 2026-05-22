#!/bin/bash

# 学习任务管理系统 - 快速启动脚本

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     学习任务管理系统 - Django 项目启动脚本              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${BLUE}[1/5] 创建虚拟环境...${NC}"
    python -m venv venv
    echo -e "${GREEN}✓ 虚拟环境创建成功${NC}"
fi

# 激活虚拟环境
echo -e "${BLUE}[2/5] 激活虚拟环境...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ 虚拟环境已激活${NC}"

# 安装依赖
echo -e "${BLUE}[3/5] 安装项目依赖...${NC}"
pip install -r requirements.txt -q
echo -e "${GREEN}✓ 依赖安装完成${NC}"

# 数据库迁移
echo -e "${BLUE}[4/5] 执行数据库迁移...${NC}"
python manage.py migrate -q
echo -e "${GREEN}✓ 数据库迁移完成${NC}"

# 启动开发服务器
echo -e "${BLUE}[5/5] 启动开发服务器...${NC}"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}服务器已启动！请在浏览器中访问：${NC}"
echo -e "${GREEN}http://127.0.0.1:8000/${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""

python manage.py runserver
