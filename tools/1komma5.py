import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from custom_components.einskomma5grad.api.client import Client
from custom_components.einskomma5grad.api.systems import Systems


def main():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    api_client = Client(username, password)

    systems = Systems(api_client).get_systems()

    for system in systems:
        print(
            system.get_prices(
                datetime.datetime.now(),
                datetime.datetime.now() + datetime.timedelta(days=1),
            )
        )


if __name__ == "__main__":
    main()
