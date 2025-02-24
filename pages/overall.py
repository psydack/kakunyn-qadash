import streamlit as st

from utils.data_utils import load_data


def main():
    st.set_page_config(page_title="Overall Status", layout="wide")

    excel_path = 'data/qa_testing_report_mock.xlsx'
    _, test_cases, _ = load_data(excel_path)

    st.title("🎾 QA Testing Dashboard - Tennis Clash")

    total_cases = len(test_cases)
    executed_cases = len(test_cases[test_cases['Status'] != 'In Progress'])
    pass_cases = len(test_cases[test_cases['Status'] == 'Pass'])
    fail_cases = len(test_cases[test_cases['Status'] == 'Fail'])

    overall_completion = (executed_cases / total_cases) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cases", total_cases)
    col2.metric("Executed Cases", f"{executed_cases}/{total_cases}")
    col3.metric("Passed ✅", f"{pass_cases}/{total_cases}")
    col4.metric("Failed ❌", f"{fail_cases}/{total_cases}")

    st.subheader("📊 Progress by Feature Group & Subgroup")
    selected_group = st.selectbox("Select Feature Group", test_cases['Feature Group'].unique())
    group_data = test_cases[test_cases['Feature Group'] == selected_group]

    group_completion = len(group_data[group_data['Status'] != 'In Progress']) / len(group_data)
    st.write(f"**{selected_group}:** {group_completion:.1%}")
    st.progress(group_completion)

    for subgroup in group_data['Subgroup'].unique():
        subgroup_data = group_data[group_data['Subgroup'] == subgroup]
        executed_subgroup_cases = len(subgroup_data[subgroup_data['Status'] != 'In Progress'])
        subgroup_completion = executed_subgroup_cases / len(subgroup_data)
        st.write(f"{subgroup}: {executed_subgroup_cases}/{len(subgroup_data)} ({subgroup_completion:.1%})")
        st.progress(subgroup_completion)


if __name__ == '__main__':
    main()
