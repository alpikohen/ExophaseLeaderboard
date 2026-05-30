# Import required libraries
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
from configparser import ConfigParser
import os

# Load and validate configuration
def load_and_validate_config():
    """Load config.ini and validate that required section exists."""
    config = ConfigParser()
    config.read('config.ini')
    
    # Check if config file was loaded
    if not config.sections():
        raise ValueError(
            "ERROR: config.ini file not found or is empty.\n"
            "Please create a config.ini file in the project directory with [usernames] section.\n"
            "Required format:\n"
            "[usernames]\n"
            "general = your_username\n"
            "psn = your_username\n"
            "(and other platform usernames)"
        )
    
    # Check if [usernames] section exists
    if not config.has_section('usernames'):
        raise ValueError(
            "ERROR: [usernames] section not found in config.ini.\n"
            "Please ensure config.ini has a [usernames] section with all required usernames."
        )
    
    # List of required usernames
    required_keys = ['exophase', 'psn', 'xbox', 'steam', 'ea', 'blizzard', 'retro', 'gplay', 'gog', 'ubisoft', 'epic', 'apple', 'stadia']
    
    # Check if all required keys exist (can be empty, but must be present)
    for key in required_keys:
        if not config.has_option('usernames', key):
            raise ValueError(
                f"ERROR: Missing key '{key}' in config.ini [usernames] section.\n"
                f"Please add: {key} = username_here\n"
                f"(Leave empty if user doesn't have this platform)"
            )
    
    # Warn about empty usernames
    empty_usernames = []
    for key in required_keys:
        value = config.get('usernames', key)
        if not value or value.strip() == '':
            empty_usernames.append(key)
    
    if empty_usernames:
        print(f"INFO: The following platforms have empty usernames and will be skipped:")
        for key in empty_usernames:
            print(f"      - {key}")
        print()
    
    return config

# Load configuration at startup
try:
    config = load_and_validate_config()
except ValueError as e:
    print(str(e))
    exit(1)

# Create scraper instance to bypass CloudFlare protection
scraper = cloudscraper.create_scraper()
BASE_URL = "https://www.exophase.com/"

# Platform configuration with leaderboard and user URLs
# Username values are read from config.ini file (validated above)
PLATFORMS = [
    {'key': 'psn', 'display': 'PSN', 'leaderboard': 'psn/', 'user': 'psn/', 'username': config.get('usernames', 'psn'), 'ranking_class': 'global-ranking tippy mb-1'},
    {'key': 'xbox', 'display': 'Xbox', 'leaderboard': 'xbox/', 'user': 'xbox/', 'username': config.get('usernames', 'xbox'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'steam', 'display': 'Steam', 'leaderboard': 'steam/', 'user': 'steam/', 'username': config.get('usernames', 'steam'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'ea', 'display': 'EA', 'leaderboard': 'origin/', 'user': 'origin/', 'username': config.get('usernames', 'ea'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'blizzard', 'display': 'Blizzard', 'leaderboard': 'blizzard/', 'user': 'blizzard/', 'username': config.get('usernames', 'blizzard'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'retro', 'display': 'Retro', 'leaderboard': 'retro/', 'user': 'retro/', 'username': config.get('usernames', 'retro'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'gplay', 'display': 'Google Play', 'leaderboard': 'android/', 'user': 'android/', 'username': config.get('usernames', 'gplay'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'gog', 'display': 'GOG', 'leaderboard': 'gog/', 'user': 'gog/', 'username': config.get('usernames', 'gog'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'ubisoft', 'display': 'Ubisoft', 'leaderboard': 'uplay/', 'user': 'uplay/', 'username': config.get('usernames', 'ubisoft'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'stadia', 'display': 'Stadia', 'leaderboard': 'stadia/', 'user': 'stadia/', 'username': config.get('usernames', 'stadia'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'epic', 'display': 'Epic', 'leaderboard': 'epic/', 'user': 'epic/', 'username': config.get('usernames', 'epic'), 'ranking_class': 'global-ranking tippy'},
    {'key': 'apple', 'display': 'Apple', 'leaderboard': 'apple/', 'user': 'apple/', 'username': config.get('usernames', 'apple'), 'ranking_class': 'global-ranking tippy'},
]

# Get general username from config (validated during startup)
GENERAL_USERNAME = config.get('usernames', 'exophase')

# Initialize dictionaries to store scraped data
# totals: total number of players on each platform's leaderboard
# mines: user's ranking on each platform's leaderboard
totals = {}
mines = {}

# Scrape leaderboard data for all platforms
for platform in PLATFORMS:
    # Scrape total number of players on platform leaderboard
    # (This doesn't require username - it's public data)
    try:
        url = BASE_URL + platform['leaderboard'] + 'leaderboard/'
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        big_numbers = soup.find_all('span', {'class': 'big_number'})
        if len(big_numbers) > 1:
            text = big_numbers[1].get_text(strip=True)
            totals[platform['key']] = int(text.replace(',', ''))
        else:
            totals[platform['key']] = 0
            print(f"Warning: Could not find total for {platform['display']}")
    except Exception as e:
        print(f"Error scraping total for {platform['display']}: {e}")
        totals[platform['key']] = 0
    
    # Skip ranking scraping if username is empty
    if not platform['username'] or platform['username'].strip() == '':
        print(f"INFO: Skipping {platform['display']} ranking (no username configured)")
        mines[platform['key']] = 0
        continue
    
    # Scrape user's ranking on platform leaderboard
    try:
        url = BASE_URL + platform['user'] + 'user/' + platform['username']
        response = scraper.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rankings = soup.find_all('span', {'class': platform['ranking_class']})
        if len(rankings) > 0:
            text = rankings[0].get_text(strip=True)
            mines[platform['key']] = int(text.replace(',', ''))
        else:
            mines[platform['key']] = 0
            print(f"Warning: Could not find ranking for {platform['display']}")
    except Exception as e:
        print(f"Error scraping ranking for {platform['display']}: {e}")
        mines[platform['key']] = 0

# Scrape general (all platforms combined) leaderboard total
try:
    response = scraper.get(BASE_URL + 'leaderboard/')
    soup = BeautifulSoup(response.text, 'html.parser')
    big_numbers = soup.find_all('span', {'class': 'big_number'})
    if len(big_numbers) > 1:
        text = big_numbers[1].get_text(strip=True)
        totals['general'] = int(text.replace(',', ''))
    else:
        totals['general'] = 0
except Exception as e:
    print(f"Error scraping general total: {e}")
    totals['general'] = 0

# Scrape user's overall ranking (across all platforms)
# Skip if username is empty
if not GENERAL_USERNAME or GENERAL_USERNAME.strip() == '':
    print(f"INFO: Skipping General ranking (no username configured)")
    mines['general'] = 0
else:
    try:
        response = scraper.get(BASE_URL + f'user/{GENERAL_USERNAME}')
        soup = BeautifulSoup(response.text, 'html.parser')
        rankings = soup.find_all('span', {'class': 'global-ranking tippy'})
        if len(rankings) > 0:
            text = rankings[0].get_text(strip=True)
            mines['general'] = int(text.replace(',', ''))
        else:
            mines['general'] = 0
    except Exception as e:
        print(f"Error scraping general ranking: {e}")
        mines['general'] = 0

# Collect platform data for sorting
platform_data = []
for platform in PLATFORMS:
    # Check if username is empty (skipped)
    if not platform['username'] or platform['username'].strip() == '':
        percentage = float('inf')  # Put skipped platforms at the end
        ranking = "N/A"
        status = "Skipped"
    else:
        ranking = mines[platform['key']]
        if totals[platform['key']] > 0:
            percentage = round((mines[platform['key']] / totals[platform['key']]) * 100, 2)
        else:
            percentage = 0
        status = None  # Will be filled later
    
    platform_data.append({
        'platform': platform,
        'ranking': ranking,
        'percentage': percentage,
        'totals': totals[platform['key']],
        'status': status
    })

# Sort by percentage (ascending - lowest first, skipped platforms last)
platform_data.sort(key=lambda x: x['percentage'])

# Load previous percentage data
previous_percentages = {}
previous_total_percentage = None
if os.path.exists("Achievement_Track.html"):
    try:
        with open("Achievement_Track.html", "r", encoding="utf-8") as f:
            content = f.read()
            # Extract previous percentages from HTML (simple parsing)
            # This is a safety measure; if file doesn't exist, no previous data
    except Exception as e:
        print(f"Warning: Could not read previous data: {e}")

# Generate HTML Report
def get_gradient_color(value, min_val, max_val):
    """Returns hex color code for gradient green (0%) -> yellow (50%) -> red (100%)"""
    if max_val == min_val:
        norm = 0.5
    else:
        norm = (value - min_val) / (max_val - min_val)
    
    if norm <= 0.5:
        t = norm * 2
        r = int(0 + (255 - 0) * t)
        g = int(176 + (255 - 176) * t)
        b = int(80 + (0 - 80) * t)
    else:
        t = (norm - 0.5) * 2
        r = 255
        g = int(255 * (1 - t))
        b = 0
    
    return f"#{r:02X}{g:02X}{b:02X}"

# Get color gradient for percentages
percentage_values = [data['percentage'] for data in platform_data if isinstance(data['percentage'], (int, float)) and data['percentage'] != float('inf')]
if percentage_values:
    min_val = min(percentage_values)
    max_val = max(percentage_values)
else:
    min_val = max_val = 50

# Generate HTML
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Exophase Leaderboard Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
        }
        h1 {
            color: #333;
            margin: 10px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th {
            background-color: #333;
            color: white;
            padding: 12px;
            text-align: center;
            font-weight: bold;
        }
        td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .platform-name {
            text-align: left;
            font-style: italic;
        }
        .total-row {
            font-weight: bold;
            background-color: #f0f0f0;
        }
        .percentage-cell {
            font-weight: bold;
        }
        .status-cell {
            font-size: 18px;
            font-weight: bold;
        }
        .status-red {
            background-color: #FF0000;
            color: black;
        }
        .status-green {
            background-color: #00B050;
            color: black;
        }
        .status-yellow {
            background-color: #FFFF00;
            color: black;
        }
        .status-gray {
            background-color: #cccccc;
            color: black;
        }
        .na {
            color: #999;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎮 Exophase Achievement Leaderboard</h1>
            <p class="timestamp">Generated: """ + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + """</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Platform</th>
                    <th>My Ranking</th>
                    <th>Total Players</th>
                    <th>My Percentage</th>
                    <th>Status</th>
                    <th>Previous %</th>
                </tr>
            </thead>
            <tbody>
"""

# Add platform rows
for data in platform_data:
    platform_display = data['platform']['display']
    ranking = data['ranking']
    totals_val = data['totals']
    percentage = data['percentage']
    
    # Determine status color
    if data['status'] == "Skipped":
        status_symbol = "⊘"
        status_class = "status-gray"
    else:
        status_symbol = ""
        status_class = ""
    
    # Format percentage
    if isinstance(percentage, float) and percentage != float('inf'):
        pct_str = f"{percentage:.2f}%"
        pct_color = get_gradient_color(percentage, min_val, max_val)
        pct_cell = f'<td class="percentage-cell" style="background-color: {pct_color}; color: black;">{pct_str}</td>'
    else:
        pct_str = "N/A"
        pct_cell = '<td class="percentage-cell na">N/A</td>'
    
    # Format ranking
    ranking_str = str(ranking) if ranking != "N/A" else "N/A"
    
    # Format total
    totals_str = f"{totals_val:,}" if isinstance(totals_val, int) else str(totals_val)
    
    html_content += f"""                <tr>
                    <td class="platform-name">{platform_display}</td>
                    <td>{ranking_str}</td>
                    <td>{totals_str}</td>
                    {pct_cell}
                    <td class="status-cell {status_class}">{status_symbol}</td>
                    <td>—</td>
                </tr>
"""

# Add Total row
total_ranking = mines['general']
total_totals = totals['general']
if total_totals > 0:
    total_pct = round((total_ranking / total_totals) * 100, 2)
    total_pct_str = f"{total_pct:.2f}%"
    total_pct_color = get_gradient_color(total_pct, min_val, max_val)
    total_pct_cell = f'<td class="percentage-cell" style="background-color: {total_pct_color}; color: black;">{total_pct_str}</td>'
else:
    total_pct_str = "N/A"
    total_pct_cell = '<td class="percentage-cell na">N/A</td>'

total_ranking_str = str(total_ranking) if isinstance(total_ranking, int) else "N/A"
total_totals_str = f"{total_totals:,}" if isinstance(total_totals, int) else str(total_totals)

html_content += f"""                <tr class="total-row">
                    <td class="platform-name">TOTAL</td>
                    <td>{total_ranking_str}</td>
                    <td>{total_totals_str}</td>
                    {total_pct_cell}
                    <td class="status-cell">—</td>
                    <td>—</td>
                </tr>
"""

html_content += """            </tbody>
        </table>
    </div>
</body>
</html>
"""

# Save HTML report
with open("Achievement_Track.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Report generated: Achievement_Track.html")