from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Airport, Passenger
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
# Create your views here.

def index(request):
    context = {'flights':Flight.objects.all()}
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except:
        raise Http404("Flight doesn't exit")

    context = {
        "flight": flight,
        "passengers":flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all(),
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No Selection"})
    except Flight.ObjectDoesNotExist:
        return render(request, "flights/error.html", {"message": "No Flight"})
    except Passenger.ObjectDoesNotExist:
        return render(request, "flights/error.html", {"message": "No Passenger"})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))
