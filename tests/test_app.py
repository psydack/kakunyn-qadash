import pandas as pd
import pytest


@pytest.fixture
def sample_test_cases():
    return pd.DataFrame({
        'Test Case ID': ['TC_001', 'TC_002'],
        'Feature Group': ['Soft Currency', 'Gameplay'],
        'Subgroup': ['Coins', 'Matchmaking'],
        'Status': ['Pass', 'Fail'],
        'Bug Severity': [None, 'High'],
        'Bug Description': ['', 'Lag during gameplay']
    })


def test_total_test_cases(sample_test_cases):
    assert len(sample_test_cases) == 2


def test_pass_cases_count(sample_test_cases):
    pass_cases = len(sample_test_cases[sample_test_cases['Status'] == 'Pass'])
    assert pass_cases == 1


def test_fail_cases_count(sample_test_cases):
    fail_cases = len(sample_test_cases[sample_test_cases['Status'] == 'Fail'])
    assert fail_cases == 1


def test_bug_severity(sample_test_cases):
    high_severity_bugs = sample_test_cases[sample_test_cases['Bug Severity'] == 'High']
    assert len(high_severity_bugs) == 1
    assert high_severity_bugs.iloc[0]['Bug Description'] == 'Lag during gameplay'


def test_no_bug_description_for_pass(sample_test_cases):
    pass_cases = sample_test_cases[sample_test_cases['Status'] == 'Pass']
    assert pass_cases.iloc[0]['Bug Description'] == ''
