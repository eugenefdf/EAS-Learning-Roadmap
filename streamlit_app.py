import streamlit as st
import pandas as pd

# Step 1: Load the CSV files from the GitHub repository with the specified encoding
programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')  # Specify encoding here

BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')  # Specify encoding here

# Hardcoded columns based on your provided information
bi_columns = [
    'Sector',
    'Dimension/ Learning Area',
    'Behavioural Indicators - Vice Principal (Admin) [VP(A)]',
    'Behavioural Indicators - Adminstrative Manager [AM]',
    'Behavioural Indicators - Operation Manager [OM]',
    'Behavioural Indicators - Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'Behavioural Indicators - ICT Manager',
    'Behavioural Indicators - Cluster ICT Manager',
    'Behavioural Indicators - STEM Instructor (Workshop)',
    'Behavioural Indicators - STEM Instructor (Laboratory)',
    'Behavioural Indicators - Corporate Support Officer [CSO]',
    'Behavioural Indicators - Admin Executive [AE]',
    'Behavioural Indicators - Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Behavioural Indicators - Operation Support Officer [OSO]'
]

# Step 2: Create a single set of checkboxes in the sidebar for role selection (initially unticked)
st.sidebar.header("Select Roles to Display")
selected_columns = []

# Role names derived from the hardcoded columns
role_columns_full = {
    'Behavioural Indicators - Vice Principal (Admin) [VP(A)]': 'Vice Principal (Admin) [VP(A)]',
    'Behavioural Indicators - Adminstrative Manager [AM]': 'Adminstrative Manager [AM]',
    'Behavioural Indicators - Operation Manager [OM]': 'Operation Manager [OM]',
    'Behavioural Indicators - Assistant Operation Manager/SLT [Assistant OM/SLT]': 'Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'Behavioural Indicators - ICT Manager': 'ICT Manager',
    'Behavioural Indicators - Cluster ICT Manager': 'Cluster ICT Manager',
    'Behavioural Indicators - STEM Instructor (Workshop)': 'STEM Instructor (Workshop)',
    'Behavioural Indicators - STEM Instructor (Laboratory)': 'STEM Instructor (Laboratory)',
    'Behavioural Indicators - Corporate Support Officer [CSO]': 'Corporate Support Officer [CSO]',
    'Behavioural Indicators - Admin Executive [AE]': 'Admin Executive [AE]',
    'Behavioural Indicators - Technical Support Officer (Audio Visual) [TSO (AV)]': 'Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Behavioural Indicators - Operation Support Officer [OSO]': 'Operation Support Officer [OSO]'
}

for full_column, simple_column in role_columns_full.items():
    # Display simplified names in checkboxes
    if st.sidebar.checkbox(simple_column, value=False):
        selected_columns.append(full_column)

# Step 3: If no roles are selected, display a warning
if not selected_columns:
    st.warning("Please select at least one role to display.")
else:
    # Step 4: Filter the Programmes DataFrame to show only selected roles with simplified headers
    filtered_programmes_df = programmes_df[['Dimension', 'Learning Area'] + selected_columns + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]]

    # Rename the columns with simplified headers for Programmes
    simplified_headers_programmes = ['Dimension', 'Learning Area'] + [role_columns_full[col] for col in selected_columns] + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]
    filtered_programmes_df.columns = simplified_headers_programmes

    # Step 5: Display the filtered Programmes DataFrame with simplified headers
    st.write("### Filtered Programmes Data")
    st.dataframe(filtered_programmes_df)

    # Step 6: Filter the Behavioural Indicators DataFrame to show only selected roles with simplified headers
    filtered_bi_df = bi_df[['Sector', 'Dimension/ Learning Area'] + selected_columns]

    # Rename the columns with simplified headers for Behavioural Indicators
    simplified_headers_bi = ['Sector', 'Dimension/ Learning Area'] + [role_columns_full[col] for col in selected_columns]
    filtered_bi_df.columns = simplified_headers_bi

    # Step 7: Display the filtered Behavioural Indicators DataFrame with simplified headers
    st.write("### Filtered Behavioural Indicators Data")
    st.dataframe(filtered_bi_df)