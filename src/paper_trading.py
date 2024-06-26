import alpaca_trade_api as tradeapi
import yaml

class AlpacaPaperTrader:
    def __init__(self, config_path='config/config.yaml'):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        self.api_key = config['alpaca']['api_key']
        self.api_secret = config['alpaca']['api_secret']
        self.base_url = config['alpaca']['base_url']
        
        self.api = tradeapi.REST(self.api_key, self.api_secret, self.base_url, api_version='v2')
        self.account = self.api.get_account()
        
    def get_account_info(self):
        return self.account

    def place_order(self, symbol, qty, side, order_type='market', time_in_force='gtc'):
        order = self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
        return order

    def get_order_status(self, order_id):
        return self.api.get_order(order_id)