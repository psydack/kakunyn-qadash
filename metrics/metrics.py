from datetime import datetime, timedelta


def estimate_completion(test_cases, hours_since_start=4):
    executed_cases = len(test_cases[test_cases['Status'] != 'In Progress'])
    total_cases = len(test_cases)
    execution_rate = executed_cases / hours_since_start
    remaining_cases = total_cases - executed_cases
    if execution_rate > 0:
        remaining_time_hours = remaining_cases / execution_rate
        return datetime.now() + timedelta(hours=remaining_time_hours)
    else:
        return datetime.now()
