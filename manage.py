#!/usr/bin/env python
import os
import sys


def main():
    """Django管理脚本入口"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django导入失败. 请确保已安装Django依赖包."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
