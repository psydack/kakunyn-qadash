from datetime import datetime

import pandas as pd
import pytest

from metrics.metrics import estimate_completion


@pytest.fixture
def sample_test_cases():
    return pd.DataFrame({'Status': ['Pass', 'Fail', 'In Progress', 'Pass']})


def test_estimate_completion(sample_test_cases):
    result = estimate_completion(sample_test_cases, hours_since_start=2)
    assert isinstance(result, datetime)
    assert result > datetime.now()
