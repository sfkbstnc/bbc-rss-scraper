"""
Utility functions for the BBC RSS scraper.
"""
import logging
import os
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logger = logging.getLogger('bbc-rss-scraper')

def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application.
    
    Args:
        log_level: Logging level (default: INFO)
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger.info(f"Logging configured with level: {log_level}")

def resolve_path(base_dir: str, relative_path: str) -> str:
    """
    Resolve a path relative to a base directory.
    
    Args:
        base_dir: Base directory
        relative_path: Path relative to the base directory
        
    Returns:
        Absolute path
    """
    return os.path.join(base_dir, relative_path)

def get_timestamp() -> str:
    """
    Get the current timestamp as a formatted string.
    
    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_entries_summary(entries: List[Dict[str, Any]]) -> str:
    """
    Format a summary of the entries.
    
    Args:
        entries: List of entry dictionaries
        
    Returns:
        Summary string
    """
    if not entries:
        return "No entries found."
        
    sources = set()
    for entry in entries:
        link = entry.get('link', '')
        if link:
            parts = link.split('/')
            if len(parts) > 2:
                sources.add(parts[2])  # Extract domain
    
    return f"Found {len(entries)} entries from {len(sources)} source(s)." 