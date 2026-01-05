from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .tasks import Task

scheduler = AsyncIOScheduler()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            Task.update_appointment_status,
            CronTrigger(hour=0, minute=5),
            id="update_appointment",
            replace_existing=True
        )

        scheduler.add_job(
            Task.update_availability_dates,
            CronTrigger(day_of_week="mon", hour=0, minute=5),
            id="update_availability",
            replace_existing=True
        )

        scheduler.start()
