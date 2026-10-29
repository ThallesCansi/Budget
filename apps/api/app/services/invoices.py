"""Credit card statement rules.

An invoice is identified by its *due month* ("fatura de novembro"). Purchases made on or after
the closing day roll over to the next statement, the usual convention for Brazilian cards.
"""

import calendar
from datetime import date


def add_months(d: date, months: int) -> date:
    """First day of the month `months` away from `d`'s month."""
    index = d.year * 12 + (d.month - 1) + months
    return date(index // 12, index % 12 + 1, 1)


def clamp_day(year: int, month: int, day: int) -> date:
    return date(year, month, min(day, calendar.monthrange(year, month)[1]))


def _closing_date(month_start: date, closing_day: int) -> date:
    return clamp_day(month_start.year, month_start.month, closing_day)


def _due_month(closing_month: date, closing_day: int, due_day: int) -> date:
    return closing_month if due_day > closing_day else add_months(closing_month, 1)


def purchase_invoice_month(purchase_date: date, closing_day: int, due_day: int) -> date:
    month = purchase_date.replace(day=1)
    closing_month = (
        month if purchase_date < _closing_date(month, closing_day) else add_months(month, 1)
    )
    return _due_month(closing_month, closing_day, due_day)


def payment_invoice_month(payment_date: date, closing_day: int, due_day: int) -> date:
    """A payment settles the most recently closed statement."""
    month = payment_date.replace(day=1)
    closing_month = (
        month if payment_date >= _closing_date(month, closing_day) else add_months(month, -1)
    )
    return _due_month(closing_month, closing_day, due_day)


def invoice_dates(invoice_month: date, closing_day: int, due_day: int) -> tuple[date, date]:
    """(closing date, due date) for the invoice due in `invoice_month`."""
    closing_month = invoice_month if due_day > closing_day else add_months(invoice_month, -1)
    return (
        _closing_date(closing_month, closing_day),
        clamp_day(invoice_month.year, invoice_month.month, due_day),
    )
