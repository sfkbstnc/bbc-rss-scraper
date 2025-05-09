#!/usr/bin/env python3
"""
BBC RSS Scraper - Main entry point.

This script fetches RSS feeds from BBC News and saves the data to JSON files.
"""
import os
import argparse
import sys

# Import from modules package
from modules.scraper import load_feed_urls, fetch_feed, extract_entries
from modules.storage import save_entries
from modules.utils import setup_logging, resolve_path, format_entries_summary

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='BBC RSS Feed Scraper',
        epilog="""Examples:
  python main.py
  python main.py --feeds custom_feeds.txt --data-dir ./output
  python main.py -f custom_feeds.txt -d ./output -l 10 -v
        """
    )
    
    parser.add_argument(
        '--feeds', '-f',
        type=str, 
        default='feed_urls.txt',
        help='Path to file containing feed URLs (default: feed_urls.txt)'
    )
    
    parser.add_argument(
        '--data-dir', '-d',
        type=str, 
        default='data',
        help='Directory to store output files (default: data)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=None,
        help='Limit the number of entries per feed (default: no limit)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable detailed logging to console'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logging level (default: INFO)'
    )
    
    return parser.parse_args()

def validate_feeds_file(feeds_file):
    """Validate that the feeds file exists and is readable"""
    if not os.path.exists(feeds_file):
        print(f"Error: Feeds file '{feeds_file}' not found.")
        return False
    
    if not os.path.isfile(feeds_file):
        print(f"Error: '{feeds_file}' is not a file.")
        return False
    
    if not os.access(feeds_file, os.R_OK):
        print(f"Error: Cannot read feeds file '{feeds_file}'. Check permissions.")
        return False
    
    return True

def main():
    """Main entry point for the script"""
    # Parse command line arguments
    args = parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else args.log_level
    setup_logging(log_level)
    
    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    feeds_file = resolve_path(script_dir, args.feeds)
    data_dir = resolve_path(script_dir, args.data_dir)
    
    # Validate feeds file
    if not validate_feeds_file(feeds_file):
        return 1
    
    # Load feed URLs
    urls = load_feed_urls(feeds_file)
    if not urls:
        print("No feed URLs found. Exiting.")
        return 1
    
    if args.verbose:
        print(f"Loaded {len(urls)} feed URLs from {feeds_file}")
    
    # Fetch and parse all feeds
    all_entries = []
    failed_urls = []
    
    for url in urls:
        try:
            feed = fetch_feed(url)
            if feed:
                entries = extract_entries(feed)
                
                # Apply limit if specified
                if args.limit is not None and len(entries) > args.limit:
                    if args.verbose:
                        print(f"Limiting entries from {url} to {args.limit} (from {len(entries)})")
                    entries = entries[:args.limit]
                
                all_entries.extend(entries)
                
                if args.verbose:
                    print(f"Fetched {len(entries)} entries from {url}")
            else:
                failed_urls.append((url, "No data returned"))
        except Exception as e:
            failed_urls.append((url, str(e)))
    
    # Report on failed URLs if any
    if failed_urls and args.verbose:
        print("\nThe following feeds could not be processed:")
        for url, reason in failed_urls:
            print(f"  - {url}: {reason}")
    
    # Save all entries to a file
    if all_entries:
        try:
            output_file = save_entries(all_entries, data_dir)
            print(f"Successfully saved {len(all_entries)} entries to {output_file}")
            print(format_entries_summary(all_entries))
        except Exception as e:
            print(f"Failed to save entries: {str(e)}")
            return 1
    else:
        print("No entries found in any feeds.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 