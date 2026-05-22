@echo off
REM 学习任务管理系统 - Windows快速启动脚本

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     学习任务管理系统 - Django 项目启动脚本              ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo [1/5] 创建虚拟环境...
    python -m venv venv
    echo ✓ 虚拟环境创建成功
) else (
    echo [1/5] 虚拟环境已存在
)

REM 激活虚拟环境
echo [2/5] 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✓ 虚拟环境已激活

REM 安装依赖
echo [3/5] 安装项目依赖...
pip install -r requirements.txt -q
echo ✓ 依赖安装完成

REM 数据库迁移
echo [4/5] 执行数据库迁移...
python manage.py migrate -q
echo ✓ 数据库迁移完成

REM 启动开发服务器
echo [5/5] 启动开发服务器...
echo.
echo ════════════════════════════════════════════════════════
echo 服务器已启动！请在浏览器中访问：
echo http://127.0.0.1:8000/
echo ════════════════════════════════════════════════════════
echo.

python manage.py runserver

pause
