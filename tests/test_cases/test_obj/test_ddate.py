import json
from datetime import date

import pytest
from freezegun import freeze_time

from d_util import DBaseModel
from d_util import DDate, DDateTime
from tests.utils.file_cmp_test_framework import output_test


@pytest.mark.usefixtures("output_test")
def test_ddate_init():
    dt = DDate(date(2020, 1, 1))
    print("When input is a date object:")
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@pytest.mark.usefixtures("output_test")
def test_ddate_create():
    dt = DDate.create(2020, 1, 1)
    print("Create a DDate object from year, month, day:")
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@pytest.mark.usefixtures("output_test")
def test_ddate_create_from_str():
    dt = DDate.create_from_str("2020-01-01", "%Y-%m-%d")
    print("Create a DDate object from string with format:")
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@freeze_time("2024-01-15 05:00:00")  # 05:00 in UTC is 00:00 in New York timezone (EST)
@pytest.mark.usefixtures("output_test")
def test_ddate_today_1():
    dt = DDate.today()
    print("Today's date at 00:00 in New York timezone (frozen to 2024-01-15 00:00:00 EST):")
    print("DDateTime:")
    print(DDateTime.now())
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@freeze_time("2024-01-16 4:59:59")  # 04:59 in UTC is 23:59 in New York timezone (EST) on the previous day
@pytest.mark.usefixtures("output_test")
def test_ddate_today_2():
    dt = DDate.today()
    print("Today's date at 23:59 in New York timezone (frozen to 2024-01-15 23:59:59 EST):")
    print("DDateTime:")
    print(DDateTime.now())
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@freeze_time("2024-01-15 00:00:00")  # 00:00 in default timezone (UTC)
@pytest.mark.usefixtures("output_test")
def test_ddate_today_3():
    dt = DDate.today()
    print("Today's date at 00:00 in default timezone (frozen to 2024-01-15 00:00:00 UTC):")
    print("DDateTime:")
    print(DDateTime.now())
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@freeze_time("2024-01-15 23:59:59")  # 23:59 in default timezone (UTC)
@pytest.mark.usefixtures("output_test")
def test_ddate_today_4():
    dt = DDate.today()
    print("Today's date at 23:59 in default timezone (frozen to 2024-01-15 23:59:59 UTC):")
    print("DDateTime:")
    print(DDateTime.now())
    print("DDate:")
    print(dt)
    print("Raw date:")
    print(dt.raw_date)
    print("Piecewise:")
    print(f"Year: {dt.year}, Month: {dt.month}, Day: {dt.day}")


@pytest.mark.usefixtures("output_test")
def test_ddate_serialization():
    dt = DDate.create(2020, 1, 1)
    serialized = json.dumps(dt)
    print("Serialized DDate:")
    print(serialized)


@pytest.mark.usefixtures("output_test")
def test_ddate_serialize_deserialize():
    dt = DDate.create(2020, 1, 1)
    serialized = dt.serialize()
    deserialized = DDate.deserialize(serialized)
    
    print("Serialize and deserialize:")
    print(f"Original: {dt}")
    print(f"Serialized: {serialized}")
    print(f"Deserialized: {deserialized}")
    print(f"Equal: {dt == deserialized}")


@pytest.mark.usefixtures("output_test")
def test_serialize_ddate_pydantic_attribute():
    class TestModel(DBaseModel):
        att1: int
        att2: DDate
    test_obj = TestModel(att1=1, att2=DDate.create(2020, 1, 1))
    print("Serialize object with DDate attribute:")
    print(test_obj.model_dump_json())


@pytest.mark.usefixtures("output_test")
def test_deserialize_ddate_pydantic_attribute():
    class TestModel(DBaseModel):
        att1: int
        att2: DDate
    test_obj = TestModel(att1=1, att2=DDate.create(2020, 1, 1))

    # Serialize the object
    json_str = test_obj.model_dump_json()
    print("\nSerialized JSON:")
    print(json_str)

    # Deserialize the object
    parsed = TestModel.model_validate_json(json_str)
    print("\nDeserialized object:")
    print(parsed)

