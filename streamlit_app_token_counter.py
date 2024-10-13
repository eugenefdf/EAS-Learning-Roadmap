import streamlit as st
import tiktoken

# Token counting constants
TOKEN_PRICE = 0.0004  # Example: price per token in USD for OpenAI

# Use the tokenizer for the specific model
def get_tokenizer():
    return tiktoken.encoding_for_model("gpt-4o-mini")

def count_tokens(prompt):
    """Count the number of tokens in a prompt using the GPT-4o-mini tokenizer."""
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(prompt))

def estimate_cost(tokens_used):
    """Estimate the cost based on tokens used."""
    return tokens_used * TOKEN_PRICE

def log_token_usage(user_input, summary_and_questions, response):
    """Log the token usage for each conversation."""
    tokens_used = count_tokens(user_input) + count_tokens(summary_and_questions) + count_tokens(response)
    estimated_cost = estimate_cost(tokens_used)

    # Log the entry with a limit of last 5 responses
    if 'token_log' not in st.session_state:
        st.session_state['token_log'] = []

    # Append new log entry
    st.session_state['token_log'].append({
        "user_input": user_input,
        "summary_and_questions": summary_and_questions,
        "tokens_used": tokens_used,
        "estimated_cost": estimated_cost,
        "response": response
    })

    # Keep only the last 5 entries
    if len(st.session_state['token_log']) > 5:
        st.session_state['token_log'] = st.session_state['token_log'][-5:]

def clear_token_log():
    """Clear the token log."""
    st.session_state['token_log'] = []

def display_token_counter():
    """Display the token counter page and log."""
    # Initialize session state for token log if it doesn't exist
    if 'token_log' not in st.session_state:
        st.session_state['token_log'] = []

    st.write("### Token Usage Log")
    if st.session_state['token_log']:
        for entry in st.session_state['token_log']:
            st.write(f"**User Input:** {entry['user_input']}")
            st.write(f"**Summary and Questions:** {entry['summary_and_questions']}")
            st.write(f"**Tokens Used:** {entry['tokens_used']}")
            st.write(f"**Estimated Cost:** ${entry['estimated_cost']:.4f}")
            st.write(f"**Assistant Response:** {entry['response']}")
            st.write("---")  # Separator for readability
    else:
        st.write("No token usage data available yet.")
