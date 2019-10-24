from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TravelTime(models.Model):
    time = models.TimeField()

    def __str__(self):
        return "{}".format(self.time.strftime('%I:%M %p'))


class Place(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{}".format(self.name)


class Route(models.Model):
    name = models.CharField(max_length=5)
    dst1 = models.ForeignKey(Place, related_name="dst_1", on_delete=models.CASCADE)
    dst2 = models.ForeignKey(Place, related_name="dst_2", on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.dst1, self.dst2)


class Vehicle(models.Model):
    plate = models.CharField(max_length=8)
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}\nRoute: {}".format(self.plate, self.route)


class Trip(models.Model):
    date = models.DateField(auto_now=True)
    departure = models.ForeignKey(TravelTime, related_name='trips', on_delete=models.DO_NOTHING)
    start = models.ForeignKey(Place, related_name="trip_start", on_delete=models.CASCADE)
    end = models.ForeignKey(Place, related_name="trip_end", on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def seats(self):
        seats = [seat for seat in self.seat_set.filter(occupied=False)]

        return seats

    def __str__(self):
        return "date: {}\ndeparture: {}\n{}\nvehicle: {}".format(
            self.date,
            self.departure,
            self.start,
            self.end,
            self.vehicle
        )


class Seat(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    number = models.CharField(max_length=8)
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.number, self.trip.vehicle.plate)


class Ticket(models.Model):
    client_name = models.CharField(blank=False, null=False, max_length=120)
    telephone = models.IntegerField(blank=False, null=False)
    seat = models.IntegerField()
    trip = models.ForeignKey(Trip, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Name: {} --\nTelephone: {} --\nSeat {} --\nTrip: {}".format(
            self.client_name,
            self.telephone,
            self.seat,
            self.trip
        )


@receiver(post_save, sender=Trip)
def create_seats(sender, instance, created, **kwargs):
    """Creates 13 seats for every trip instance created"""

    if created:
        for num in range(1, 12):
            Seat.objects.create(
                trip=instance,
                number=str(num),
                occupied=False
            )
