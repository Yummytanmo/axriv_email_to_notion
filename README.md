# arXiv Email to Notion

将 arXiv 邮件通知自动处理并添加论文到 Notion 数据库的工具。

**[English](README.en.md) | [中文](#)**

### 目录
- [概述](#概述)
- [功能特点](#功能特点)
- [设置](#设置)
  - [前提条件](#前提条件)
  - [安装](#安装)
  - [Notion 配置](#notion-配置)
  - [邮箱配置](#邮箱配置)
    - [Gmail 设置](#gmail-设置)
    - [QQ邮箱设置](#qq邮箱设置)
- [使用方法](#使用方法)
  - [自动邮件监控](#自动邮件监控)
  - [手动处理](#手动处理)
- [日志系统](#日志系统)
- [常见问题解决](#常见问题解决)
- [工作原理](#工作原理)
- [许可协议](#许可协议)

## 概述

这个工具可以自动处理 arXiv 邮件通知，并将论文信息添加到 Notion 数据库中。它可以手动处理邮件，也可以自动监控收件箱中的 arXiv CS daily mailings。

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
- 全面的日志系统
- 完善的邮件获取和 Notion API 调用错误处理
- 支持多种邮件提供商（Gmail、QQ邮箱等）

## 设置

### 前提条件

- Python 3.7 或更高版本
- Notion 账户
- 订阅了 arXiv 每日邮件的邮箱账户
- Gmail 用户：需启用两步验证

### 安装

1. 克隆此仓库：
```bash
git clone https://github.com/yourusername/arxiv-email-to-notion.git
cd arxiv-email-to-notion
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

### Notion 配置

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

4. 配置环境变量：
```bash
cp .env.example .env
```
编辑 `.env` 文件并添加：
- Notion 集成令牌
- Notion 数据库 ID
- 邮箱地址
- 邮箱密码
- MAX_PAPERS (可选，限制每次处理的论文数量，默认为10)
- CONSOLE_LOG_LEVEL (可选，默认为 INFO)
- FILE_LOG_LEVEL (可选，默认为 DEBUG)

### 邮箱配置

#### Gmail 设置

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

#### QQ邮箱设置

如果使用 QQ 邮箱，请按以下步骤操作：

1. 启用 IMAP 服务：
   - 登录 QQ 邮箱 (mail.qq.com)
   - 进入设置 -> 账户
   - 找到 POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务
   - 开启 IMAP 服务
   - 生成并保存授权码

2. 配置 .env 文件：
```
EMAIL=your_qq_email@qq.com
EMAIL_PASSWORD=your_authorization_code
```

注意：应用程序已经配置为使用 QQ 邮箱的 IMAP 服务器 (imap.qq.com)。

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

## 日志系统

应用程序包含一个全面的日志系统：

- 日志文件存储在 `logs` 目录中，使用基于日期的文件名
- 日志会自动轮换（每个文件最大 10MB，保留 10 个备份文件）
- 控制台日志显示基本信息（默认：INFO 级别）
- 文件日志包含详细的调试信息（默认：DEBUG 级别）

您可以在 `.env` 文件中配置日志级别：
```
CONSOLE_LOG_LEVEL=INFO  # 选项：DEBUG, INFO, WARNING, ERROR, CRITICAL
FILE_LOG_LEVEL=DEBUG    # 选项：DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 常见问题解决

1. 登录失败：
   - 验证应用专用密码是否正确
   - 确认已开启两步验证
   - 检查 .env 文件中的邮箱地址

2. 连接错误：
   - 检查网络连接
   - 验证 IMAP 设置
   - 确保邮箱中已启用 IMAP 访问

## 工作原理

应用程序通过两个主要组件工作：

1. **ArxivEmailProcessor** (`arxiv_to_notion.py`)：
   - 解析 arXiv 邮件内容
   - 使用正则表达式提取论文详情
   - 格式化数据以适配 Notion
   - 在 Notion 数据库中创建条目

2. **ArxivEmailMonitor** (`arxiv_email_monitor.py`)：
   - 通过 IMAP 连接到您的邮件服务器
   - 搜索未读的 arXiv CS daily mailing 邮件
   - 将邮件内容传递给 ArxivEmailProcessor
   - 将处理过的邮件标记为已读
   - 每4小时运行一次计划任务

系统使用环境变量进行配置，并包含一个全面的日志系统，该系统会同时写入控制台和日志文件。

## 许可协议

本项目采用 MIT 许可协议。详情请参阅 [LICENSE](LICENSE) 文件。
