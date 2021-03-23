import datetime


class Holiday:
    def __init__(self, name: str, date: str):
        """
        :param name: Name des Feiertags
        :param date: Datum im Format YYYY-MM-DD
        """
        self.name = name
        self.date = datetime.date.fromisoformat(date)

    def __repr__(self):
        return f"Holiday({self.name}, {self.date})"