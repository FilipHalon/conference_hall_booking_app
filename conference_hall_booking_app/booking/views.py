from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
# from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ConferenceHall, Booking
from datetime import date, timedelta, datetime


today = date.today()
halls = ConferenceHall.objects.all()


def prepare_date_list(year, month, day):
    date_range = int((date(year, month, day) - today).days)
    dates = [today + timedelta(day) for day in range(date_range)]
    return dates


def get_reservation_list(hall_id):
    reservations = Booking.objects.filter(hall=hall_id)
    reservations = [str(reservation.date) for reservation in reservations]
    return reservations


dates = prepare_date_list(2020, 1, 1)

# Create your views here.


@csrf_exempt
def show_all_halls(request):
    return render(request, 'show_all_halls.html', {'halls': halls,
                                                   'dates': dates})


@csrf_exempt
def search(request):
    reservation_date = request.GET['reservation']
    name = request.GET['hall']
    capacity = request.GET['capacity']
    projector = request.GET.get('projector')
    if not projector:
        projector = False
    # search_list = Booking.objects.filter(date=reservation_date).filter(hall__name=name)

    # request.session['reservation'] = datetime.strptime(reservation_date, '%Y-%m-%d').date()
    request.session['reservation'] = reservation_date
    request.session['name'] = name
    request.session['capacity'] = int(capacity)
    request.session['projector'] = projector

    if name == 'None' and capacity == '-1':
        search_list = ConferenceHall.objects.exclude(booking__date=reservation_date) \
            .filter(projector_available=projector)
    elif name == 'None':
        search_list = ConferenceHall.objects.exclude(booking__date=reservation_date) \
            .filter(capacity__gte=capacity).filter(projector_available=projector)
    elif capacity == '-1':
        search_list = ConferenceHall.objects.exclude(booking__date=reservation_date).filter(name=name) \
            .filter(projector_available=projector)
    else:
        search_list = ConferenceHall.objects.exclude(booking__date=reservation_date).filter(name=name) \
            .filter(capacity__gte=capacity).filter(projector_available=projector)
    return render(request, 'search_results.html', {'search_list': search_list,
                                                   'reservation_date': reservation_date,
                                                   'halls': halls,
                                                   'dates': dates})


class ShowHallDetails(View):

    def get(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        reservations = get_reservation_list(hall_id)

        return render(request, 'show_hall_details.html', {'hall': hall,
                                                          'dates': dates,
                                                          'reservations': reservations})

    def post(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        reservation_date = request.POST['reservation']
        comment = request.POST.get('comment')
        Booking.objects.create(date=reservation_date, hall=hall, comment=comment)

        return redirect('home')


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
        reservations = get_reservation_list(hall_id)

        return render(request, 'make_a_reservation.html', {'dates': dates,
                                                           'reservations': reservations})

    def post(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        reservation_date = request.POST['reservation']
        Booking.objects.create(date=reservation_date, hall=hall)

        return redirect('home')


class ModifyDeleteReservation(View):

    def get(self, request, hall_id):
        hall = ConferenceHall.objects.get(pk=hall_id)
        reservations = get_reservation_list(hall_id)
        reservation_dates = Booking.objects.filter(hall=hall_id).order_by('date')
        return render(request, 'modify_delete_a_reservation.html', {'hall': hall,
                                                                    'dates': dates,
                                                                    'reservations': reservations,
                                                                    'reservation_dates': reservation_dates})

    def post(self, request, hall_id):
        reservation_date = request.POST.get('reservation_date')
        comment = request.POST.get('comment')
        former_reservation = Booking.objects.get(pk=request.POST['former_date'])

        if reservation_date:
            former_reservation.date = reservation_date
            former_reservation.comment = comment
            former_reservation.save()

        else:
            former_reservation.delete()

        return redirect('hall-details', hall_id=hall_id)


# class Reserve(View):
#
#     # def get(self, request, hall_id):
#     #     return render(request, 'add_a_comment.html')
#
#     def post(self, request, hall_id):
#         hall = ConferenceHall.objects.get(pk=hall_id)
#         Booking.objects.create(date=reservation_date, hall=hall)
#         return redirect('home')
