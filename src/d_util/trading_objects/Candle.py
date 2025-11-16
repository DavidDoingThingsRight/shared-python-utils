from d_util.objects.DDateTime import DDateTime


class Candle:
    def __init__(self, start_timestamp: DDateTime, end_timestamp: DDateTime, open: float, high: float, low: float, close: float, volume: float) -> None:
        assert round(open, 2) <= round(high, 2), f"open {open} should be less than or equal to high {high}"
        assert round(close, 2) <= round(high, 2), f"close {close} must be less than or equal to high {high}"
        assert round(open, 2) >= round(low, 2), f"open {open} must be greater than or equal to low {low}"
        assert round(close, 2) >= round(low, 2), f"close {close} must be greater than or equal to low {low}"
        self.__start_timestamp: DDateTime = start_timestamp
        self.__end_timestamp: DDateTime = end_timestamp
        self.__open: float = open
        self.__high: float = high
        self.__low: float = low
        self.__close: float = close
        self.__volume: float = volume

    @property
    def start_timestamp(self) -> DDateTime:
        return self.__start_timestamp

    @property
    def end_timestamp(self) -> DDateTime:
        return self.__end_timestamp

    @property
    def timestamp(self) -> DDateTime:
        return self.start_timestamp

    @property
    def open(self) -> float:
        return self.__open

    @property
    def high(self) -> float:
        return self.__high

    @property
    def low(self) -> float:
        return self.__low

    @property
    def close(self) -> float:
        return self.__close

    @property
    def volume(self) -> float:
        return self.__volume

    def __repr__(self) -> str:
        return f"{self.timestamp}: open: {self.open}, high: {self.high}, low: {self.low}, close: {self.close}, volume: {self.volume}"


# Candle used for backtesting. We only have access to the open price at the start of the candle
class BacktestCandle(Candle):
    def __init__(self, start_timestamp: DDateTime, end_timestamp: DDateTime, open: float, high: float, low: float, close: float, volume: float) -> None:
        super().__init__(start_timestamp, end_timestamp, open, high, low, close, volume)
        # if true, then we are accessing this candle when it's first being created. Only timestamp() and open() can be accessed
        # if false, then we are accessing it after the candle is complete. All properties (ohlcv) can be accessed
        self.__start_of_candle: bool = True

    def set_start_of_candle(self, start_of_candle: bool) -> None:
        self.__start_of_candle = start_of_candle

    @property
    def timestamp(self) -> DDateTime:
        if self.__start_of_candle:
            return super().start_timestamp
        else:
            return super().end_timestamp

    @property
    def open(self) -> float:
        return super().open

    @property
    def high(self) -> float:
        assert not self.__start_of_candle
        return super().high

    @property
    def low(self) -> float:
        assert not self.__start_of_candle
        return super().low

    @property
    def close(self) -> float:
        assert not self.__start_of_candle
        return super().close

    @property
    def volume(self) -> float:
        assert not self.__start_of_candle
        return super().volume

    def __repr__(self) -> str:
        if self.__start_of_candle:
            return f"{self.timestamp}: open: {self.open}"
        else:
            return super().__repr__()
