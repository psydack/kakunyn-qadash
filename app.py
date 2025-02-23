import hashlib

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="QA Dashboard", layout="wide")

# Hardcoded Excel file path
excel_path = 'data/qa_testing_report_mock.xlsx'

@st.cache_data(ttl=60)
def load_data(file_path):
    with open(file_path, 'rb') as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    client_data = pd.read_excel(file_path, sheet_name="Client_Stats")
    test_cases = pd.read_excel(file_path, sheet_name="Test_Cases")
    return client_data, test_cases, file_hash

client_data, test_cases, file_hash = load_data(excel_path)

# Extract project name from Excel for title
project_name = client_data.loc[client_data['Metric'] == 'Project Name', 'Value'].values[0]
st.title(f"🎾 QA Testing Dashboard - {project_name}")

# Sidebar - Project Info
st.sidebar.header("📌 Project Information")
for _, row in client_data.iterrows():
    st.sidebar.write(f"**{row['Metric']}:** {row['Value']}")

# Additional project information
st.sidebar.write("**Technical Lead:** John Doe")
st.sidebar.write("**Test Start Time:** 09:00 AM")
st.sidebar.write("**Test End Time:** 06:00 PM")

# Display file hash
st.sidebar.caption(f"File hash: {file_hash}")

# Main metrics
st.header("🚦 Overall Test Status")
total_cases = len(test_cases)
executed_cases = len(test_cases[test_cases['Status'] != 'In Progress'])
pass_cases = len(test_cases[test_cases['Status'] == 'Pass'])
fail_cases = len(test_cases[test_cases['Status'] == 'Fail'])

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Cases", total_cases)
col2.metric("Executed Cases", executed_cases, f"{(executed_cases / total_cases) * 100:.1f}%")
col3.metric("Passed ✅", pass_cases, f"{(pass_cases / total_cases) * 100:.1f}%")
col4.metric("Failed ❌", fail_cases, f"{(fail_cases / total_cases) * 100:.1f}%")

# Test status overall
status_overall = "In Progress"  # "To Start", "Finished"
col5.metric("Overall Status", status_overall)

# Category and Subcategory Status by Platform
st.header("📈 Category & Subcategory Status by Platform")
if 'Platform' in test_cases.columns:
    category_platform = test_cases.groupby(['Platform', 'Feature Group', 'Subgroup']).size().reset_index(name='Count')
    fig_category_platform = px.bar(category_platform, x='Subgroup', y='Count', color='Feature Group',
                                   facet_col='Platform',
                                   title="Test Cases by Category, Subcategory, and Platform")
    st.plotly_chart(fig_category_platform, use_container_width=True)
else:
    st.info("No 'Platform' data available in the test cases.")

# Feature Group Progress
st.header("🔍 Feature Group Progress")
group_filter = st.selectbox("Select Feature Group", test_cases['Feature Group'].unique())
group_data = test_cases[test_cases['Feature Group'] == group_filter]

subgroup_status = group_data.groupby(['Subgroup', 'Status']).size().reset_index(name='Count')
fig_subgroup = px.bar(subgroup_status, x='Subgroup', y='Count', color='Status', barmode='stack',
                      title=f"Progress by Subgroup - {group_filter}")
st.plotly_chart(fig_subgroup, use_container_width=True)

# Detailed Bug Report with mock links
st.header("🐞 Bug Details")
bugs = test_cases[test_cases['Status'] == 'Fail'][['Test Case ID', 'Subgroup', 'Bug Severity', 'Bug Description']]
bugs['Issue Link'] = bugs['Test Case ID'].apply(lambda x: f"[Open Issue](https://kakunyn.atlassian.net/jira/{x})")
st.dataframe(bugs, use_container_width=True)
