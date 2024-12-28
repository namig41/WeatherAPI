from celery import Celery

from infrastructure.cache.config import CacheConfig


def create_task_queue(cache_config: CacheConfig) -> Celery:
    task_queue: Celery = Celery(
        "tasks",
        broker=cache_config.get_url("redis"),
        backend=cache_config.get_url("redis"),
        include=[
            "app.infrastructure.task_queue.user_tasks",
            "app.infrastructure.task_queue.weather_tasks",
        ],
    )
    return task_queue


cache_config: CacheConfig = CacheConfig()
celery: Celery = create_task_queue(cache_config)
