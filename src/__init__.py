from pprint import pprint

from api_context.api import ApiManager


# %%
def _main():
    api_manager = ApiManager()
    while True:
        input_currency = input("Please enter the name of a currency. : ")
        api_resp = api_manager.query_get_x_rate(input_currency)
        if api_resp is None:
            continue
        print(api_resp)
        break


if __name__ == "__main__":
    _main()

# %%


# Let's use https://restcountries.com/ for Task 2
