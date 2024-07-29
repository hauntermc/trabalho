# utils/pdf_utils.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

def generate_form_pdf(filename, ordem_servico, material_info):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    cabecalho = ParagraphStyle(name='centered', alignment=1, fontSize=12)
    elements.append(Paragraph("Poder Judiciário do Estado do Rio de Janeiro - PJERJ", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Departamento de Segurança Eletrônica e de Telecomunicacoes - DETEL", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Serviço de Controle de Materiais", cabecalho))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("REQUISIÇÃO DE MATERIAIS", styles['Title']))
    elements.append(Spacer(1, 12))

    # Horizontal Table Data
    data = [
        ['Número da OS:', ordem_servico, 'Data de retirada:', material_info.get('data_retirada', '____________________')],
        ['Nome do técnico:', material_info.get('nome_tecnico', '____________________'), 'Matrícula:', material_info.get('matricula_tecnico', '____________________')],
        ['Resp. Controle:', material_info.get('responsavel_controle', '____________________'), 'Matrícula:', material_info.get('matricula_responsavel', '____________________')],
        ['Local de destino:', material_info.get('local_destino', '____________________'), 'Nº Patrimônio:', material_info.get('numero_patrimonio', '____________________')]
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
        ['Téc. Responsável:', material_info.get('tecnico_responsavel', '____________________'), 'Matrícula:', material_info.get('matricula_tecnico_responsavel', '____________________')],
        ['Supervisor Técnico:', material_info.get('supervisor_tecnico', '____________________'), 'Matrícula:', material_info.get('matricula_supervisor', '____________________')],
        ['Controle de Materiais:', material_info.get('controle_materiais', '____________________'), 'Matrícula:', material_info.get('matricula_controle', '____________________')],
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
