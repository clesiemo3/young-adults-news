import news
import auth_flow
from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()

#schedule.add_job(auth_flow.update_token, trigger='cron', day_of_week='tue', hour=18)
#schedule.add_job(auth_flow.update_token, trigger='cron', day_of_week='thu', hour=18)
#schedule.add_job(auth_flow.update_token, trigger='cron', day_of_week='sat', hour=18)
schedule.add_job(news.main, trigger='cron', day_of_week='wed', hour=12)

schedule.start()
