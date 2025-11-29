import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging
from src.core.config import Config

class EmailSender:
    def __init__(self):
        self.sender_email = Config.get_email_sender()
        self.password = Config.get_email_password()
        
    def send_appointment_confirmation(self, to_email: str, appointment_details: str, ics_path: str = None) -> bool:
        """
        Send an appointment confirmation email with optional ICS attachment.
        
        Args:
            to_email: Recipient email address
            appointment_details: Text details of the appointment
            ics_path: Path to the .ics file to attach
            
        Returns:
            True if successful, False otherwise
        """
        if not self.sender_email or not self.password:
            logging.warning("Email credentials not set. Skipping email sending.")
            return False
            
        if self.password == "no need":
            logging.warning("Email password is set to placeholder 'no need'. Skipping email sending.")
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = "אישור תור - היפות של רותי"

            body = f"""
            היי! 👋
            
            שמחה שקבענו! הנה פרטי התור שלך:
            
            {appointment_details}
            
            מצורף קובץ זימון ליומן.
            נתראה בקרוב! 🌸
            """
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            if ics_path and os.path.exists(ics_path):
                with open(ics_path, "rb") as f:
                    part = MIMEApplication(
                        f.read(),
                        Name=os.path.basename(ics_path)
                    )
                # After the file is closed
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ics_path)}"'
                msg.attach(part)

            # Connect to Gmail SMTP server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
                
            logging.info(f"Confirmation email sent to {to_email}")
            return True

        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return False

    def send_owner_notification(self, owner_email: str, details: str, ics_path: str = None) -> bool:
        """
        Send a notification email to the owner about a new appointment.
        """
        if not self.sender_email or not self.password:
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = owner_email
            msg['Subject'] = "📅 תור חדש נקבע! - היפות של רותי"

            body = f"""
            היי רותי!
            
            יש לך תור חדש ביומן:
            
            {details}
            
            מצורף קובץ הזימון.
            """
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            if ics_path and os.path.exists(ics_path):
                with open(ics_path, "rb") as f:
                    part = MIMEApplication(
                        f.read(),
                        Name=os.path.basename(ics_path)
                    )
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ics_path)}"'
                msg.attach(part)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.password)
                server.send_message(msg)
                
            logging.info(f"Owner notification sent to {owner_email}")
            return True

        except Exception as e:
            logging.error(f"Failed to send owner notification: {e}")
            return False
