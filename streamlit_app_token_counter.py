import streamlit as st
import tiktoken

# Token counting constants
INPUT_TOKEN_PRICE = 0.150 / 1_000_000  # Price per input token in USD
OUTPUT_TOKEN_PRICE = 0.600 / 1_000_000  # Price per output token in USD

# Ensure selected_columns and token_log are initialized
if 'selected_columns' not in st.session_state:
    st.session_state['selected_columns'] = []
if 'token_log' not in st.session_state:
    st.session_state['token_log'] = []

def get_tokenizer():
    return tiktoken.encoding_for_model("gpt-4o-mini")

def count_tokens(text):
    tokenizer = get_tokenizer()
    return len(tokenizer.encode(text))

def estimate_cost(input_tokens_used, output_tokens_used):
    return (input_tokens_used * INPUT_TOKEN_PRICE) + (output_tokens_used * OUTPUT_TOKEN_PRICE)

def log_token_usage(user_input, prompt, json_filtereddata, context, response):
    # Count tokens for each part
    prompt_tokens = count_tokens(prompt)  # Tokens for the prompt
    json_tokens = count_tokens(json_filtereddata)  # Tokens for JSON data
    context_tokens = count_tokens(context)
    response_tokens = count_tokens(response)  # Count output tokens

    # Log the token usage
    st.session_state['token_log'].append({
        "user_input": user_input,
        "prompt_tokens": prompt_tokens,
        "context_tokens": context_tokens,
        "json_tokens": json_tokens,
        "response_tokens": response_tokens,
        "estimated_cost": estimate_cost(prompt_tokens, response_tokens)  # Cost estimation
    })

    # Keep only the last 5 entries
    if len(st.session_state['token_log']) > 5:
        st.session_state['token_log'] = st.session_state['token_log'][-5:]

def clear_token_log():
    st.session_state['token_log'] = []

def display_token_counter():
    st.title("Token Counter")
    st.write("""The token counter is used for cost evaluation and is not meant for end users. All values and costs displayed here are based on an estimate.""")

    if st.button("Clear Log"):
        clear_token_log()
        st.success("Token log cleared.")

    st.write("### Token Usage Log")
    if st.session_state['token_log']:
        for entry in st.session_state['token_log']:
            st.write(f"**User Input:** {entry.get('user_input', 'N/A')}")
            st.write(f"**Prompt Tokens:** {entry.get('prompt_tokens', 0)}")
            st.write(f"**Context Tokens:** {entry.get('context_tokens', 0)}")
            st.write(f"**JSON Tokens:** {entry.get('json_tokens', 0)}")
            st.write(f"**Response Tokens:** {entry.get('response_tokens', 0)}")
            st.write(f"**Estimated Cost:** ${entry.get('estimated_cost', 0):.8f}")
            st.write("---")
    else:
        st.write("No token usage data available yet.")

# Call the display function to render the token counter
if __name__ == "__main__":
    display_token_counter()