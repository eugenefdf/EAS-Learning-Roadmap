import streamlit as st
import pandas as pd

# Load the CSV files
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

# Define the role columns
role_columns = [
    'Vice Principal (Admin) [VP(A)]',
    'Adminstrative Manager [AM]',
    'Operation Manager [OM]',
    'Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'ICT Manager',
    'Cluster ICT Manager',
    'STEM Instructor (Workshop)',
    'STEM Instructor (Laboratory)',
    'Corporate Support Officer [CSO]',
    'Admin Executive [AE]',
    'Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Operation Support Officer [OSO]'
]

# Sidebar for role selection
st.sidebar.header("Select Roles to Display")
selected_columns = []
for full_column in role_columns:
    if st.sidebar.checkbox(full_column, value=False):
        selected_columns.append(full_column)

# Check if any roles are selected
if not selected_columns:
    st.warning("Please select at least one role to display.")
else:
    # Create multi-level columns for the filtered Behavioural Indicators DataFrame
    bi_columns = ['Sector', 'Dimension/ Learning Area'] + selected_columns
    bi_multi_columns = pd.MultiIndex.from_tuples([
        ('Behavioural Indicator', 'Vice Principal (Admin) [VP(A)]'),
        ('Behavioural Indicator', 'Adminstrative Manager [AM]'),
        ('Behavioural Indicator', 'Operation Manager [OM]'),
        ('Behavioural Indicator', 'Assistant Operation Manager/SLT [Assistant OM/SLT]'),
        ('Behavioural Indicator', 'ICT Manager'),
        ('Behavioural Indicator', 'Cluster ICT Manager'),
        ('Behavioural Indicator', 'STEM Instructor (Workshop)'),
        ('Behavioural Indicator', 'STEM Instructor (Laboratory)'),
        ('Behavioural Indicator', 'Corporate Support Officer [CSO]'),
        ('Behavioural Indicator', 'Admin Executive [AE]'),
        ('Behavioural Indicator', 'Technical Support Officer (Audio Visual) [TSO (AV)]'),
        ('Behavioural Indicator', 'Operation Support Officer [OSO]')
    ])

    # Filter and structure the Behavioural Indicators DataFrame
    filtered_bi_df = bi_df[bi_columns]
    # Adjust the columns to have a multi-index header for the specified roles
    filtered_bi_df.columns = ['Sector', 'Dimension/ Learning Area'] + list(bi_multi_columns[:len(selected_columns)])

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
    
    programmes_multi_columns = pd.MultiIndex.from_tuples([
        ('Course Type', 'Vice Principal (Admin) [VP(A)]'),
        ('Course Type', 'Adminstrative Manager [AM]'),
        ('Course Type', 'Operation Manager [OM]'),
        ('Course Type', 'Assistant Operation Manager/SLT [Assistant OM/SLT]'),
        ('Course Type', 'ICT Manager'),
        ('Course Type', 'Cluster ICT Manager'),
        ('Course Type', 'STEM Instructor (Workshop)'),
        ('Course Type', 'STEM Instructor (Laboratory)'),
        ('Course Type', 'Corporate Support Officer [CSO]'),
        ('Course Type', 'Admin Executive [AE]'),
        ('Course Type', 'Technical Support Officer (Audio Visual) [TSO (AV)]'),
        ('Course Type', 'Operation Support Officer [OSO]')
    ])

    # Filter and structure the Programmes DataFrame
    filtered_programmes_df = programmes_df[programmes_columns]
    # Adjust the columns to have a multi-index header for the specified roles
    filtered_programmes_df.columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + list(programmes_multi_columns[:len(selected_columns)]) + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]

    # Display the filtered Programmes DataFrame
    st.write("### Filtered Programmes Data")
    st.dataframe(filtered_programmes_df)