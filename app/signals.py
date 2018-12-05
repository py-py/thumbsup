from sqlalchemy import event

from app.models import Job
from app.tasks import thumbs_up

__all__ = ('signal_job_after',)


@event.listens_for(Job, 'after_insert')
def signal_job_after(mapper, connection, target):
    thumbs_up.apply_async((target.id, ), countdown=3)
