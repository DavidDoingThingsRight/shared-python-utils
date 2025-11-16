import exchange_calendars as xcals

from d_util.objects.DDateTime import DDate, DDateTime


class MarketCalendar:

    @staticmethod
    def previous_market_day(today: DDate) -> DDate:
        calendar = xcals.get_calendar("XNYS")
        previous_close = calendar.previous_close(today.raw_date)
        return DDateTime(previous_close).date

