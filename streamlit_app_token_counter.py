import streamlit as st

def display_token_counter():
    """Display the token counter page."""
    st.title("Token Counter")

    if 'token_log' not in st.session_state:
        st.session_state['token_log'] = []  # Initialize the token log if it doesn't exist

    # Display the log entries
    st.write("### Token Usage Log")
    if st.session_state.token_log:
        for entry in st.session_state.token_log:
            tokens_used = entry.get('tokens_used', 0)  # Default to 0 if key doesn't exist
            cost = entry.get('cost', 0)  # Default to 0 if key doesn't exist
            st.write(f"Tokens Used: {tokens_used}, Cost: ${cost:.10f}")
    else:
        st.write("No token usage recorded yet.")

def log_token_usage(tokens_used, cost):
    """Log the token usage and cost."""
    if 'token_log' not in st.session_state:
        st.session_state.token_log = []  # Initialize the token log if it doesn't exist

    # Append the log entry
    st.session_state.token_log.append({
        'tokens_used': tokens_used,
        'cost': cost
    })