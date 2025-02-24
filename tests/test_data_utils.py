from utils.data_utils import load_data


def test_load_data():
    client_data, test_cases, file_hash = load_data('data/qa_testing_report_mock.xlsx')
    assert not client_data.empty
    assert not test_cases.empty
    assert isinstance(file_hash, str) and len(file_hash) == 32
