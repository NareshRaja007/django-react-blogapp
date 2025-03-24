
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/v1/blog_app/', include('blog.urls')),  

]
