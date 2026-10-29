from datetime import date

import pytest

from app.services.invoices import invoice_dates, payment_invoice_month, purchase_invoice_month


@pytest.mark.parametrize(
    ("purchase", "expected"),
    [
        (date(2026, 10, 2), date(2026, 10, 1)),  # before closing (day 3) -> due 10/oct
        (date(2026, 10, 3), date(2026, 11, 1)),  # on closing day -> next statement
        (date(2026, 10, 31), date(2026, 11, 1)),
        (date(2026, 12, 15), date(2027, 1, 1)),  # year rollover
    ],
)
def test_purchase_due_same_month(purchase: date, expected: date) -> None:
    # closes on the 3rd, due on the 10th of the same month
    assert purchase_invoice_month(purchase, closing_day=3, due_day=10) == expected


@pytest.mark.parametrize(
    ("purchase", "expected"),
    [
        (date(2026, 10, 24), date(2026, 11, 1)),  # closes 25/oct, due 5/nov
        (date(2026, 10, 25), date(2026, 12, 1)),
    ],
)
def test_purchase_due_next_month(purchase: date, expected: date) -> None:
    assert purchase_invoice_month(purchase, closing_day=25, due_day=5) == expected


def test_closing_day_clamped_to_short_month() -> None:
    # closing day 31 in February behaves as the last day of the month
    assert purchase_invoice_month(date(2026, 2, 27), 31, 10) == date(2026, 3, 1)
    assert purchase_invoice_month(date(2026, 2, 28), 31, 10) == date(2026, 4, 1)


def test_payment_settles_last_closed_statement() -> None:
    # closes 25, due 5: paying on 5/nov settles the invoice that closed on 25/oct (due nov)
    assert payment_invoice_month(date(2026, 11, 5), 25, 5) == date(2026, 11, 1)
    assert payment_invoice_month(date(2026, 10, 26), 25, 5) == date(2026, 11, 1)


def test_invoice_dates() -> None:
    assert invoice_dates(date(2026, 11, 1), 25, 5) == (date(2026, 10, 25), date(2026, 11, 5))
    assert invoice_dates(date(2026, 2, 1), 3, 31) == (date(2026, 2, 3), date(2026, 2, 28))
