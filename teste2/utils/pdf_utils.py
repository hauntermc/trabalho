from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def generate_form_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    cabecalho = ParagraphStyle(name='centered', alignment=1, fontSize=12)
    elements.append(Paragraph("Poder Judiciário do Estado do Rio de Janeiro - PJERJ", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Departamento de Segurança Eletrônica e de Telecomonicações - DETEL", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Serviço de Controle de Materiais", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("REQUISIÇÃO DE MATERIAIS", styles['Title']))
    elements.append(Spacer(1, 12))

    # Horizontal Table Data
    data = [
        ['Número da OS:', '____________________', 'Data de retirada:', '____________________'],
        ['Nome do técnico:', '____________________', 'Matrícula:', '____________________'],
        ['Resp. Controle:', '____________________', 'Matrícula:', '____________________'],
        ['Local de destino:', '____________________', 'Nº Patrimônio:', '____________________']
    ]

    table = Table(data, colWidths=[120, 150, 120, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add space before signatures
    elements.append(Spacer(1, 350))

    # Signatures Section
    signatures_data = [
        ['Téc. Responsável:', '____________________', 'Matrícula:', '____________________'],
        ['Supervisor Técnico:', '____________________', 'Matrícula:', '____________________'],
        ['Controle de Materiais:', '____________________', 'Matrícula:', '____________________'],
    ]

    signatures_table = Table(signatures_data, colWidths=[140, 150, 80, 150])
    signatures_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(signatures_table)

    # Build PDF
    doc.build(elements)
