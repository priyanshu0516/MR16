
from .models import Trip
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .route_data import ROUTES
from .places_data import PLACES
from .cities import CITIES
from .city_images import CITY_IMAGES
import requests
from .city_coordinates import CITY_COORDINATES

def home(request):
    trip = None
    distance = None
    time = None
    fuel_cost = None
    total_budget = None
    distance_km = None
    places = []
    trip_date = None
    per_person = None
    city_image = None

    if request.method == "POST":

        from_city = request.POST.get('from_city').strip().lower()
        to_city = request.POST.get('to_city').strip().lower()
        people = int(request.POST.get('people') or 1)
        trip_date = request.POST.get('trip_date')

        city_image = CITY_IMAGES.get(to_city.lower())

        weather = "Not Available"

        try:
            url = f"https://wttr.in/{to_city}?format=%t+%C"

            response = requests.get(url)

            weather = response.text

        except:
            weather = "Weather unavailable"

        trip = f"{from_city} to {to_city}"


        # Route database

        distance_km = None
        time = "Not Available"

        try:

            start = CITY_COORDINATES.get(from_city.lower())
            end = CITY_COORDINATES.get(to_city.lower())

            if start and end:
                url = f"https://router.project-osrm.org/route/v1/driving/{start};{end}?overview=false"

                response = requests.get(url)

                data = response.json()

                route = data['routes'][0]

                distance_km = round(route['distance'] / 1000, 2)

                hours = route['duration'] / 3600

                time = f"{round(hours, 1)} Hours"

        except:
            time = "Route not found"

        places = PLACES.get(to_city.lower(), [])


    if distance_km:

        mileage = 15
        petrol_price = 100

        fuel_cost = (distance_km / mileage) * petrol_price

        distance = f"{distance_km} KM"
        hotel_cost = 2000
        food_cost = 1000

        total_budget = fuel_cost + hotel_cost + food_cost
        per_person = total_budget / people
        Trip.objects.create(
            user=request.user,
            from_city=from_city,
            to_city=to_city,
            people=people,
            trip_date=trip_date,
            total_budget=total_budget
        )

    else:
        fuel_cost = None
        distance = "Not Available"




    return render(request, 'home.html', {
        'trip': trip,
        'distance': distance,
        'time': time,
        'fuel_cost': round(fuel_cost,2) if fuel_cost else None,
        'total_budget': round(total_budget, 2) if fuel_cost else None,
        'per_person': round(per_person, 2) if fuel_cost else None,
        'trip_date': trip_date,
        'places': places,
        'cities': CITIES,
        'city_image': city_image,
        'weather': weather,
    })

@login_required
def history(request):
    trips = Trip.objects.filter(user=request.user).order_by('-id')

    return render(request, 'history.html', {
        'trips': trips
    })

@login_required
def delete_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()

    return redirect('/history/')

@login_required
def edit_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)

    if request.method == "POST":
        trip.people = request.POST.get('people')
        trip.trip_date = request.POST.get('trip_date')

        trip.save()

        return redirect('/history/')

    return render(request, 'edit.html', {
        'trip': trip
    })

