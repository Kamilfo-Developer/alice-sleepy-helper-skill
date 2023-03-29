import sys
import os
from pathlib import Path

# FIXME: CHANGE THIS TO GETTING PATH

ROOT_DIR = str(Path(os.path.abspath(__file__)).parent.parent)

sys.path.append(ROOT_DIR)

from skill.entities import Activity, TipsTopic, Tip
from skill.db.repos.get_repo import get_repo
from datetime import UTC, datetime, timedelta
from skill.utils import TextWithTTS
from argparse import ArgumentParser
from uuid import uuid4
import pandas as pd
import asyncio


def prep(s: str) -> str:
    return s.replace('"', "")


async def extract_activities(activities: pd.DataFrame) -> list[Activity]:
    activities_to_insert: list[Activity] = []

    for _, row in activities.iterrows():
        hours, minutes = list(map(lambda x: int(x), row[2].split(":")))

        activities_to_insert.append(
            Activity(
                uuid4(),
                TextWithTTS(row[0], row[1]),
                occupation_time=timedelta(hours=hours, minutes=minutes),
                repo=repo,
                created_date=datetime.utcnow().astimezone(UTC),
            )
        )

    return activities_to_insert


async def extract_tips_topics(
    tips_topics: pd.DataFrame,
) -> list[TipsTopic]:
    tips_topics_to_insert: list[TipsTopic] = []

    for _, row in tips_topics.iterrows():
        tips_topics_to_insert.append(
            TipsTopic(
                uuid4(),
                TextWithTTS(prep(row.iloc[0]).lower(), prep(row.iloc[1])),
                TextWithTTS(prep(row.iloc[2]), prep(row.iloc[3])),
                created_date=datetime.utcnow().astimezone(UTC),
                repo=repo,
            )
        )

    return tips_topics_to_insert


async def extract_tips(
    tips: pd.DataFrame,
) -> list[Tip]:
    tips_to_insert: list[Tip] = []

    for _, row in tips.iterrows():
        # topic = list(
        #     filter(
        #         lambda tips_topic: tips_topic.name.text.lower()
        #         == row.topic_name.lower(),
        #         tips_topics,
        #     )
        # )[0]

        # if not topic:
        #     raise ValueError(
        #         f"No topic with next name: {row.topic_name}\n"
        #         f"This error found in row with next data: {row}"
        # )

        topic_name = prep(row.iloc[4]).lower().strip()

        topic = await repo.get_tips_topic_by_name(topic_name)

        if not topic:
            print(f"No topic with such topic name: {topic_name}")
            sys.exit()

        tips_to_insert.append(
            Tip(
                uuid4(),
                TextWithTTS(prep(row.iloc[0]), prep(row.iloc[1])),
                TextWithTTS(prep(row.iloc[2]), prep(row.iloc[3])),
                tips_topic=topic,
                created_date=datetime.utcnow().astimezone(UTC),
                repo=repo,
            )
        )

    return tips_to_insert


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Manager for tips and activities content"
    )

    parser.add_argument(
        "-a",
        "--activities",
        action="store_true",
        help="either drop all activities and import new ones or not",
    )

    parser.add_argument(
        "-T",
        "--tips",
        action="store_true",
        help="either drop all tips topics with all tips and"
        "import new ones or not",
    )

    args = vars(parser.parse_args())

    if not (args.get("activities") or args.get("tips")):
        print(
            "At least one correct argument should be provided. "
            "If you need help, add --help flag"
        )
        sys.exit()

    repo = get_repo("sa")

    loop = asyncio.get_event_loop()

    if args.get("activities"):
        activities = pd.read_csv(
            ROOT_DIR + "/content/activities.csv", index_col=False
        )

        extracted_activities = loop.run_until_complete(
            extract_activities(activities)
        )

        loop.run_until_complete(repo.delete_all_activities())

        loop.run_until_complete(repo.insert_activities(extracted_activities))

    if args.get("tips"):
        tips_topics = pd.read_csv(
            ROOT_DIR + "/content/tips_topics.csv", index_col=False
        )

        extracted_topics = loop.run_until_complete(
            extract_tips_topics(tips_topics)
        )

        loop.run_until_complete(repo.delete_all_tips_topics())

        loop.run_until_complete(repo.insert_tips_topics(extracted_topics))

        tips = pd.read_csv(ROOT_DIR + "/content/tips.csv", index_col=False)

        extracted_tips = loop.run_until_complete(extract_tips(tips))

        loop.run_until_complete(repo.delete_all_tips())

        loop.run_until_complete(repo.insert_tips(extracted_tips))

    print("Content successfully imported!")

    loop.close()
