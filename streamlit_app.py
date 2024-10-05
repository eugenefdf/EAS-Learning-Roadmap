import streamlit as st
import pandas as pd

# Load the CSV files
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

# Define the role columns as per the latest structure
role_columns_full = {
    'Vice Principal (Admin) [VP(A)]': 'Vice Principal (Admin) [VP(A)]',
    'Adminstrative Manager [AM]': 'Adminstrative Manager [AM]',
    'Operation Manager [OM]': 'Operation Manager [OM]',
    'Assistant Operation Manager/SLT [Assistant OM/SLT]': 'Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'ICT Manager': 'ICT Manager',
    'Cluster ICT Manager': 'Cluster ICT Manager',
    'STEM Instructor (Workshop)': 'STEM Instructor (Workshop)',
    'STEM Instructor (Laboratory)': 'STEM Instructor (Laboratory)',
    'Corporate Support Officer [CSO]': 'Corporate Support Officer [CSO]',
    'Admin Executive [AE]': 'Admin Executive [AE]',
    'Technical Support Officer (Audio Visual) [TSO (AV)]': 'Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Operation Support Officer [OSO]': 'Operation Support Officer [OSO]'
}

# Sidebar for role selection
st.sidebar.header("Select Roles to Display")
selected_columns = []
for full_column in role_columns_full.keys():
    if st.sidebar.checkbox(full_column, value=False):
        selected_columns.append(full_column)

# Check if any roles are selected
if not selected_columns:
    st.warning("Please select at least one role to display.")
else:
    # Create multi-level columns for the filtered Behavioural Indicators DataFrame
    bi_columns = ['Sector', 'Dimension/ Learning Area'] + selected_columns
    bi_multi_columns = pd.MultiIndex.from_tuples([('Behavioural Indicator', col) for col in bi_columns])

    # Filter and structure the Behavioural Indicators DataFrame
    filtered_bi_df = bi_df[bi_columns]
    filtered_bi_df.columns = bi_multi_columns

    # Display the filtered Behavioural Indicators DataFrame
    st.write("### Filtered Behavioural Indicators Data")
    st.dataframe(filtered_bi_df)

    # Create multi-level columns for the filtered Programmes DataFrame
    programmes_columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + selected_columns + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]
    programmes_multi_columns = pd.MultiIndex.from_tuples([('Type of Courses', col) if col not in ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] else ('', col) for col in programmes_columns])

    # Filter and structure the Programmes DataFrame
    filtered_programmes_df = programmes_df[programmes_columns]
    filtered_programmes_df.columns = programmes_multi_columns

    # Display the filtered Programmes DataFrame
    st.write("### Filtered Programmes Data")
    st.dataframe(filtered_programmes_df)