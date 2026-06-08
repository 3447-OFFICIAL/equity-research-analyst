import numpy as np
from pydantic import BaseModel

class MonteCarloResult(BaseModel):
    bear_case: float
    base_case: float
    bull_case: float
    undervalued_probability: float

def run_monte_carlo_dcf(
    current_fcf: float,
    shares_outstanding: float,
    current_price: float,
    years: int = 5,
    simulations: int = 10000,
    growth_mean: float = 0.08,
    growth_std: float = 0.03,
    wacc_mean: float = 0.10,
    wacc_std: float = 0.015,
    terminal_growth_mean: float = 0.02,
    terminal_growth_std: float = 0.005
) -> MonteCarloResult:
    """
    Runs 10,000 Monte Carlo simulations using NumPy vectorization.
    Calculates 10th, 50th, and 90th percentile intrinsic values per share.
    """
    
    # Generate random normal distributions for each variable
    np.random.seed(42) # For reproducibility in testing
    
    growth_rates = np.random.normal(growth_mean, growth_std, simulations)
    waccs = np.random.normal(wacc_mean, wacc_std, simulations)
    terminal_growths = np.random.normal(terminal_growth_mean, terminal_growth_std, simulations)
    
    # Ensure realistic bounds
    waccs = np.clip(waccs, 0.04, 0.25)
    terminal_growths = np.clip(terminal_growths, 0.0, np.minimum(waccs - 0.01, 0.05)) # Terminal growth must be < WACC
    
    # Array to hold Present Value for each simulation
    total_pv = np.zeros(simulations)
    
    # Calculate NPV of free cash flows for 'years'
    for year in range(1, years + 1):
        fcf_year = current_fcf * ((1 + growth_rates) ** year)
        discount_factor = (1 + waccs) ** year
        total_pv += (fcf_year / discount_factor)
        
    # Calculate Terminal Value PV
    final_fcf = current_fcf * ((1 + growth_rates) ** years)
    terminal_value = (final_fcf * (1 + terminal_growths)) / (waccs - terminal_growths)
    terminal_value_pv = terminal_value / ((1 + waccs) ** years)
    
    total_enterprise_value = total_pv + terminal_value_pv
    intrinsic_value_per_share = total_enterprise_value / shares_outstanding
    
    # Determine percentiles
    bear = np.percentile(intrinsic_value_per_share, 10)
    base = np.percentile(intrinsic_value_per_share, 50)
    bull = np.percentile(intrinsic_value_per_share, 90)
    
    # Calculate probability that intrinsic value > current price
    undervalued_prob = np.sum(intrinsic_value_per_share > current_price) / simulations
    
    return MonteCarloResult(
        bear_case=float(bear),
        base_case=float(base),
        bull_case=float(bull),
        undervalued_probability=float(undervalued_prob)
    )
