from bs4 import BeautifulSoup
from uk_bin_collection.uk_bin_collection.get_bin_data import AbstractGetBinDataClass
from datetime import datetime

import re
import requests


def get_token(res) -> str:
    """
Get a UFPRT code for the form data to be processed
    :param res:
    :return:
    """
    soup = BeautifulSoup(res, features="html.parser")
    soup.prettify()
    token = soup.find("input", {"name": "ufprt"}).get("value")
    return token


# import the wonderful Beautiful Soup and the URL grabber
class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def parse_data(self, page: str, **kwargs) -> dict:
        api_url = "https://www.midsussex.gov.uk/waste-recycling/bin-collection/"
        user_postcode = kwargs.get("postcode")
        user_paon = kwargs.get("paon")
        postcode_re = "^([A-Za-z][A-Ha-hJ-Yj-y]?[0-9][A-Za-z0-9]? ?[0-9][A-Za-z]{2}|[Gg][Ii][Rr] ?0[Aa]{2})$"
        user_full_addr = f"{user_paon} {user_postcode}"

        try:
            if user_postcode is None or not re.fullmatch(postcode_re, user_postcode):
                raise ValueError("Invalid postcode")
        except Exception as ex:
            print(f"Exception encountered: {ex}")
            print(
                "Please check the provided postcode. If this error continues, please first trying setting the "
                "postcode manually on line 24 before raising an issue."
            )
            exit(1)

        try:
            if user_paon is None:
                raise ValueError("Invalid house number")
        except Exception as ex:
            print(f"Exception encountered: {ex}")
            print(
                "Please check the provided house number. If this error continues, please first trying setting the "
                "house number manually on line 25 before raising an issue."
            )
            exit(1)
        form_data = {"PostCodeStep.strAddressSearch": user_postcode, "AddressStep.strAddressSelect": user_full_addr,
                     "Next":                          "true", "StepIndex": "1"}

        # Get a ufprt by posting here (I have no idea how ufprt works, so may as well grab one from the server)
        init = requests.post(api_url, data=form_data)
        ufprt = get_token(init.text)
        form_data.update({"ufprt": ufprt})

        response = requests.post(api_url, data=form_data)

        # Make a BS4 object
        soup = BeautifulSoup(response.text, features="html.parser")
        soup.prettify()

        data = {"bins": []}

        table_element = soup.find("table", {"class": "collDates"})
        table_rows = table_element.find_all_next("tr")

        row_index = 0
        for row in table_rows:
            if row_index < 1:
                row_index += 1
                continue
            else:
                details = row.find_all_next("td")
                dict_data = {
                    "type":           details[1].get_text().replace("collection", "").strip(),
                    "collectionDate": datetime.strptime(details[2].get_text(), "%A %d %B %Y").strftime("%d/%m/%Y")
                }
                data["bins"].append(dict_data)
                row_index += 1

        return data
