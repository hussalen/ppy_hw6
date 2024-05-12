import json
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import requests
from nbp.currency import CurrencyCode, CurrentExchangeRateResponse


class ApiManager:
    def __init__(self):
        self.default_accept_header: str = "application/json"
        self.domain: str = "http://api.nbp.pl"
        self.table = "C"

    def _get_query_response(self, req_endpoint):
        try:
            query = requests.get(
                url=req_endpoint,
                headers={"Accept": self.default_accept_header},
                timeout=35,
            )
            resp = None
            if query.ok:
                resp = query.json()
        except (requests.exceptions.BaseHTTPError, json.decoder.JSONDecodeError) as e:
            err_msg = f"Request failed!: {e}"
            raise RuntimeError(err_msg) from e

        resp_code = int(str(query.status_code)[0])

        if resp is None and (resp_code in (4, 5)):
            err_msg = f"Invalid request {query.status_code}."
            raise RuntimeError(err_msg)
        return resp

    def query_get_x_rate(self, input_currency: str) -> str:
        try:
            currency = CurrencyCode(input_currency)
        except ValueError as e:
            print(f"Invalid currency: {e}. Please try again.")
            return None

        path_x_rate = f"/api/exchangerates/rates/{self.table}/{currency.code}/"
        req_endpoint = self.domain + path_x_rate

        resp = self._get_query_response(req_endpoint)

        currency_x_rate_resp = CurrentExchangeRateResponse(
            resp["code"],
            resp["currency"],
            resp["rates"],
        )

        rate = currency_x_rate_resp.rates[0]
        return f"Currency code: {currency_x_rate_resp.code}: Buy: {rate["bid"]}, Sell: {rate["ask"]}"

    def query_get_x_rate_last_n_days(
        self,
        input_currency: str,
        last_nr_of_days: int,
    ):
        if not last_nr_of_days > 0:
            raise ValueError("Last no. of days must be greater than 1")
        try:
            currency = CurrencyCode(input_currency)
        except ValueError as e:
            print(f"Invalid currency: {e}. Please try again.")
            return

        path_x_rate_last_n_days = f"/api/exchangerates/rates/{self.table}/{currency.code}/last/{last_nr_of_days}"
        req_endpoint = self.domain + path_x_rate_last_n_days

        resp = self._get_query_response(req_endpoint)

        currency_x_rate_resp = CurrentExchangeRateResponse(
            resp["code"],
            resp["currency"],
            resp["rates"],
        )
        rates = currency_x_rate_resp.rates

        buying_rates = [float(rate["bid"]) for rate in rates]
        print(buying_rates)
        buying_rates_over_time = [
            datetime.strptime(rate["effectiveDate"], "%Y-%m-%d") for rate in rates
        ]
        print(buying_rates_over_time)

        plt.plot_date(
            buying_rates_over_time,
            buying_rates,
            linestyle="solid",
        )

        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Price vs. Date")

        plt.gca().xaxis.set_major_locator(
            mdates.AutoDateLocator(),
        )  # Set ticks at the beginning of each month
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        plt.xticks(buying_rates_over_time, rotation=45)

        plt.show()

    def query_get_x_rate_range(
        self,
        input_currency: str,
        input_start_date: str,
        input_end_date: str,
    ):
        start_date = datetime.strptime(input_start_date, "%Y-%m-%d")
        end_date = datetime.strptime(input_end_date, "%Y-%m-%d")

        date_threshold = datetime(2002, 1, 2)

        if start_date < date_threshold or end_date < date_threshold:
            msg = f"Date is older than {date_threshold}"
            raise ValueError(msg)
        if start_date > end_date:
            msg = "End date is newer than start date"
            raise ValueError(msg)

        try:
            currency = CurrencyCode(input_currency)
        except ValueError as e:
            print(f"Invalid currency: {e}. Please try again.")
            return

        path_x_rate_last_n_days = f"/api/exchangerates/rates/{self.table}/{currency.code}/{input_start_date}/{input_end_date}"
        print(path_x_rate_last_n_days)
        req_endpoint = self.domain + path_x_rate_last_n_days

        resp = self._get_query_response(req_endpoint)

        currency_x_rate_resp = CurrentExchangeRateResponse(
            resp["code"],
            resp["currency"],
            resp["rates"],
        )
        rates = currency_x_rate_resp.rates

        buying_rates = [float(rate["bid"]) for rate in rates]
        print(buying_rates)
        buying_rates_over_time = [
            datetime.strptime(rate["effectiveDate"], "%Y-%m-%d") for rate in rates
        ]
        print(buying_rates_over_time)

        plt.plot_date(
            buying_rates_over_time,
            buying_rates,
            linestyle="solid",
        )

        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Price vs. Date")

        plt.gca().xaxis.set_major_locator(
            mdates.AutoDateLocator(),
        )  # Set ticks at the beginning of each month
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

        plt.xticks(buying_rates_over_time, rotation=45)

        plt.show()


# end def
