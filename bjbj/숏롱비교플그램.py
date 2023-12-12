import tkinter as tk
from datetime import datetime, timedelta
from binance.client import Client

# 바이낸스 API 키와 시크릿 키 설정
api_key = 'your_api_key'
api_secret = 'your_api_secret'

client = Client(api_key, api_secret)

def get_binance_data(symbol):
    trades = client.futures_recent_trades(symbol=symbol, limit=1000)
    return trades

def calculate_totals(trades):
    short_total_sell = 0
    long_total_buy = 0

    for trade in trades:
        price = float(trade['price'])
        qty = float(trade['qty'])

        if trade['isBuyerMaker']:  # Buyer가 Maker인 경우 (롱 - 코인을 사는 경우)
            long_total_buy += price * qty
        else:  # Seller가 Maker인 경우 (숏 - 코인을 파는 경우)
            short_total_sell += price * qty

    return short_total_sell, long_total_buy

def convert_to_krw(amount_usd, exchange_rate):
    krw_amount = amount_usd * exchange_rate
    return "{:,.0f}".format(krw_amount) + "원"

def measure_volumes(symbol, exchange_rate):
    short_count = 0
    long_count = 0

    def on_click():
        nonlocal short_count, long_count
        coin_name = entry.get()
        coin_trades = get_binance_data(coin_name)
        
        if coin_trades:
            short_total, long_total = calculate_totals(coin_trades)
            short_total_krw = convert_to_krw(short_total, exchange_rate)
            long_total_krw = convert_to_krw(long_total, exchange_rate)

           
            long_label.config(text=f"롱 구매금액 총 합 (KRW): {long_total_krw}")
            short_label.config(text=f"숏 판매금액 총 합 (KRW): {short_total_krw}")
            
            
            long_count_label.config(text=f"롱 구매금액 총 합: {long_total:.2f}")
            short_count_label.config(text=f"숏 판매금액 총 합: {short_total:.2f}")
        else:
            short_label.config(text="잘못된 코인 이름입니다.")
            long_label.config(text="")
            short_count_label.config(text="")
            long_count_label.config(text="")

    root = tk.Tk()
    root.title("바이낸스 거래량 측정기")

    label = tk.Label(root, text="코인 이름을 입력하세요 (예: BTCUSDT):")
    label.pack()

    entry = tk.Entry(root)
    entry.pack()

    button = tk.Button(root, text="조회", command=on_click)
    button.pack()

    short_label = tk.Label(root, text="")
    short_label.pack()

    long_label = tk.Label(root, text="")
    long_label.pack()

    author_label = tk.Label(root, text="-By Park Byeong Jun-")
    author_label.pack()

    root.mainloop()

# 환율 입력 후 GUI 실행
while True:
    try:
        exchange_rate = float(input("1달러당 한국돈 환율을 입력하세요: "))
        measure_volumes("", exchange_rate)
        break
    except ValueError:
        print("숫자를 입력하세요.")
