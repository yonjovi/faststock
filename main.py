import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()


@app.get("/get_ticker_data/{ticker}")
async def get_ticker_data(ticker: str):
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
    response = session.get(f'https://finance.yahoo.com/quote/{ticker}')
    if response.status_code != 200:
        return {"error": f"bad status code {response.status_code}"}
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        data = {
            "name": ticker,
            "price": soup.find("fin-streamer", {"class": "Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text
        }
        ticker_update_results = {"results": data}
        return ticker_update_results
    except KeyError:
        return {"error": "Unable to parse page"}
    await get_ticker_data