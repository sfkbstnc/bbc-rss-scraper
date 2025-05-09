"""
RSS feed fetching and parsing functionality using requests and BeautifulSoup4.
"""
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

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
    Fetch and parse an RSS feed using requests and BeautifulSoup4.
    
    Args:
        url: URL of the RSS feed
        
    Returns:
        Parsed feed or None if there was an error
    """
    try:
        logger.info(f"Fetching feed: {url}")
        
        # Make HTTP request to fetch the RSS feed
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        # Parse XML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')
        
        # Extract channel information
        channel = soup.find('channel')
        if not channel:
            logger.warning(f"No channel element found in feed: {url}")
            return None
            
        # Extract items
        items = channel.find_all('item')
        if not items:
            logger.warning(f"No items found in feed: {url}")
            
        # Create feed dictionary similar to feedparser structure
        feed = {
            'feed': {
                'title': get_text(channel.find('title')),
                'link': get_text(channel.find('link')),
                'description': get_text(channel.find('description'))
            },
            'entries': [],
            'url': url
        }
        
        # Parse each item and add to entries
        for item in items:
            entry = {
                'title': get_text(item.find('title')),
                'link': get_text(item.find('link')),
                'published': get_text(item.find('pubDate')),
                'description': get_text(item.find('description'))
            }
            feed['entries'].append(entry)
            
        logger.info(f"Successfully parsed feed with {len(feed['entries'])} entries")
        return feed
        
    except requests.RequestException as e:
        logger.error(f"Request error fetching feed {url}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error parsing feed {url}: {str(e)}")
        return None

def get_text(element) -> str:
    """
    Extract text from a BeautifulSoup element safely.
    
    Args:
        element: BeautifulSoup element
        
    Returns:
        Text content or empty string if element is None
    """
    if element is None:
        return ''
    return element.get_text(strip=True)

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