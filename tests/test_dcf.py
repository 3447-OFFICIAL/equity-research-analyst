import pytest
from backend.valuation.dcf import calculate_dcf, DCFResult

def test_calculate_dcf_basic():
    result = calculate_dcf(
        starting_fcf=10.0,
        growth_rate=0.05,
        discount_rate=0.10,
        terminal_growth_rate=0.02,
        periods=5,
        market_price=100.0
    )
    
    assert isinstance(result, DCFResult)
    assert result.intrinsic_value > 0
    assert result.terminal_value > 0
    assert result.margin_of_safety is not None

def test_calculate_dcf_invalid_discount_rate():
    with pytest.raises(ValueError, match="discount_rate must be greater than terminal_growth_rate"):
        calculate_dcf(
            starting_fcf=10.0,
            growth_rate=0.05,
            discount_rate=0.02,
            terminal_growth_rate=0.02,
            periods=5
        )
