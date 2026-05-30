# Import required libraries
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
from configparser import ConfigParser
import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

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

# Create Excel workbook and worksheet
wb = Workbook()
ws = wb.create_sheet("General", 0)

# Write headers
ws['A1'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
ws['B2'] = "Platform"
ws['C2'] = "My Ranking"
ws['D2'] = "Total Players"
ws['E2'] = "My Percentage"
ws['F2'] = "Status"
ws['G2'] = "Previous Percentage"

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

# Populate platform data from scraped information in sorted order
row = 3
for data in platform_data:
    ws[f'B{row}'] = data['platform']['display']
    ws[f'C{row}'] = data['ranking']
    ws[f'D{row}'] = data['totals']
    
    if data['status'] == "Skipped":
        ws[f'E{row}'] = "N/A"
        ws[f'F{row}'] = "Skipped"
    else:
        ws[f'E{row}'] = data['percentage']
    
    row += 1

# Add general totals (all platforms combined)
ws['B15'] = "Total"
ws['D15'] = totals['general']

# Check if general username is empty (skipped)
if not GENERAL_USERNAME or GENERAL_USERNAME.strip() == '':
    ws['C15'] = "N/A"
    ws['E15'] = "N/A"
    ws['F15'] = "Skipped"
else:
    ws['C15'] = mines['general']
    if totals['general'] > 0:
        ws['E15'] = round((mines['general'] / totals['general']) * 100, 2)
    else:
        ws['E15'] = 0

# Align columns B, C, D, E, F, G to center horizontally
for row in ws.iter_rows(min_col=2, max_col=7, min_row=1, max_row=ws.max_row):
    for cell in row:
        cell.alignment = Alignment(horizontal='center')

# Auto-adjust column widths based on content length
for column in ws.columns:
    column_letter = get_column_letter(column[0].column)
    max_length = 0
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    ws.column_dimensions[column_letter].width = max_length + 2

# Make row 2 (headers) bold
for col in range(1, ws.max_column + 1):
    cell = ws.cell(row=2, column=col)
    cell.font = Font(bold=True)

# Make column B (Platform names) italic from B3 to B14 (excluding header B2 and Total B15)
for row in ws.iter_rows(min_col=2, max_col=2, min_row=3, max_row=14):
    for cell in row:
        cell.font = Font(italic=True)

# Format column E (percentages) to display as percentages with 2 decimal places
for row_num in range(3, 16):
    ws[f'E{row_num}'].number_format = '0.00"%"'

# Color code column E (percentages) with gradient from green (min) to red (max)
# Collect all numeric percentage values (exclude N/A)
percentage_values = []
for row_num in range(3, 16):
    cell_value = ws[f'E{row_num}'].value
    if isinstance(cell_value, (int, float)) and cell_value != 0:
        percentage_values.append((row_num, cell_value))

# Find min and max values
if percentage_values:
    min_val = min(v for _, v in percentage_values)
    max_val = max(v for _, v in percentage_values)
    
    # Function to interpolate color from green -> yellow -> red based on normalized value
    def get_gradient_color(value, min_val, max_val):
        """Returns hex color code for gradient green (0%) -> yellow (50%) -> red (100%)"""
        if max_val == min_val:
            norm = 0.5
        else:
            norm = (value - min_val) / (max_val - min_val)
        
        if norm <= 0.5:
            # Green to Yellow transition: (0,176,80) -> (255,255,0)
            t = norm * 2
            r = int(0 + (255 - 0) * t)
            g = int(176 + (255 - 176) * t)
            b = int(80 + (0 - 80) * t)
        else:
            # Yellow to Red transition: (255,255,0) -> (255,0,0)
            t = (norm - 0.5) * 2
            r = 255
            g = int(255 * (1 - t))
            b = 0
        
        return f"{r:02X}{g:02X}{b:02X}"
    
    # Apply gradient colors to all percentage cells
    for row_num, value in percentage_values:
        color = get_gradient_color(value, min_val, max_val)
        ws[f'E{row_num}'].fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

# Load previous percentage data from existing file if it exists
# Create a mapping of platform display names to previous percentages
previous_percentages = {}
previous_total_percentage = None
if os.path.exists("Achievement_Track.xlsx"):
    try:
        old_wb = load_workbook("Achievement_Track.xlsx")
        old_ws = old_wb.active
        
        # Read all platform data from old file and create a mapping by display name
        # Assuming platforms are in rows 3-14 in old file
        for row_num in range(3, 15):
            platform_name = old_ws[f'B{row_num}'].value
            old_value = old_ws[f'E{row_num}'].value
            if platform_name and old_value is not None and old_value != "N/A":
                previous_percentages[platform_name] = old_value
        
        # Also read Total row (row 15) previous percentage
        old_total_name = old_ws['B15'].value
        if old_total_name == "Total":
            old_total_value = old_ws['E15'].value
            if old_total_value is not None and old_total_value != "N/A":
                previous_total_percentage = old_total_value
    except Exception as e:
        print(f"Warning: Could not read previous percentage data: {e}")

# Populate G column (Previous Percentage) for each platform using sorted data
# row variable already points to the next available row after platforms
row = 3
for data in platform_data:
    platform_display = data['platform']['display']
    if platform_display in previous_percentages:
        ws[f'G{row}'] = previous_percentages[platform_display]
    else:
        ws[f'G{row}'] = "N/A"
    row += 1

# Add previous percentage for Total row
if previous_total_percentage is not None:
    ws['G15'] = previous_total_percentage
else:
    ws['G15'] = "N/A"

# Update Status column (F) based on comparison of My Percentage (E) and Previous Percentage (G)
for row_num in range(3, 17):  # Include Total row (row 15) and beyond if needed
    # Skip if status is already "Skipped"
    if ws[f'F{row_num}'].value == "Skipped":
        continue
    
    current_pct = ws[f'E{row_num}'].value
    previous_pct = ws[f'G{row_num}'].value
    
    # Compare percentages if both are numeric values
    if isinstance(current_pct, (int, float)) and isinstance(previous_pct, (int, float)):
        if current_pct > previous_pct:
            ws[f'F{row_num}'] = "↓"  # Down arrow for Increased
            ws[f'F{row_num}'].font = Font(color="000000", bold=True)  # Black text
            ws[f'F{row_num}'].fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")  # Red background
        elif current_pct < previous_pct:
            ws[f'F{row_num}'] = "↑"  # Up arrow for Decreased
            ws[f'F{row_num}'].font = Font(color="000000", bold=True)  # Black text
            ws[f'F{row_num}'].fill = PatternFill(start_color="00B050", end_color="00B050", fill_type="solid")  # Green background
        else:
            ws[f'F{row_num}'] = "="  # Equals for Same
            ws[f'F{row_num}'].font = Font(color="000000", bold=True)  # Black text
            ws[f'F{row_num}'].fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Yellow background
    else:
        # If no previous data exists, leave empty
        ws[f'F{row_num}'] = ""

# Save the workbook to file
wb.save("Achievement_Track.xlsx")