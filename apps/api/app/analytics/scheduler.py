import time
from datetime import datetime
from zoneinfo import ZoneInfo

from redis import Redis
from rq import Queue, Retry

from app.config import get_settings


def main() -> None:
    settings = get_settings()
    connection = Redis.from_url(settings.redis_url)
    queue = Queue("analytics", connection=connection)
    while True:
        day = datetime.now(ZoneInfo("Asia/Taipei")).date().isoformat()
        service_queue = Queue("travel-services", connection=connection)
        service_job = f"travel-services-maintenance-{day}"
        if service_queue.fetch_job(service_job) is None:
            service_queue.enqueue(
                "app.travel_services.jobs.run_daily",
                job_id=service_job,
                job_timeout=1800,
                result_ttl=86_400,
                failure_ttl=604_800,
                retry=Retry(max=3, interval=[60, 300, 900]),
            )
        job_id = f"analytics-maintenance-{day}"
        if queue.fetch_job(job_id) is None:
            queue.enqueue(
                "app.analytics.jobs.run_analytics_maintenance",
                job_id=job_id,
                result_ttl=86_400,
                failure_ttl=604_800,
                retry=Retry(max=3, interval=[60, 300, 900]),
            )
        time.sleep(settings.analytics_scheduler_interval_seconds)


if __name__ == "__main__":
    main()
