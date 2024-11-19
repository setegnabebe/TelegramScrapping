import logging
import os
from telethon import TelegramClient, sync
from telethon.tl.types import PeerChannel
import json

# Set up logging
logging.basicConfig(
    filename="telegram_scraping.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Started Telegram Scraping Process.")

# 1. Telegram API Credentials
api_id = '21259805'  
api_hash = 'ec1c96e0b0e0455d99a75e002549e153'  
# Initialize Telegram Client
client = TelegramClient('telegram_scraper_session', api_id, api_hash)

def main():
    # 2. Connect to Telegram
    try:
        client.start()
        logging.info("Successfully connected to Telegram.")
    except Exception as e:
        logging.error(f"Failed to connect to Telegram: {e}")
        raise

    # 3. Define channels to scrape
    channels = [
        "DoctorsET",
        "lobelia4cosmetics",
        "yetenaweg",
        "EAHCI"
        # Add more channels as needed
    ]

    # 4. Function to scrape messages and images from a channel
    def scrape_channel(channel_name, output_folder):
        """Scrape messages and images from a Telegram channel."""
        try:
            # Ensure output folder exists
            os.makedirs(output_folder, exist_ok=True)

            # Get channel entity
            channel = client.get_entity(PeerChannel(client.get_input_entity(channel_name).channel_id))

            # Fetch messages
            messages = []
            for message in client.iter_messages(channel, limit=100):  # Adjust limit as needed
                msg_dict = {
                    "id": message.id,
                    "date": str(message.date),
                    "message": message.message,
                    "media": None
                }

                # Check if media exists and download it
                if message.media:
                    file_path = client.download_media(message.media, file=output_folder)
                    msg_dict["media"] = file_path

                messages.append(msg_dict)
            
            # Save messages to JSON
            output_file = os.path.join(output_folder, f"{channel_name}_messages.json")
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=4)
            
            logging.info(f"Scraped {len(messages)} messages from {channel_name}.")
        
        except Exception as e:
            logging.error(f"Error while scraping channel {channel_name}: {e}")

    # 5. Run scraping for each channel
    output_directory = "raw_telegram_data"
    for channel in channels:
        scrape_channel(channel, output_directory)

    # 6. Close client connection
    client.disconnect()
    logging.info("Telegram scraping process completed successfully.")

if __name__ == "__main__":
    main()
