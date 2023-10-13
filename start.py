#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# Konfiguration als Konstanten
PAGE_URL = "https://steamcommunity.com/sharedfiles/filedetails/?id="
WORKSHOP_IDS = ["12345", "67890"]  # Beispiel-IDs, ersetzen Sie diese durch die tatsächlichen IDs
DISCORD_WEBHOOK_URL = '<DISCORD-WEBHOOK>'
DEBUG_MODE = True

def debug(message):
    if DEBUG_MODE:
        print(f'[DEBUG] {message}')

def fetch_web_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.HTTPError as e:
        print(f"Error retrieving the page: {e}")
        return None

def save_config(data, file_name='config.json'):
    with open(file_name, 'w') as config_file:
        json.dump(data, config_file)

def load_config(file_name='config.json'):
    try:
        with open(file_name, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {}

def main():
    saved_data = load_config()

    for workshop_id in WORKSHOP_IDS:
        changelog_url = f"https://steamcommunity.com/sharedfiles/filedetails/changelog/{workshop_id}"

        debug(f"Processing Workshop ID {workshop_id}")

        last_saved_entry = saved_data.get(changelog_url, {}).get('entry', '')
        last_saved_title = saved_data.get(changelog_url, {}).get('title', '')

        # Webseiteninhalt holen und prüfen
        soup = fetch_web_page(changelog_url)
        if not soup:
            continue

        target_element = soup.find('p', id=re.compile(r'(\d+)'))
        title_element = soup.find(class_='workshopItemTitle')

        if target_element:
            current_entry = target_element.get_text()
            current_title = title_element.get_text() if title_element else 'No title found'

            if (last_saved_entry != current_entry) or (last_saved_title != current_title):
                debug(f'There is a change in {changelog_url}')
                debug(f'Title: {current_title}')
                debug(f'Entry: {current_entry}')

                current_datetime = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
                discord_message = {
                    "username": "Soul's Patchbot",
                    "avatar_url": "https://i.imgur.com/4M34hi2.png",
                    "embeds": [
                        {
                            "title": current_title,
                            "url": changelog_url,
                            "description": f"Patch Notes for: {current_title}",
                            "color": 15258703,
                            "fields": [
                                {
                                    "name": "News",
                                    "value": f"Date and Time: {current_datetime}\n\n{current_entry}",
                                    "inline": True
                                }
                            ],
                            "footer": {
                                "text": "by SoulofSorrow",
                                "icon_url": "https://i.imgur.com/fKL31aD.jpg"
                            }
                        }
                    ]
                }

                response = requests.post(DISCORD_WEBHOOK_URL, json=discord_message)

                # Aktuelle Einträge und Titel speichern
                saved_data[changelog_url] = {'entry': current_entry, 'title': current_title}
                save_config(saved_data)

if __name__ == "__main__":
    main()
