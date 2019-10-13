import click
from ticket_click.utils import Ticket


@click.command()
def cli():
    click.echo("""
    ******************************************************************************************************
    Jeżeli nie pamiętasz daty aktywacji biletu, to podaj datę końca ważności biletu
    i rodzaj biletu (30/90 dni).
    ******************************************************************************************************
    """)
