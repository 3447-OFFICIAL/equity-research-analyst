from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"

@dataclass
class RiskScore:
    health_score: int
    risk_level: RiskLevel
    bankruptcy_probability: float

def calculate_altman_z(
    working_capital: float,
    retained_earnings: float,
    ebit: float,
    market_value_equity: float,
    total_assets: float,
    total_liabilities: float
) -> float:
    """
    Altman Z-Score formula for public manufacturing companies.
    Z = 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5
    """
    if total_assets == 0:
        return 0.0

    x1 = working_capital / total_assets
    x2 = retained_earnings / total_assets
    x3 = ebit / total_assets
    x4 = market_value_equity / total_liabilities if total_liabilities > 0 else 10.0
    # x5 = Sales / Total Assets (omitting for standard 4-factor non-manufacturing or simplifying)
    # Using 4 factor emerging market model: Z = 6.56X1 + 3.26X2 + 6.72X3 + 1.05X4
    
    z_score = (6.56 * x1) + (3.26 * x2) + (6.72 * x3) + (1.05 * x4)
    return z_score

def calculate_piotroski_f(
    roa: float,
    cfo: float,
    delta_roa: float,
    accrual: float, # CFO - Net Income
    delta_leverage: float,
    delta_liquidity: float,
    equity_issued: float,
    delta_margin: float,
    delta_turnover: float
) -> int:
    """
    Piotroski F-Score (0-9)
    """
    score = 0
    if roa > 0: score += 1
    if cfo > 0: score += 1
    if delta_roa > 0: score += 1
    if accrual > 0: score += 1 # CFO > Net Income
    if delta_leverage < 0: score += 1 # Decreasing debt
    if delta_liquidity > 0: score += 1 # Increasing current ratio
    if equity_issued <= 0: score += 1 # No dilution
    if delta_margin > 0: score += 1
    if delta_turnover > 0: score += 1
    
    return score

def generate_risk_report(z_score: float, f_score: int) -> RiskScore:
    # Normalize Z-score (Safe > 2.6, Distress < 1.1)
    # F-score (Safe > 7, Distress < 3)
    
    health = min(100, max(0, int((z_score / 3.0) * 50 + (f_score / 9.0) * 50)))
    
    if z_score < 1.1 or f_score <= 3:
        level = RiskLevel.HIGH
        prob = 0.25
    elif z_score > 2.6 and f_score >= 7:
        level = RiskLevel.LOW
        prob = 0.01
    else:
        level = RiskLevel.MODERATE
        prob = 0.05
        
    return RiskScore(health_score=health, risk_level=level, bankruptcy_probability=prob)
