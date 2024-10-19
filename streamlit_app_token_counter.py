import streamlit as st
import tiktoken  # Make sure you have this imported

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

def count_tokens(text):
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(text))

def estimate_cost(input_tokens_used, output_tokens_used):
    return (input_tokens_used * INPUT_TOKEN_PRICE) + (output_tokens_used * OUTPUT_TOKEN_PRICE)

def log_token_usage(user_input, summary_and_questions, response, total_tokens_used):
    # Count output tokens
    output_tokens_used = count_tokens(response)

    # Calculate total input tokens (user input + prompt context) and total tokens used
    input_tokens_used = count_tokens(user_input) + total_tokens_used
    total_tokens = input_tokens_used + output_tokens_used  # Total tokens used

    # Calculate estimated cost
    estimated_cost = estimate_cost(input_tokens_used, output_tokens_used)

    st.session_state['token_log'].append({
        "user_input": user_input,
        "summary_and_questions": summary_and_questions,
        "input_tokens_used": input_tokens_used,
        "output_tokens_used": output_tokens_used,
        "total_tokens": total_tokens,  # New field for total tokens
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
            st.write(f"**User Input:** {entry.get('user_input', 'N/A')}")
            st.write(f"**Summary and Questions:** {entry.get('summary_and_questions', 'N/A')}")
            st.write(f"**Input Tokens Used:** {entry.get('input_tokens_used', 0)}")
            st.write(f"**Output Tokens Used:** {entry.get('output_tokens_used', 0)}")
            st.write(f"**Total Tokens Used:** {entry.get('total_tokens', 0)}")  # New line for total tokens
            st.write(f"**Estimated Cost:** ${entry.get('estimated_cost', 0):.8f}")
            st.write("---")
    else:
        st.write("No token usage data available yet.")

# Call the display function to render the token counter
display_token_counter()