import pendulum
import configparser
import os


def create_config():
    config_dir = os.path.expanduser('~') + '/.ticket_click'
    config_file_path = config_dir + '/.ticket_click_conf.ini'

    if not os.path.isdir(config_dir):
        os.mkdir(config_dir)
    elif not os.path.isfile(config_file_path):
        config = configparser.ConfigParser()
        config['HANDLING FEE'] = {'handling_fee_percent' : 0.2,
                                  'max_handling_fee' : 50}
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)


class Ticket:

    def __init__(self, start_date = None, day = 0, stop_date = None, cancel_date = None, ticket_price = None, handling_fee_percent = None, max_handling_fee = None):
        self.start_date = start_date
        self.day = day
        self.stop_date = stop_date
        self.cancel_date = cancel_date
        self.money_back = None
        self.ticket_price = ticket_price
        self.handling_fee_percent = handling_fee_percent
        self.max_handling_fee = max_handling_fee

    @staticmethod
    def convert_date(date):
        day, month, year = date.split('-')
        return pendulum.date(int(year), int(month), int(day))

    def count_money_back(self):
        config = configparser.ConfigParser()
        config_file_path = os.path.expanduser('~') + '/.ticket_click/.ticket_click_conf.ini'

        if os.path.isfile(config_file_path):
            config.read(config_file_path)
            self.handling_fee_percent = float(config['HANDLING FEE']['handling_fee_percent'])
            self.max_handling_fee = float(config['HANDLING FEE']['max_handling_fee'])
        else:
            self.handling_fee_percent = 0.2
            self.max_handling_fee = 50

        self.handling_fee = self.handling_fee_percent * self.ticket_price
        if self.handling_fee > self.max_handling_fee:
            self.handling_fee = self.max_handling_fee

        self.cancled_days = self.stop_date - self.cancel_date
        self.money_back = round(float((self.ticket_price - self.handling_fee)/self.day * int(self.cancled_days.days)),2)

        result = {
            'start_date': self.start_date,
            'stop_date': self.stop_date,
            'cancel_date': self.cancel_date,
            'period': self.day,
            'one_day_cost': round((self.ticket_price - self.money_back) / int((self.cancel_date - self.start_date).days + 1), 2),
            'handling_fee': self.handling_fee,
            'money_back': self.money_back,
            'costs_incurred': round(self.ticket_price - self.money_back, 2)
        }

        return result

    def __str__(self):
        return 'Nowy bilet {} - {} (dni: {})'.format(self.start_date, self.stop_date, self.day)
