"""Pipeline to load slack into duckdb."""

from typing import List

import dlt
from pendulum import datetime
from slack import slack_source


def load_all_resources() -> None:
    """Load all resources from slack without any selection of channels."""

    pipeline = dlt.pipeline(
        pipeline_name="slack", destination='duckdb', dataset_name="slack_data"
    )

    source = slack_source(
        page_size=1000, start_date=datetime(2023, 9, 1), end_date=datetime(2023, 12, 20),
    )

    # Uncomment the following line to load only the access_logs resource. It is not selectes
    # by default because it is a resource just available on paid accounts.
    # source.access_logs.selected = True

    load_info = pipeline.run(
        source,
    )
    print(load_info)


def select_resource(selected_channels: List[str]) -> None:
    """Execute a pipeline that will load the given Slack list of channels with the selected
    channels incrementally beginning at the given start date."""

    pipeline = dlt.pipeline(
        pipeline_name="slack", destination='duckdb', dataset_name="slack_data"
    )

    source = slack_source(
        page_size=20,
        selected_channels=selected_channels,
        start_date=datetime(2023, 9, 1),
        end_date=datetime(2023, 9, 8),
    ).with_resources("channels", "1-announcements")

    load_info = pipeline.run(
        source,
    )
    print(load_info)


def get_users() -> None:
    """Execute a pipeline that will load Slack users list."""

    pipeline = dlt.pipeline(
        pipeline_name="slack", destination='duckdb', dataset_name="slack_data"
    )

    source = slack_source(
        page_size=20,
    ).with_resources("users")

    load_info = pipeline.run(
        source,
    )
    print(load_info)


if __name__ == "__main__":
    # Add your desired resources to the list...
    # resources = ["access_logs", "conversations", "conversations_history"]

    load_all_resources()
    # select_resource(selected_channels=["dlt-github-ci"])

    # select_resource(selected_channels=["1-announcements"])

    # get_users()
