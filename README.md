# BBC RSS Scraper

A simple Python application that fetches and parses RSS feeds from BBC News, extracting key information and saving it to structured JSON files.

## Features

- Fetches RSS feeds from configurable URLs
- Extracts title, link, publication date, and summary from each news entry
- Saves collected news entries to a daily JSON file
- Provides error handling for unreachable feeds
- Uses UTF-8 encoding and proper JSON indentation
- Flexible command-line interface with various options

## Project Structure

```
bbc-rss-scraper/
├── data/                  # Directory to store output files
├── modules/               # Python modules
│   ├── __init__.py        # Package initialization
│   ├── scraper.py         # RSS feed fetching and parsing
│   ├── storage.py         # Data storage functionality
│   └── utils.py           # Utility functions
├── main.py                # Main entry point
├── feed_urls.txt          # List of BBC RSS feed URLs
├── requirements.txt       # Project dependencies
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## Requirements

- Python 3.9+
- feedparser
- python-dateutil

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/bbc-rss-scraper.git
   cd bbc-rss-scraper
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the scraper with default settings:

```
python main.py
```

This will:
1. Load feed URLs from `feed_urls.txt`
2. Fetch and parse each feed
3. Extract the required fields from each news entry
4. Save all entries to a JSON file in the `data/` directory

### Command Line Options

You can customize the behavior with command line options:

```
python main.py --help
```

Available options:

- `--feeds`, `-f`: Path to a file containing feed URLs (default: `feed_urls.txt`)
- `--data-dir`, `-d`: Directory to store output files (default: `data/`)
- `--limit`, `-l`: Limit the number of entries per feed (default: no limit)
- `--verbose`, `-v`: Enable detailed logging to console
- `--log-level`: Logging level (default: `INFO`)

### Examples

Basic usage with default settings:
```
python main.py
```

Use custom feed file and output directory:
```
python main.py --feeds custom_feeds.txt --data-dir ./output
```

Limit to 10 entries per feed with verbose output:
```
python main.py -f feed_urls.txt -d data -l 10 -v
```

Use short form arguments with custom paths:
```
python main.py -f ./my-feeds.txt -d ./news-data -v
```

## Sample Output

The generated JSON file will look something like this:

```json
[
    {
        "title": "Who is Robert Prevost, the new Pope Leo XIV?",
        "link": "https://www.bbc.com/news/articles/c0ln80lzk7ko",
        "published": "Thu, 08 May 2025 18:48:36 GMT",
        "summary": "After a conclave that lasted only three sessions and 24 hours, 133 cardinals have elected Robert Prevost, now known as Pope Leo XIV."
    },
    {
        "title": "India reports strikes on military bases, Pakistan denies any role",
        "link": "https://www.bbc.com/news/articles/cjrndypy3l4o",
        "published": "Thu, 08 May 2025 20:05:55 GMT",
        "summary": "India has accused Pakistan of attacking three military bases, a claim which has been denied by Islamabad."
    },
    ...
]
```

## Customizing Feed Sources

You can edit `feed_urls.txt` to add or remove RSS feed URLs. Each URL should be on a separate line.

## License

MIT 