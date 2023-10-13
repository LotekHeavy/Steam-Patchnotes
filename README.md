# Steam Workshop Changelog Monitor
This Python script has been developed to monitor changes in Steam Workshop changelogs and send notifications via Discord webhooks when new patch notes are available. Original Version: https://github.com/SoulofSorrow/Steam-Patchnotes

## Functionality

- The script scans a Steam Workshop Collection page for workshop IDs and extracts them.
- It continuously monitors these workshop IDs to detect new patch notes.
- When new patch notes are found, it sends a notification via a Discord webhook.

## Usage

1. Set the URL of the Steam Workshop Collection page you want to monitor in the `page_url` variable.
2. Specify the Discord webhook URL in the `discord_webhook_url` variable.
3. Execute the script, and it will monitor changes in patch notes and send notifications.

## Dependencies

- [Requests](https://docs.python-requests.org/en/latest/) - For making HTTP requests.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - For parsing HTML.
- [json](https://docs.python.org/3/library/json.html) - For reading and writing configuration data.
- [datetime](https://docs.python.org/3/library/datetime.html) - For processing date and time information.

## Configuration

- The script stores the last seen patch notes in a configuration file named `config.json`. You can customize the configuration file to your needs.

## Note

This script was created for demonstration purposes and should be used with caution. Ensure that you comply with Steam usage policies and Discord guidelines when using it.

Feel free to extend and customize the script to meet your requirements.
