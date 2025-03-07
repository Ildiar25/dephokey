import unittest
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class TestMailcatcher(unittest.TestCase):
    def setUp(self):
        self.smtp_host = "localhost"
        self.smtp_port = 1025
        self.sender = "test@dephokey.com"
        self.recipient = "user@example.com"

    def test_send_email(self):
        """Test sending an email through mailcatcher."""
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = "Test Email from Dephokey"
        
        # Add body
        body = "This is a test email sent to mailcatcher."
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        try:
            smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
            smtp.send_message(msg)
            smtp.quit()
            success = True
        except Exception as e:
            print(f"Failed to send email: {e}")
            success = False
            
        self.assertTrue(success, "Email should be sent successfully")


if __name__ == "__main__":
    print("Sending test email to mailcatcher...")
    print("Make sure mailcatcher is running (run 'make up' first)")
    print("Check http://localhost:1080 to see if the email was received")
    
    # Create instance and run test directly
    test = TestMailcatcher()
    test.setUp()
    test.test_send_email()
    print("Test email sent. Check mailcatcher interface.")