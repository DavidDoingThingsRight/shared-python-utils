import datetime
from functools import total_ordering
from json import JSONEncoder
from zoneinfo import ZoneInfo

# from bokeh.core.serialization import Serializer

# We want to solve this issue:
#   Object of type DDateTime is not JSON serializable
# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# According to the source above, we will monkey-patch the JSONEncoder so it allows
# us to use __json__ to serialize the object

# create the patch
def wrapped_default(self, obj): # type: ignore # noqa: ANN001, ANN201
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)  # type: ignore # noqa: ANN201


wrapped_default.default = JSONEncoder().default # type: ignore
# apply the patch
JSONEncoder.original_default = JSONEncoder.default # type: ignore
JSONEncoder.default = wrapped_default  # type: ignore



# # Patch Bokeh to recognize DDateTime
# def custom_ddatetime_serializer(obj):   # type: ignore # noqa: ANN001, ANN201
#     if isinstance(obj, DDateTime):
#         return obj.raw_datetime.isoformat()
#     else:
#         raise TypeError(f"Object of type {obj.__class__.__name__} is a DDateTime Object")
#
#
# # Extend Bokeh's Serializer to handle DDateTime
# original_encode_other = Serializer._encode_other


# def patched_encode_other(self, obj):  # type: ignore # noqa: ANN001, ANN201
#     if isinstance(obj, DDateTime):
#         return custom_ddatetime_serializer(obj)  # type: ignore
#     else:
#         return original_encode_other(self, obj)
#
#
# # Apply patch
# Serializer._encode_other = patched_encode_other  # type: ignore




@total_ordering
class DTime:
    __time: datetime.time

    def __init__(self, t: datetime.time) -> None:
        self.__time = t

    @classmethod
    def create(cls, hour: int, minute: int = 0, second: int = 0) -> "DTime":
        t = datetime.time(hour, minute, second)
        return cls(t)

    @property
    def hour(self) -> int:
        return self.__time.hour

    @property
    def minute(self) -> int:
        return self.__time.minute

    @property
    def second(self) -> int:
        return self.__time.second

    def __repr__(self) -> str:
        return self.__time.__repr__()

    def __str__(self) -> str:
        return self.__time.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DTime):
            return NotImplemented
        return self.__time == other.__time

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DTime):
            return NotImplemented
        return self.__time < other.__time

    def __hash__(self) -> int:
        return hash(self.__time)

    def __json__(self) -> str:
        return self.__time.isoformat()


@total_ordering
class DDate:
    __date: datetime.date

    def __init__(self, dt: datetime.date) -> None:
        self.__date = dt

    def market_open_datetime(self) -> "DDateTime":
        return DDateTime.create(self.year, self.month, self.day, 9, 30)

    def market_close_datetime(self) -> "DDateTime":
        return DDateTime.create(self.year, self.month, self.day, 16)

    def earliest_datetime(self) -> "DDateTime":
        return DDateTime.create(self.year, self.month, self.day, 0, 0, 0)

    def latest_datetime(self) -> "DDateTime":
        return DDateTime.create(self.year, self.month, self.day, 23, 59, 59)

    @classmethod
    def today(cls) -> "DDate":
        return DDateTime.now().date

    @classmethod
    def create(cls, year: int, month: int, day: int) -> "DDate":
        dt = datetime.date(year, month, day)
        return cls(dt)

    @classmethod
    def create_from_str(cls, s: str, format: str) -> "DDate":
        dt = datetime.datetime.strptime(s, format).date()
        return cls(dt)

    @classmethod
    def default_early_date(cls) -> "DDate":
        return cls(datetime.date(1990, 1, 1))

    @property
    def date(self) -> datetime.date:
        return self.__date

    @property
    def year(self) -> int:
        return self.__date.year

    @property
    def month(self) -> int:
        return self.__date.month

    @property
    def day(self) -> int:
        return self.__date.day

    @property
    def raw_date(self) -> datetime.date:
        return self.__date

    def __repr__(self) -> str:
        return self.__date.__repr__()

    def __str__(self) -> str:
        return self.__date.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DDate):
            return NotImplemented
        return self.__date == other.__date

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DDate):
            return NotImplemented
        return self.__date < other.__date

    def __sub__(self, other: "DDate") -> datetime.timedelta:
        return self.__date - other.__date

    def __hash__(self) -> int:
        return hash(self.__date)

    def __json__(self) -> str:
        return self.__date.isoformat()

    def serialize(self) -> str:
        return self.__date.isoformat()

    @classmethod
    def deserialize(cls, s: str) -> "DDate":
        dt = datetime.date.fromisoformat(s)
        return DDate(dt)


# Custom DateTime object to make sure we are always in New York Time (for consistency purposes)
# Includes information for date, time, and timezone (always new york timezone)
# Note that we NEVER want to set pytz.tzinfo in the constructor
# because we don't use the default 1883 timezone information (-4:56)
# Two possible solutions are to:
# - use pytz with timezone.localize()
# - use the new zoneinfo module

@total_ordering
class DDateTime:
    __datetime: datetime.datetime

    def __init__(self, dt: datetime.datetime) -> None:
        if dt.tzinfo is None:
            raise ValueError("DDateTime must be initialized with a timezone-aware datetime object")
        tz = ZoneInfo("America/New_York")
        self.__datetime = dt.astimezone(tz)

    #######################
    # Creates a DDateTime. Assumes the input is referring to New York Timezone
    #######################
    @classmethod
    def create(cls, year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> "DDateTime":
        tz = ZoneInfo("America/New_York")
        dt = datetime.datetime(year, month, day, hour, minute, second, tzinfo=tz)
        return cls(dt)

    @classmethod
    def from_date(cls, date: DDate) -> "DDateTime":
        tz = ZoneInfo("America/New_York")
        dt = datetime.datetime(date.year, date.month, date.day, tzinfo=tz)
        return cls(dt)

    @classmethod
    def default_early_datetime(cls) -> "DDateTime":
        tz = ZoneInfo("America/New_York")
        dt = datetime.datetime(1990, 1, 1, 0, 0, 0, tzinfo=tz)
        return cls(dt)

    @classmethod
    def now(cls) -> "DDateTime":
        tz = ZoneInfo("America/New_York")
        dt = datetime.datetime.now(tz)
        return cls(dt)

    @property
    def year(self) -> int:
        return self.__datetime.year

    @property
    def month(self) -> int:
        return self.__datetime.month

    @property
    def day(self) -> int:
        return self.__datetime.day

    @property
    def hour(self) -> int:
        return self.__datetime.hour

    @property
    def minute(self) -> int:
        return self.__datetime.minute

    @property
    def second(self) -> int:
        return self.__datetime.second

    @property
    def microsecond(self) -> int:
        return self.__datetime.microsecond

    @property
    def date(self) -> DDate:
        return DDate(self.__datetime.date())

    @property
    def time(self) -> DTime:
        return DTime(self.__datetime.time())

    @property
    def raw_datetime(self) -> datetime.datetime:
        return self.__datetime

    def __repr__(self) -> str:
        return self.__datetime.__repr__()

    def __str__(self) -> str:
        return self.__datetime.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DDateTime):
            return NotImplemented
        return self.__datetime == other.__datetime

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DDateTime):
            return NotImplemented
        return self.__datetime < other.__datetime

    def __sub__(self, other: "DDateTime") -> datetime.timedelta:
        return self.__datetime - other.__datetime

    def __add__(self, other: datetime.timedelta) -> "DDateTime":
        return DDateTime(self.__datetime + other)

    def __hash__(self) -> int:
        return hash(self.__datetime)

    def __json__(self) -> str:
        return self.serialize()

    def serialize(self) -> str:
        return self.__datetime.isoformat()

    @classmethod
    def deserialize(cls, s: str) -> "DDateTime":
        dt = datetime.datetime.fromisoformat(s)
        return DDateTime(dt)
