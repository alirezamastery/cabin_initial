from django.db.models import Q, F, Count, Sum, Case, When, IntegerField
from cabin.models import *
from django.db.models.query import QuerySet


def query_0(x):
    q = Driver.objects.filter(rating__gt=x)
    return q


def query_1(x):
    q = Driver.objects.get(pk=x).car_set.aggregate(payment_sum=Sum('ride__payment__amount'))  # a better way
    # driver = Driver.objects.get(pk=x)
    # cars = Car.objects.filter(owner=driver)
    # rides = Ride.objects.filter(car__in=cars)
    # payments = Payment.objects.filter(ride__in=rides)
    # if payments.count() == 0:
    #     return {'payment_sum': None}
    # value = sum([payment.amount for payment in payments])
    return q


def query_2(x):
    q = Ride.objects.filter(request__rider_id=x)  # a better way
    # rider = Rider.objects.get(pk=x)
    # ride_requests = RideRequest.objects.filter(rider=rider)
    # rides = Ride.objects.filter(request__in=ride_requests)

    return q


def query_3(t):
    q = Ride.objects.annotate(travel_time=F('dropoff_time') - F('pickup_time')).filter(travel_time__gt=t).count()
    # count = 0
    # rides = Ride.objects.all()
    # for ride in rides:
    #     if ride.dropoff_time - ride.pickup_time > t:
    #         count += 1

    return q


def query_4(x, y, r):
    q = Driver.objects.annotate(distance=((F('x') - x) ** 2 + (F('y') - y) ** 2) ** 0.5). \
        filter(distance__lt=r, active=True)
    # drivers = Driver.objects.all()
    # available_drivers_pk = list()
    # for driver in drivers:
    #     if driver.active:
    #         distance = ((driver.x - x) ** 2 + (driver.y - y) ** 2) ** 0.5
    #         if distance < r:
    #             available_drivers_pk.append(driver.pk)
    # available_drivers = Driver.objects.filter(pk__in=available_drivers_pk)
    return q


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
    q = Rider.objects.annotate(total_payments=Sum('riderequest__ride__payment__amount'),
                               total_rides=Count('riderequest__ride')) \
        .filter(total_payments__gt=t, total_rides__gte=x)

    # riders = Rider.objects.all()
    # q_pk = list()
    # for rider in riders:
    #     ride_requests = RideRequest.objects.filter(rider=rider)
    #     rides = Ride.objects.filter(request__in=ride_requests)
    #     rides_count = rides.count()
    #     payments = Payment.objects.filter(ride__in=rides)
    #     payments_sum = sum([payment.amount for payment in payments])
    #     if rides_count >= x and payments_sum > t:
    #         q_pk.append(rider.id)
    # q = Rider.objects.filter(pk__in=q_pk)

    return q


def query_7():
    q = Driver.objects.annotate(
            d_first_name=F('account__first_name'),
            ride_obj=F('car__ride__request__rider__account__first_name')  # you can go deep apparently
    ).filter(d_first_name=F('ride_obj'))
    print(q)
    for b in q:
        print('**** ', b.d_first_name, b.ride_obj)
    # drivers = Driver.objects.all()
    # print(drivers)
    # drivers_pk = list()
    # for driver in drivers:
    #     print(f'--- {driver}')
    #     cars = Car.objects.filter(owner=driver)
    #     rides = Ride.objects.filter(car__in=cars)
    #     for ride in rides:
    #         print(ride.request.rider, ride)
    #
    #         # GenericForeignKey query:
    #         d_first_name = driver.account.get(object_id=driver.pk).first_name  # with get()
    #         r_first_name = ride.request.rider.account.first().first_name  # with filter() or first()
    #         print(f'----- {d_first_name} | {r_first_name}')
    #
    #         # Reverse relations:
    #         # 1- if GenericRelation field was NOT used in related models to "Account" you can
    #         # use this method to query database:
    #         rider_ct = ContentType.objects.get_for_model(ride.request.rider)
    #         rider_first_name = Account.objects.filter(content_type=rider_ct,
    #                                                   object_id=ride.request.rider.pk).first().first_name
    #         driver_ct = ContentType.objects.get_for_model(driver)
    #         driver_first_name = Account.objects.filter(content_type=driver_ct, object_id=driver.pk).first().first_name
    #         print(f'----- {driver_first_name} | {rider_first_name}')
    #         # 2- this method can be used when GenericRelation field is specified in related models to "Account"
    #         driver_account = Account.objects.get(drivers__pk=driver.pk)  # get() also works!
    #         rider_account = Account.objects.filter(riders__pk=ride.request.rider.pk).first()
    #         print(f'----- {driver_account.first_name} | {rider_account.first_name}')
    #         if rider_first_name == driver_first_name:
    #             drivers_pk.append(driver.pk)
    #
    # drivers_pk = set(drivers_pk)
    # q = Driver.objects.filter(pk__in=drivers_pk)
    # print(q)
    return q


def query_8():
    q = Driver.objects.annotate(d_last_name=F('account__first_name'),
                                r_last_name=F('car__ride__request__rider__account__last_name')) \
        .annotate(occur_count=Count(Case(When(d_last_name=F('r_last_name'), then=1),
                                         output_field=IntegerField()
                                         ))
                  )
    for b in q:
        print('**** ', b, b.occur_count)

    # drivers = Driver.objects.all()
    # q = list()
    # for driver in drivers:
    #     cars = Car.objects.filter(owner=driver)
    #     rides = Ride.objects.filter(car__in=cars)
    #     ride_count = 0
    #     print(f'--- {driver}')
    #     for ride in rides:
    #         driver_account = Account.objects.get(drivers__pk=driver.pk)
    #         rider_account = Account.objects.get(riders__pk=ride.request.rider.pk)
    #         print(f'----- {driver_account.last_name} | {rider_account.last_name}')
    #         if driver_account.last_name == rider_account.last_name:
    #             ride_count += 1
    #     q.append({'id': driver.pk, 'n': ride_count})
    # print(q)
    return q


def query_9(n, t):
    q = Driver.objects.annotate(car_model=F('car__model'),
                                ride_duration=F('car__ride__dropoff_time') - F('car__ride__pickup_time')) \
        .annotate(occur_count=Count(Case(When(car_model__gt=n, ride_duration__gt=t, then=1),
                                         output_field=IntegerField()
                                         ))
                  )
    for b in q:
        print('**** ', b, b.car_model, b.ride_duration , b.occur_count)

    # drivers = Driver.objects.all()
    # q = list()
    # for driver in drivers:
    #     driver_cars = Car.objects.filter(driver=driver)
    #     rides = Ride.objects.filter(car__in=driver_cars)
    #     rides_count = 0
    #     for ride in rides:
    #         if ride.car.model > 2 and ride.dropoff_time - ride.pickup_time > t:
    #             rides_count += 1
    #     q.append({'id': driver.pk, 'n': rides_count})

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
