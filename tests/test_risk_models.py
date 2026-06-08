import pytest
from backend.quant.risk_models import calculate_altman_z, calculate_piotroski_f, generate_risk_report, RiskLevel

def test_altman_z():
    z = calculate_altman_z(
        working_capital=100,
        retained_earnings=50,
        ebit=20,
        market_value_equity=500,
        total_assets=1000,
        total_liabilities=500
    )
    assert z > 0
    assert round(z, 2) == 2.0

def test_piotroski_f():
    f = calculate_piotroski_f(
        roa=0.05, cfo=100, delta_roa=0.01, accrual=10, 
        delta_leverage=-0.05, delta_liquidity=0.1, 
        equity_issued=0, delta_margin=0.02, delta_turnover=0.05
    )
    assert f == 9 # Perfect score

def test_risk_report():
    report = generate_risk_report(z_score=3.0, f_score=8)
    assert report.risk_level == RiskLevel.LOW
    assert report.health_score > 80
    assert report.bankruptcy_probability == 0.01
