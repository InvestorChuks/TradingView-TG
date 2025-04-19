import os
import json
import logging
import telebot
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = telebot.TeleBot(TOKEN, parse_mode=None)


@app.route('/trading-view-alert', methods=['POST'])
def trading_view_alert():
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = request.data.decode('utf-8')
            message_text = data
        else:
            message_text = json.dumps(data, indent=2)

        logging.info("Received alert data: %s", message_text)
        bot.send_message(chat_id=CHAT_ID, text=message_text)
        logging.info("Message sent to Telegram successfully")

        return jsonify({"status": "success", "message": "Alert received"}), 200

    except json.JSONDecodeError as e:
        logging.error("Failed to decode JSON data: %s", e)
        return jsonify({"status": "error", "message": "Invalid JSON data"}), 400

    except Exception as e:
        logging.error("An error occurred: %s", e)
        return jsonify({"status": "error", "message": "An error occurred while processing the request"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)