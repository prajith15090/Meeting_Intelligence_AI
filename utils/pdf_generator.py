from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Sales Meeting Intelligence Report', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def safe_text(text):
    return str(text).encode('latin-1', 'replace').decode('latin-1') if text else ""

def create_pdf_report(data: dict, output_path: str):
    pdf = PDFReport()
    pdf.add_page()
    
    # Title and Date
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Customer: {safe_text(data.get('customer_name'))}", 0, 1)
    pdf.cell(0, 10, f"Date: {safe_text(data.get('meeting_date'))}", 0, 1)
    pdf.cell(0, 10, f"Sentiment: {safe_text(data.get('sentiment'))}", 0, 1)
    pdf.cell(0, 10, f"Deal Stage: {safe_text(data.get('deal_stage'))} (Prob: {safe_text(data.get('probability'))})", 0, 1)
    pdf.ln(5)
    
    sections = [
        ("Minutes of Meeting (MoM)", data.get('mom')),
        ("Summary", data.get('summary')),
        ("Customer Insights", data.get('customer_insights')),
    ]
    
    for title, content in sections:
        if content:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, title, 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 8, safe_text(content))
            pdf.ln(5)
            
    # Action Items
    action_items = data.get('action_items', [])
    if action_items:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Action Items", 0, 1)
        pdf.set_font('Arial', '', 11)
        for idx, ai in enumerate(action_items):
            if isinstance(ai, dict):
                text = f"{idx+1}. {ai.get('task')} (Owner: {ai.get('owner')}, Due: {ai.get('due_date')})"
            else:
                text = f"{idx+1}. {ai}"
            pdf.multi_cell(0, 8, safe_text(text))
    
    pdf.output(output_path)
    return output_path
