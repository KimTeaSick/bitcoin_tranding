import websocket
import json
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import pandas as pd

# Use a context manager to handle database sessions
def get_coin_names():
    with SessionLocal() as db:
        coin_list = db.query(models.coinList).all()
        return [coin.coin_name for coin in coin_list]

coin_names = get_coin_names()

def is_minute_odd():
    now = datetime.datetime.now().strftime("%H%M")
    return int(now) % 2 == 1

def on_open(ws):
    print('WebSocket connection opened')
    subscribe_data = {
        "type": "transaction",
        "symbols": coin_names
    }
    ws.send(json.dumps(subscribe_data))

def on_message(ws, message):
    try:
        now = datetime.datetime.now().strftime("%H%M")
        data = json.loads(message)
        odd_even = int(now) % 2

        if odd_even == 1:
            odd_collector.extend(data['content']['list'])
        else:
            even_collector.extend(data['content']['list'])

        if min_odd_even == 'even' and odd_even == 1:
            min_odd_even = 'odd'
            collect_and_insert(even_collector)
            even_collector.clear()

        if min_odd_even == 'odd' and odd_even == 0:
            min_odd_even = 'even'
            collect_and_insert(odd_collector)
            odd_collector.clear()
    except Exception as e:
        print(f"Error in on_message: {e}")

def on_close(ws):
    print('WebSocket connection closed')

def on_error(ws, error):
    print(f"Error: {error}")

def collect_and_insert(collector):
    with SessionLocal() as db:
        now1 = datetime.datetime.now()
        df = pd.DataFrame(collector)

        current_prices = db.query(models.coinCurrentPrice).all()
        bulk_insert = []

        for coin in current_prices:
            df_filtered = df.loc[df['symbol'] == coin.coin_name]
            transaction_count = len(df_filtered)
            now = datetime.datetime.now()
            unix_timestamp = int(now.timestamp() / 60) * 60

            if transaction_count == 0:
                continue

            df_filtered = df_filtered.astype({'contPrice': 'float', 'contQty': 'float', 'contAmt': 'float'})
            avg_price = df_filtered['contPrice'].mean()
            min_price = df_filtered['contPrice'].min()
            open_price = df_filtered['contPrice'].iloc[0]
            close_price = df_filtered['contPrice'].iloc[-1]
            max_price = df_filtered['contPrice'].max()
            transaction_amount = df_filtered['contAmt'].sum()
            volume = df_filtered['contQty'].sum()
            disparity = (avg_price / close_price) * 100

            bulk_insert.append({
                'coin_name': coin.coin_name, 'S_time': unix_timestamp, 'time': datetime.datetime.fromtimestamp(unix_timestamp),
                'Open': open_price, 'Close': close_price, 'High': max_price, 'Low': min_price,
                'Avg_price': avg_price, 'Transaction_amount': transaction_amount, 'Volume': volume,
                'Disparity': disparity, 'Ask_price': 0
            })

        try:
            db.bulk_insert_mappings(models.coinPrice1M, bulk_insert)
            db.commit()
        except Exception as e:
            print(f"Database insert error: {e}")
            db.rollback()

        now2 = datetime.datetime.now()
        print(f"Insert duration: {now2 - now1}")
        print(f"Inserted {len(bulk_insert)} records")

# Initialize WebSocket collectors and state
odd_collector = []
even_collector = []
min_odd_even = 'even' if not is_minute_odd() else 'odd'

websocket_url = 'wss://pubwss.bithumb.com/pub/ws'
ws = websocket.WebSocketApp(websocket_url,
                            on_open=on_open,
                            on_message=on_message,
                            on_close=on_close,
                            on_error=on_error)

ws.run_forever()
