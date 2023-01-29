import requests
from typing import List
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from models import CurrentTicker, UpdateTicker
from uuid import UUID, uuid4


app = FastAPI()

db: List[CurrentTicker] = [
    CurrentTicker(
        id=UUID("5cd1e186-1d4a-4378-91fc-bea9f58b4cfa"),
        current_ticker = "TSLA"
    )
]


@app.get("/api/v1/ticker")
async def fetch_ticker():
    return db

@app.put("/api/v1/ticker/{new_ticker}")
async def update_ticker(ticker_update: UpdateTicker, new_ticker):
    for ticker in db:
        if ticker.current_ticker != new_ticker:
            if ticker_update.new_ticker is not None:
                ticker.current_ticker = new_ticker
            return
    raise HTTPException(
        status_code=404,
        detail = f"ticker '{new_ticker}' does not exist"
    )

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

