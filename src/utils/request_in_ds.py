from openai import OpenAI
# from core.config import settings

TOKEN = "sk-7e9624555176470fba0f80af1854b78c"

# Initialize the client
client = OpenAI(api_key=TOKEN, base_url="https://api.deepseek.com")

article = 'r346-456'

text_answer = f"Find all suppliers selling the article number: {article}, output the data in a table with columns: Company name, currency, cost, delivery time"

# Round 1
messages = [{"role": "assistant", "content": text_answer}]
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=messages,
    space_id="133"
)

# Access the reasoning and final answer
reasoning_content = response.choices[0].message.reasoning_content
content = response.choices[0].message.content

# Print outputs
print("Reasoning:", reasoning_content)
print("Answer:", content)

# # Round 2
# messages.append({'role': 'assistant', 'content': content})
# messages.append({'role': 'user', 'content': "How many Rs are there in the word 'strawberry'?"})
# response = client.chat.completions.create(
#     model="deepseek-reasoner",
#     messages=messages
# )
#
# # Access and print results for Round 2
# reasoning_content = response.choices[0].message.reasoning_content
# content = response.choices[0].message.content
# print("Reasoning:", reasoning_content)
# print("Answer:", content)