from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from .models import ConferenceHall, Booking
from datetime import date, timedelta

# Create your views here.


def show_all_halls(request):
    halls = ConferenceHall.objects.all()
    return render(request, 'show_all_halls.html', {'halls': halls})


def show_hall_details(request, hall_id):
    hall = ConferenceHall.objects.get(pk=hall_id)
    return render(request, 'show_hall_details.html', {'hall': hall})


class AddNewHall(View):

    def get(self, request):
        return render(request, 'add_new_hall.html')

    def post(self, request):

        name = request.POST.get('name')
        try:
            capacity = int(request.POST.get('capacity'))
        except ValueError:
            return HttpResponse("Capacity is not an integer.")
        projector_available = request.POST.get('projector_available')

        ConferenceHall.objects.create(name=name,
                                      capacity=capacity,
                                      projector_available=projector_available)
        return redirect('home')


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
            return HttpResponse("Capacity is not a integer.")
        hall.projector_available = request.POST['projector_available']
        hall.save()

        return redirect('home')


class DeleteHall(View):

    def get(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        return render(request, 'delete_hall.html', {'hall_name': hall.name})

    def post(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        hall.delete()
        return redirect('home')


class MakeReservation(View):

    def get(self, request, hall_id):

        hall = ConferenceHall.objects.get(pk=hall_id)

        today = date.today()
        date_range = int((date(2020, 1, 1) - today).days)
        dates = [today + timedelta(day) for day in range(date_range)]

        reservations = Booking.objects.filter(hall=hall_id)
        reservations = [str(reservation.date) for reservation in reservations]

        return render(request, 'make_a_reservation.html', {'hall': hall,
                                                           'dates': dates,
                                                           'reservations': reservations})

    def post(self, request, hall_id):

        hall = ConferenceHall.objects.get(pk=hall_id)
        reservation_date = request.POST['reservation']
        Booking.objects.create(date=reservation_date, hall=hall)

        return redirect('reserve')


class Reserve(View):

    # def get(self, request, hall_id):
    #     return render(request, 'add_a_comment.html')

    def post(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        Booking.objects.create(date=reservation_date, hall=hall)
        return redirect('home')
