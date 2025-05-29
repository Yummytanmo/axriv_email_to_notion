import os
import re
from datetime import datetime
from typing import Dict, List
from bs4 import BeautifulSoup
from notion_client import Client
from dotenv import load_dotenv

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

class ArxivEmailProcessor:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")

    def parse_email_content(self, email_content: str) -> List[ArxivPaper]:
        """Parse arXiv email content and extract paper information."""
        papers = []
        # Split email into individual paper entries
        paper_entries = re.split(r'\\\\', email_content)
        
        for entry in paper_entries:
            if not entry.strip() or '----------------------' in entry:
                continue
                
            # Extract paper information using regex
            arxiv_id_match = re.search(r'arXiv:(\d+\.\d+)', entry)
            if not arxiv_id_match:
                continue
                
            arxiv_id = arxiv_id_match.group(1)
            
            # Extract title
            title_match = re.search(r'Title: (.*?)(?=Authors:|$)', entry, re.DOTALL)
            title = title_match.group(1).strip() if title_match else ""
            
            # Extract authors
            authors_match = re.search(r'Authors?: (.*?)(?=Categories:|$)', entry, re.DOTALL)
            authors = authors_match.group(1).strip() if authors_match else ""
            
            # Extract categories
            categories_match = re.search(r'Categories: (.*?)(?=Comments:|Abstract:|$)', entry, re.DOTALL)
            categories = categories_match.group(1).strip() if categories_match else ""
            
            # Extract abstract
            abstract_match = re.search(r'Abstract: (.*?)(?=\\|$)', entry, re.DOTALL)
            abstract = abstract_match.group(1).strip() if abstract_match else ""
            
            # Extract date
            date_match = re.search(r'Date: (.*?)(?=\(|$)', entry)
            date = date_match.group(1).strip() if date_match else ""
            
            # Extract comments if available
            comments_match = re.search(r'Comments: (.*?)(?=\\|$)', entry)
            comments = comments_match.group(1).strip() if comments_match else None
            
            # Create URL
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
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Title": {"title": [{"text": {"content": paper.title}}]},
                    "Authors": {"rich_text": [{"text": {"content": paper.authors}}]},
                    "Categories": {"rich_text": [{"text": {"content": paper.categories}}]},
                    "Abstract": {"rich_text": [{"text": {"content": paper.abstract[:2000]}}]},
                    "arXiv ID": {"rich_text": [{"text": {"content": paper.arxiv_id}}]},
                    "URL": {"url": paper.url},
                    "Date": {"date": {"start": paper.date}},
                    "Comments": {"rich_text": [{"text": {"content": paper.comments or ""}}]},
                }
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
    
    # Read email content from stdin or file
    email_content = input()
    processor.process_email(email_content)

if __name__ == "__main__":
    main()