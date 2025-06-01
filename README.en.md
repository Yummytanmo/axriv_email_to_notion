# arXiv Email to Notion

A tool that automatically processes arXiv email notifications and adds papers to a Notion database.

**[English](#) | [中文](README.md)**

### Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Notion Configuration](#notion-configuration)
  - [Email Configuration](#email-configuration)
    - [Gmail Setup](#gmail-setup)
    - [QQ Mail Setup](#qq-mail-setup)
- [Usage](#usage)
  - [Automatic Email Monitoring](#automatic-email-monitoring)
  - [Manual Processing](#manual-processing)
- [Logging System](#logging-system)
- [Troubleshooting](#troubleshooting)
- [How It Works](#how-it-works)
- [License](#license)

### Overview

This tool automatically processes arXiv email notifications and adds papers to a Notion database. It can either process emails manually or monitor your inbox automatically for new arXiv CS daily mailings.

### Features

- Automatic email monitoring every 4 hours
- Processes only unread arXiv CS daily mailings
- Extracts paper details including:
  - Title
  - Authors
  - Categories
  - Abstract
  - arXiv ID
  - URL
  - Publication date
  - Comments (if available)
- Automatically formats data for Notion
- Handles multiple papers per email
- Comprehensive logging system
- Error handling for both email fetching and Notion API calls
- Support for multiple email providers (Gmail, QQ Mail, etc.)

### Setup

#### Prerequisites

- Python 3.7 or higher
- A Notion account
- An email account with arXiv daily mailings
- For Gmail users: Two-factor authentication enabled

#### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/arxiv-email-to-notion.git
cd arxiv-email-to-notion
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

#### Notion Configuration

1. Create a Notion integration:
   - Go to https://www.notion.so/my-integrations
   - Create a new integration
   - Copy the integration token

2. Create a Notion database with the following properties:
   - Title (title)
   - Authors (rich text)
   - Categories (rich text)
   - Abstract (rich text)
   - arXiv ID (rich text)
   - URL (url)
   - Date (date)
   - Comments (rich text)

3. Share your database with the integration:
   - Open your database in Notion
   - Click "Share" and add your integration
   - Copy the database ID from the URL (it's the part after the workspace name and before the "?")

4. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your:
- Notion integration token
- Notion database ID
- Email address
- Email password
- MAX_PAPERS (optional, limits the number of papers processed each time, default is 10)
- CONSOLE_LOG_LEVEL (optional, default is INFO)
- FILE_LOG_LEVEL (optional, default is DEBUG)

#### Email Configuration

##### Gmail Setup

If you're using Gmail, follow these steps:

1. Enable 2-Step Verification:
   - Visit https://myaccount.google.com/security
   - Click "2-Step Verification"
   - Follow the setup instructions

2. Generate App Password:
   - Visit https://myaccount.google.com/security
   - Find "App passwords" (requires 2-Step Verification to be enabled)
   - Click "Select app" and choose "Other (Custom name)"
   - Enter a name (e.g., "ArXiv Notion")
   - Click "Generate"
   - Save the 16-digit password

3. Configure .env file:
```
EMAIL=your.email@gmail.com
EMAIL_PASSWORD=your_16_digit_app_password
IMAP_SERVER=imap.gmail.com
```

Note: For G Suite/Google Workspace accounts, you may need to:
1. Visit Google Workspace Admin Console
2. Go to Security > Basic settings
3. Enable "Allow users to manage their access to less secure apps"

##### QQ Mail Setup

If you're using QQ Mail, follow these steps:

1. Enable IMAP service:
   - Login to your QQ Mail (mail.qq.com)
   - Go to Settings (设置) -> Accounts (账户)
   - Find POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV Service
   - Enable IMAP service
   - Generate and save the authorization code

2. Configure .env file:
```
EMAIL=your_qq_email@qq.com
EMAIL_PASSWORD=your_authorization_code
```

Note: The application is already configured to use QQ Mail's IMAP server (imap.qq.com).

### Usage

#### Automatic Email Monitoring

To automatically monitor your inbox for new arXiv CS daily mailings every 4 hours:

```bash
python arxiv_email_monitor.py
```

The script will:
1. Check your inbox every 4 hours
2. Process any new unread arXiv CS daily mailing emails
3. Add the papers to your Notion database
4. Mark the emails as read

#### Manual Processing

You can also manually process email content:

1. Save your arXiv email content to a file:
```bash
cat > arxiv_email.txt
# Paste email content and press Ctrl+D
```

2. Process the email:
```bash
cat arxiv_email.txt | python arxiv_to_notion.py
```

### Logging System

The application includes a comprehensive logging system:

- Log files are stored in the `logs` directory with date-based filenames
- Logs are rotated (max 10MB per file, keeping 10 backup files)
- Console logging shows basic information (default: INFO level)
- File logging includes detailed debug information (default: DEBUG level)

You can configure the log levels in your `.env` file:
```
CONSOLE_LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
FILE_LOG_LEVEL=DEBUG    # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Troubleshooting

1. Login failures:
   - Verify app password is correct
   - Confirm 2-Step Verification is enabled
   - Check email address in .env file

2. Connection errors:
   - Check network connection
   - Verify IMAP settings
   - Ensure IMAP access is enabled in Gmail settings

### How It Works

The application works through two main components:

1. **ArxivEmailProcessor** (`arxiv_to_notion.py`):
   - Parses arXiv email content
   - Extracts paper details using regular expressions
   - Formats the data for Notion
   - Creates entries in your Notion database

2. **ArxivEmailMonitor** (`arxiv_email_monitor.py`):
   - Connects to your email server via IMAP
   - Searches for unread arXiv CS daily mailing emails
   - Passes email content to the ArxivEmailProcessor
   - Marks processed emails as read
   - Runs on a schedule every 4 hours

The system uses environment variables for configuration and includes a comprehensive logging system that writes to both the console and log files.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
