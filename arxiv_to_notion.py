import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from notion_client import Client
from dotenv import load_dotenv
import email.utils

# Load environment variables
load_dotenv()

class ArxivPaper:
    def __init__(self, arxiv_id: str, title: str, authors: str, categories: str, 
                 abstract: str, url: str, date: str, comments: Optional[str] = None):
        """Represents an arXiv paper with metadata"""
        self.arxiv_id = arxiv_id
        self.title = title
        self.authors = authors
        self.categories = categories
        self.abstract = abstract
        self.url = url
        self.date = date
        self.comments = comments

    def get_iso_date(self) -> Optional[str]:
        """Convert email date format to ISO 8601 format"""
        try:
            parsed_date = email.utils.parsedate_to_datetime(self.date)
            return parsed_date.isoformat()
        except Exception as e:
            print(f"Warning: Could not parse date '{self.date}': {str(e)}")
            return None

class ArxivEmailProcessor:
    def __init__(self):
        """Initialize Notion client with environment credentials"""
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")

    def parse_email_content(self, email_content: str, max_papers: Optional[int] = None) -> List[ArxivPaper]:
        """Parse arXiv email content and extract paper information with max_papers limit"""
        papers = []
        # Use exact separator pattern to split paper entries
        separator = "-" * 78
        paper_entries = email_content.split(separator)
        
        paper_count = 0
        
        for entry in paper_entries:
            # Stop processing if max_papers limit reached
            if max_papers is not None and paper_count >= max_papers:
                break
                
            entry = entry.strip()
            if not entry:
                continue
                
            # Extract arXiv ID (supports both old and new formats)
            arxiv_id_match = re.search(
                r'arXiv:([\w\-/\.]+)',
                entry, 
                re.IGNORECASE
            )
            if not arxiv_id_match:
                continue
                
            # Extract all fields using helper method
            arxiv_id = arxiv_id_match.group(1)
            date = self._extract_field(entry, r'Date:\s*([^\n(]+)')
            title = self._extract_field(entry, r'Title:\s*(.*?)(?=\s*Authors?:)', re.DOTALL)
            authors = self._extract_field(entry, r'Authors?:\s*(.*?)(?=\s*Categories:)', re.DOTALL)
            categories = self._extract_field(entry, r'Categories:\s*(.*?)(?=\s*(?:Comments|Abstract|\\|$))', re.DOTALL)
            comments = self._extract_field(entry, r'Comments:\s*(.*?)(?=\s*(?:Abstract|\\|$))', re.DOTALL)
            abstract = self._extract_field(entry, r'(?:.*?\\\\\s*){2}(.*?)\\\\', re.DOTALL)            
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
            paper_count += 1  # Increment counter after successful extraction
            
        return papers

    def _extract_field(self, entry: str, pattern: str, flags=0) -> str:
        """Helper method to extract field using regex pattern"""
        match = re.search(pattern, entry, flags)
        return match.group(1).strip() if match else ""

    def add_to_notion(self, paper: ArxivPaper) -> None:
        """Add paper metadata to Notion database"""
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
            
            # Add date if successfully parsed
            if iso_date:
                properties["Date"] = {"date": {"start": iso_date}}
            
            # Create Notion page
            self.notion.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
        except Exception as e:
            print(f"Error adding paper {paper.arxiv_id} to Notion: {str(e)}")

    def process_email(self, email_content: str, max_papers: Optional[int] = None) -> None:
        """Process email content and add papers to Notion with max_papers limit"""
        papers = self.parse_email_content(email_content, max_papers)
        print(f"Processing {len(papers)} papers")
        for paper in papers:
            self.add_to_notion(paper)
        print(f"Successfully processed {len(papers)} papers")

def main():
    """Main entry point for command-line execution"""
    processor = ArxivEmailProcessor()
    
    import sys
    if len(sys.argv) < 2:
        print("Usage: python arxiv_to_notion.py <email_file_path> [max_papers]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    max_papers = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            email_content = f.read()
        processor.process_email(email_content, max_papers)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing email: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()