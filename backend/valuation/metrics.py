def calculate_revenue_growth(current_revenue: float, prior_revenue: float) -> float:
    if prior_revenue == 0:
        raise ValueError("prior_revenue must be non-zero")
    return (current_revenue - prior_revenue) / prior_revenue


def calculate_eps_growth(current_eps: float, prior_eps: float) -> float:
    if prior_eps == 0:
        raise ValueError("prior_eps must be non-zero")
    return (current_eps - prior_eps) / abs(prior_eps)


def calculate_margin(numerator: float, revenue: float) -> float:
    if revenue == 0:
        raise ValueError("revenue must be non-zero")
    return numerator / revenue


def calculate_debt_to_equity(total_debt: float, total_equity: float) -> float:
    if total_equity == 0:
        raise ValueError("total_equity must be non-zero")
    return total_debt / total_equity
