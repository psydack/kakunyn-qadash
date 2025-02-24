import plotly.express as px
import streamlit as st

from utils.data_utils import load_data


def main():
    st.set_page_config(page_title="Bug Details", layout="wide")

    excel_path = 'data/qa_testing_report_mock.xlsx'
    _, test_cases, _ = load_data(excel_path)

    st.title("🐞 Bug Details")

    feature_group = st.selectbox("Select Feature Group", ["All"] + list(test_cases['Feature Group'].unique()))

    if feature_group != "All":
        filtered_cases = test_cases[test_cases['Feature Group'] == feature_group]
    else:
        filtered_cases = test_cases

    total_bugs = filtered_cases[filtered_cases['Status'] == 'Fail']

    st.header("🐞 Overall Bug Status")
    severity_counts = total_bugs['Bug Severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']

    fig_severity = px.pie(severity_counts, names='Severity', values='Count', title="Bugs by Severity")
    st.plotly_chart(fig_severity, use_container_width=True)

    st.header("📱 Progress by Platform and Feature Group")
    platform_groups = total_bugs.groupby(['Platform', 'Feature Group']).size().reset_index(name='Bugs')
    fig_platform = px.bar(platform_groups, x='Feature Group', y='Bugs', color='Platform', barmode='group')
    st.plotly_chart(fig_platform, use_container_width=True)

    st.subheader("📋 Detailed Bug List")
    st.dataframe(
        total_bugs[['Test Case ID', 'Platform', 'Feature Group', 'Subgroup', 'Bug Severity', 'Bug Description']])


if __name__ == '__main__':
    main()
