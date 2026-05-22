from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 总路由配置
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('study.urls')),  # 学习任务应用路由
]

# 开发环境下配置静态文件和媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
