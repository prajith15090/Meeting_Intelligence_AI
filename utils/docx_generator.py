from docx import Document
import os

def create_docx_report(data: dict, output_path: str):
    doc = Document()
    
    doc.add_heading('Meeting Intelligence AI Report', 0)
    
    doc.add_paragraph(f"Customer: {data.get('customer_name', '')}")
    doc.add_paragraph(f"Date: {data.get('meeting_date', '')}")
    doc.add_paragraph(f"Sentiment: {data.get('sentiment', '')}")
    doc.add_paragraph(f"Deal Stage: {data.get('deal_stage', '')} (Probability: {data.get('probability', '')})")
    
    sections = [
        ("Minutes of Meeting (MoM)", data.get('mom')),
        ("Summary", data.get('summary')),
        ("Customer Insights", data.get('customer_insights')),
    ]
    
    for title, content in sections:
        if content:
            doc.add_heading(title, level=1)
            doc.add_paragraph(content)
            
    action_items = data.get('action_items', [])
    if action_items:
        doc.add_heading('Action Items', level=1)
        for ai in action_items:
            if isinstance(ai, dict):
                doc.add_paragraph(
                    f"Task: {ai.get('task')}\nOwner: {ai.get('owner')}\nDue: {ai.get('due_date')}",
                    style='List Bullet'
                )
            else:
                doc.add_paragraph(str(ai), style='List Bullet')
            
    doc.save(output_path)
    return output_path
