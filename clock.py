import news
import auth_flow
from apscheduler.schedulers.blocking import BlockingScheduler

schedule = BlockingScheduler()


def tmp_print():
    print('testing...')

schedule.add_job(tmp_print, minutes=2)
schedule.add_job(news.main, minutes=5)

schedule.add_job(auth_flow.update_token, days=2)
schedule.add_job(news.main, day_of_week='wed', hour=19)

schedule.start()
