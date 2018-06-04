from cookiespool.scheduler import Scheduler
from cookiespool.api import app
def main():
    s = Scheduler()
    s.run()
    app.run()

if __name__ == '__main__':
    main()