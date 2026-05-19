import structlog
from common.tasks.base_task import BaseTask
from config.celery import app

logger = structlog.getLogger(__name__)


class SendServiceNoticeEmailTask(BaseTask):

  def run(self, user_id: int, subject: str, title: str, body_html: str):
    from users.models import User

    from ..services import SendServiceNoticeEmailService

    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      logger.info("service_notice_email_skipped_deleted_user", user_id=user_id)
      return None

    return SendServiceNoticeEmailService(
      user=user,
      subject=subject,
      title=title,
      body_html=body_html,
    ).perform()


RegisteredSendServiceNoticeEmailTask = app.register_task(SendServiceNoticeEmailTask())
