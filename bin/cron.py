import datetime as dttm


if dttm.date.today().isoweekday() == 3:
    import news
    news.main()
