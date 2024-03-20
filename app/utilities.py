import json
from typing import List
from app.models import Event


def get_events_json(events: List[Event]):
    return json.dumps(
        [
            {
                "id": event.id,
                "owner": {
                    "username": event.owner.user.username,
                    "id": event.owner.id,
                    "profile_picture": event.owner.profile_picture.url,
                },
                "name": event.name,
                "start_date_time": event.start_date_time.isoformat(),
                "end_date_time": event.end_date_time.isoformat(),
                "location_latitude": event.location_latitude,
                "location_longitude": event.location_longitude,
                "description": event.description,
                "recurring": event.recurring,
                "recurring_frequency": event.recurring_frequency,
            }
            for event in events
        ]
    )
