import os
import openai
import datetime

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Read prompt template
with open("prompt.txt") as f:
    prompt_text = f.read()

# Prepare the messages parameter for chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt_text}
]

# Generate tip using ChatCompletion API
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=500,
    temperature=0.7
)

content = response.choices[0].message.content.strip()

# Save to file
today = datetime.date.today().isoformat()
filename = f"tips/{today}.md"

import os
os.makedirs("tips", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ndate: {today}\nstatus: draft\n---\n\n")
    f.write(content)

print(f"Generated tip saved to {filename}")
