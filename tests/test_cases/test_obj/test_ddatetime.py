import json
import zoneinfo
from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time

from d_util.objects.DBaseModel import DBaseModel
from d_util.objects.DDateTime import DDateTime
from tests.utils.file_cmp_test import output_test


@pytest.mark.usefixtures("output_test")
def test_ddatetime_init():
    dt = DDateTime(datetime(2020, 1, 1, 9, tzinfo=pytz.utc))
    print("When input is a datetime object with UTC timezone, it will be converted to New York timezone")
    print("DDateTime:")
    print(dt)
    print("Date:")
    print(dt.date)
    print("Time:")
    print(dt.time)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}, Hour: {dt.hour}, Minute: {dt.minute}, Second: {dt.second}, Microsecond: {dt.microsecond}")


@pytest.mark.usefixtures("output_test")
def test_ddatetime_init2():
    # when we use pytz timezone, the offset will be strange (-4:56) because it uses the default 1883 timezone
    dt = DDateTime(datetime(2020, 1, 1, 9, tzinfo=pytz.timezone("America/New_York")))
    print("When input is a datetime object with New York timezone in wrong offset, it will be converted to New York timezone")
    print("DDateTime:")
    print(dt)
    print("Date:")
    print(dt.date)
    print("Time:")
    print(dt.time)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}, Hour: {dt.hour}, Minute: {dt.minute}, Second: {dt.second}, Microsecond: {dt.microsecond}")


@pytest.mark.usefixtures("output_test")
def test_ddatetime_init3():
    # when we use pytz timezone using localize, the offset will be correct
    dt = DDateTime(pytz.timezone("America/New_York").localize(datetime(2020, 1, 1, 9)))
    print("When input is a datetime object in New York timezone, it will be treated correctly")
    print("DDateTime:")
    print(dt)
    print("Date:")
    print(dt.date)
    print("Time:")
    print(dt.time)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}, Hour: {dt.hour}, Minute: {dt.minute}, Second: {dt.second}, Microsecond: {dt.microsecond}")


@pytest.mark.usefixtures("output_test")
def test_ddatetime_init4():
    # when we use zoneinfo timezone, the offset will be correct
    dt = DDateTime(datetime(2020, 1, 1, 9, tzinfo=zoneinfo.ZoneInfo("America/New_York")))
    print("When input is a datetime object in New York timezone, it will be treated correctly")
    print("DDateTime:")
    print(dt)
    print("Date:")
    print(dt.date)
    print("Time:")
    print(dt.time)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}, Hour: {dt.hour}, Minute: {dt.minute}, Second: {dt.second}, Microsecond: {dt.microsecond}")


@pytest.mark.usefixtures("output_test")
def test_ddatetime_get_raw_datetime():
    dt = DDateTime.create(2020, 1, 1, 9)
    print("Getting the raw datetime from DDateTime and raw date from DDate")
    print("DDateTime:")
    print(type(dt))
    print(dt)
    print("Raw datetime:")
    print(type(dt.raw_datetime))
    print(dt.raw_datetime)
    print("Date:")
    print(type(dt.date))
    print(dt.date)
    print("Raw date:")
    print(type(dt.date.raw_date))
    print(dt.date.raw_date)


@pytest.mark.usefixtures("output_test")
def test_ddatetime_create():
    dt = DDateTime.create(2020, 1, 1, 9)
    print("Create a DDateTime object from year, month, day, hour")
    print("DDateTime:")
    print(dt)
    print("Date:")
    print(dt.date)
    print("Time:")
    print(dt.time)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}, Hour: {dt.hour}, Minute: {dt.minute}, Second: {dt.second}, Microsecond: {dt.microsecond}")


@pytest.mark.usefixtures("output_test")
def test_serialize_ddatetime_pydantic_attribute():
    class TestModel(DBaseModel):
        att1: int
        att2: DDateTime
    test_obj = TestModel(att1=1, att2=DDateTime.create(2020, 1, 1, 9))
    print("Serialize object with DDateTime attribute:")
    print(test_obj.model_dump_json())


@pytest.mark.usefixtures("output_test")
def test_deserialize_ddatetime_pydantic_attribute():
    class TestModel(DBaseModel):
        att1: int
        att2: DDateTime
    test_obj = TestModel(att1=1, att2=DDateTime.create(2020, 1, 1, 9))

    # Serialize the object
    json_str = test_obj.model_dump_json()
    print("\nSerialized JSON:")
    print(json_str)

    # Deserialize the object
    parsed = TestModel.model_validate_json(json_str)
    print("\nDeserialized object:")
    print(parsed)


@pytest.mark.usefixtures("output_test")
def test_serialize_ddatetime():
    dt = DDateTime.create(2020, 1, 1, 9)
    serialized = json.dumps(dt)
    print("Serialized DDateTime:")
    print(serialized)


@freeze_time("2024-07-01 12:00:00")
@pytest.mark.usefixtures("output_test")
def test_now_1():
    print("Testing datetime.now() in summer:")
    print(DDateTime.now())


@freeze_time("2024-01-01 12:00:00")
@pytest.mark.usefixtures("output_test")
def test_now_2():
    print("Testing datetime.now() in winter:")
    print(DDateTime.now())


@freeze_time("2024-01-01 6:00:00")
@pytest.mark.usefixtures("output_test")
def test_now_3():
    print("Testing datetime.now() at 6 with UTC timezone:")
    print(DDateTime.now())


@freeze_time("2024-01-01 3:00:00")
@pytest.mark.usefixtures("output_test")
def test_now_4():
    print("Testing datetime.now() at 3 with UTC timezone:")
    print(DDateTime.now())
