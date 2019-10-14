import pendulum

class Ticket:
    #handling fee is 20% but not more than 50 zl
    handling_fee_percent = 0.2

    def __init__(self, start_date = None, day = 0, stop_date = None, cancel_date = None, ticket_price = None):
        self.start_date = start_date
        self.day = day
        self.stop_date = stop_date
        self.cancel_date = cancel_date
        self.money_back = None
        self.ticket_price = ticket_price

    @staticmethod
    def convert_date(date):
        day, month, year = date.split('-')
        return pendulum.date(int(year), int(month), int(day))

    def count_money_back(self):
        self.handling_fee = self.handling_fee_percent * self.ticket_price
        if self.handling_fee > 50:
            self.handling_fee = 50

        self.cancled_days = self.stop_date - self.cancel_date
        self.money_back = round(float((self.ticket_price - self.handling_fee)/self.day * int(self.cancled_days.days)),2)
        return '\nOpłata manipulacyjna: {:.2f} zł' \
               '\n\nDo zwrotu: {:.2f} zł.' \
               '\nPoniesiony koszt: {:.2f} zł ({} zł/dzień) '.format(self.handling_fee,
                                                       self.money_back,
                                                       self.ticket_price - self.money_back,
                                                       round((self.ticket_price - self.money_back)/int((self.cancel_date-self.start_date).days + 1),2),)

    def __str__(self):
        return 'Nowy bilet {} - {} (dni: {})'.format(self.start_date, self.stop_date, self.day)