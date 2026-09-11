from typing import List
from datetime import datetime

from django.db import transaction
from django.db.models.query import QuerySet

from db.models import Order, Ticket, User


def create_order(tickets: List[Ticket], username: str, date: datetime ) -> Order:
    order = Order.objects.create(created_at=date, user__username=username)

    for ticket in tickets:
        created_ticket = Ticket.objects.create(ticket=ticket, order=order)
        created_ticket.order = order
        created_ticket.created_at = date
        created_ticket.save()
    return order

@transaction.atomic
def get_orders(username: str = '') -> QuerySet[Order]:
    try:
        orders = Order.objects.filter(user__username=username)
        return orders
    except User.DoesNotExist:
        return Order.objects.all()