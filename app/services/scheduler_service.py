from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.services.inventory_service import inventory_service
from app.services.feedback_service import feedback_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for managing scheduled tasks using APScheduler"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._setup_jobs()
    
    def _setup_jobs(self):
        """Set up scheduled jobs"""
        # Daily check for low stock at 8 AM
        self.scheduler.add_job(
            func=self._daily_low_stock_check,
            trigger=CronTrigger(hour=8, minute=0),
            id='daily_low_stock_check',
            name='Daily Low Stock Check',
            replace_existing=True
        )
        
        # Daily check for low ratings at 9 PM
        self.scheduler.add_job(
            func=self._daily_low_rating_check,
            trigger=CronTrigger(hour=21, minute=0),
            id='daily_low_rating_check',
            name='Daily Low Rating Check',
            replace_existing=True
        )
        
        logger.info("Scheduled jobs configured successfully")
    
    def _daily_low_stock_check(self):
        """Daily job to check for low stock items"""
        logger.info("Running daily low stock check...")
        try:
            alerts = inventory_service.check_low_stock()
            if alerts:
                logger.warning(f"Low stock alert: {len(alerts)} items need restocking")
                for alert in alerts:
                    logger.warning(alert.message)
            else:
                logger.info("All inventory items are adequately stocked")
        except Exception as e:
            logger.error(f"Error in daily low stock check: {e}")
    
    def _daily_low_rating_check(self):
        """Daily job to check for low ratings"""
        logger.info("Running daily low rating check...")
        try:
            alerts = feedback_service.check_low_ratings(days=1)
            if alerts:
                logger.warning(f"Low rating alert: {len(alerts)} items received poor feedback today")
                for alert in alerts:
                    logger.warning(alert.message)
            else:
                logger.info("No low ratings today - food quality is satisfactory")
        except Exception as e:
            logger.error(f"Error in daily low rating check: {e}")
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started successfully")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler shut down successfully")
    
    def get_jobs(self):
        """Get list of scheduled jobs"""
        return [
            {
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None
            }
            for job in self.scheduler.get_jobs()
        ]


# Singleton instance
scheduler_service = SchedulerService()
