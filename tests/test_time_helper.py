from time_helper import Date
from datetime import datetime
from unittest.mock import patch

date= Date()

def test_range_is_seven_days():
    fetched_date = date.get_the_current_week()
    assert len(fetched_date) == 2, f'The received length was {len(fetched_date)}, instead of 2'
    (start_str, end_str) = fetched_date
    start = datetime.strptime(start_str, '%Y-%m-%d')
    end = datetime.strptime(end_str, '%Y-%m-%d')
    assert (end - start).days == 6, f'The received difference is {(end - start).days} days instead of 6 days'
    assert start.weekday() == 0, f'The received first day in a week is {start.weekday()}, instead of 0 (Monday)'

def test_get_the_next_week():
    fetched_new_week = date.get_the_next_week()
    assert len(fetched_new_week) == 2, f'The received length was {len(fetched_new_week)}, instead of 2'
    fetched_this_week = date.get_the_current_week()
    (next_start_str, next_end_str) = fetched_new_week
    current_start_str = fetched_this_week[0]
    next_start = datetime.strptime(next_start_str, '%Y-%m-%d')
    next_end = datetime.strptime(next_end_str, '%Y-%m-%d')
    current_start = datetime.strptime(current_start_str, '%Y-%m-%d')
    assert (next_end - next_start).days == 6, f'The received difference is {(next_end - next_start).days} days instead of 6 days'
    assert next_start.weekday() == 0, f'The received first day in a week is {next_start.weekday()}, instead of 0 (Monday)'
    assert (next_start - current_start).days == 7, f'The received difference is {(next_start - current_start)} instead of 7'

@patch('time_helper.datetime')
def test_freeze_today(fake_today):
    fake_today.today.return_value = datetime(2026,8, 22)
    date1 = Date()
    fetched_this_week = date1.get_the_current_week()
    (start_str, end_str) = fetched_this_week

    today_str = date1.today.strftime('%Y-%m-%d')
    today = datetime.strptime(today_str, '%Y-%m-%d')

    start = datetime.strptime(start_str, '%Y-%m-%d')
    end = datetime.strptime(end_str, '%Y-%m-%d')

    expected_start = datetime(2026,8,17)
    expected_end = datetime(2026,8,23)

    assert fake_today.today.return_value == today, f'the fake today is {fake_today.return_value} and today is {today}'
    assert (start, end) == (expected_start, expected_end), f'The received week is {fetched_this_week}, expected are {(expected_start, expected_end)}'