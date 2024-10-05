import streamlit as st
import pandas as pd

# Step 1: Load the Excel file directly from your system (no user upload needed)
# Replace "path_to_your_file.xlsx" with the actual path to the Excel file

file_path = "C:\Data Files\2024 AI Champions Bootcamp\Documents\Database\SAT Learning Roadmap_FY24_3 Sep 24 (For Testing).xlsx"
df = pd.read_excel(file_path)

# Step 2: Display the dataframe before filtering
st.write("### Full Data")
st.dataframe(df)

# Step 3: Define pre-defined checkboxes for filtering
st.sidebar.header("Filter Options")

# Example columns to filter
filter_columns = ['Column1', 'Column2', 'Column3']  # Change to match your DataFrame columns

# Create checkboxes dynamically based on unique values in each column
selected_filters = {}
for column in filter_columns:
    unique_values = df[column].unique()
    selected_values = st.sidebar.multiselect(f"Select values for {column}", unique_values)
    if selected_values:
        selected_filters[column] = selected_values

# Step 4: Apply the filters if any checkboxes were selected
if selected_filters:
    filtered_df = df.copy()
    for column, values in selected_filters.items():
        filtered_df = filtered_df[filtered_df[column].isin(values)]
    st.write("### Filtered Data")
    st.dataframe(filtered_df)
