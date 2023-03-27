import datetime
import pytz
from skill.exceptions import InvalidInputError
from skill.dataconvert.base_converter import BaseDataConverter


class YaDataConverter(BaseDataConverter):
    """Data converter for Yandex Alice API."""

    @staticmethod
    def time(obj: dict, timezone: str | datetime.tzinfo) -> datetime.time:
        """Convert YANDEX.DATETIME JSON object to datetime.time with
        given timezone"""

        if obj["type"] != "YANDEX.DATETIME":
            raise InvalidInputError(
                "obj must be Alice API YANDEX.DATETIME object"
            )

        tzinfo = (
            timezone
            if isinstance(timezone, datetime.tzinfo)
            else pytz.timezone(timezone)
        )

        if "hour" not in obj["value"] or "minute" not in obj["value"]:
            raise InvalidInputError(
                "obj should contain hour and minute information"
            )

        time = datetime.time(
            hour=obj["value"]["hour"],
            minute=obj["value"]["minute"],
            tzinfo=tzinfo,
        )

        return time

    @staticmethod
    def datetime(obj: dict, timezone: str) -> datetime.datetime:
        """Convert YANDEX.DATETIME JSON object to datetime.datetime with
        given timezone"""

        if obj["type"] != "YANDEX.DATETIME":
            raise InvalidInputError(
                "obj must be Alice API YANDEX.DATETIME object"
            )
        if isinstance(timezone, str):
            tzinfo = pytz.timezone(timezone)
        elif isinstance(timezone, datetime.tzinfo):
            tzinfo = timezone  # type: ignore
        else:
            raise InvalidInputError("Invalid timezone type")

        if not (
            "year" in obj["value"]
            and "month" in obj["value"]
            and "day" in obj["value"]
            and "hour" in obj["value"]
            and "minute" in obj["value"]
        ):
            raise InvalidInputError("Incomplete obj")

        result_datetime = datetime.datetime(
            year=obj["value"]["year"],
            month=obj["value"]["month"],
            day=obj["value"]["day"],
            hour=obj["value"]["hour"],
            minute=obj["value"]["minute"],
            tzinfo=tzinfo,
        )
        return result_datetime
