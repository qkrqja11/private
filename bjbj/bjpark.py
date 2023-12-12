import time
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
    short_total_buy = 0
    long_total_buy = 0

    for trade in trades:
        price = float(trade['price'])
        qty = float(trade['qty'])

        if trade['isBuyerMaker']:  # Seller가 Maker인 경우 (숏 - 코인을 파는 경우)
            short_total_buy += price * qty
        else:  # Buyer가 Maker인 경우 (롱 - 코인을 사는 경우)
            long_total_buy += price * qty

    return short_total_buy, long_total_buy

def convert_to_krw(amount_usd, exchange_rate):
    krw_amount = amount_usd * exchange_rate
    return "{:,.0f}".format(krw_amount) + "원"

def measure_volumes(symbol, exchange_rate):
    start_time = datetime.utcnow().replace(second=0, microsecond=0)
    short_count = 0
    long_count = 0

    while True:
        current_time = datetime.utcnow().replace(second=0, microsecond=0)
        trades = get_binance_data(symbol)
        
        if trades:
            short_total, long_total = calculate_totals(trades)
            short_total_krw = convert_to_krw(short_total, exchange_rate)
            long_total_krw = convert_to_krw(long_total, exchange_rate)

            if current_time != start_time:
                print(f"{'='*20} New Interval {'='*20}")
                start_time = current_time
                short_count = 0
                long_count = 0

            if short_total > long_total:
                print(f"숏 구매금액 총 합이 롱보다 큽니다. (숏: {short_count + 1}, 롱: {long_count})")
                print(f"숏 구매금액 총 합 (KRW): {short_total_krw}")
                short_count += 1
            elif short_total < long_total:
                print(f"롱 구매금액 총 합이 숏보다 큽니다. (숏: {short_count}, 롱: {long_count + 1})")
                print(f"롱 구매금액 총 합 (KRW): {long_total_krw}")
                long_count += 1
            else:
                print(f"숏 구매금액 총 합과 롱 구매금액 총 합이 동일합니다. (숏: {short_count}, 롱: {long_count})")
                print(f"숏 구매금액 총 합 (KRW): {short_total_krw}")
                print(f"롱 구매금액 총 합 (KRW): {long_total_krw}")

            print(f"숏 구매금액 총 합: {short_total:.2f}")
            print(f"롱 구매금액 총 합: {long_total:.2f}")

        time.sleep(5)

while True:
    coin_name = input("코인 이름을 입력하세요 (예: BTCUSDT): ")
    exchange_rate = float(input("1달러당 한국돈 환율을 입력하세요: "))

    coin_trades = get_binance_data(coin_name)
    
    if coin_trades:
        measure_volumes(coin_name, exchange_rate)
    else:
        print("잘못된 코인 이름입니다. 다시 입력하세요.")
