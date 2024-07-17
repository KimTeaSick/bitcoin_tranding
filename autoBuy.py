import requests
import datetime
from database import SessionLocal
from sqlalchemy.orm import Session
import models
import asyncio
from pybithumb import Bithumb
from buy.optionStandardization import OptionStandardization
import askingPrice
import json

async def recommend_coins(options, m_max, h_max):
    coins = await recommend.recommendCoin(options, m_max, h_max)
    return coins

def get_active_users(db):
    return db.query(models.USER_T).filter(models.USER_T.active == 1).all()

def get_user_data(db, user):
    possession_coins = db.query(models.possessionCoin).filter(models.possessionCoin.user_idx == user.idx).all()
    use_recommend_option = db.query(models.searchOption).filter(models.searchOption.idx == user.search_option).first()
    use_trading_option = db.query(models.tradingOption).filter(models.tradingOption.idx == user.trading_option).first()
    account_option = db.query(models.tradingAccountOption).filter(models.tradingAccountOption.idx == use_trading_option.idx).first()
    buy_option = db.query(models.tradingBuyOption).filter(models.tradingBuyOption.idx == use_trading_option.idx).first()
    return possession_coins, use_recommend_option, use_trading_option, account_option, buy_option

def delete_previous_recommendations(db, user):
    prev_coin = db.query(models.recommendList).filter(models.recommendList.user_idx == user.idx).all()
    for coin in prev_coin:
        db.delete(coin)
    db.commit()

def insert_recommendations(db, coins, user_idx, option_name):
    for coin in coins['recommends']:
        coin_name = list(coin.keys())[0]
        rc_coin = models.recommendList()
        rc_coin.coin_name = coin_name
        rc_coin.catch_price = coin[coin_name]['closing_price']
        rc_coin.option_name = option_name
        rc_coin.user_idx = user_idx
        db.add(rc_coin)
    db.commit()

def get_balance(bithumb, currency):
    balance = bithumb.get_balance(currency)
    return balance[2] - balance[3]

def calculate_money_per_coin(buy_option, money):
    if buy_option.checkbox == 1:
        return buy_option.price_to_buy_method * 10000
    elif buy_option.checkbox == 2:
        return (money * buy_option.percent_to_buy_method) / 100

def main():
    now1 = datetime.datetime.now()

    with SessionLocal() as db:
        active_users = get_active_users(db)

        for active_user in active_users:
            bithumb = Bithumb(active_user.public_key, active_user.secret_key)
            possession_coins, use_recommend_option, use_trading_option, account_option, buy_option = get_user_data(db, active_user)

            coin_count = len(possession_coins)
            if coin_count > account_option.price_count:
                print('Exceeded maximum coin count')
                continue

            had_coins = [coin.coin for coin in possession_coins]

            option_result = OptionStandardization(
                db.query(models.PriceOption).filter(models.PriceOption.idx == use_recommend_option.idx).first(),
                db.query(models.TransactionAmountOption).filter(models.TransactionAmountOption.idx == use_recommend_option.idx).first(),
                db.query(models.MASPOption).filter(models.MASPOption.idx == use_recommend_option.idx).first(),
                db.query(models.TrendOption).filter(models.TrendOption.idx == use_recommend_option.idx).first(),
                db.query(models.DisparityOption).filter(models.DisparityOption.idx == use_recommend_option.idx).first(),
                db.query(models.MACDOption).filter(models.MACDOption.idx == use_recommend_option.idx).first()
            )
            options, m_max, h_max = option_result

            delete_previous_recommendations(db, active_user)

            coins = asyncio.run(recommend_coins(options, m_max, h_max))
            insert_recommendations(db, coins, active_user.idx, use_recommend_option.name)

            sorted_by_disparity = sorted(
                [{'name': list(coin.keys())[0], 'disparity': coin[list(coin.keys())[0]]['disparity'], 'price': coin[list(coin.keys())[0]]['closing_price']}
                for coin in coins['recommends']],
                key=lambda x: x['disparity']
            )

            money = get_balance(bithumb, 'BTC')
            money_per_coin = calculate_money_per_coin(buy_option, money)

            orders = []
            for coin in sorted_by_disparity:
                if coin_count >= int(account_option.price_count) or money_per_coin > money or coin['name'] in had_coins:
                    continue

                ask_price = askingPrice.ASK_PRICE(f"{coin['name']}", f"{buy_option.callmoney_to_buy_method:+d}", 'buy')
                fee = bithumb.get_trading_fee(coin['name'])
                payment = float(money_per_coin * (1 - fee))
                split_unit = round(payment / float(ask_price), 4)

                order = bithumb.buy_limit_order(
                    coin['name'], round(float(ask_price), 2), round(split_unit, 4), 'KRW'
                )
                order_id = order[2]

                money -= money_per_coin
                coin_count += 1

                orders.append({'coin': coin['name'], 'orders': order_id})

                # Add to orderCoin and possessionCoin tables
                order_coin = models.orderCoin(
                    coin=coin['name'],
                    status=1,
                    transaction_time=datetime.datetime.now(),
                    order_id=order_id,
                    cancel_time=datetime.datetime.now() + datetime.timedelta(seconds=account_option.buy_cancle_time),
                    user_idx=active_user.idx
                )
                db.add(order_coin)

                possession_coin = models.possessionCoin(
                    coin=coin['name'],
                    unit=0.0,
                    price=0.0,
                    total=0.0,
                    fee=0.0,
                    status=1,
                    transaction_time=datetime.datetime.now(),
                    order_id=order_id,
                    cancel_time=datetime.datetime.now() + datetime.timedelta(seconds=account_option.buy_cancle_time),
                    macd_chart=use_recommend_option.macdOption.chart_term,
                    disparity_chart=use_recommend_option.disparityOption.chart_term,
                    optionName=use_recommend_option.name,
                    trailingstop_flag=0,
                    max=0.0,
                    user_idx=active_user.idx
                )
                db.add(possession_coin)

            try:
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()

            with open("./buyLog", "a") as file:
                file.write(f'{datetime.datetime.now()} ------------------------------------------------------------------\n')
                for buy_coin in sorted_by_disparity:
                    file.write(str(buy_coin) + '\n')

    now2 = datetime.datetime.now()
    print(f'Execution Time: {now2 - now1}')

if __name__ == '__main__':
    main()
