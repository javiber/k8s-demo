import time

import click
import pandas as pd
import requests
from dateutil import parser
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner


@click.command()
@click.option(
    "--user",
    "-u",
    default="Jim",
    help="user to be included in the headers. Defaults to Jim",
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
    type=float,
    help="delay between requests in seconds. Defaults to 1",
)
def run(user, endpoint, delay):
    """Run a consumer that pings the API regularly"""
    headers = {"user": user}

    df = pd.DataFrame(columns=["datetime", "message", "failed", "latency"])
    df["latency"] = pd.to_timedelta(df["latency"])
    header = Layout(Panel(Spinner("dots", text=f"Consumer\nUser: [bold]'{user}'[/]")))
    messages = Layout()
    stats = Layout()
    body = Layout()
    body.split_row(messages, stats)
    layout = Layout()
    layout.split_column(header, body)
    with Live(layout, refresh_per_second=4):
        while True:
            failed = False
            latency = None
            dt = None
            try:
                req = requests.get(endpoint, headers=headers)
                latency = req.elapsed
                dt = parser.parse(req.headers["date"])
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
                l.append(f"{x.datetime} '{m}'")
            messages.update(Panel("\n".join(l)))

            df = df.iloc[-30:]

            stats.update(
                Panel(
                    "\n".join(
                        [
                            "[bold]Stats(last 30)[/]",
                            f"failed: {df['failed'].mean().round(2)}",
                            f"latency: {df['latency'].mean()} ({round(1000 * df['latency'].mean().total_seconds())}ms)",
                            "values:",
                            *[
                                f"    {v}: {p}"
                                for v, p in df.message.value_counts(
                                    normalize=True
                                ).iteritems()
                            ],
                        ]
                    )
                )
            )
            time.sleep(delay)


if __name__ == "__main__":
    run()
