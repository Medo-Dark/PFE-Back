import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import MailSettings


def send_email(recipient_email: str, subject: str, html_body: str, settings: MailSettings):
    auth = (settings.FROM, settings.PASSWORD)

    # Connect to Gmail's SMTP server
    with smtplib.SMTP(settings.HOST, settings.PORT) as server:
        server.starttls()
        server.login(auth[0], auth[1])

        # Construct the email message
        message = MIMEMultipart()
        message["From"] = settings.FROM
        message["To"] = recipient_email
        message["Subject"] = subject

        # Attach the HTML content
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        # Send the email
        server.sendmail(settings.FROM, recipient_email, message.as_string())


reset_pwd_html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset Instructions</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
        }}
        p {{
            margin-bottom: 20px;
        }}
        .link {{
            color: #34568B;
            text-decoration: none;
            font-weight: bold;
        }}
        .link:hover {{
            text-decoration: underline;
        }}
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Password Reset Instructions</h1>
        <p>Dear {username},</p>
        <p>We have received a request to reset your password. To proceed with resetting your password, please click on the link below within <strong>{link_expiry_min} minutes</strong>:</p>
        <p><a href="{reset_link}" class="link">Click Here</a></p>
        <p>If you did not request a password reset, you can ignore this email.</p>
        <div class="footer">
            <p>Thank you!</p>
        </div>
    </div>
</body>
</html>
"""

problem_notify_html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Problem Notification</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            max-width: 600px;
            margin: auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #333;
        }}
        p {{
            margin-bottom: 20px;
        }}
        .link {{
            color: #34568B;
            text-decoration: none;
            font-weight: bold;
        }}
        .link:hover {{
            text-decoration: underline;
        }}   
        .footer {{
            margin-top: 20px;
            text-align: center;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Problem Alert</h1>
        <p>Dear {alerted},</p>
        <p>I hope this message finds you well. We want to inform you that we have
          recently received a notification regarding a problem in the <b> {where}</b> location. This issue was 
            flagged by <b>{username}</b>, and it is crucial that we
              address it swiftly to ensure the safety of all personnel and assets.
                </p>
        <ul>
            <li>Problem type: <b>{type}</b></li>
            <li>Problem description: <b>{description}</b></li>
            <li>Problem detection date: <b>{when}</b></li>

        </ul>
        
        <div class="footer">
            <p>Thank you!</p>
        </div>
    </div>  
</body>
</html>"""
