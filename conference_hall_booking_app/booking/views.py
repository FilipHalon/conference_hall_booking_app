from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import ConferenceHall, Booking

# Create your views here.


class AddNewHall(View):

    def get(self, request):
        return render(request, 'add_new_hall.html')

    def post(self, request):

        name = request.POST.get('name')
        try:
            capacity = int(request.POST.get('capacity'))
        except ValueError:
            return HttpResponse("Pojemność nie jest liczbą całkowitą.")
        projector_available = request.POST.get('projector_available')

        ConferenceHall.objects.create(name=name,
                                      capacity=capacity,
                                      projector_available=projector_available)
        return redirect('add-new-hall')


class ModifyHall(View):

    def get(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        return render(request, 'modify_hall.html', {'hall': hall})

    def post(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        hall.name = request.POST['name']
        try:
            hall.capacity = request.POST['capacity']
        except ValueError:
            return HttpResponse("Pojemność nie jest liczbą całkowitą.")
        hall.projector_available = request.POST['projector_available']
        hall.save()

        return HttpResponse("Zmieniono")


class DeleteHall(View):

    def get(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        return render(request, 'delete_hall.html', {'hall_name': hall.name})

    def post(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        hall.delete()
        return HttpResponse("Usunięto")


def show_hall_details(request, hall_id):
    hall = ConferenceHall.objects.get(pk=hall_id)
    return render(request, 'show_hall_details.html', {'hall': hall})


def show_all_halls(request):
    halls = ConferenceHall.objects.all()
    return render(request, 'show_all_halls.html', {'halls': halls})
