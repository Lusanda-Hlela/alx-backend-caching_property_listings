from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection


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


def get_redis_cache_metrics():
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)
    total = hits + misses

    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    return metrics