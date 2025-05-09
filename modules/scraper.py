"""
RSS feed fetching and parsing functionality.
"""
import feedparser
import logging
from typing import List, Dict, Any, Optional

# Configure logging
logger = logging.getLogger('bbc-rss-scraper')

def load_feed_urls(file_path: str) -> List[str]:
    """
    Load RSS feed URLs from a file.
    
    Args:
        file_path: Path to the file containing feed URLs
        
    Returns:
        List of feed URLs
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        logger.info(f"Loaded {len(urls)} feed URLs from {file_path}")
        return urls
    except FileNotFoundError:
        logger.error(f"Feed URL file not found: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error loading feed URLs: {str(e)}")
        return []

def fetch_feed(url: str) -> Optional[Dict[str, Any]]:
    """
    Fetch and parse an RSS feed.
    
    Args:
        url: URL of the RSS feed
        
    Returns:
        Parsed feed or None if there was an error
    """
    try:
        logger.info(f"Fetching feed: {url}")
        feed = feedparser.parse(url)
        
        if feed.get('bozo_exception'):
            logger.warning(f"Malformed feed at {url}: {feed.get('bozo_exception')}")
        
        if not feed.get('entries'):
            logger.warning(f"No entries found in feed: {url}")
            
        return feed
    except Exception as e:
        logger.error(f"Error fetching feed {url}: {str(e)}")
        return None

def extract_entries(feed: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract required fields from feed entries.
    
    Args:
        feed: Parsed feed
        
    Returns:
        List of dictionaries with extracted entry data
    """
    entries = []
    
    try:
        for entry in feed.get('entries', []):
            # Extract required fields
            entry_data = {
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
                'summary': entry.get('description', '')
            }
            entries.append(entry_data)
            
        logger.info(f"Extracted {len(entries)} entries from feed")
        return entries
    except Exception as e:
        logger.error(f"Error extracting entries: {str(e)}")
        return [] 