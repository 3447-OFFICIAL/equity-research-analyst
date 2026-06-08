from typing import Dict, List, Any
from datetime import datetime

# Mapping US-GAAP XBRL tags to our standardized metric names
GAAP_MAPPING = {
    "Revenues": "Revenue",
    "RevenueFromContractWithCustomerExcludingAssessedTax": "Revenue",
    "GrossProfit": "Gross Profit",
    "OperatingIncomeLoss": "Operating Income",
    "NetIncomeLoss": "Net Income",
    "CashAndCashEquivalentsAtCarryingValue": "Cash",
    "Assets": "Total Assets",
    "Liabilities": "Total Liabilities",
    "StockholdersEquity": "Total Equity",
    "NetCashProvidedByUsedInOperatingActivities": "Operating Cash Flow",
    "PaymentsToAcquirePropertyPlantAndEquipment": "CapEx",
    "CommonStockSharesOutstanding": "Shares Outstanding"
}

class XbrlParser:
    """
    Parses raw SEC CompanyFacts JSON and normalizes it into a standard time-series format.
    """
    @staticmethod
    def parse_facts(raw_json: Dict[str, Any]) -> List[Dict[str, Any]]:
        facts = raw_json.get("facts", {}).get("us-gaap", {})
        normalized_data = []
        
        for gaap_tag, mapped_metric in GAAP_MAPPING.items():
            if gaap_tag in facts:
                # We only want USD values (or shares)
                units = facts[gaap_tag].get("units", {})
                unit_key = "USD" if "USD" in units else "shares"
                
                if unit_key in units:
                    for data_point in units[unit_key]:
                        # Only take 10-K (annual) data for simplicity in this pipeline, or Q3/Q4
                        if data_point.get("form") in ["10-K", "10-Q"]:
                            normalized_data.append({
                                "metric_name": mapped_metric,
                                "value": data_point.get("val"),
                                "period_end_date": datetime.strptime(data_point.get("end"), "%Y-%m-%d").date(),
                                "filing_type": data_point.get("form"),
                                "source": "SEC_XBRL"
                            })
                            
        return normalized_data
