from django.contrib import admin

from .models import CalculoFgts
from django.contrib.auth.models import User

class ListandoCalculoFgts(admin.ModelAdmin):
    list_display = ('created_at', 'username', 'nome_completo', 'valor_causa', 'pago', 'hide')
    list_display_links = ('created_at', 'username', 'nome_completo',)
    search_fields = ('username', 'nome_completo',)
    list_editable = ('hide',)
    list_per_page = 20
    ordering = ('-created_at',)

admin.site.register(CalculoFgts, ListandoCalculoFgts)