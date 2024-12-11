from v1.models import Ticket, TicketType, Showtime, Booking

class TicketFactory:
    @staticmethod
    def create_ticket(booking_id, ticket_type_id, seat_number, showtime_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            ticket_type = TicketType.objects.get(id=ticket_type_id)
            showtime = Showtime.objects.get(id=showtime_id)

            ticket = Ticket.objects.create(
                booking=booking,
                ticket_type=ticket_type,
                seat_number=seat_number,
                showtime=showtime,
            )
            return ticket
        except Booking.DoesNotExist:
            raise ValueError("Invalid booking ID")
        except TicketType.DoesNotExist:
            raise ValueError("Invalid ticket type ID")
        except Showtime.DoesNotExist:
            raise ValueError("Invalid showtime ID")
