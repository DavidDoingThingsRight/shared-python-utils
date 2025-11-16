from d_util import DDate, MarketCalendar


def test_market_calendar_1():
    # prev(wednesday) is tuesday, one day before
    assert MarketCalendar.previous_market_day(DDate.create(2025, 2, 19)) == DDate.create(2025, 2, 18)
    # 2025-2-17 is presidents' day. Market is closed. prev(tuesday) is the previous friday
    assert MarketCalendar.previous_market_day(DDate.create(2025, 2, 18)) == DDate.create(2025, 2, 14)
    # prev(tuesday) is monday if there's no holiday
    assert MarketCalendar.previous_market_day(DDate.create(2025, 2, 11)) == DDate.create(2025, 2, 10)
    # prev(monday) is friday if there's no holiday
    assert MarketCalendar.previous_market_day(DDate.create(2025, 2, 10)) == DDate.create(2025, 2, 7)
