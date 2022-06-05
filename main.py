from news_puller.routes import app
import news_puller.scheduler
from news_puller.database import Database


Database.initialize()


if __name__ == '__main__':
    app.run()
