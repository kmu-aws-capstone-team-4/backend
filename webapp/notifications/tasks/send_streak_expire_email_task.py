import structlog
from common.tasks.base_task import BaseTask
from config.celery import app

logger = structlog.getLogger(__name__)


class SendStreakExpireEmailTask(BaseTask):

  def run(self, user_id: int, current_streak: int = 0):
    from users.models import User

    from ..services import SendStreakExpireEmailService

    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      logger.info("streak_expire_email_skipped_deleted_user", user_id=user_id)
      return None

    return SendStreakExpireEmailService(user=user, current_streak=current_streak).perform()


RegisteredSendStreakExpireEmailTask = app.register_task(SendStreakExpireEmailTask())
