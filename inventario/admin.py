from django.contrib import admin
from .models import Producto

from io import BytesIO
from openpyxl import Workbook
from django.http import HttpResponse


@admin.action(description="Exportar Productos a Excel")
def exportar_productos_excel(modeladmin, request, queryset):
    # Crear libro y hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Productos"

    # Encabezados
    ws.append(["nombre", "precio", "stock", "activo", "fecha_creacion", "fecha_actualizacion"])

    # Filas de datos
    for producto in queryset:
        ws.append([
            producto.nombre,
            producto.precio,
            producto.stock,
            producto.activo,
            producto.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            producto.fecha_actualizacion.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    # Guardar en buffer en memoria y responder
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="productos.xlsx"'
    return response


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'activo',
                    'fecha_creacion', 'fecha_actualizacion')
    list_filter = ('activo', 'fecha_creacion', 'precio')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('stock', 'activo')
    ordering = ('-fecha_creacion',)
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Precio y Stock', {
            'fields': ('precio', 'stock')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    actions = [ exportar_productos_excel ]
