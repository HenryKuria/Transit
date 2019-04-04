from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from reportlab.pdfgen import canvas
from payments.models import Payment
from django.contrib import messages
from .forms import TicketForm, FindForm
from .models import Trip, TravelTime, Ticket, Seat, Place
from io import BytesIO


class IndexView(View):
    form_class = FindForm
    template_name = 'index.html'

    def get(self, request):
        form = self.form_class(None)

        context = {'form': form}

        return render(request, self.template_name, context)

    def post(self, request):
        time = request.POST['time']
        start = request.POST['start']
        end = request.POST['end']

        return redirect('home:find', time, start, end)


class FindTripView(View):
    form_class = FindForm
    template_name = 'index.html'

    def get(self, request, **kwargs):
        form = self.form_class(None)

        context = {'form': form}

        if kwargs['start'] != kwargs['end']:
            departure = TravelTime.objects.get(id=kwargs['time'])
            start = Place.objects.get(id=kwargs['start'])
            end = Place.objects.get(id=kwargs['end'])

            if Trip.objects.filter(available=True, departure=departure, start=start, end=end):

                trips = [trip for trip in Trip.objects.filter(
                    available=True,
                    departure=departure,
                    start=start,
                    end=end
                )]

                context = {
                    'form': form,
                    'trips': trips,
                }
            else:
                messages.error(request, 'Sorry. Trips not Available')

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        trip = request.POST['time']
        start = request.POST['start']
        end = request.POST['end']

        return redirect('home:find', trip, start, end)


class BookView(View):
    form_class = TicketForm
    template_name = 'book.html'

    def get(self, request, pk):
        form = self.form_class(None)
        trip = Trip.objects.get(id=pk)

        context = {
            'trip': trip,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, pk):
        name = request.POST['name']
        telephone = request.POST['telephone']
        code = request.POST['code']

        trip = Trip.objects.get(id=pk)
        seat = Seat.objects.get(number=request.POST['seat'], trip=trip)

        if Payment.objects.filter(used=False, code=code, telephone=telephone):
            seat.occupied = True
            seat.save()
            occupancy = [seat.occupied for seat in Seat.objects.filter(trip=trip)]

            for status in occupancy:
                if status is False:
                    trip.available = True
                    break
                else:
                    trip.available = False

            trip.save()

            ticket = Ticket.objects.create(
                client_name=name,
                telephone=telephone,
                seat=seat.number,
                trip=trip
            )

            payment = Payment.objects.get(used=False, code=code, telephone=telephone)
            payment.used = True
            payment.save()

            return redirect('home:ticket', ticket.id)
        else:
            messages.error(request, 'Invalid Payment Code')
            return redirect('home:book', pk)


class TicketView(View):
    template_name = 'ticket.html'

    def get(self, request, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['pk'])

        context = {
            'ticket': ticket
        }
        return render(request, self.template_name, context)


class DownloadView(View):
    def get(self, request, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['pk'])

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

        buffer = BytesIO()
        size = (200.0, 320.0)
        p = canvas.Canvas(buffer, pagesize=size)

        p.line(10, 10, 10, 310)
        p.line(10, 310, 190, 310)
        p.line(190, 310, 190, 10)
        p.line(10, 10, 190, 10)
        p.setTitle("ticket.pdf")
        p.drawString(80, 280, "TICKET")
        p.drawString(30, 250, "Name      -  {}".format(str(ticket.client_name)))
        p.drawString(30, 230, "Phone     -   0{}".format(str(ticket.telephone)))
        p.drawString(30, 210, "Departure - {} h".format(str(ticket.trip.departure)))
        p.drawString(30, 190, "Vehicle   -   {}".format(str(ticket.trip.vehicle.plate)))
        p.drawString(30, 170, "Route     - {} to {}".format(str(ticket.trip.start), str(ticket.trip.end)))
        p.drawString(30, 150, "Seat      -    {}".format(str(ticket.seat)))
        p.drawString(85, 13, "Edge")
        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response
