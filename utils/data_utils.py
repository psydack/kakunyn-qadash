import hashlib

import pandas as pd


def load_data(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    client_data = pd.read_excel(file_path, sheet_name="Client_Stats")
    test_cases = pd.read_excel(file_path, sheet_name="Test_Cases")
    return client_data, test_cases, file_hash
