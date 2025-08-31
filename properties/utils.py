from django.core.cache import cache
from .models import Property


def get_all_properties():
    # Try to get cached properties
    properties = cache.get("all_properties")

    if properties is None:
        # Cache miss -> fetch from DB
        properties = list(
            Property.objects.all().values(
                "id", "title", "description", "price", "location", "created_at"
            )
        )
        # Store in Redis for 1 hour (3600 seconds)
        cache.set("all_properties", properties, timeout=3600)

    return properties
