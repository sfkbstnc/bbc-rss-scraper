"""
Storage functionality for saving data to disk.
"""
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logger = logging.getLogger('bbc-rss-scraper')

def ensure_data_directory(directory: str) -> None:
    """
    Ensure the data directory exists.
    
    Args:
        directory: Path to the data directory
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        raise

def generate_filename() -> str:
    """
    Generate a filename based on the current date.
    
    Returns:
        Filename in the format news_YYYYMMDD.json
    """
    current_date = datetime.now().strftime('%Y%m%d')
    return f"news_{current_date}.json"

def save_entries(entries: List[Dict[str, Any]], data_dir: str) -> str:
    """
    Save entries to a JSON file.
    
    Args:
        entries: List of entry dictionaries to save
        data_dir: Directory to save the file in
        
    Returns:
        Path to the saved file
    """
    try:
        # Ensure the data directory exists
        ensure_data_directory(data_dir)
        
        # Generate the filename
        filename = generate_filename()
        file_path = os.path.join(data_dir, filename)
        
        # Save entries to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=4)
            
        logger.info(f"Saved {len(entries)} entries to {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error saving entries: {str(e)}")
        raise 