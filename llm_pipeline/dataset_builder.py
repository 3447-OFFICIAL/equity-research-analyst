import json
import os

def export_db_to_jsonl(output_path: str = "dataset.jsonl"):
    """
    Extracts reports and citations from the Postgres DB and structures them
    into a ChatML/Alpaca format JSONL file for LLM fine-tuning.
    """
    # Pseudo-code for DB extraction
    # session = SessionLocal()
    # reports = session.query(Report).filter(Report.is_golden == True).all()
    
    reports = [
        {
            "instruction": "Analyze the financial health of AAPL based on the following XBRL and earnings data.",
            "input": "Revenue: 383B, Net Income: 96B, SEC Filings context...",
            "output": "Based on the robust 15% net margin and strong FCF generation, AAPL remains highly solvent. Risks include China supply chain exposure..."
        }
    ]
    
    with open(output_path, "w") as f:
        for r in reports:
            # ChatML format
            formatted = {
                "messages": [
                    {"role": "system", "content": "You are an elite quantitative equity research analyst."},
                    {"role": "user", "content": f"{r['instruction']}\n{r['input']}"},
                    {"role": "assistant", "content": r['output']}
                ]
            }
            f.write(json.dumps(formatted) + "\n")
            
    print(f"Generated {len(reports)} golden training samples at {output_path}")

if __name__ == "__main__":
    export_db_to_jsonl()
