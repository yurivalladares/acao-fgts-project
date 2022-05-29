from django.contrib import admin

from .models import IndicePeriodo

class ListandoIndicePeriodo(admin.ModelAdmin):
    list_display = ('periodo_format', 'indice_jam_3', 'indice_jam_6', 'variacao_inpc')
    list_display_links = ('periodo_format',)
    search_fields = ('periodo_format',)
    list_filter = ('periodo_ano',)
    list_per_page = 12
    ordering = ('-periodo',)

    def periodo_format(self, obj):
        return obj.periodo.strftime('%Y-%m')

    periodo_format.admin_order_field = 'periodo'
    periodo_format.short_description = 'Período'

admin.site.register(IndicePeriodo, ListandoIndicePeriodo)