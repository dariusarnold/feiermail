import requests


class TelegramMessageSender:
    def __init__(self, chat_id: str, bot_token: str):
        """

        :param chat_id:
        :param bot_token:
        """
        self._chat_id = chat_id
        self._url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, text: str):
        params = {"chat_id": self._chat_id,
                  "text": text,
                  "parse_mode": "Markdown"}
        response = requests.get(self._url, params=params)
        return response

    def __repr__(self):
        return f"TelegramMessageSender({self._chat_id})"
