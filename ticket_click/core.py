import click
import pendulum


from ticket_click.utils import Ticket
from ticket_click.utils import create_config

# add config file
create_config()


@click.command()
@click.option('--start_date', prompt='Kiedy bilet został aktywowany? ', help="Date in format dd-mm-yyyy", default='')
@click.option('--stop_date', prompt='Do kiedy bilet jest ważny? ', help="Date in format dd-mm-yyyy")
@click.option('--cancel_date', prompt='Kiedy chcesz anulować bilet? ', help="Date in format dd-mm-yyyy")
@click.option('--period', default=30, prompt='Na ile dni wykupiłeś bilet (30/90)? ', help="Number: 30 or 90. Default value: 30")
@click.option('--ticket_price',default=0.00, prompt='Ile zapłaciłeś za bilet? ', help="Ticker price: float. Default value: 0.00")
def cli(start_date, stop_date, cancel_date, period, ticket_price):
    """ This is a simple app in which you can count how much money you will receive back,
        if you cancel your ZTM (Warsaw) ticket."""

    if start_date == '':
        start_date = None
        while True:
            try:
                stop_date = Ticket.convert_date(stop_date)
                break
            except ValueError:
                raise click.ClickException('-- Wprowadzona data końca ważności biletu jest błędna! ---')
    else:
        while True:
            try:
                start_date = Ticket.convert_date(start_date)
                stop_date = Ticket.convert_date(stop_date)
                break
            except ValueError:
                raise click.ClickException('-- Wprowadzona data aktywacji biletu jest błędna! ---')

    if start_date == None:
        start_date = stop_date - pendulum.duration(days=period) + pendulum.duration(days=1)

    while period != 30 and period != 90:
        raise click.ClickException('-- Wprowadzono błędną wartość! ---')

    while True:
        try:
            cancel_date = Ticket.convert_date(cancel_date)
            if cancel_date < start_date:
                raise click.ClickException("-- Nie można zwrócić biletu przed jego aktywacją! --")
            elif cancel_date > stop_date:
                raise click.ClickException('-- Nie można zwrócić biletu po terminie ważnośći! --')
            else:
                break
        except ValueError:
            raise click.ClickException('--- Wprowadzona data anulowania biletu jest błędna! ---')

    ticket_price = round(ticket_price, 2)

    new_ticket = Ticket(start_date, period, stop_date, cancel_date, ticket_price)
    result = new_ticket.count_money_back()

    click.echo(f'\nOpłata manipulacyjna: {result.get("handling_fee")} zł \
               \n\nDo zwrotu: {result.get("money_back")} zł. \
               \nPoniesiony koszt: {result.get("costs_incurred")} zł ({result.get("one_day_cost")} zł/dzień)')