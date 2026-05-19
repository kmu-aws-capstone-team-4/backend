import structlog
from common.tasks.base_task import BaseTask
from config.celery import app

logger = structlog.getLogger(__name__)


class SendReportReadyEmailTask(BaseTask):

  def run(self, user_id: int, report_url: str = "", interview_title: str = ""):
    from users.models import User

    from ..services import SendReportReadyEmailService

    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      logger.info("report_ready_email_skipped_deleted_user", user_id=user_id)
      return None

    return SendReportReadyEmailService(
      user=user,
      report_url=report_url,
      interview_title=interview_title,
    ).perform()


RegisteredSendReportReadyEmailTask = app.register_task(SendReportReadyEmailTask())
