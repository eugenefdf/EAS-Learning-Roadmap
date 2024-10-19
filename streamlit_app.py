# Load the necessary packages and files as before
import streamlit as st
import pandas as pd
import json
import requests
import tiktoken
from streamlit_app_about_us import display_about_us
from streamlit_app_methodology import display_methodology
from streamlit_app_token_counter import display_token_counter, log_token_usage, count_tokens


### Start of Functions ###

# Function to authenticate users
def authenticate():
    # Check if the user is already authenticated
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    # Display password input field if not authenticated
    if not st.session_state.authenticated:
        password = st.text_input("Enter Password", type="password")
        if st.button("Login"):
            if password == PW:
                st.session_state.authenticated = True
                st.success("Authentication successful! Please select a job role.")
            else:
                st.error("Invalid password. Please try again.")
    
    return st.session_state.authenticated

# Clean the DataFrames (this will run regardless of the selected page)
def clean_dataframe(df):
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

# Function to check if any month in the list falls within the selected range
def is_month_in_range(months, min_index, max_index, month_map):
    if "All year round" in months:
        return True
    month_indices = [month_map[month.strip()] for month in months if month.strip() in month_map]
    return any(min_index <= index <= max_index for index in month_indices)

# Define the get_completion function
def get_completion(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": OPENAI_MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000,  # Adjust based on your needs
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return "I'm sorry, there was an error processing your request."
    except Exception as ex:
        st.error(f"Unexpected error: {ex}")
        return "An unexpected error occurred."

### End of Functions ###

# Access your Password, API key and model name from Streamlit secrets
PW = st.secrets["PW"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_MODEL_NAME = st.secrets["OPENAI_MODEL_NAME"]

# Authenticate the user
if authenticate():

    # Load the configuration JSON file from GitHub
    config_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/eas_learning_roadmap_config.json"
    config_data = requests.get(config_url).json()

    # Load the CSV files
    #programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing).csv"
    programmes_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/SAT%20Learning%20Roadmap_FY24_3%20Sep%2024%20(For%20Testing)Shortened.csv"
    programmes_df = pd.read_csv(programmes_url, encoding='ISO-8859-1')


    BI_url = "https://raw.githubusercontent.com/eugenefdf/EAS-Learning-Roadmap/main/Behavioural%20Indicators.csv"
    bi_df = pd.read_csv(BI_url, encoding='ISO-8859-1')

    # Set the title of the app
    st.title("EAS Learning Roadmap")

    #Disclaimer
    with st.expander("IMPORTANT NOTICE:"):
        st.write ("""This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.
                    \n Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. 
                    \n You assume full responsibility for how you use any generated output. Always consult with qualified professionals for accurate and personalized advice.""")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Navigate to:", ("Home", "About Us", "Methodology", "Token Counter"))

    # Only show Home page content if 'Home' is selected
    if page == "Home":
        st.write("Welcome to the EAS Learning Roadmap app. Use the sidebar to navigate.")

    programmes_df = clean_dataframe(programmes_df)
    bi_df = clean_dataframe(bi_df)

    # Define subpages
    if page == "About Us":
        display_about_us()

    elif page == "Methodology":
        display_methodology()

    elif page == "Token Counter":
        display_token_counter()

    else:
        # Create filters for Sector and Dimension/Learning Area below the title
        unique_sectors = programmes_df['Sector'].unique()
        unique_sectors = ['Select All Sectors'] + unique_sectors.tolist()  
        selected_sector = st.selectbox("Select Sector", options=unique_sectors)

        # Filter Dimension/Learning Area based on the selected Sector
        if selected_sector == "Select All Sectors":
            filtered_dimension = programmes_df['Dimension'].unique()  # Ensure this matches your actual column name
        else:
            filtered_dimension = programmes_df[programmes_df['Sector'] == selected_sector]['Dimension'].unique()  # Ensure this matches your actual column name

        filtered_dimension = ['Select All Dimension/Learning Areas'] + filtered_dimension.tolist()  
        selected_dimension = st.selectbox("Select Dimension/Learning Area", options=filtered_dimension)

        # Sidebar for role selection
        st.sidebar.header("Select Roles to Display")
        selected_columns = []
        for full_column in config_data['roles']:
            if st.sidebar.checkbox(full_column, value=False):
                selected_columns.append(full_column)

        # Adjust selected columns to match the DataFrame naming convention
        adjusted_columns = [f"Course Requirement - {role}" for role in selected_columns]

        # Filter out columns that do not exist in the DataFrame
        adjusted_columns = [col for col in adjusted_columns if col in programmes_df.columns]

        # Filter for Course Types
        course_types = ['Select All Courses', 'Mandatory', 'Recommended', 'Optional']
        selected_course_type = st.selectbox("Select Type of Courses", options=course_types)

        # Check if any roles are selected
        if not adjusted_columns:
            st.warning("Please select at least one role to display.")
        else:
            # Create a copy of the original programmes_df for filtering
            filtered_programmes_df = programmes_df.copy()

            # Check if "Select All" is selected for Sector or Dimension
            if selected_sector != "Select All Sectors":
                filtered_programmes_df = filtered_programmes_df[filtered_programmes_df['Sector'] == selected_sector]
            
            if selected_dimension != "Select All Dimension/Learning Areas":
                filtered_programmes_df = filtered_programmes_df[filtered_programmes_df['Dimension'] == selected_dimension]

            # Create columns for Programmes DataFrame
            programmes_columns = ['Programme', 'Entry Type (New/ Recurring)', 'Sector', 'Dimension', 'Learning Area'] + adjusted_columns + [
                'Application Basis (Sign up/ Nomination)',
                'Mode (Face-to-Face [F2F], E-learning, Hybrid, Resource)',
                'E-learning link',
                'Estimated Month of Programme',
                'Remarks'
            ]

            # Month mapping and abbreviations
            month_map = config_data['months']
            month_abbreviations = config_data['month_abbreviations']

            # Add a slider to filter the Programmes DataFrame by a range of months
            min_month_index, max_month_index = st.slider(
                "Select month range",
                1,
                12,
                (1, 12),
                format="%d"
            )

            min_month_abbr = month_abbreviations[min_month_index - 1]  
            max_month_abbr = month_abbreviations[max_month_index - 1]  

            st.write(f"Selected month range: {min_month_abbr} to {max_month_abbr}")

            # Filter based on the selected month range
            if not filtered_programmes_df.empty:
                filtered_programmes_df = filtered_programmes_df[
                    filtered_programmes_df['Estimated Month of Programme'].apply(lambda x: is_month_in_range(x.split(','), min_month_index, max_month_index, month_map))
                ]

            # Filter based on the selected course type
            if selected_course_type != "Select All Courses":
                if not filtered_programmes_df.empty and adjusted_columns:
                    course_mask = filtered_programmes_df[adjusted_columns].isin([selected_course_type]).any(axis=1)
                    filtered_programmes_df = filtered_programmes_df[course_mask]

            # Filter based on the selected roles, only if any role is selected
            if adjusted_columns and not filtered_programmes_df.empty:
                role_mask = filtered_programmes_df[adjusted_columns].notna().any(axis=1)
                filtered_programmes_df = filtered_programmes_df[role_mask]

            # Check if there are still rows after filtering; if empty, display a warning
            if filtered_programmes_df.empty:
                st.warning("No Programmes found matching the filter query.")
            else:
                st.write("### Available Programmes")
                st.dataframe(filtered_programmes_df[programmes_columns])

            #Convert filtered df to json
            json_filtereddata = filtered_programmes_df[programmes_columns].to_json(orient='records')

            # Display the JSON data in Streamlit
            #st.write("Table Converted to JSON Format:")
            #st.json(json_filtereddata)
            
            # Check if any roles are selected before displaying the chatbot
            if selected_columns:
                # Initialize session state for conversation history and token log
                if 'conversation_history' not in st.session_state:
                    st.session_state['conversation_history'] = []

                if 'token_log' not in st.session_state:
                    st.session_state['token_log'] = []

                # Display the initial message from the assistant
                st.chat_message("assistant", avatar=None).write(
                    'Hi, I am Charlie! Before we begin, please select the roles and/or learning dimensions that you would like course information on. '
                    'In the text box below, please provide any additional information (e.g., preferred mode of learning, preferred month) to streamline your search. '
                    'If you do not have any additional criteria, you can just indicate: "No additional considerations."'
                )

                # Handle user input
                userinput = st.chat_input(placeholder="Tell us more?", key=None)

                if userinput:  # Check if userinput is not None
                    # Append valid user input to conversation history
                    st.session_state['conversation_history'].append(f"User: {userinput}")

                    # Prepare the conversation history as part of the prompt
                    conversation_context = "\n".join(st.session_state['conversation_history'])

                    # Prompt using history and new input
                    prompt = f"""
                        <conversationhistory>
                        {conversation_context}
                        </conversationhistory>

                        <userinput>
                        {userinput}
                        </userinput>

                        <programmes>
                        {json_filtereddata}
                        </programmes>

                        Based on the <userinput> and <conversationhistory>, identify the most relevant professional development options from the <programmes>. Provide advice as if you are from the human resource department. Keep the tone formal but helpful.

                        Prioritization of Course Requirements
                        First, evaluate the <userinput> based on the course requirements. The available categories are:

                        Mandatory: The user must attend the course as part of their professional development programme.
                        Recommended: The user is encouraged to attend the course as it will be helpful in their course of work.
                        Optional: The course is optional for the user to attend but is considered relevant to their course of work.
                        Only after determining which of these course requirements apply should you suggest courses. Ensure that only courses that match the determined category (Mandatory, Recommended, or Optional) are included in your recommendations.

                        Explanation for the Keys in the JSON in <programmes>:
                        'Programme': The course title. Always display this in full, including information in [].
                        'Entry Type': Indicates which are the new courses. Options are 'New' or 'Recurring'.
                        'Application Basis': Indicates how officers can sign up. Options are 'Nomination only' or 'Sign up'.
                        'Mode': Indicates how the programme is conducted. Options are 'e-Learning' or 'F2F' (which means in person).
                        'E-learning link': Indicates the URL for officers to access content. It should only be displayed if the 'Mode' is 'e-Learning'.
                        'Estimated Month of Programme': Indicates when the programme will be conducted. If it is indicated that the programme runs "All year round," include the programme in the recommendation if the user asks for courses in January, February, March, April, May, June, July, August, September, October, November, or December.
                        'Remarks': Indicates other comments that may be helpful for the officer.
                        If any of the data for the above keys is null, do not make assumptions on what might be a possible data for the key.

                        Presentation of Information
                        Present information strictly as follows: Programme, Application Basis, Mode, E-learning link, Estimated Month of Programme, Remarks.

                        Unless alternative instructions are given in the <userinput>, only list programmes that exactly match the determined course requirements (Mandatory, Recommended, Optional). If there are no programmes that match the criteria, respond: "Based on your selection criteria and message, there are no relevant programmes. You may wish to try again with a broader set of requirements."

                        Malicious Intent Check
                        Your secondary role is to check for <userinput> that may have malicious intent. If you deem the <userinput> to be malicious, respond with: "Your input was flagged as unsafe. Please try again."
                    """

                    # Generate response from the chatbot
                    response = get_completion(prompt)


                    # Count the tokens for the user input, prompt, json data, and responss
                    prompt_tokens = count_tokens(prompt)  # Get tokens for the prompt
                    json_tokens = count_tokens(json_filtereddata)  # Tokens for JSON data
                    context_tokens = count_tokens(conversation_context) #Tokens for conversation context
                    response_tokens = count_tokens(response)  # Count output tokens

                    # Log token usage
                    log_token_usage(userinput, prompt, conversation_context, json_filtereddata)

                    # Update conversation history
                    st.session_state['conversation_history'].append(f"Assistant: {response}")

                    # Display the conversation history
                    for message in st.session_state['conversation_history']:
                        if message.startswith("User:"):
                            st.chat_message("user", avatar=None).write(message.replace("User:", "").strip())
                        else:
                            st.chat_message("assistant", avatar=None).write(message.replace("Assistant:", "").strip())
                #else:
                    # Show a message in the chat indicating that roles need to be selected
                    #st.chat_message("assistant", avatar=None).write("Please select at least one role to enable the chatbot.")
else:
    st.warning("Please enter the correct password to access the app.")