import datetime

def test_str_to_datetime():
  date_str = "2024-06-15"
  time_str = "14:30"
  dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
  assert dt.year == 2024
  assert dt.month == 6
  assert dt.day == 15
  assert dt.hour == 14
  assert dt.minute == 30

def run_all_utils_tests():
    test_str_to_datetime()
    print("All utils tests passed!")

