import datetime
import pytz
from skill.sh_exceptions import SHInvalidInputError
from skill.dataconvert.base_converter import BaseDataConverter


class YaDataConverter(BaseDataConverter):
    """Data converter for Yandex Alice API."""

    @staticmethod
    def time(obj: dict, timezone: str | datetime.tzinfo) -> datetime.time:
        """Convert YANDEX.DATETIME JSON object to datetime.time with
        given timezone"""

        if obj["type"] != "YANDEX.DATETIME":
            raise SHInvalidInputError(
                "obj must be Alice API YANDEX.DATETIME object"
                )
        if isinstance(timezone, str):
            tzinfo = pytz.timezone(timezone)
        elif isinstance(timezone, datetime.tzinfo):
            tzinfo = timezone  # type: ignore
        else:
            raise SHInvalidInputError("Invalid timezone type")

        try:
            time = datetime.time(
                hour=obj["hour"],
                minute=obj["minute"],
                tzinfo=tzinfo
            )
        except KeyError as e:
            if "hour" not in obj or "minute" not in obj:
                raise SHInvalidInputError(
                    "obj should contain hour and minute information"
                    )
            raise e
        return time

    @staticmethod
    def datetime(obj: dict, timezone: str) -> datetime.datetime:
        """Convert YANDEX.DATETIME JSON object to datetime.datetime with
        given timezone"""

        if obj["type"] != "YANDEX.DATETIME":
            raise SHInvalidInputError(
                "obj must be Alice API YANDEX.DATETIME object"
                )
        if isinstance(timezone, str):
            tzinfo = pytz.timezone(timezone)
        elif isinstance(timezone, datetime.tzinfo):
            tzinfo = timezone  # type: ignore
        else:
            raise SHInvalidInputError("Invalid timezone type")

        try:
            result_datetime = datetime.datetime(
                year=obj["year"],
                month=obj["month"],
                day=obj["day"],
                hour=obj["hour"],
                minute=obj["minute"],
                tzinfo=tzinfo
            )
        except KeyError as e:
            if "year" not in obj or "month" not in obj or "day" not in obj \
                    or "hour" not in obj or "minute" not in obj:
                raise SHInvalidInputError(f"Incomplete obj: {e}")
            raise e
        return result_datetime
