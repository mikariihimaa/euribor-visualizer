import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def fetch_euribor_data(start_date: str, end_date: str):
    """
    Hakee Euribor-korkoja ECB:n APIsta valitulta aikaväliltä.
    """
    base_url = "https://sdw-wsrest.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR{maturity}.R?startPeriod={start}&endPeriod={end}&format=csv"
    
    maturities = {"1M": "1M", "3M": "3M", "6M": "6M", "12M": "12M"}
    data = {}
    
    for key, maturity in maturities.items():
        url = base_url.format(maturity=maturity, start=start_date, end=end_date)
        response = requests.get(url)
        
        if response.status_code == 200:
            df = pd.read_csv(pd.compat.StringIO(response.text), skiprows=5)
            df = df[["TIME_PERIOD", "OBS_VALUE"]]
            df.columns = ["Date", key]
            df["Date"] = pd.to_datetime(df["Date"])
            data[key] = df
        else:
            print(f"Failed to fetch {key} data: {response.status_code}")
    
    if data:
        merged_df = list(data.values())[0]
        for key in list(data.keys())[1:]:
            merged_df = merged_df.merge(data[key], on="Date", how="outer")
        return merged_df
    return None

def plot_euribor(data, start_date, end_date):
    """ Piirtää Euribor-käyrät valitulta aikaväliltä. """
    plt.figure(figsize=(10, 5))
    
    for column in data.columns[1:]:
        plt.plot(data["Date"], data[column], label=column)
    
    plt.xlabel("Päivämäärä")
    plt.ylabel("Korko (%)")
    plt.title(f"Euribor-korot {start_date} - {end_date}")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    start_date = input("Syötä aloituspäivä (YYYY-MM-DD): ")
    end_date = input("Syötä lopetuspäivä (YYYY-MM-DD): ")
    
    data = fetch_euribor_data(start_date, end_date)
    if data is not None:
        plot_euribor(data, start_date, end_date)
    else:
        print("Tietoa ei saatavilla valitulle aikavälille.")
