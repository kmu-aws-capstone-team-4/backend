import structlog
from common.tasks.base_task import BaseTask
from config.celery import app

logger = structlog.getLogger(__name__)


class SendStreakReminderEmailTask(BaseTask):

  def run(self, user_id: int):
    from users.models import User

    from ..services import SendStreakReminderEmailService

    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      logger.info("streak_reminder_email_skipped_deleted_user", user_id=user_id)
      return None

    return SendStreakReminderEmailService(user=user).perform()


RegisteredSendStreakReminderEmailTask = app.register_task(SendStreakReminderEmailTask())
