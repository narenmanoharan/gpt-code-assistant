import os
from typing import Dict, Any

import posthog
import sentry_sdk
from posthog.sentry.posthog_integration import PostHogIntegration
from sentry_sdk import configure_scope


def configure_posthog(has_opted_out_of_analytics: bool):
    if has_opted_out_of_analytics:
        return

    posthog.api_key = "phc_j6el7kHDTCeAAPIFz5xgQjnoQOwOcp7ka8FofcLC3KP"
    posthog.host = "https://app.posthog.com"
    posthog.sync_mode = True
    posthog.disable_geoip = True


def configure_sentry(has_opted_out_of_analytics: bool, uuid: str):
    if has_opted_out_of_analytics:
        return

    sentry_sdk.init(
        dsn="https://2d40c26a4709425e8caae75fb9682b43@o1337433.ingest.sentry.io/4505420989071360",
        integrations=[PostHogIntegration()],
        send_default_pii=False,
    )
    with configure_scope() as scope:
        scope.set_tag("posthog_distinct_id", uuid)


def send_event(event_name: str, id: str, properties: Dict[str, Any]):
    if os.getenv("LOCAL_DEV"):
        return
    posthog.capture(
        distinct_id=id,
        event=event_name,
        properties=properties,
    )
