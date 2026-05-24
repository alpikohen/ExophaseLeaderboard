import cloudscraper
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook

url_general = "https://www.exophase.com/leaderboard/"
scraper = cloudscraper.create_scraper()

general_data = scraper.get(url_general).text
soup = BeautifulSoup(general_data, "html.parser")
general_user_number = soup.find_all("span", {"class":"big_number"})
print(general_user_number)
message = str(general_user_number[1]).split('>')
message2 = message[1].split('<')
general_total = int(message2[0].replace(',', ''))

url_psn = "https://www.exophase.com/psn/leaderboard/"
psn_data = scraper.get(url_psn).text
soup = BeautifulSoup(psn_data, "html.parser")
psn_user_number = soup.find_all("span", {"class":"big_number"})
message = str(psn_user_number[1]).split('>')
message2 = message[1].split('<')
psn_total = int(message2[0].replace(',', ''))

url_xbox = "https://www.exophase.com/xbox/leaderboard/"
xbox_data = scraper.get(url_xbox).text
soup = BeautifulSoup(xbox_data, "html.parser")
xbox_user_number = soup.find_all("span", {"class":"big_number"})
message = str(xbox_user_number[1]).split('>')
message2 = message[1].split('<')
xbox_total = int(message2[0].replace(',', ''))

url_steam = "https://www.exophase.com/steam/leaderboard/"
steam_data = scraper.get(url_steam).text
soup = BeautifulSoup(steam_data, "html.parser")
steam_user_number = soup.find_all("span", {"class":"big_number"})
message = str(steam_user_number[1]).split('>')
message2 = message[1].split('<')
steam_total = int(message2[0].replace(',', ''))

url_ea = "https://www.exophase.com/origin/leaderboard/"
ea_data = scraper.get(url_ea).text
soup = BeautifulSoup(ea_data, "html.parser")
ea_user_number = soup.find_all("span", {"class":"big_number"})
message = str(ea_user_number[1]).split('>')
message2 = message[1].split('<')
ea_total = int(message2[0].replace(',', ''))

url_blizzard = "https://www.exophase.com/blizzard/leaderboard/"
blizzard_data = scraper.get(url_blizzard).text
soup = BeautifulSoup(blizzard_data, "html.parser")
blizzard_user_number = soup.find_all("span", {"class":"big_number"})
message = str(blizzard_user_number[1]).split('>')
message2 = message[1].split('<')
blizzard_total = int(message2[0].replace(',', ''))

url_retro = "https://www.exophase.com/retro/leaderboard/"
retro_data = scraper.get(url_retro).text
soup = BeautifulSoup(retro_data, "html.parser")
retro_user_number = soup.find_all("span", {"class":"big_number"})
message = str(retro_user_number[1]).split('>')
message2 = message[1].split('<')
retro_total = int(message2[0].replace(',', ''))

url_gplay = "https://www.exophase.com/android/leaderboard/"
gplay_data = scraper.get(url_gplay).text
soup = BeautifulSoup(gplay_data, "html.parser")
gplay_user_number = soup.find_all("span", {"class":"big_number"})
message = str(gplay_user_number[1]).split('>')
message2 = message[1].split('<')
gplay_total = int(message2[0].replace(',', ''))

url_gog = "https://www.exophase.com/gog/leaderboard/"
gog_data = scraper.get(url_gog).text
soup = BeautifulSoup(gog_data, "html.parser")
gog_user_number = soup.find_all("span", {"class":"big_number"})
message = str(gog_user_number[1]).split('>')
message2 = message[1].split('<')
gog_total = int(message2[0].replace(',', ''))

url_ubisoft = "https://www.exophase.com/uplay/leaderboard/"
ubisoft_data = scraper.get(url_ubisoft).text
soup = BeautifulSoup(ubisoft_data, "html.parser")
ubisoft_user_number = soup.find_all("span", {"class":"big_number"})
message = str(ubisoft_user_number[1]).split('>')
message2 = message[1].split('<')
ubisoft_total = int(message2[0].replace(',', ''))

url_epic = "https://www.exophase.com/epic/leaderboard/"
epic_data = scraper.get(url_epic).text
soup = BeautifulSoup(epic_data, "html.parser")
epic_user_number = soup.find_all("span", {"class":"big_number"})
message = str(epic_user_number[1]).split('>')
message2 = message[1].split('<')
epic_total = int(message2[0].replace(',', ''))

url_apple = "https://www.exophase.com/apple/leaderboard/"
apple_data = scraper.get(url_apple).text
soup = BeautifulSoup(apple_data, "html.parser")
apple_user_number = soup.find_all("span", {"class":"big_number"})
message = str(apple_user_number[1]).split('>')
message2 = message[1].split('<')
apple_total = int(message2[0].replace(',', ''))

exophase_username = "alpikohen"
psn_username      = "alpikohen"
xbox_username     = "alpikohen"
steam_username    = "alpikohen"
ea_username       = "alpikohen"
blizzard_username = "alpikohen-2359"
retro_username    = "alpikohen"
gplay_username    = "alpikohen"
gog_username      = "alpikohen"
ubisoft_username  = "alpikohen"
epic_username     = "alpikohen"
apple_username    = "alpikohen"

exophase_url = "https://www.exophase.com/"

url_user_general = exophase_url + "user/" + exophase_username
general_user_data = scraper.get(url_user_general).text
soup = BeautifulSoup(general_user_data, "html.parser")
general_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(general_ranking).split('>')
message2 = message[3].split('<')
general_mine = int(message2[0].replace(',', ''))

url_user_psn = exophase_url + "psn/user/" + psn_username
psn_user_data = scraper.get(url_user_psn).text
soup = BeautifulSoup(psn_user_data, "html.parser")
psn_ranking = soup.find_all("span", {"class":"global-ranking tippy mb-1"})
message = str(psn_ranking).split('>')
message2 = message[3].split('<')
psn_mine = int(message2[0].replace(',', ''))

url_user_xbox = exophase_url + "xbox/user/" + xbox_username
xbox_user_data = scraper.get(url_user_xbox).text
soup = BeautifulSoup(xbox_user_data, "html.parser")
xbox_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(xbox_ranking).split('>')
message2 = message[3].split('<')
xbox_mine = int(message2[0].replace(',', ''))

url_user_steam = exophase_url + "steam/user/" + steam_username
steam_user_data = scraper.get(url_user_steam).text
soup = BeautifulSoup(steam_user_data, "html.parser")
steam_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(steam_ranking).split('>')
message2 = message[3].split('<')
steam_mine = int(message2[0].replace(',', ''))

url_user_ea = exophase_url + "origin/user/" + ea_username
ea_user_data = scraper.get(url_user_ea).text
soup = BeautifulSoup(ea_user_data, "html.parser")
ea_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(ea_ranking).split('>')
message2 = message[3].split('<')
ea_mine = int(message2[0].replace(',', ''))

url_user_blizzard = exophase_url + "blizzard/user/" + blizzard_username
blizzard_user_data = scraper.get(url_user_blizzard).text
soup = BeautifulSoup(blizzard_user_data, "html.parser")
blizzard_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(blizzard_ranking).split('>')
message2 = message[3].split('<')
blizzard_mine = int(message2[0].replace(',', ''))

url_user_retro = exophase_url + "retro/user/" + retro_username
retro_user_data = scraper.get(url_user_retro).text
soup = BeautifulSoup(retro_user_data, "html.parser")
retro_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(retro_ranking).split('>')
message2 = message[3].split('<')
retro_mine = int(message2[0].replace(',', ''))

url_user_gplay = exophase_url + "android/user/" + gplay_username
gplay_user_data = scraper.get(url_user_gplay).text
soup = BeautifulSoup(gplay_user_data, "html.parser")
gplay_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(gplay_ranking).split('>')
message2 = message[3].split('<')
gplay_mine = int(message2[0].replace(',', ''))

url_user_gog = exophase_url + "gog/user/" + gog_username
gog_user_data = scraper.get(url_user_gog).text
soup = BeautifulSoup(gog_user_data, "html.parser")
gog_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(gog_ranking).split('>')
message2 = message[3].split('<')
gog_mine = int(message2[0].replace(',', ''))

url_user_ubisoft = exophase_url + "uplay/user/" + ubisoft_username
ubisoft_user_data = scraper.get(url_user_ubisoft).text
soup = BeautifulSoup(ubisoft_user_data, "html.parser")
ubisoft_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(ubisoft_ranking).split('>')
message2 = message[3].split('<')
ubisoft_mine = int(message2[0].replace(',', ''))

url_user_epic = exophase_url + "epic/user/" + epic_username
epic_user_data = scraper.get(url_user_epic).text
soup = BeautifulSoup(epic_user_data, "html.parser")
epic_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(epic_ranking).split('>')
message2 = message[3].split('<')
epic_mine = int(message2[0].replace(',', ''))

url_user_apple = exophase_url + "apple/user/" + apple_username
apple_user_data = scraper.get(url_user_apple).text
soup = BeautifulSoup(apple_user_data, "html.parser")
apple_ranking = soup.find_all("span", {"class":"global-ranking tippy"})
message = str(apple_ranking).split('>')
message2 = message[3].split('<')
apple_mine = int(message2[0].replace(',', ''))

wb = load_workbook("Achievement_Track.xlsx")
ws = wb["General"]
ws['C3']  = psn_mine
ws['C4']  = xbox_mine
ws['C5']  = steam_mine
ws['C6']  = ea_mine
ws['C7']  = blizzard_mine
ws['C8']  = retro_mine
ws['C9']  = gplay_mine
ws['C10'] = gog_mine
ws['C11'] = ubisoft_mine
ws['C12'] = epic_mine
ws['C13'] = apple_mine
ws['C14'] = general_mine

ws['D3']  = psn_total
ws['D4']  = xbox_total
ws['D5']  = steam_total
ws['D6']  = ea_total
ws['D7']  = blizzard_total
ws['D8']  = retro_total
ws['D9']  = gplay_total
ws['D10'] = gog_total
ws['D11'] = ubisoft_total
ws['D12'] = epic_total
ws['D13'] = apple_total
ws['D14'] = general_total
wb.save("Achievement_Track.xlsx")