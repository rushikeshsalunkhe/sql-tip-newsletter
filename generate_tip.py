import os
import openai
import datetime

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


# Read prompt template
with open("prompt.txt") as f:
    prompt = f.read()

# Generate tip using OpenAI GPT-3.5 Turbo
response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt=prompt,
    max_tokens=500,
    temperature=0.7
)

# Extract generated content
content = response.choices[0].text.strip()

# Prepare filename with today's date
today = datetime.date.today().isoformat()
filename = f"tips/{today}.md"

# Ensure tips folder exists
os.makedirs("tips", exist_ok=True)

# Write the generated tip to markdown file with front matter
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"---\ndate: {today}\nstatus: draft\n---\n\n")
    f.write(content)

print(f"Generated tip saved to {filename}")
