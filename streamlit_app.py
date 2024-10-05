import streamlit as st
import pandas as pd

# Step 1: Load the Excel file from the GitHub repository
file_url = "https://github.com/eugenefdf/EAS-Learning-Roadmap/blob/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).xlsx"  # Replace with your actual file URL
df = pd.read_excel(file_url)

# Step 2: Define columns representing roles and simplified names for checkboxes
role_columns_full = {
    'Type of Course - Vice Principal (Admin) [VP(A)]': 'Vice Principal (Admin) [VP(A)]',
    'Type of Course - Adminstrative Manager [AM]': 'Adminstrative Manager [AM]',
    'Type of Course - Operation Manager [OM]': 'Operation Manager [OM]',
    'Type of Course - Assistant Operation Manager/SLT [Assistant OM/SLT]': 'Assistant Operation Manager/SLT [Assistant OM/SLT]',
    'Type of Course - ICT Manager': 'ICT Manager',
    'Type of Course - Cluster ICT Manager': 'Cluster ICT Manager',
    'Type of Course - STEM Instructor (Workshop)': 'STEM Instructor (Workshop)',
    'Type of Course - STEM Instructor (Laboratory)': 'STEM Instructor (Laboratory)',
    'Type of Course - Corporate Support Officer [CSO]': 'Corporate Support Officer [CSO]',
    'Type of Course - Admin Executive [AE]': 'Admin Executive [AE]',
    'Type of Course - Technical Support Officer (Audio Visual) [TSO (AV)]': 'Technical Support Officer (Audio Visual) [TSO (AV)]',
    'Type of Course - Operation Support Officer [OSO]': 'Operation Support Officer [OSO]'
}

# Step 3: Create checkboxes dynamically in the sidebar for role selection (initially unticked)
st.sidebar.header("Select Roles to Display")
selected_columns = []
for full_column, simple_column in role_columns_full.items():
    # Display simplified names in checkboxes
    if st.sidebar.checkbox(simple_column, value=False):
        selected_columns.append(full_column)

# Step 4: If no roles are selected, display a warning
if not selected_columns:
    st.warning("Please select at least one role to display.")
else:
    # Step 5: Filter the DataFrame to show only selected roles with simplified headers
    filtered_df = df[['Dimension', 'Learning Area'] + selected_columns + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]]

    # Rename the columns with simplified headers
    simplified_headers = ['Dimension', 'Learning Area'] + [role_columns_full[col] for col in selected_columns] + [
        'Application Basis (Sign up/ Nomination)',
        'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
        'E-learning link',
        'Estimated Month of Programme',
        'Remarks'
    ]
    filtered_df.columns = simplified_headers
    
    # Step 6: Display the filtered DataFrame with simplified headers
    st.write("### Filtered Data")
    st.dataframe(filtered_df)