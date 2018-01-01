import news
import auth_flow
from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()

schedule.add_job(auth_flow.update_token, trigger='interval', days=2)
schedule.add_job(news.main, trigger='cron', day_of_week='wed', hour=19)

schedule.start()
