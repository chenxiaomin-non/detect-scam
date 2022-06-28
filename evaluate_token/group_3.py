import json
import math
import sys

sys.path.append('./')

import get_info_api.moralis as moralis
from decimal import *
getcontext().prec = 35

def complicated_scam_check(data: dict):
    token_address = data['token_address']
    chain = data['moralis']['chain']
    # get the result from moralis
    try:
        trans = moralis.get_transactions_erc20(token_address, chain=chain, limit=1000)
    except:
        return {
            'status': 'ERR',
            'developer_message': 'Token address is not valid for moralis check'
        }
    
    # code process the data
    value = []
    for tran in trans:
        print(json.dumps(tran, indent=4))
        try:
            print(tran.get('value'))
            temp = int(tran['value'])
            value.append(temp)
        except:
            pass
    
    sum = int(0)
    for i in range(len(value)):
        sum += value[i]
    
    average = Decimal(sum / len(value))

    sigma = Decimal(0)
    for i in range(len(value)):
        sigma += (value[i] - average) ** 2
    sigma = Decimal(math.sqrt(sigma / len(value)))

    print(sigma, average, sigma/average)
    if sigma/average > 15.0:
        return {
            'status': 'OK',
            'possibility': 0,
            'developer_message': 'Token is not a scam token'
        }
    elif sigma/average > 10.0:
        return {
            'status': 'OK',
            'possibility': 25,
            'developer_message': 'Token is not a scam token'
        }
    elif sigma/average > 5.0:
        return {
            'status': 'ERR',
            'possibility': 55,
            'developer_message': 'Token is a scam token'
        }
    elif sigma/average > 2.4:
        return {
            'status': 'WARN',
            'possibility': 80,
            'developer_message': 'Token is a scam token'
        }
    else:
        return {
            'status': 'ERR',
            'possibility': 100,
            'developer_message': 'Token is a scam token'
        }
    
complicated_scam_check({
    'token_address': '0x0d8775f648430679a709e98d2b0cb6250d2887ef',
    'moralis': {
        'chain': 'eth',
    }
})
    