import pandas as pd
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Criar um dataframe vazio para armazenar as tarefas
df = pd.DataFrame(columns=["Tarefa", "Prioridade", "Tempo estimado"])

# Adicionar tarefas ao dataframe
df.loc[len(df)] = ["Tarefa 1", 1, 240] # Tarefa 1, Prioridade 2, 60 minutos estimados
df.loc[len(df)] = ["Tarefa 2", 2, 60] # Tarefa 2, Prioridade 1, 30 minutos estimados
df.loc[len(df)] = ["Tarefa 3", 3, 45] # Tarefa 3, Prioridade 3, 45 minutos estimados

# Ordenar o dataframe por prioridade (ordem crescente) e tempo estimado (ordem decrescente)
df = df.sort_values(by=["Prioridade", "Tempo estimado"], ascending=[True, False])

# Dividir as tarefas em 7 dias da semana, das 8h às 22h, com intervalos de 45 minutos entre cada tarefa e no máximo 6 horas de tarefas por dia
agenda = {}
horario_atual = datetime.time(hour=8)
minutos_disponiveis = (22 - horario_atual.hour) * 60
for dia in range(7):
    agenda[dia] = []
    minutos_disponiveis = (22 - horario_atual.hour) * 60
    minutos_de_trabalho = 0
    while minutos_disponiveis > 0 and len(df) > 0 and minutos_de_trabalho < 360:
        tarefa = df.iloc[0]
        if tarefa["Tempo estimado"] <= minutos_disponiveis:
            horario_inicio = horario_atual.strftime("%H:%M")
            horario_atual_datetime = datetime.datetime.combine(datetime.date.today(), horario_atual)
            horario_atual_datetime += datetime.timedelta(minutes=int(tarefa["Tempo estimado"]))
            horario_atual = horario_atual_datetime.time()
            horario_fim = horario_atual.strftime("%H:%M")
            agenda[dia].append((tarefa["Tarefa"], horario_inicio, horario_fim))
            minutos_disponiveis -= tarefa["Tempo estimado"]
            minutos_de_trabalho += tarefa["Tempo estimado"] + 45
            df = df.drop(df.index[0])
        else:
            break
    horario_atual = datetime.time(hour=8)  # Reiniciar o horário para o próximo dia

dados = []
for dia in range(7):
    dados.append([f"Agenda para o dia {dia+1}", "", ""])
    dados.append(["Tarefa", "Início", "Fim"])
    for tarefa in agenda[dia]:
        dados.append([tarefa[0], tarefa[1], tarefa[2]])
    dados.append(["", "", ""])

style = TableStyle([
    ("BACKGROUND", (0, 0), (2, 0), colors.gray),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, 0), 14),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("BACKGROUND", (0, 0), (-1, 0), colors.darkslategray),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
    ("TOPPADDING", (0, 0), (-1, 0), 12),
    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
    ("FONTSIZE", (0, 1), (-1, -1), 12),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
])

table = Table(dados, style=style, colWidths=[4 * cm, 3 * cm, 3 * cm])

doc = SimpleDocTemplate("agenda.pdf")
elements = []
elements.append(table)

doc.build(elements)

print("Agenda salva em arquivo PDF com sucesso!")
