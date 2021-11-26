import time

import click
import requests


@click.command()
@click.option("--beta", "-b", is_flag=True, default=False)
@click.option("--endpoint", "-e", default="http://localhost")
@click.option("--delay", "-d", default=1, type=int)
def run(beta, endpoint, delay):
    headers = {}
    if beta:
        headers["beta-user"] = True
    while True:
        try:
            print(requests.get(endpoint, headers=headers).json()["message"])
        except Exception as e:
            print(e)
        time.sleep(delay)


if __name__ == "__main__":
    run()
