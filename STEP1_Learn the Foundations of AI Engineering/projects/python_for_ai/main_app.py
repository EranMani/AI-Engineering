# main_app.py
# We import the tools we just made in the other file!
import ai_utils 

user_input = "  Tell me about Deep Learning...   "

# Using functions from our imported module
cleaned_input = ai_utils.clean_text(user_input)
token_est = ai_utils.count_tokens_simple(cleaned_input)

print(f"Original: '{user_input}'")
print(f"Cleaned:  '{cleaned_input}'")
print(f"Estimated Tokens: {token_est}")