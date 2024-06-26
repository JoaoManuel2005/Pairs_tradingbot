from statsmodels.tsa.stattools import coint

def perform_cointegration_test(stock1, stock2):
    score, p_value, _ = coint(stock1['Close'], stock2['Close'])
    return p_value