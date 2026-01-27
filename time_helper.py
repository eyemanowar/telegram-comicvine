from datetime import datetime, timedelta

class Date:

    def __init__(self):
        self.today = datetime.today()

    def get_the_next_week(self):
        start = self.today + timedelta(days=(7 - self.today.weekday()))
        end = start + timedelta(days=6)
        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')
        return (start_str, end_str)

    def get_the_current_week(self):
        start = self.today + timedelta(days=(0 - self.today.weekday()))
        end = start + timedelta(days=6)
        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')
        return (start_str, end_str)