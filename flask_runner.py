import os
import json
import logging
import telebot
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Enable logging
logging.basicConfig(level=logging.INFO)

@app.route('/trading-view-alert', methods=['POST'])
def trading_view_alert():
    try:
        # Get JSON data from the request
        data = request.get_json(silent=True)

        # If no JSON data or invalid structure, return error
        if not data or "coins" not in data:
            return jsonify({"status": "error", "message": "Invalid data format or missing 'coins' list"}), 400

        # Loop through each coin in the 'coins' list and send Telegram message for each
        for coin in data["coins"]:
            ticker = coin.get("ticker")
            timeframe = coin.get("timeframe")
            signal = coin.get("signal")

            # Create a message for Telegram
            message_text = f"Signal: {signal}\nCoin: {ticker}\nTimeframe: {timeframe}"

            # Send message to Telegram
            bot.send_message(chat_id=CHAT_ID, text=message_text)
            logging.info(f"Message sent to Telegram for {ticker}: {message_text}")

        return jsonify({"status": "success", "message": "Alert received and processed"}), 200

    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON: {e}")
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    except Exception as e:
        logging.error(f"Error processing the request: {e}")
        return jsonify({"status": "error", "message": "An error occurred while processing the request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Running on port 5000 for local testing
