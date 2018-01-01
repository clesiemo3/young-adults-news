import news
import auth_flow
from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()


def tmp_print():
    print('testing...')

schedule.add_job(tmp_print, trigger='interval', minutes=2)
schedule.add_job(news.main, trigger='interval', minutes=5)

schedule.add_job(auth_flow.update_token, trigger='interval', days=2)
schedule.add_job(news.main, trigger='cron', day_of_week='wed', hour=19)

schedule.start()
