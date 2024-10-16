from django.http import JsonResponse
from django.shortcuts import render
from .models import Estado, Municipio
from django.http import HttpResponse

# Create your views here.
def index(request):
    estados = Estado.objects.all()
    return render(request, 'polls/index.html', {'estados': estados})

def cargar_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = Municipio.objects.filter(estado_id=estado_id).all()
    municipios_list = list(municipios.values('id', 'nombre'))
    return JsonResponse(municipios_list, safe=False)