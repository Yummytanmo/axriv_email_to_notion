import os
import re
from datetime import datetime
from typing import Dict, List
from bs4 import BeautifulSoup
from notion_client import Client
from dotenv import load_dotenv
import email.utils

# Load environment variables
load_dotenv()

class ArxivPaper:
    def __init__(self, arxiv_id: str, title: str, authors: str, categories: str, 
                 abstract: str, url: str, date: str, comments: str = None):
        self.arxiv_id = arxiv_id
        self.title = title
        self.authors = authors
        self.categories = categories
        self.abstract = abstract
        self.url = url
        self.date = date
        self.comments = comments

    def get_iso_date(self) -> str:
        """Convert email date format to ISO 8601 format."""
        try:
            # Parse the date string using email.utils
            parsed_date = email.utils.parsedate_to_datetime(self.date)
            # Convert to ISO 8601 format
            return parsed_date.isoformat()
        except Exception as e:
            print(f"Warning: Could not parse date '{self.date}': {str(e)}")
            return None

class ArxivEmailProcessor:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")

    def parse_email_content(self, email_content: str) -> List[ArxivPaper]:
        """Parse arXiv email content and extract paper information."""
        papers = []
        # 使用更可靠的分隔符分割邮件内容
        separator = "------------------------------------------------------------------------------"
        paper_entries = email_content.split(separator)
        
        for entry in paper_entries:
            if not entry.strip() or 'To unsubscribe' in entry or 'Archives at' in entry:
                continue
                
            # 提取arxiv ID - 更可靠的方法
            arxiv_id = ""
            if "arXiv:" in entry:
                arxiv_start = entry.index("arXiv:") + 6
                arxiv_end = entry.find("\n", arxiv_start)
                if arxiv_end == -1:
                    arxiv_end = len(entry)
                arxiv_id = entry[arxiv_start:arxiv_end].split()[0].strip()
            
            if not arxiv_id:
                continue
                
            # 提取标题
            title = ""
            if "Title:" in entry:
                title_start = entry.index("Title:") + 6
                title_end = entry.find("\n", title_start)
                if title_end == -1:
                    title_end = len(entry)
                title = entry[title_start:title_end].strip()
            
            # 提取作者
            authors = ""
            if "Authors:" in entry:
                authors_start = entry.index("Authors:") + 8
                authors_end = entry.find("\n", authors_start)
                if authors_end == -1:
                    authors_end = len(entry)
                authors = entry[authors_start:authors_end].strip()
            
            # 提取分类
            categories = ""
            if "Categories:" in entry:
                cats_start = entry.index("Categories:") + 11
                cats_end = entry.find("\n", cats_start)
                if cats_end == -1:
                    cats_end = len(entry)
                categories = entry[cats_start:cats_end].strip()
            
            # 提取摘要 - 不使用正则表达式
            abstract = ""
            # 查找摘要开始位置（在Comments后的\\之后）
            if "Comments:" in entry and "\\\\" in entry:
                comments_end = entry.index("Comments:") + len("Comments:")
                # 找到Comments部分后的第一个\\
                abstract_start_marker = entry.find("\\\\", comments_end)
                if abstract_start_marker != -1:
                    # 移动到摘要内容开始位置（跳过\\和可能的换行）
                    abstract_start = abstract_start_marker + 2
                    if abstract_start < len(entry) and entry[abstract_start] == '\n':
                        abstract_start += 1
                    
                    # 查找摘要结束位置（下一个\\之前）
                    abstract_end_marker = entry.find("\\\\", abstract_start)
                    if abstract_end_marker != -1:
                        # 检查结束标记后是否有URL
                        url_check = entry.find("https://arxiv.org/abs/", abstract_end_marker)
                        if url_check != -1 and url_check - abstract_end_marker < 20:
                            abstract = entry[abstract_start:abstract_end_marker].strip()
            
            # 提取日期
            date = ""
            if "Date:" in entry:
                date_start = entry.index("Date:") + 5
                date_end = entry.find("(", date_start)
                if date_end == -1:
                    date_end = entry.find("\n", date_start)
                if date_end == -1:
                    date_end = len(entry)
                date = entry[date_start:date_end].strip()
            
            # 提取评论
            comments = None
            if "Comments:" in entry:
                comments_start = entry.index("Comments:") + 9
                comments_end = entry.find("\\\\", comments_start)
                if comments_end == -1:
                    comments_end = entry.find("\n", comments_start)
                if comments_end == -1:
                    comments_end = len(entry)
                comments = entry[comments_start:comments_end].strip()
            
            # 创建URL
            url = f"https://arxiv.org/abs/{arxiv_id}"
            
            paper = ArxivPaper(
                arxiv_id=arxiv_id,
                title=title,
                authors=authors,
                categories=categories,
                abstract=abstract,
                url=url,
                date=date,
                comments=comments
            )
            papers.append(paper)
            
        return papers

    def add_to_notion(self, paper: ArxivPaper) -> None:
        """Add a paper to the Notion database."""
        try:
            iso_date = paper.get_iso_date()
            properties = {
                "Title": {"title": [{"text": {"content": paper.title}}]},
                "Authors": {"rich_text": [{"text": {"content": paper.authors}}]},
                "Categories": {"rich_text": [{"text": {"content": paper.categories}}]},
                "Abstract": {"rich_text": [{"text": {"content": paper.abstract[:2000]}}]},
                "arXiv ID": {"rich_text": [{"text": {"content": paper.arxiv_id}}]},
                "URL": {"url": paper.url},
                "Comments": {"rich_text": [{"text": {"content": paper.comments or ""}}]},
            }
            
            # Only add date if we successfully parsed it
            if iso_date:
                properties["Date"] = {"date": {"start": iso_date}}
            
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
        except Exception as e:
            print(f"Error adding paper {paper.arxiv_id} to Notion: {str(e)}")

    def process_email(self, email_content: str) -> None:
        """Process email content and add papers to Notion."""
        papers = self.parse_email_content(email_content)
        for paper in papers:
            self.add_to_notion(paper)

def main():
    # Example usage
    processor = ArxivEmailProcessor()
    
    # Read email content from file
    import sys
    if len(sys.argv) != 2:
        print("Usage: python arxiv_to_notion.py <email_file_path>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            email_content = f.read()
        processor.process_email(email_content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()