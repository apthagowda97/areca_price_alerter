import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date



def parse_url(url: str):
    """Parses the URL and returns the Areca Price data as DataFrame"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    price_table = soup.find(id="_ctl0_content5_Table1")
    price_df = pd.read_html(str(price_table), header=0)[0]

    return price_df


def get_body(city: str):
    """" Returns message body consisting of Areca price for the given city"""

    today = date.today()
    today_date = today.strftime("%d/%m/%Y")
    price_df = parse_url(open("url.txt").read())
    if city in price_df.Market.values:
        data = (
            price_df[price_df["Market"] == city][
                ["Variety", "Market Date", "Maximum Price"]
            ]
            .sort_values("Variety")
            .values.tolist()
        )
        if today_date == data[0][1]:
            body = f"\n  {city}\n"
            for row in data:
                body += "{0}({1}): {2}\n".format(row[0][:5], row[1].split("/")[0], row[2])
            return body
        else:
            return None
    else:
        return None
