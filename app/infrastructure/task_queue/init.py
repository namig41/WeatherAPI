from celery import Celery

from infrastructure.cache.config import CacheConfig


def create_task_queue(cache_config: CacheConfig) -> Celery:
    task_queue: Celery = Celery(
        "tasks",
        broker=cache_config.get_url("redis"),
        backend=cache_config.get_url("redis"),
        include=[
            "infrastructure.task_queue.email_tasks.user",
        ],
    )
    return task_queue


cache_config: CacheConfig = CacheConfig()
celery_app: Celery = create_task_queue(cache_config)
