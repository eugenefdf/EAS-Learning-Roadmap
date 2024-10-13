import streamlit as st
import tiktoken

# Token counting constants
INPUT_TOKEN_PRICE = 0.150 / 1_000_000  # Price per input token in USD
OUTPUT_TOKEN_PRICE = 0.600 / 1_000_000  # Price per output token in USD

# Ensure selected_columns is initialized
if 'selected_columns' not in st.session_state:
    st.session_state['selected_columns'] = []

# Ensure token_log is initialized
if 'token_log' not in st.session_state:
    st.session_state['token_log'] = []

def get_tokenizer():
    return tiktoken.encoding_for_model("gpt-4o-mini")

def count_tokens(prompt):
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(prompt))

def estimate_cost(input_tokens_used, output_tokens_used):
    return (input_tokens_used * INPUT_TOKEN_PRICE) + (output_tokens_used * OUTPUT_TOKEN_PRICE)

def log_token_usage(user_input, response):
    input_tokens_used = count_tokens(user_input)
    output_tokens_used = count_tokens(response)
    estimated_cost = estimate_cost(input_tokens_used, output_tokens_used)

    st.session_state['token_log'].append({
        "user_input": user_input,
        "input_tokens_used": input_tokens_used,
        "output_tokens_used": output_tokens_used,
        "estimated_cost": estimated_cost
    })

    # Keep only the last 5 entries
    if len(st.session_state['token_log']) > 5:
        st.session_state['token_log'] = st.session_state['token_log'][-5:]

def clear_token_log():
    st.session_state['token_log'] = []

def display_token_counter():
    """Display the token counter page and log."""
    if st.button("Clear Log", key="clear_log_button_1"):
        clear_token_log()
        st.success("Token log cleared.")

    st.write("### Token Usage Log")
    if st.session_state['token_log']:
        for entry in st.session_state['token_log']:
            # Check if the log entry should be skipped
            if entry.get('summary_and_questions', 'N/A') == "N/A" and entry.get('input_tokens_used', 0) == 0 and entry.get('output_tokens_used', 0) == 0:
                continue  # Skip this log entry

            st.write(f"**User Input:** {entry.get('user_input', 'N/A')}")
            st.write(f"**Input Tokens Used:** {entry.get('input_tokens_used', 0)}")
            st.write(f"**Output Tokens Used:** {entry.get('output_tokens_used', 0)}")
            st.write(f"**Estimated Cost:** ${entry.get('estimated_cost', 0):.8f}")
            st.write("---")
    else:
        st.write("No token usage data available yet.")

# Call the display function to render the token counter
display_token_counter()