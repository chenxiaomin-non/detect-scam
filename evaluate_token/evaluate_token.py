import sys
sys.path.append('./')
import database.total_token as total_token
import evaluate_token.group_1 as validator
import get_info_interface as get_info

def get_latest_result(token_address: str = None, name: str = None, symbol: str = None):
    data = None
    if token_address != None:
        data = total_token.find('address', token_address)
    if name != None:
        data = total_token.find('name', name)
    if symbol != None:
        data = total_token.find('symbol', symbol)
    print('data: ',data)
    total_token.clear_result()
    return data

def jsonify_latest_result(result: tuple):
    if result == None: 
        return None
    if result[3] == None:
        return None
    return_value = {
        'token_name': result[0],
        'token_address': result[1],
        'symbol': result[2],
        'chain': result[3],
        'category': result[4][0],
        'possibility': int(result[4][1:]),
        'timestamp': result[5]
    }
    if return_value['category'] == '0':
        return_value['category'] = 'no value token'
    elif return_value['category'] == '1':
        return_value['category'] = 'simple scam token'
    elif return_value['category'] == '2':
        return_value['category'] = 'complex scam token'
    else:
        return_value['category'] = 'an OK token'
    return return_value

def save_result(result, data):
    # if result['category'] == 'simple scam token':
    #     result['category'] = '1'
    # elif result['category'] == 'complex scam token':
    #     result['category'] = '2'
    # elif result['category'] == 'no value token':
    #     result['category'] = '0'
    # else:
    #     result['category'] = '3'
    if result['status'] == 'OK':
        result['category'] = '3'
        result['possibility'] = 0
    else:
        result['category'] = '0'
        result['possibility'] = 100
    if data.get('moralis') is None:
        chain = None
    else:
        chain = data['moralis'].get('chain')
    total_token.insert_processed_data({
        "token_name": data.get('name', None),
        "token_address": data.get('token_address', None),
        "symbol": data.get('symbol', None),
        "chain": chain,
        "lastest_result": result['category'] +str(result['possibility'])
    })


def evaluate_token(token_address: str = None, name: str = None, symbol: str = None):
    data = get_latest_result(token_address, name, symbol)
    print('data: ',data)
    data = jsonify_latest_result(data)

    if data == None:
        data = get_info.get_info_for_validator(token_address)
        """
        data = {
            'token_address': token_address,
            'name': name,
            'symbol': symbol,
            'cmc_metadata': {},
            'moralis': {},
            'bsc'/'eth': {}
        }
        """
        # stage 01: check no value token
        result = validator.evaluate(data)
        print('result: ', result)
        if result['status'] != 'OK':
            save_result(result, data)
            return {
                'token_name': data['name'],
                'token_address': data['token_address'],
                'symbol': data['symbol'],
                'category': 'no value token',
                'possibility': 100
            }
        
        else:
            save_result(result, data)
            return {
                'token_name': data['name'],
                'token_address': data['token_address'],
                'symbol': data['symbol'],
                'category': 'an OK token',
                'possibility': 0
            }
        # stage 02: check simple scam token

        """
        there will be some code here in future
        """

        # stage 03: check complex scam token
        
        """
        there will be some code here in future
        """

        #4 save to database
        



    else:
        return data, 'OK'
    

