import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
# In production with wkhtmltopdf installed via Docker:
# import pdfkit

def generate_pdf_report(data: dict, output_path: str):
    """
    Renders the Jinja2 HTML template with agent data and compiles to PDF.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("institutional.html")
    
    # Inject live data
    html_out = template.render(
        ticker=data.get("ticker", "UNKNOWN"),
        date=datetime.now().strftime("%Y-%m-%d"),
        recommendation=data.get("final_recommendation", "HOLD"),
        confidence=data.get("confidence", 0.0),
        thesis=data.get("thesis", "No thesis provided."),
        bull_case=data.get("bull_case_citations", []),
        bear_case=data.get("bear_case_citations", []),
        val_bear=data.get("val_bear", 0),
        val_base=data.get("val_base", 0),
        val_bull=data.get("val_bull", 0),
        prob_undervalued=data.get("prob_undervalued", 0)
    )
    
    # For demonstration without pdfkit system dependency breaking, we save as HTML.
    # In full production docker: pdfkit.from_string(html_out, output_path)
    html_path = output_path.replace(".pdf", ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_out)
        
    print(f"Report generated successfully at {html_path}")
    return html_path
