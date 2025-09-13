import os
import smtplib
import csv
import datetime
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read today’s tip markdown file
today = datetime.date.today().isoformat()
with open(f"tips/{today}.md", encoding="utf-8") as f:
    raw = f.read()
# Split front matter and body (front matter between --- markers)
_, front_matter, body = raw.split('---', 2)
meta = yaml.safe_load(front_matter)
title = meta.get("title", f"SQL Tip {today}")

# Load subscribers from CSV
subscribers = []
with open("subscribers.csv", newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    subscribers = list(reader)

# SMTP Gmail setup (use environment variables)
gmail_user = os.getenv("GMAIL_USER")
gmail_pass = os.getenv("GMAIL_APP_PASSWORD")

# Connect to Gmail SMTP server
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login(gmail_user, gmail_pass)

# Send email to each subscriber
for sub in subscribers:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = title
    msg["From"] = gmail_user
    msg["To"] = sub["email"]
    
    html_content = f"""
    <html>
      <body>
        <h2>{title}</h2>
        <pre style="font-family: monospace; background-color: #f4f4f4; padding: 10px;">{body}</pre>
        <p>Enjoy your SQL learning journey!</p>
      </body>
    </html>
    """
    part = MIMEText(html_content, "html")
    msg.attach(part)
    
    server.sendmail(gmail_user, sub["email"], msg.as_string())
    print(f"Sent email to {sub['email']}")

server.quit()
