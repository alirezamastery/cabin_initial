from django.db.models import Q, Count
from cabin.models import *
from django.db.models.query import QuerySet


def query_0(x):
    q = Driver.objects.filter(rating__gt=x)
    return q


def query_1(x):
    driver = Driver.objects.get(pk=x)
    cars = Car.objects.filter(owner=driver)
    rides = Ride.objects.filter(car__in=cars)
    payments = Payment.objects.filter(ride__in=rides)
    if payments.count() == 0:
        return {'payment_sum': None}
    value = sum([payment.amount for payment in payments])
    return {'payment_sum': value}


def query_2(x):
    rider = Rider.objects.get(pk=x)
    ride_requests = RideRequest.objects.filter(rider=rider)
    rides = Ride.objects.filter(request__in=ride_requests)

    return rides


def query_3(t):
    count = 0
    rides = Ride.objects.all()
    for ride in rides:
        if ride.dropoff_time - ride.pickup_time > t:
            count += 1

    return count


def query_4(x, y, r):
    drivers = Driver.objects.all()
    available_drivers_pk = list()
    for driver in drivers:
        if driver.active:
            distance = ((driver.x - x) ** 2 + (driver.y - y) ** 2) ** 0.5
            if distance < r:
                available_drivers_pk.append(driver.pk)
    available_drivers = Driver.objects.filter(pk__in=available_drivers_pk)
    return available_drivers


def query_5(n, c):
    q = Driver.objects.annotate(num_rides=Count('car__ride', distinct=True)) \
        .filter(Q(car__car_type='A') | Q(car__color=c), num_rides__gte=n)  # better way to do this query
    # drivers = Driver.objects.all()
    # q_pk = list()
    # for driver in drivers:
    #     cars = Car.objects.filter(owner=driver)
    #     rides = Ride.objects.filter(car__in=cars)
    #     if rides.count() >= n:
    #         if driver.car_set.filter(car_type='A').count() > 0 or \
    #                 driver.car_set.filter(color=c).count() > 0:
    #             q_pk.append(driver.pk)
    # q = Driver.objects.filter(pk__in=q_pk)
    return q


def query_6(x, t):
    riders = Rider.objects.all()
    q_pk = list()
    for rider in riders:
        ride_requests = RideRequest.objects.filter(rider=rider)
        rides = Ride.objects.filter(request__in=ride_requests)
        rides_count = rides.count()
        payments = Payment.objects.filter(ride__in=rides)
        payments_sum = sum([payment.amount for payment in payments])
        if rides_count >= x and payments_sum > t:
            q_pk.append(rider)
    q = Rider.objects.filter(pk__in=q_pk)

    return q


def query_7():
    drivers = Driver.objects.all()
    drivers_pk = list()
    for driver in drivers:
        cars = Car.objects.filter(owner=driver)
        rides = Ride.objects.filter(car__in=cars)
        for ride in rides:
            if ride.request.rider.account.first_name == driver.account.first_name:
                drivers_pk.append(driver.pk)
    drivers_pk = set(drivers_pk)
    q = Driver.objects.filter(pk__in=drivers_pk)
    return q


def query_8():
    drivers = Driver.objects.all()
    q = list()
    for driver in drivers:
        cars = Car.objects.filter(owner=driver)
        rides = Ride.objects.filter(car__in=cars)
        ride_count = 0
        for ride in rides:
            if ride.request.rider.account.last_name == driver.account.last_name:
                ride_count += 1
        q.append({'id': driver.pk, 'n': ride_count})
    return q


def query_9(n, t):
    drivers = Driver.objects.all()
    q = list()
    for driver in drivers:
        driver_cars = Car.objects.filter(driver=driver)
        rides = Ride.objects.filter(car__in=driver_cars)
        rides_count = 0
        for ride in rides:
            if ride.car.model > 2 and ride.dropoff_time - ride.pickup_time > t:
                rides_count += 1
        q.append({'id': driver.pk, 'n': rides_count})

    return q


def query_10():
    cars = Car.objects.all()
    q = list()
    for car in cars:
        if car.model == 'A':
            rides = Ride.objects.filter(car=car)
            q.append({'id': car.pk, 'extra': rides.count()})
        elif car.model == 'B':
            rides = Ride.objects.filter(car=car)
            duration = 0
            for ride in rides:
                duration += ride.dropoff_time - ride.pickup_time
            q.append({'id': car.pk, 'extra': duration})
        elif car.model == 'C':
            rides = Ride.objects.filter(car=car)
            payments_sum = 0
            for ride in rides:
                payments = Payment.objects.filter(ride=ride)
                amounts = sum([payment.amount for payment in payments])
                payments_sum += amounts
            q.append({'id': car.pk, 'extra': payments_sum})

    return q
