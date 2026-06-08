import pytest
from backend.quant.monte_carlo import run_monte_carlo_dcf

def test_monte_carlo_dcf_vectorization():
    result = run_monte_carlo_dcf(
        current_fcf=100.0,
        shares_outstanding=10.0,
        current_price=120.0,
        simulations=10000
    )
    
    assert result.bear_case > 0
    assert result.bull_case > result.base_case
    assert result.base_case > result.bear_case
    assert 0.0 <= result.undervalued_probability <= 1.0

def test_monte_carlo_dcf_bounds():
    # If price is astronomically high, undervalued prob should be 0
    result = run_monte_carlo_dcf(
        current_fcf=100.0,
        shares_outstanding=10.0,
        current_price=999999.0,
        simulations=1000
    )
    assert result.undervalued_probability == 0.0
