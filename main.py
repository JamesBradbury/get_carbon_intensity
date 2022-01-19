from http import HTTPStatus

import requests as requests


def get_outward_postcode(postcode: str) -> str:
    """Outward postcode is the first part, excluding any spaces and the last 3 characters."""
    if len(postcode) > 4:
        return postcode[:-3].replace(" ", "")
    return postcode


def get_intensity_for_postcode(postcode: str, from_date=None, to_date=None) -> int:
    """
    Returns the carbon intensity as an integer. This value is described here:
    https://raw.githubusercontent.com/carbon-intensity/methodology/master/
    Regional%20Carbon%20Intensity%20Forecast%20Methodology.pdf
    :param postcode: Postcode for the carbon intensity. Only the outgoing (first part) is used.
    :param from_date: datetime in ISO8601 format YYYY-MM-DDThh:mmZ
    :param to_date: datetime in ISO8601 format YYYY-MM-DDThh:mmZ
    :return:
    """
    outward_postcode = get_outward_postcode(postcode)
    if from_date and to_date:
        url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_date}/{to_date}/postcode/{outward_postcode}"
    else:
        url = f"https://api.carbonintensity.org.uk/regional/postcode/{outward_postcode}"
    response = requests.get(url=url)
    if response.status_code != HTTPStatus.OK:
        raise ConnectionError(f"GET request to '{url}' failed with status: {response.status_code}")
    data = response.json()["data"][0]["data"][0]

    return data["intensity"]["forecast"]


# # Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Intensity:", get_intensity_for_postcode("RG14"))

