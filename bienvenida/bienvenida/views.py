from django.http import HttpResponse

def inicio(request):
    nombre = "SebaMorales74"
    return HttpResponse(f"¡Bienvenidos a mi primera app Django, {nombre}!")