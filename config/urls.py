"""acao_fgts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from acao_fgts.apps.calculo.views import index, calcular_fgts, deletar_calculo, memoria_calculo, MemoriaPdf, como_funciona
from acao_fgts.apps.user.views import cadastro, login, logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('calcularfgts/', calcular_fgts, name='calcular_fgts'),
    path('comofunciona/', como_funciona, name='como_funciona'),
    path('deletarcalculo/', deletar_calculo, name='deletar_calculo'),
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('memoriacalculo', memoria_calculo, name='memoria_calculo'),
    path('memoria_pdf', MemoriaPdf.as_view(), name='memoria_pdf')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

