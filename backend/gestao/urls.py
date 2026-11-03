from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from escola import visualizacao as escola_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/login/', auth_views.LoginView.as_view(template_name='telas/login.html'), name='login'),
    path('contas/cadastro/', escola_views.cadastro, name='cadastro'),
    path('cadastro/', escola_views.cadastro),
    path('contas/', include('django.contrib.auth.urls')),
    path('', include('escola.urls')),
]
