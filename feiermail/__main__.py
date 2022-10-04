import argparse
import datetime
import locale
import sys

from telegram_msg_sender import TelegramMessageSender
from feiertage_api import parse_json, get_holiday_json
from holiday import Holiday


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Notify ahead of public holidays in Germany using a Telegram message.")
    parser.add_argument("-i", "--chat_id", required=True, nargs="+",
                        help="Telegram chat id where notification messages will be sent")
    parser.add_argument("-t", "--bot_token", required=True,
                        help="Telegram bot token which is used for sending notification messages")
    parser.add_argument("-d", "--days_ahead", default=14, type=int,
                        help="How many days ahead should the message for a holiday be sent")
    parser.add_argument("-b", "--bundesland", required=True,
                        help="Code for bundesland from https://feiertage-api.de/. Possible values are:"
                             "BW, BY, BE, BB, HB, HH, HE, MV, NI, NW, RP, SL, SN, ST, SH, TH.")
    return parser


def format_telegram_message(holiday: Holiday) -> str:
    return f"{holiday.date.strftime('%A, %d. %B')} ist Feiertag ({holiday.name})."


def main():
    preferred_locale = "de_DE.utf8"
    try:
        locale.setlocale(locale.LC_TIME, preferred_locale)
    except locale.Error:
        print(f"Couldn't set locale to {preferred_locale}.", file=sys.stderr)
    parser = create_arg_parser()
    args = parser.parse_args()
    holidays_json = get_holiday_json(datetime.datetime.today().year, args.bundesland)
    holidays = parse_json(holidays_json)
    receivers = [TelegramMessageSender(chat_id, args.bot_token) for chat_id in args.chat_id]
    today = datetime.datetime.today().date()
    holidays = [h for h in holidays if (h.date - today).days < args.days_ahead]
    print(f"Upcoming holidays {holidays}")
    for h in holidays:
        print(f"Sending {h} to {receivers}")
        for receiver in receivers:
            receiver.send(format_telegram_message(h))


if __name__ == '__main__':
    main()
