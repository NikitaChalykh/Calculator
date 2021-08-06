"""ККалькулятор денег и калорий."""
import datetime as dt
FORMAT_DATE = '%d.%m.%Y'


class Record:
    """Класс для создания записей в калькулятор.
    Свойство класса {amount} определяет количество
    единиц калькулятора для записи.
    Свойство класса {comment} определяет комментарий к записи.
    Свойство класса {date} определяет дату записи.
    Если дата не указана, присваивается значение
    текущей даты.
    """

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, FORMAT_DATE).date()


class Calculator:
    """Родительский класс калькулятора.
    Пустой список 'records' создается для сохранения списка всех записей.
    Свойство класса {limit} задает ограничение для подсчета максимального
    количества единц калькулятора за текущий день.
    Переменная {today_date} присваивается для создания текущей даты
    в формате строки 'день года [001,366]'.
    """

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Родительский метод создания записи класса калькулятора.
        Метод создает запись в конец списка 'records'.
        В качестве типа записи выступает
        объект класса Record.
        """
        self.records.append(record)

    def get_today_stats(self):
        """Родительский метод подсчета единц калькулятора за текущий день.
        Метод суммирует единицы калькулятора
        из списка 'records' за текущий день.
        """
        today_date = dt.datetime.now().date()
        sum_today = 0
        for record in self.records:
            if record.date == today_date:
                sum_today += record.amount
        return sum_today

    def get_week_stats(self):
        """Родительский метод подсчета единц калькулятора за неделю.
        Метод суммирует единицы калькулятора из списка 'records'
        за последнюю неделю.
        """
        today_date = dt.datetime.now().date()
        last_week_date = today_date - dt.timedelta(days=7)
        sum_week = 0
        for record in self.records:
            if record.date >= last_week_date and record.date <= today_date:
                sum_week += record.amount
        return sum_week

    def today_remainder(self):
        """Родительский метод подсчета остатка единиц за день от лимита."""
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Дочерний класс калькулятора калорий."""

    def get_calories_remained(self):
        """Дочерний метод подсчета остатка калорий за день от лимита."""
        calories_remainder = self.today_remainder()
        if calories_remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {calories_remainder} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Дочерний класс калькулятора валюты."""

    USD_RATE = 80.50
    EURO_RATE = 90.51

    def get_today_cash_remained(self, currency):
        """Дочерний метод подсчета остатка валюты за день
        от лимита c учетом типа валюты.
        """
        cash_remained = self.today_remainder()
        if cash_remained == 0:
            return 'Денег нет, держись'
        currency_list = {
            'usd': {'text': 'USD', 'cur': self.USD_RATE},
            'eur': {'text': 'Euro', 'cur': self.EURO_RATE},
            'rub': {'text': 'руб', 'cur': 1}
        }
        text = currency_list[currency]['text']
        currency_remainder = cash_remained / currency_list[currency]['cur']
        correct_currency_remainder = abs(round(currency_remainder, 2))
        if cash_remained > 0:
            return f'На сегодня осталось {correct_currency_remainder} {text}'
        return (f'Денег нет, держись: твой долг - '
                f'{correct_currency_remainder} {text}')
