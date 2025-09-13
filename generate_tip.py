import os
from openai import OpenAI
import datetime

# Create OpenAI client (reads OPENAI_API_KEY from environment variable)
client = OpenAI()

# Read the prompt from prompt.txt
with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt_text = f.read()

# Prepare chat messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt_text}
]

# Call OpenAI chat completions API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=500,
    temperature=0.7
)

# Extract the generated content
content = response.choices[0].message.content.strip()

# Prepare filename with today's date
today = datetime.date.today().isoformat()
os.makedirs("tips", exist_ok=True)
filename = f"tips/{today}.md"

# Write the generated tip to a markdown file with front matter
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ndate: {today}\nstatus: draft\n---\n\n")
    f.write(content)

print(f"Generated tip saved to {filename}")
