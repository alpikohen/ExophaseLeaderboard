# Import required libraries
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

# Create scraper instance to bypass CloudFlare protection
scraper = cloudscraper.create_scraper()
BASE_URL = "https://www.exophase.com/"

# Platform configuration with leaderboard and user URLs
# Add new platforms by adding a dictionary to this list
PLATFORMS = [
    {'key': 'psn', 'display': 'PSN', 'leaderboard': 'psn/', 'user': 'psn/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy mb-1'},
    {'key': 'xbox', 'display': 'Xbox', 'leaderboard': 'xbox/', 'user': 'xbox/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'steam', 'display': 'Steam', 'leaderboard': 'steam/', 'user': 'steam/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'ea', 'display': 'EA', 'leaderboard': 'origin/', 'user': 'origin/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'blizzard', 'display': 'Blizzard', 'leaderboard': 'blizzard/', 'user': 'blizzard/', 'username': 'alpikohen-2359', 'ranking_class': 'global-ranking tippy'},
    {'key': 'retro', 'display': 'Retro', 'leaderboard': 'retro/', 'user': 'retro/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'gplay', 'display': 'Google Play', 'leaderboard': 'android/', 'user': 'android/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'gog', 'display': 'GOG', 'leaderboard': 'gog/', 'user': 'gog/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'ubisoft', 'display': 'Ubisoft', 'leaderboard': 'uplay/', 'user': 'uplay/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'epic', 'display': 'Epic', 'leaderboard': 'epic/', 'user': 'epic/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
    {'key': 'apple', 'display': 'Apple', 'leaderboard': 'apple/', 'user': 'apple/', 'username': 'alpikohen', 'ranking_class': 'global-ranking tippy'},
]

# Initialize dictionaries to store scraped data
# totals: total number of players on each platform's leaderboard
# mines: user's ranking on each platform's leaderboard
totals = {}
mines = {}

# Scrape leaderboard data for all platforms
for platform in PLATFORMS:
    # Scrape total number of players on platform leaderboard
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
try:
    response = scraper.get(BASE_URL + 'user/alpikohen')
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

# Populate platform data from scraped information using loop
row = 3
for platform in PLATFORMS:
    ws[f'B{row}'] = platform['display']
    ws[f'C{row}'] = mines[platform['key']]
    ws[f'D{row}'] = totals[platform['key']]
    if totals[platform['key']] > 0:
        ws[f'E{row}'] = round((mines[platform['key']] / totals[platform['key']]) * 100, 2)
    else:
        ws[f'E{row}'] = 0
    row += 1

# Add general totals (all platforms combined)
ws['B14'] = "Total"
ws['C14'] = mines['general']
ws['D14'] = totals['general']
if totals['general'] > 0:
    ws['E14'] = round((mines['general'] / totals['general']) * 100, 2)
else:
    ws['E14'] = 0

# Align columns B, C, D, E to center horizontally
for row in ws.iter_rows(min_col=2, max_col=5, min_row=1, max_row=ws.max_row):
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

# Make column B (Platform names) italic from B3 to B14 (excluding header B2)
for row in ws.iter_rows(min_col=2, max_col=2, min_row=3, max_row=14):
    for cell in row:
        cell.font = Font(italic=True)

# Format column E (percentages) to display as percentages with 2 decimal places
for row_num in range(3, 15):
    ws[f'E{row_num}'].number_format = '0.00"%"'

# Save the workbook to file
wb.save("Achievement_Track.xlsx")