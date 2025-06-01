import os
import time
import schedule
import signal
import sys
from datetime import datetime
from imap_tools import MailBox, AND
from dotenv import load_dotenv
from arxiv_to_notion import ArxivEmailProcessor
from logger import Logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = Logger("arxiv_email_monitor").logger

# Note: For email configuration:
# - For QQ Mail, you need to use an authorization code as the password
# - For Gmail, you need to use an App Password if 2FA is enabled
# Configuration is done through the .env file:
# - IMAP_SERVER: The IMAP server address (e.g., imap.qq.com, imap.gmail.com)
# - IMAP_PORT: The IMAP server port (usually 993 for SSL)
# - IMAP_SSL: Whether to use SSL (True/False)

class ArxivEmailMonitor:
    def __init__(self):
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.imap_server = os.getenv("IMAP_SERVER")
        self.imap_port = int(os.getenv("IMAP_PORT", "993"))
        self.max_papers = int(os.getenv("MAX_PAPERS", "10"))
        self.processor = ArxivEmailProcessor()
        self.last_processed_uid = None
        
        # Log configuration (without sensitive data)
        logger.info(f"ArxivEmailMonitor initialized with: email={self.email}, server={self.imap_server}, port={self.imap_port}")
        logger.info(f"Max papers per email: {self.max_papers}")

    def fetch_and_process_emails(self):
        """Fetch and process new arXiv CS daily emails."""
        try:
            logger.info("Checking for new arXiv emails...")
            
            # Connect to IMAP server with settings from environment variables
            with MailBox(self.imap_server, self.imap_port).login(self.email, self.password) as mailbox:
                logger.debug("Connected to the mailbox successfully.")
                # Search for arXiv CS daily emails
                emails = list(mailbox.fetch(
                    criteria=AND(
                        subject='cs daily Subj-class mailing',
                        seen=False  # Only fetch unread emails
                    ),
                    mark_seen=True  # Mark as read after fetching
                ))
                
                logger.info(f"Found {len(emails)} unread arXiv emails to process")
                
                for email in emails:
                    logger.info(f"Processing email: {email.subject}")
                    
                    # Extract email content
                    email_content = email.text or email.html
                    
                    if email_content:
                        try:
                            # Process the email content
                            self.processor.process_email(email_content, max_papers=self.max_papers)
                            logger.info(f"Successfully processed email: {email.subject}")
                        except Exception as e:
                            logger.error(f"Error processing email: {str(e)}", exc_info=True)
                    else:
                        logger.warning("Email content is empty")

        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}", exc_info=True)

def main():
    # Signal handler for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Received shutdown signal, exiting gracefully")
        sys.exit(0)
        
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Starting ArXiv Email Monitor")
    monitor = ArxivEmailMonitor()
    
    # Schedule the job to run every 4 hours
    schedule.every(4).hours.do(monitor.fetch_and_process_emails)
    logger.info("Scheduled task to run every 4 hours")
    
    # Run immediately on start
    logger.info("Running initial check for emails")
    monitor.fetch_and_process_emails()
    
    # Keep the script running
    logger.info("Entering main loop to monitor scheduled tasks")
    while True:
        try:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour for scheduled tasks
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {str(e)}", exc_info=True)
            # Short sleep before retrying to avoid tight error loops
            time.sleep(60)

if __name__ == "__main__":
    logger.info("=== ArXiv Email Monitor Starting ===")
    logger.info(f"Logger initialized. Log files will be saved in the logs directory.")
    main()