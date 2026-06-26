from fpdf import FPDF
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Meeting Intelligence AI Report', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def safe_text(text):
    return str(text).encode('latin-1', 'replace').decode('latin-1') if text else ""

def write_inline_formatting(pdf, text):
    """
    Parses a string for **bold** text and writes it using pdf.write to allow mixed formatting on a line.
    """
    parts = text.split('**')
    for idx, part in enumerate(parts):
        # Even indices are normal text, odd indices are bold text
        if idx % 2 == 1:
            pdf.set_font('Arial', 'B', 10)
        else:
            pdf.set_font('Arial', '', 10)
        pdf.write(5, safe_text(part))

def write_markdown_to_pdf(pdf, text):
    if not text:
        return
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
            
        # Check if line is a header
        if line.startswith('#'):
            level = 0
            while level < len(line) and line[level] == '#':
                level += 1
            header_text = line[level:].strip()
            
            # Header font (Bold, size 11)
            pdf.set_font('Arial', 'B', 11)
            pdf.multi_cell(0, 7, safe_text(header_text))
            pdf.set_font('Arial', '', 10)
            pdf.ln(2)
            
        # Check if line is a bullet point
        elif line.startswith('- ') or line.startswith('* '):
            bullet_text = line[2:].strip()
            
            # Write a bullet prefix
            pdf.set_font('Arial', '', 10)
            pdf.write(5, safe_text("  o   "))
            
            # Parse inline bold in the bullet text
            write_inline_formatting(pdf, bullet_text)
            pdf.ln(5)
            
        # Check if numbered list
        elif any(line.startswith(f"{i}. ") for i in range(1, 100)):
            # Find the dot to separate number
            dot_idx = line.find('. ')
            num = line[:dot_idx]
            item_text = line[dot_idx+2:].strip()
            
            pdf.set_font('Arial', '', 10)
            pdf.write(5, safe_text(f"  {num}.   "))
            write_inline_formatting(pdf, item_text)
            pdf.ln(5)
            
        else:
            # Regular line, parse inline bold
            write_inline_formatting(pdf, line)
            pdf.ln(5)

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
            pdf.ln(2)
            write_markdown_to_pdf(pdf, content)
            pdf.ln(5)
            
    # Action Items
    action_items = data.get('action_items', [])
    if action_items:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, "Action Items", 0, 1)
        pdf.ln(2)
        for idx, ai in enumerate(action_items):
            if isinstance(ai, dict):
                text = f"{idx+1}. **{ai.get('task')}** (Owner: {ai.get('owner')}, Due: {ai.get('due_date')})"
            else:
                text = f"{idx+1}. {ai}"
            write_markdown_to_pdf(pdf, text)
    
    pdf.output(output_path)
    return output_path
