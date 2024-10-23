from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from .forms import FriendForm
from .models import Friend

from django.views import View

def indexView(request):
    form = FriendForm()
    friends = Friend.objects.all()
    return render(request, "index.html", {"form": form, "friends": friends})


# views.py
def postFriend(request):
    # Verificamos si la solicitud es AJAX y si el método es POST
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
        form = FriendForm(request.POST)
        if form.is_valid():
            instance = form.save()
            ser_instance = serializers.serialize('json', [instance])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    # Si no es AJAX o POST, retornamos un error
    return JsonResponse({"error": "Solicitud inválida o no es AJAX"}, status=400)




# BONUS CBV
def checkNickName(request):
    # Verificamos si es una solicitud AJAX y si el método es GET
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "GET":
        nick_name = request.GET.get("nick_name", None)
        print(f"Nickname recibido: {nick_name}")  # Debug

        if not nick_name:
            return JsonResponse({"valid": False, "error": "No se proporcionó un nickname"}, status=400)

        if Friend.objects.filter(nick_name=nick_name).exists():
            return JsonResponse({"valid": False, "message": "El nickname ya está en uso"}, status=200)

        return JsonResponse({"valid": True}, status=200)

    # Si no es AJAX o no es GET, retornamos un error
    return JsonResponse({"error": "Solicitud inválida o no es AJAX"}, status=400)
    



class FriendView(View):
    form_class = FriendForm
    template_name = "index.html"

    def get(self, *args, **kwargs):
        form = self.form_class()
        friends = Friend.objects.all()
        return render(self.request, self.template_name, 
            {"form": form, "friends": friends})

    def post(self, *args, **kwargs):
        # request should be ajax and method should be POST.
        if self.request.is_ajax and self.request.method == "POST":
            # get the form data
            form = self.form_class(self.request.POST)
            # save the data and after fetch the object in instance
            if form.is_valid():
                instance = form.save()
                # serialize in new friend object in json
                ser_instance = serializers.serialize('json', [ instance, ])
                # send to client side.
                return JsonResponse({"instance": ser_instance}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"error": form.errors}, status=400)

        # some error occured
        return JsonResponse({"error": ""}, status=400)
