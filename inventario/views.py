from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Producto
from .forms import ProductoForm

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer, ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by("nombre")
    serializer_class = ProductoSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# READ (List)
def producto_list(request):
    """Vista para listar todos los productos"""
    productos = Producto.objects.filter(activo=True)
    return render(request, 'inventario/producto_list.html', 
                  {'object_list': productos})

# READ (Detail) 
def producto_detail(request, pk):
    """Vista para mostrar el detalle de un producto"""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    return render(request, 'inventario/producto_detail.html', 
                  {'object': producto})

# CREATE
@csrf_protect
def producto_create(request):
    """Vista para crear un nuevo producto"""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente')
            return redirect('producto_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/producto_form.html', {'form': form})

# UPDATE
@csrf_protect
def producto_update(request, pk):
    """Vista para actualizar un producto existente"""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            producto_actualizado = form.save()
            messages.success(request, f'Producto "{producto_actualizado.nombre}" actualizado exitosamente')
            return redirect('producto_detail', pk=producto.pk)
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/producto_form.html', 
                  {'form': form, 'producto': producto})

# DELETE
@csrf_protect
def producto_delete(request, pk):
    """Vista para eliminar un producto"""
    producto = get_object_or_404(Producto, pk=pk, activo=True)
    
    if request.method == 'POST':
        # Eliminación lógica (marcar como inactivo)
        producto.activo = False
        producto.save()
        
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente')
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Producto eliminado exitosamente'})
        
        return redirect('producto_list')
    
    return render(request, 'inventario/producto_confirm_delete.html', 
                  {'object': producto})