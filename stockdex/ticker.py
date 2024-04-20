"""
Moduel for the Ticker class
"""

import pandas as pd
from bs4 import BeautifulSoup

from stockdex.config import VALID_SECURITY_TYPES
from stockdex.digrin_interface import Digrin_Interface
from stockdex.justetf import JustETF
from stockdex.nasdaq_interface import NASDAQInterface
from stockdex.ticker_api import TickerAPI
from stockdex.yahoo_web import YahooWeb


class Ticker(TickerAPI, JustETF, NASDAQInterface, Digrin_Interface, YahooWeb):
    """
    Class for the Ticker
    """

    def __init__(
        self,
        ticker: str = "",
        isin: str = "",
        security_type: VALID_SECURITY_TYPES = "stock",
    ) -> None:
        """
        Initialize the Ticker class

        Args:
        ticker (str): The ticker of the stock
        isin (str): The ISIN of the etf
        security_type (str): The security type of the ticker
            default is "stock"
        """

        self.ticker = ticker
        self.isin = isin
        self.security_type = security_type if security_type else "stock"

        if not ticker and not isin:
            raise Exception("Please provide either a ticker or an ISIN")

        if security_type == "etf":
            super().__init__(isin=isin, security_type=security_type)
        else:
            super().__init__(ticker=ticker, security_type=security_type)

    @property
    def summary(self) -> pd.DataFrame:
        """
        Get data for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the data
        visible in the Yahoo Finance first page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        # for data in the table, generating 16 rows
        raw_data = soup.find_all("td", {"data-test": True})
        data_df = pd.DataFrame()
        for item in raw_data:
            data_df[item["data-test"].replace("-value", "")] = [item.text]

        # for data in top of the page, generating 10 rows
        raw_data = soup.find_all("fin-streamer", {"data-field": True})
        for item in raw_data:
            data_df[item["data-field"]] = [item.text]

        return data_df.T

    @property
    def statistics(self) -> pd.DataFrame:
        """
        Get statistics for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the statistics
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/key-statistics"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")
        raw_data = soup.find_all("tr", {"class": True})

        data_df = pd.DataFrame()
        for item in raw_data:
            cols = item.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data_df[cols[0]] = [cols[1]]

        return data_df.T

    @property
    def analysis(self) -> pd.DataFrame:
        """
        Get analysis for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the analysis
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/analysis"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        raw_data = soup.find_all("tbody")

        data_df = pd.DataFrame()
        for item in raw_data:
            for row in item.find_all("tr"):
                row = row.find_all("td")
                criteria = row[0].text

                # the rest of the row is the data
                data_list = []
                for data in row[1:]:
                    data_list.append(data.text)

                data_df[criteria] = data_list

        return data_df.T

    @property
    def calls(self) -> pd.DataFrame:
        """
        Get calls for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the calls
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/options"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        # gets calls and puts
        tables = soup.find_all("table")
        headers, data = [], []

        thead = tables[0].find("thead")
        tbody = tables[0].find("tbody")
        data_df = pd.DataFrame()

        # get headers
        for th in thead.find_all("th"):
            headers.append(th.text)

        # get data
        for tr in tbody.find_all("tr"):
            row = tr.find_all("td")
            data.append([data.text for data in row])

        data_df = pd.DataFrame(data, columns=headers)

        return data_df

    @property
    def puts(self) -> pd.DataFrame:
        """
        Get puts for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the puts
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/options"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        # gets calls and puts
        tables = soup.find_all("table")
        headers, data = [], []

        thead = tables[1].find("thead")
        tbody = tables[1].find("tbody")
        data_df = pd.DataFrame()

        # get headers
        for th in thead.find_all("th"):
            headers.append(th.text)

        # get data
        for tr in tbody.find_all("tr"):
            row = tr.find_all("td")
            data.append([data.text for data in row])

        data_df = pd.DataFrame(data, columns=headers)

        return data_df

    @property
    def key_executives(self) -> pd.DataFrame:
        """
        Get profile key executives for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the profile key executives
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/profile"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        raw_data = soup.find_all("table")

        data_df = pd.DataFrame()
        data = []

        criteria = [th.text for th in raw_data[0].find_all("thead")[0].find_all("th")]
        for tr in raw_data[0].find_all("tbody")[0].find_all("tr"):
            data.append([td.text for td in tr.find_all("td")])

        data_df = pd.DataFrame(data, columns=criteria)

        return data_df

    @property
    def description(self) -> str:
        """
        Get the description of the ticker

        Returns:
        str: A string including the description of the ticker
        visible in the Yahoo Finance profile page for the ticker
        """
        if self.security_type == "etf":
            return self.etf_description

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/profile"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        raw_data = soup.find_all("p")

        return raw_data[2].text

    @property
    def corporate_governance(self) -> str:
        """
        Get the description of the ticker

        Returns:
        str: A string including the description of the ticker
        visible in the Yahoo Finance profile page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/profile"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        raw_data = soup.find_all("p")

        return raw_data[3].text

    @property
    def major_holders(self) -> pd.DataFrame:
        """
        Get major holders for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the major holders
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/holders"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")

        raw_data = soup.find_all("div", {"data-test": "holder-summary"})

        data_df = pd.DataFrame()
        data = []

        table = raw_data[0].find_all("tr")
        for tr in table:
            data.append([td.text for td in tr.find_all("td")])

        data_df = pd.DataFrame(data)
        data_df.columns = ["percentage", "holders"]
        return data_df

    @property
    def top_institutional_holders(self) -> pd.DataFrame:
        """
        Get top institutional holders for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the top institutional holders
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/holders"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")
        raw_data = soup.find_all("table")

        data_df = pd.DataFrame()
        data = []

        table = raw_data[1].find_all("tr")
        for tr in table:
            data.append([td.text for td in tr.find_all("td")])

        data_df = pd.DataFrame(data)
        data_df.columns = ["holder", "shares", "date_reported", "percentage", "value"]
        return data_df

    @property
    def top_mutual_fund_holders(self) -> pd.DataFrame:
        """
        Get top mutual fund holders for the ticker

        Returns:
        pd.DataFrame: A pandas DataFrame including the top mutual fund holders
        visible in the Yahoo Finance statistics page for the ticker
        """

        # URL of the website to scrape
        url = f"https://finance.yahoo.com/quote/{self.ticker}/holders"
        response = self.get_response(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, "html.parser")
        raw_data = soup.find_all("table")

        data_df = pd.DataFrame()
        data = []

        table = raw_data[2].find_all("tr")
        for tr in table:
            data.append([td.text for td in tr.find_all("td")])

        data_df = pd.DataFrame(data)
        data_df.columns = ["holder", "shares", "date_reported", "percentage", "value"]
        return data_df
