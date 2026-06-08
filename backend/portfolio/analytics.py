import numpy as np

def calculate_sharpe_ratio(returns: list[float], risk_free_rate: float = 0.04) -> float:
    """
    Calculates the annualized Sharpe Ratio given a list of daily/monthly returns.
    """
    if not returns:
        return 0.0
    
    returns_array = np.array(returns)
    mean_return = np.mean(returns_array)
    std_dev = np.std(returns_array)
    
    if std_dev == 0:
        return 0.0
        
    # Assuming daily returns, annualized factor is 252
    annualized_return = mean_return * 252
    annualized_volatility = std_dev * np.sqrt(252)
    
    sharpe = (annualized_return - risk_free_rate) / annualized_volatility
    return float(sharpe)

def calculate_correlation_matrix(price_histories: dict[str, list[float]]) -> dict:
    """
    Calculates a Pearson correlation matrix for multiple assets.
    """
    tickers = list(price_histories.keys())
    data_matrix = np.array([price_histories[t] for t in tickers])
    
    corr_matrix = np.corrcoef(data_matrix)
    
    # Format into a nested dictionary
    result = {}
    for i, t1 in enumerate(tickers):
        result[t1] = {}
        for j, t2 in enumerate(tickers):
            result[t1][t2] = float(corr_matrix[i, j])
            
    return result
