import sentry_sdk

from core.config import has_opted_out_of_analytics


def configure_sentry():
    if has_opted_out_of_analytics():
        return

    sentry_sdk.init(
        dsn="https://2d40c26a4709425e8caae75fb9682b43@o1337433.ingest.sentry.io/4505420989071360",
        send_default_pii=False,
    )
