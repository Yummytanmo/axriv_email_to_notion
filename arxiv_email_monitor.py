import os
import time
import schedule
from datetime import datetime
from imap_tools import MailBox, AND
from dotenv import load_dotenv
from arxiv_to_notion import ArxivEmailProcessor

# Load environment variables
load_dotenv()

class ArxivEmailMonitor:
    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.processor = ArxivEmailProcessor()
        self.last_processed_uid = None

    def fetch_and_process_emails(self):
        """Fetch and process new arXiv CS daily emails."""
        try:
            print(f"[{datetime.now()}] Checking for new arXiv emails...")
            
            # Connect to email server
            with MailBox(self.imap_server).login(self.email, self.password) as mailbox:
                # Search for arXiv CS daily emails
                emails = mailbox.fetch(
                    criteria=AND(
                        subject='cs daily Subj-class mailing',
                        seen=False  # Only fetch unread emails
                    ),
                    mark_seen=True  # Mark as read after fetching
                )

                for email in emails:
                    print(f"Processing email: {email.subject}")
                    
                    # Extract email content
                    email_content = email.text or email.html
                    
                    if email_content:
                        try:
                            # Process the email content
                            self.processor.process_email(email_content)
                            print(f"Successfully processed email: {email.subject}")
                        except Exception as e:
                            print(f"Error processing email: {str(e)}")
                    else:
                        print("Email content is empty")

        except Exception as e:
            print(f"Error fetching emails: {str(e)}")

def main():
    monitor = ArxivEmailMonitor()
    
    # Schedule the job to run every 4 hours
    schedule.every(4).hours.do(monitor.fetch_and_process_emails)
    
    # Run immediately on start
    monitor.fetch_and_process_emails()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute for scheduled tasks

if __name__ == "__main__":
    main() 