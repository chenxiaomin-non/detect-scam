
def evaluate(data: dict):
    """
    data = {
        'token_address': token_address,
        'name': name,
        'symbol': symbol,
        'cmc_metadata': {
            'id', 'name', 'symbol', 'slug', 'cmc_rank', 'is_active',
            'first_historical_data', 'last_historical_data', 'platform', 'token_address'
        },
        'moralis': {
            'chain', 'name', 'symbol', 'decimal',
            'create_at', 'price', 'numberTransaction'
        },
        'bsc'/'eth': {
            
            ----------
            'total_supply', 'circulating_supply', 'liquidity',
                    'contract_owner', 'contract_abi'
        }
    }
    """

    try:
        if data.get('moralis').get('name') == '' or data.get('moralis').get('name') is None:
            return {
                'status': 'ERROR',
                'developer_message': 'ERROR - name is empty'
            }
        
        if data.get('moralis').get('symbol') == '' or data.get('moralis').get('symbol') is None:
            return {
                'status': 'ERROR',
                'developer_message': 'ERROR - symbol is empty'
            }
    except Exception:
        pass
    
    try:
        if data.get('price') == 0 or data.get('price') is None:
            return {
                'status': 'ERROR',
                'developer_message': 'ERROR - price is empty'
            }
        
        if data.get('moralis').get('numberTransaction') < 500:
            return {
                'status': 'ERROR',
                'developer_message': 'ERROR - numberTransaction is less than 500'
            }


        if data.get('token_address') is None or data.get('name') is None or data.get('symbol') is None:
            return {
                'status': 'NOT OK',
                'developer_message': 'token_address, name, symbol is required'
            }

        if data.get('cmc_metadata') is None:
            return {
                'status': 'NOT OK',
                'developer_message': 'cmc_metadata is required'
            }
        
        if data.get('cmc_metadata').get('cmc_rank') < 200 and data['cmc_rank'].get('is_active') == '1':
            return {
                'status': 'OK',
                'developer_message': 'reputation of token is good'
            }
        
        if data['cmc_rank']['is_active'] == '0':
            return {
                'status': 'NOT OK',
                'developer_message': 'token is not active'
            }
    except Exception:
        return {
            'status': 'NOT OK',
            'developer_message': 'token_address, name, symbol is required'
        }

    if data.get('bsc', None) is not None:
        result = validator_for_bsc(data)
        return result

    if data.get('eth', None) is not None:
        result = validator_for_eth(data)
        return result

    return {
        'status': 'OK',
        'developer_message': 'OK - pass the validator check'
    }


def validator_for_bsc(data):
    if data.get('bsc').get('liquidity') < 1000:
        return {
            'status': 'NOT OK',
            'developer_message': 'liquidity is less than 1000'
        }
    if data.get('bsc').get('contract_abi') is None or data.get('bsc').get('contract_abi') == '':
        return {
            'status': 'NOT OK',
            'developer_message': 'contract_abi is required'
        }
    return {
        'status': 'OK',
        'developer_message': 'OK - pass the validator check'
    }

def validator_for_eth(data):
    if data.get('eth').get('liquidity') < 1000:
        return {
            'status': 'NOT OK',
            'developer_message': 'liquidity is less than 1000'
        }
    if data.get('eth').get('contract_abi') is None or data.get('eth').get('contract_abi') == '':
        return {
            'status': 'NOT OK',
            'developer_message': 'contract_abi is required'
        }

    return {
        'status': 'OK',
        'developer_message': 'OK - pass the validator check'
    }
