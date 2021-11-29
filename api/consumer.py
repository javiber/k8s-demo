import random
import time

import click
import pandas as pd
import requests
import rich
from dateutil import parser
from rich import print
from rich.columns import Columns
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


@click.command()
@click.option(
    "--beta",
    "-b",
    is_flag=True,
    default=False,
    help="if true include 'beta-user' to headers. Defaults to False",
)
@click.option(
    "--endpoint",
    "-e",
    required=True,
    help="endpoint to ping, ex: http://10.104.244.194",
)
@click.option(
    "--delay",
    "-d",
    default=1,
    type=int,
    help="delay between requests in seconds. Defaults to 1",
)
def run(beta, endpoint, delay):
    """Run a consumer that pings the API regularly"""
    headers = {}
    if beta:
        headers["beta-user"] = "true"
    df = pd.DataFrame(columns=["datetime", "message", "failed", "latency"])
    header = Layout(Panel(f"{'[bold yellow]Beta' if beta else 'Regular'} Consumer"))
    messages = Layout()
    stats = Layout()
    body = Layout()
    body.split_row(messages, stats)
    layout = Layout()
    layout.split_column(header, body)
    with Live(layout, refresh_per_second=2):
        while True:
            failed = False
            latency = None
            dt = None
            req = requests.get(endpoint, headers=headers, timeout=1)
            latency = req.elapsed
            dt = parser.parse(req.headers["date"])
            try:
                req.raise_for_status()
                message = req.json()["message"]
            except Exception as e:
                message = str(e)
                failed = True

            df = df.append(
                {
                    "datetime": dt,
                    "message": message,
                    "failed": failed,
                    "latency": latency,
                },
                ignore_index=True,
            )
            l = ["[bold]Messages[/]"]
            for x in df[-5:].itertuples():
                m = x.message
                if x.failed:
                    m = f"[bold red]{m}[/]"
                l.append(f"{x.datetime} {m} {x.latency}")
            messages.update(Panel("\n".join(l)))

            stats.update(
                Panel(
                    "\n".join(
                        [
                            "[bold]Stats(last 30)[/]",
                            f"failed: {df[-30:]['failed'].mean().round(2)}",
                            f"latency: {df[-30:]['latency'].mean()}",
                        ]
                    )
                )
            )
            time.sleep(delay)


if __name__ == "__main__":
    run()
