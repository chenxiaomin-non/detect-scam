PRICE_FIELDS = ['id', 'num_market_pair', 'circulating_supply', 'total_supply',
                'max_supply', 'last_updated', 'date_added', 'usd_price', 'usd_volume_24h',
                'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'market_cap',
                'fully_diluted_market_cap']

import datetime
import math

def abs(x):
    if x < 0:
        return -x
    return x

def simple_scam_check(data_source):
    token_name = data_source['name']
    token_address = data_source['token_address']

    data = data_source['cmc_metadata']
    score = 20

    if data['num_market_pair'] > 20:
        score += 5
    if data['circulating_supply'] < data['total_supply']:
        score += 5
    if int(data['date_added'][:4]) < 2021:
        score += 5
        if int(data['date_added'][:4]) < 2019:
            score += 10
            if int(data['date_added'][:4]) < 2015:
                score += 10
    if abs(float(data['percent_change_1h'])) < 4:
        score += 5
        if abs(float(data['percent_change_1h'])) < 1.5:
            score += 5
            if abs(float(data['percent_change_1h'])) < 0.2:
                score += 5
    elif abs(float(data['percent_change_1h'])) < 10:
        score -= 10
    else:
        score -= 20
    if abs(data['percent_change_24h']) < 5:
        score += 5
        if abs(data['percent_change_24h']) < 2.5:
            score += 5
            if abs(data['percent_change_24h']) < 1.5:
                score += 5
    elif abs(data['percent_change_24h']) < 15:
        score -= 10
    else:
        score -= 20

    if abs(data['percent_change_7d']) < 15:
        score += 5
        if abs(data['percent_change_7d']) < 9.5:
            score += 5
            if abs(data['percent_change_7d']) < 5.5:
                score += 5
    elif abs(data['percent_change_7d']) < 30:
        score -= 10
    else:
        score -= 20
    
    if data['market_cap'] > 100000:
        score += 5
        if data['market_cap'] > 10000000:
            score += 5
            if data['market_cap'] > 100000000:
                score += 5
                if data['market_cap'] > 1000000000:
                    score += 5
    elif data['market_cap'] < 100000:
        score -= 10
    if data['market_cap'] < 10000:
        score -= 10

    if data['fully_diluted_market_cap'] > 100000:
        score += 5
        if data['fully_diluted_market_cap'] > 10000000:
            score += 5
            if data['fully_diluted_market_cap'] > 100000000:
                score += 5
                if data['fully_diluted_market_cap'] > 1000000000:
                    score += 5
    elif data['fully_diluted_market_cap'] < 100000:
        score -= 10
    if data['fully_diluted_market_cap'] < 10000:
        score -= 10
    

    if data['usd_price'] > 0.1:
        score += 5
    
    ### give score
    if score > 60:
        return {
            'name': token_name,
            'address': token_address,
            'score': score,
            'category': 'an OK token',
            'possibility': 0,
            'status': 'OK'
        }
    else:
        return {
            'name': token_name,
            'address': token_address,
            'score': score,
            'category': 'simple scam token',
            'possibility': 85,
            'status': 'SCAM'
        }
