# app.py
import math
from datetime import datetime

import streamlit as st

from metrics.metrics import estimate_completion
from utils.data_utils import load_data


def format_countdown(td):
    total_seconds = math.ceil(td.total_seconds() / 300) * 300  # round up to nearest 5 min
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours}h {minutes}m"


def main():
    st.set_page_config(page_title="QA Dashboard", layout="wide")

    excel_path = 'data/qa_testing_report_mock.xlsx'
    client_data, test_cases, _ = load_data(excel_path)

    project_name = client_data.loc[client_data['Metric'] == 'Project Name', 'Value'].values[0]
    version = client_data.loc[client_data['Metric'] == 'Version', 'Value'].values[0]
    platform = client_data.loc[client_data['Metric'] == 'Platform', 'Value'].values[0]

    estimated_completion = estimate_completion(test_cases)
    countdown = estimated_completion - datetime.now()

    bugs_by_severity = test_cases[test_cases['Status'] == 'Fail']['Bug Severity'].value_counts().reset_index()
    bugs_by_severity.columns = ['Severity', 'Count']

    st.sidebar.header("📌 Project Information")
    st.sidebar.write(f"**Project Name:** {project_name}")
    st.sidebar.write(f"**Version:** {version} - buildversion #1234")
    st.sidebar.write(f"**Platform:** {platform}")
    st.sidebar.write(f"**Estimated Completion:** {estimated_completion.strftime('%Y-%m-%d %H:%M')}")
    st.sidebar.write(f"**Countdown to finish:** {format_countdown(countdown)}")
    st.sidebar.write("**Responsible:** John Doe")

    st.sidebar.header("🐞 Bugs by Severity")
    for _, row in bugs_by_severity.iterrows():
        st.sidebar.write(f"**{row['Severity']}:** {row['Count']}")

    st.sidebar.page_link("pages/overall.py", label="Overall")
    st.sidebar.page_link("pages/bug_details.py", label="Bug Details")

    st.title("📌 Project Information")
    st.write(f"**Project Name:** {project_name}")
    st.write(f"**Version:** {version} - buildversion #1234")
    st.write(f"**Platform:** iOS, Android")
    st.write(f"**Estimated Completion:** {estimated_completion.strftime('%Y-%m-%d %H:%M')}")
    st.write(f"**Countdown to finish:** {format_countdown(countdown)}")
    st.write("**Responsible:** John Doe")

    st.subheader("🐞 Total Bugs by Severity")
    for _, row in bugs_by_severity.iterrows():
        st.write(f"**{row['Severity']}:** {row['Count']}")


if __name__ == '__main__':
    main()
