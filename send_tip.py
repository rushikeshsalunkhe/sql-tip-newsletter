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
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8fafc; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 28px; font-weight: 600;">📊 SQL Tips Newsletter</h1>
                <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 16px;">Master SQL, One Tip at a Time</p>
            </div>
            
            <!-- Main Content -->
            <div style="padding: 30px 25px;">
                <h2 style="color: #2d3748; margin: 0 0 20px 0; font-size: 24px; border-bottom: 3px solid #667eea; padding-bottom: 10px;">{title.replace('Daily SQL Tip - ', '').replace(today, '')}</h2>
                
                <div style="background-color: #f7fafc; border-left: 4px solid #667eea; margin: 20px 0; padding: 20px; border-radius: 0 8px 8px 0;">
                    <pre style="font-family: 'Consolas', 'Monaco', 'Courier New', monospace; background-color: #1a202c; color: #e2e8f0; padding: 20px; border-radius: 8px; margin: 0; overflow-x: auto; font-size: 14px; line-height: 1.5;">{body.strip()}</pre>
                </div>
                
                <!-- Tip of the Day Box -->
                <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 20px; border-radius: 12px; margin: 25px 0; text-align: center;">
                    <p style="margin: 0; color: #744210; font-weight: 600; font-size: 16px;">💡 Pro Tip: Practice this query in your favorite SQL environment!</p>
                </div>
                
                <!-- Premium Upgrade CTA -->
                <div style="background-color: #f0fff4; border: 2px solid #48bb78; border-radius: 12px; padding: 25px; margin: 30px 0; text-align: center;">
                    <h3 style="color: #276749; margin: 0 0 15px 0; font-size: 20px;">🚀 Upgrade to Premium</h3>
                    <p style="color: #2f855a; margin: 0 0 20px 0; font-size: 16px;">Get advanced SQL techniques, interview questions, and exclusive content!</p>
                    <a href="#" style="display: inline-block; background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);">Subscribe for $1/month</a>
                    <p style="color: #68d391; margin: 15px 0 0 0; font-size: 14px;">✨ Cancel anytime • 7-day free trial</p>
                </div>
            </div>
            
            <!-- Social & Engagement -->
            <div style="background-color: #edf2f7; padding: 25px; text-align: center;">
                <h3 style="color: #4a5568; margin: 0 0 15px 0; font-size: 18px;">📢 Spread the Knowledge</h3>
                <p style="color: #718096; margin: 0 0 20px 0;">Know someone who'd love these SQL tips?</p>
                <a href="#" style="display: inline-block; background-color: #667eea; color: white; padding: 10px 25px; text-decoration: none; border-radius: 20px; margin: 0 10px; font-weight: 500;">Share Newsletter</a>
                <a href="#" style="display: inline-block; background-color: #38b2ac; color: white; padding: 10px 25px; text-decoration: none; border-radius: 20px; margin: 0 10px; font-weight: 500;">Follow on Twitter</a>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #2d3748; color: #a0aec0; padding: 30px 25px; text-align: center;">
                <p style="margin: 0 0 15px 0; font-size: 16px; color: #e2e8f0;">Happy Querying! 🎯</p>
                <p style="margin: 0 0 20px 0; font-size: 14px;">You're receiving this because you subscribed to SQL Tips Newsletter</p>
                
                <div style="border-top: 1px solid #4a5568; padding-top: 20px; margin-top: 20px;">
                    <p style="margin: 0 0 10px 0; font-size: 13px;">SQL Tips Newsletter • Daily SQL Learning</p>
                    <a href="#" style="color: #81e6d9; text-decoration: none; font-size: 12px; margin: 0 10px;">Unsubscribe</a>
                    <a href="#" style="color: #81e6d9; text-decoration: none; font-size: 12px; margin: 0 10px;">Manage Preferences</a>
                    <a href="#" style="color: #81e6d9; text-decoration: none; font-size: 12px; margin: 0 10px;">Contact Us</a>
                </div>
            </div>
            
        </div>
    </body>
    </html>
    """
    part = MIMEText(html_content, "html")
    msg.attach(part)
    
    server.sendmail(gmail_user, sub["email"], msg.as_string())
    print(f"Sent email to {sub['email']}")

server.quit()
