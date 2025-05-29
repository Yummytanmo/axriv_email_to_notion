# arXiv Email to Notion

[English](#english) | [中文](#chinese)

<a name="english"></a>
# English

This tool automatically processes arXiv email notifications and adds papers to a Notion database. It can either process emails manually or monitor your inbox automatically for new arXiv CS daily mailings.

## Setup

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

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your:
- Notion integration token
- Notion database ID
- Email address
- Email password
- IMAP server address (e.g., imap.gmail.com for Gmail)

### Gmail Setup

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

## Usage

### Automatic Email Monitoring

To automatically monitor your inbox for new arXiv CS daily mailings every 4 hours:

```bash
python arxiv_email_monitor.py
```

The script will:
1. Check your inbox every 4 hours
2. Process any new unread arXiv CS daily mailing emails
3. Add the papers to your Notion database
4. Mark the emails as read

### Manual Processing

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

## Features

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
- Error handling for both email fetching and Notion API calls

## Troubleshooting

1. Login failures:
   - Verify app password is correct
   - Confirm 2-Step Verification is enabled
   - Check email address in .env file

2. Connection errors:
   - Check network connection
   - Verify IMAP settings
   - Ensure IMAP access is enabled in Gmail settings

---

<a name="chinese"></a>
# 中文

这个工具可以自动处理 arXiv 邮件通知，并将论文信息添加到 Notion 数据库中。它可以手动处理邮件，也可以自动监控收件箱中的 arXiv CS daily mailings。

## 设置

1. 创建 Notion 集成：
   - 访问 https://www.notion.so/my-integrations
   - 创建新的集成
   - 复制集成令牌

2. 创建 Notion 数据库，包含以下属性：
   - Title (标题，类型：title)
   - Authors (作者，类型：rich text)
   - Categories (类别，类型：rich text)
   - Abstract (摘要，类型：rich text)
   - arXiv ID (arXiv编号，类型：rich text)
   - URL (链接，类型：url)
   - Date (日期，类型：date)
   - Comments (评论，类型：rich text)

3. 与集成共享数据库：
   - 在 Notion 中打开数据库
   - 点击"Share"并添加你的集成
   - 从 URL 中复制数据库 ID（在工作区名称之后，"?"之前的部分）

4. 安装依赖：
```bash
pip install -r requirements.txt
```

5. 配置环境变量：
```bash
cp .env.example .env
```
编辑 `.env` 文件并添加：
- Notion 集成令牌
- Notion 数据库 ID
- 邮箱地址
- 邮箱密码
- IMAP 服务器地址（例如 Gmail 使用 imap.gmail.com）

### Gmail 设置

如果使用 Gmail，请按以下步骤操作：

1. 开启两步验证：
   - 访问 https://myaccount.google.com/security
   - 点击"2-Step Verification"（两步验证）
   - 按照提示完成设置

2. 生成应用专用密码：
   - 访问 https://myaccount.google.com/security
   - 找到"App passwords"（应用专用密码，需要先开启两步验证）
   - 点击"Select app"并选择"Other (Custom name)"
   - 输入名称（例如："ArXiv Notion"）
   - 点击"Generate"（生成）
   - 保存生成的16位密码

3. 配置 .env 文件：
```
EMAIL=your.email@gmail.com
EMAIL_PASSWORD=your_16_digit_app_password
IMAP_SERVER=imap.gmail.com
```

注意：如果使用的是 G Suite/Google Workspace 账户，可能还需要：
1. 访问 Google Workspace 管理控制台
2. 转到安全性 > 基本设置
3. 启用"允许用户管理对不太安全应用的访问权限"

## 使用方法

### 自动邮件监控

要每4小时自动检查收件箱中的新 arXiv CS daily mailings：

```bash
python arxiv_email_monitor.py
```

脚本将：
1. 每4小时检查一次收件箱
2. 处理所有未读的 arXiv CS daily mailing 邮件
3. 将论文添加到 Notion 数据库
4. 将处理过的邮件标记为已读

### 手动处理

你也可以手动处理邮件内容：

1. 保存 arXiv 邮件内容到文件：
```bash
cat > arxiv_email.txt
# 粘贴邮件内容后按 Ctrl+D
```

2. 处理邮件：
```bash
cat arxiv_email.txt | python arxiv_to_notion.py
```

## 功能特点

- 每4小时自动监控邮件
- 仅处理未读的 arXiv CS daily mailings
- 提取论文详细信息，包括：
  - 标题
  - 作者
  - 类别
  - 摘要
  - arXiv 编号
  - URL
  - 发布日期
  - 评论（如果有）
- 自动格式化数据以适配 Notion
- 支持处理包含多篇论文的邮件
- 完善的邮件获取和 Notion API 调用错误处理

## 常见问题解决

1. 登录失败：
   - 验证应用专用密码是否正确
   - 确认已开启两步验证
   - 检查 .env 文件中的邮箱地址

2. 连接错误：
   - 检查网络连接
   - 验证 IMAP 设置
   - 确保 Gmail 中已启用 IMAP 访问 