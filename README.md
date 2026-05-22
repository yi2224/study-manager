# 学习任务管理系统

基于Python Django的智能学习任务管理系统，集成学习任务拆分管理、任务进度自动统计、截止日期提醒、番茄钟计时、学习数据可视化统计五大核心功能。

## 项目特性

- ✅ **主任务+子任务层级管理** - 支持将大任务拆分成小任务，自动计算完成进度
- ✅ **番茄钟计时器** - 经典25分钟工作+5分钟休息的番茄工作法实现
- ✅ **智能任务提醒** - 自动筛选即将过期的任务，支持浏览器桌面通知
- ✅ **学习数据可视化** - ECharts交互式图表展示日/周学习趋势、任务完成率
- ✅ **响应式界面** - Bootstrap 5构建，完美适配电脑端
- ✅ **零配置部署** - 基于SQLite3数据库，无需配置外部数据库

## 技术栈

### 后端
- **Python 3.10**
- **Django 4.2 LTS**
- **SQLite3** 数据库
- **Pandas** 数据处理

### 前端
- **HTML5 + CSS3**
- **原生JavaScript**
- **Bootstrap 5** UI框架
- **ECharts** 可视化图表

### 核心依赖
```
django==4.2.11
django-crispy-forms==2.0
crispy-bootstrap5==0.7
pandas==2.1.4
python-dotenv==1.0.1
```

## 项目结构

```
study_manager/
├── config/                      # Django项目配置
│   ├── settings.py             # 项目设置
│   ├── urls.py                 # 总路由
│   ├── wsgi.py                 # WSGI配置
│   └── __init__.py
├── study/                       # 核心应用
│   ├── models.py               # 数据模型（MainTask、SubTask、StudyRecord）
│   ├── views.py                # 业务逻辑视图
│   ├── urls.py                 # 应用路由
│   ├── admin.py                # Django管理界面
│   ├── apps.py                 # 应用配置
│   ├── __init__.py
│   └── migrations/             # 数据库迁移文件
├── templates/                   # HTML模板
│   ├── base.html               # 基础模板
│   └── study/                  # 应用模板
│       ├── index.html          # 首页
│       ├── task_list.html      # 任务列表
│       ├── task_form.html      # 任务表单
│       ├── pomodoro.html       # 番茄钟
│       └── statistics.html     # 数据统计
├── static/                      # 静态文件
├── manage.py                    # Django管理脚本
└── requirements.txt             # 依赖配置

```

## 安装与运行

### 1. 创建Python虚拟环境

```bash
# Windows系统
python -m venv venv
venv\Scripts\activate

# macOS/Linux系统
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

### 5. 启动开发服务器

```bash
python manage.py runserver
```

### 6. 访问应用

打开浏览器，访问：
- **主应用地址**：http://127.0.0.1:8000/
- **管理后台**：http://127.0.0.1:8000/admin/

## 功能说明

### 首页（/）

展示系统介绍和核心数据看板：
- 今日学习时长
- 已完成任务数
- 待完成任务数
- 即将过期任务提醒

### 任务管理（/tasks/）

#### 创建任务
- 访问 `/tasks/create/`
- 填写任务名称、描述、截止时间
- 创建后自动跳转到任务列表

#### 任务列表
- 查看所有主任务
- 显示任务完成进度（进度条）
- 支持添加、编辑、删除主任务
- 支持添加、完成、删除子任务
- 自动计算和刷新任务进度

#### 编辑任务
- 访问 `/tasks/<task_id>/edit/`
- 修改任务信息后保存

#### 删除任务
- 点击删除按钮
- 级联删除关联的子任务和学习记录

### 番茄钟（/pomodoro/）

经典番茄工作法计时器：
- 25分钟学习 + 5分钟休息模式
- 支持开始、暂停、重置操作
- 计时完成时弹窗提醒
- 自动生成学习记录并绑定到任务
- 支持任务选择，完成后记录到对应任务

### 数据统计（/statistics/）

学习数据可视化展示：
- **统计卡片**：今日/周学习时长、任务数等
- **折线图**：最近14天学习趋势
- **饼图**：任务完成率分布
- **柱状图**：各任务学习时长排名

## 数据模型

### 主任务表（MainTask）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | 主键 | 唯一标识 |
| task_name | 字符串 | 任务名称 |
| task_desc | 文本 | 任务描述 |
| create_time | 日期时间 | 创建时间（自动） |
| deadline | 日期时间 | 截止时间 |
| progress | 浮点型 | 完成进度0-100（自动计算） |

### 子任务表（SubTask）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | 主键 | 唯一标识 |
| main_task | 外键 | 关联主任务 |
| sub_name | 字符串 | 子任务名称 |
| is_finish | 布尔值 | 完成状态 |
| create_time | 日期时间 | 创建时间（自动） |

### 学习记录表（StudyRecord）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | 主键 | 唯一标识 |
| task | 外键 | 关联主任务 |
| study_start | 日期时间 | 学习开始时间（自动） |
| study_end | 日期时间 | 学习结束时间 |
| study_duration | 整型 | 学习时长（分钟） |

## 核心业务逻辑

### 任务进度自动计算

```python
# 进度计算公式
已完成子任务数 / 总子任务数 * 100% = 任务完成进度

# 子任务状态修改时自动触发更新
在models.py中SubTask.save()方法中调用
main_task.calculate_progress()
```

### 截止提醒逻辑

系统自动筛选：
- 未完成的任务
- 截止时间 < 当前时间 + 24小时

在首页顶部红色横幅展示，支持浏览器桌面通知。

### 番茄钟计时

- 前端使用原生JavaScript实现计时逻辑
- 计时完成时自动发送AJAX请求
- 后端创建StudyRecord并自动保存

## API接口

### 子任务管理

- `POST /api/subtask/create/` - 创建子任务
- `POST /api/subtask/toggle/` - 切换子任务完成状态
- `POST /api/subtask/delete/` - 删除子任务

### 番茄钟

- `POST /api/pomodoro/finish/` - 保存学习记录

### 数据接口

- `GET /api/task/<task_id>/` - 获取任务详情（JSON格式）

## 常见问题

### Q1: 如何重置密码？

```bash
python manage.py changepassword <username>
```

### Q2: 如何清空所有数据？

```bash
# 删除数据库文件
rm db.sqlite3

# 重新迁移
python manage.py migrate
```

### Q3: 如何启用浏览器通知？

在首页点击"启用通知"按钮，授予浏览器权限后即可接收通知。

### Q4: 如何查看后台管理界面？

1. 确保已创建超级用户
2. 访问 http://127.0.0.1:8000/admin/
3. 使用创建的超级用户账号登录

## 浏览器兼容性

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- 移动浏览器（iOS Safari, Chrome Mobile）

## 性能优化建议

1. **生产环境部署**：修改 `settings.py` 中的 `DEBUG=False`
2. **静态文件优化**：运行 `python manage.py collectstatic`
3. **数据库优化**：定期备份 `db.sqlite3`
4. **缓存配置**：根据需要配置Redis缓存

## 代码规范

- 代码遵循PEP 8规范
- 核心逻辑有详细中文注释
- 分层架构清晰（MTV模式）
- 无冗余代码和硬编码路径

## 版本信息

- **系统名称**：学习任务管理系统
- **版本**：1.0
- **发布日期**：2024年
- **Python版本**：3.10
- **Django版本**：4.2 LTS

## 许可证

MIT License

## 贡献和反馈

若有问题或建议，欢迎提交反馈。

---

**祝您使用愉快！🎓**
