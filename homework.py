import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        """
        Класс для создания записей в калькулятор.
        Свойство класса {amount} определяет количество
        единиц калькулятора для записи.
        Свойство класса {comment} определяет комментарий к записи.
        Свойство класса {date} определяет дату записи.
        Если дата не указана, присваивается значение
        текущей даты.
        """
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    today_date = dt.datetime.now().date()

    def __init__(self, limit):
        """
        Родительский класс калькулятора.
        Пустой список 'records' создается для сохранения списка всех записей.
        Свойство класса {limit} задает ограничение для подсчета максимального
        количества единц калькулятора за текущий день.
        Переменная {today_date} присваивается для создания текущей даты
        в формате строки 'день года [001,366]'.
        """
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """
        Родительский метод создания записи класса калькулятора.
        Метод создает запись в конец списка 'records'.
        В качестве типа записи выступает другой список
        - свойства объекта класса Record (записи в калькулятор).
        """
        self.records.append(record)

    def get_today_stats(self):
        """
        Родительский метод подсчета единц калькулятора за текущий день.
        Метод суммирует единицы калькулятора
        из списка 'records' за текущий день.
        """
        sum_today = 0
        for i in range(0, len(self.records)):
            if self.records[i].date == self.today_date:
                sum_today += self.records[i].amount
        return sum_today

    def get_week_stats(self):
        """
        Родительский метод подсчета единц калькулятора за неделю.
        Метод суммирует единицы калькулятора из списка 'records'
        за последнюю неделю.
        """
        sum_week = 0
        for i in range(0, len(self.records)):
            if (self.today_date - self.records[i].date >= dt.timedelta(days=0)
                    and self.today_date
                    - self.records[i].date <= dt.timedelta(days=7)):
                sum_week += self.records[i].amount
        return sum_week


class CaloriesCalculator(Calculator):
    """
    Дочерний класс калькулятора калорий.
    """
    def get_calories_remained(self):
        """
        Дочерний метод подсчета остатка калорий за день от лимита.
        """
        delta = self.limit - super().get_today_stats()
        if delta >= 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {delta} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    """
    Дочерний класс калькулятора валюты.
    """
    USD_RATE = 80.50
    EURO_RATE = 90.51

    def get_today_cash_remained(self, currency):
        """
        Дочерний метод подсчета остатка денег за день
        от лимита c учетом типа валюты.
        """
        if currency == 'usd':
            actual_currency = self.USD_RATE
            text = 'USD'
            delta = (self.limit - super().get_today_stats()) / actual_currency
            remainder = round(delta, 2)
        elif currency == 'eur':
            actual_currency = self.EURO_RATE
            text = 'Euro'
            delta = (self.limit - super().get_today_stats()) / actual_currency
            remainder = round(delta, 2)
        else:
            text = 'руб'
            delta = self.limit - super().get_today_stats()
            remainder = int(delta)
        if delta > 0:
            return f"На сегодня осталось {remainder} {text}"
        elif delta == 0:
            return "Денег нет, держись"
        else:
            return f"Денег нет, держись: твой долг - {-remainder} {text}"
