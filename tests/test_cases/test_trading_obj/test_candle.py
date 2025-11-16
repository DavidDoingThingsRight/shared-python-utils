import pytest

from d_util import BacktestCandle, Candle, DDateTime


def test_base_candle():
    candle = Candle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=1.0, high=5.0, low=0.5, close=4.0, volume=1.0)
    assert candle.start_timestamp == DDateTime.create(2020, 1, 1, 9)
    assert candle.end_timestamp == DDateTime.create(2020, 1, 1, 16)
    assert candle.open == 1.0
    assert candle.high == 5.0
    assert candle.low == 0.5
    assert candle.close == 4.0
    assert candle.volume == 1.0


def test_backtest_candle_1():
    # by default, BackTestCandle is at the start of day
    # we can access Open, but not high, low, close, volume
    candle = BacktestCandle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=1.0, high=5.0, low=0.5, close=4.0, volume=1.0)
    assert candle.timestamp == DDateTime.create(2020, 1, 1, 9)
    assert candle.open == 1.0

    with pytest.raises(AssertionError):
        tmp = candle.close

    with pytest.raises(AssertionError):
        tmp = candle.high

    with pytest.raises(AssertionError):
        tmp = candle.low

    with pytest.raises(AssertionError):
        tmp = candle.volume


def test_backtest_candle_2():
    # at end of day, we can now access everything
    candle = BacktestCandle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=1.0, high=5.0, low=0.5, close=4.0, volume=1.0)
    candle.set_start_of_candle(False)
    assert candle.timestamp == DDateTime.create(2020, 1, 1, 16)
    assert candle.open == 1.0
    assert candle.high == 5.0
    assert candle.low == 0.5
    assert candle.close == 4.0
    assert candle.volume == 1.0


def test_backtest_candle_3():
    # negative: open > high
    with pytest.raises(AssertionError):
        candle = BacktestCandle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=6.0, high=5.0, low=0.5, close=4.0, volume=1.0)

    # negative: open < low
    with pytest.raises(AssertionError):
        candle = BacktestCandle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=0.5, high=5.0, low=0.6, close=4.0, volume=1.0)

    # negative: close > high
    with pytest.raises(AssertionError):
        candle = BacktestCandle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=1.0, high=5.0, low=0.5, close=6.0, volume=1.0)

    # negative: close < low
    with pytest.raises(AssertionError):
        candle = BacktestCandle(start_timestamp=DDateTime.create(2020, 1, 1, 9), end_timestamp=DDateTime.create(2020, 1, 1, 16), open=1.0, high=5.0, low=0.5, close=0.3, volume=1.0)
