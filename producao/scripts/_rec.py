# -*- coding: utf-8 -*-
"""Receituário de produção — O Beco Gelato. Documento da funcionária."""
import json, datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak)

D = json.load(open("_dossie.json", encoding="utf-8"))
HOJE = datetime.date(2026, 10, 21)
POTE = D["pote"]

TINTA  = colors.HexColor("#1F1A17"); MARROM = colors.HexColor("#6B4A2F")
AREIA  = colors.HexColor("#F3EDE5"); LINHA  = colors.HexColor("#D8CEC1")
VERM   = colors.HexColor("#A3321E"); VERDE  = colors.HexColor("#2E6B4F")
CINZA  = colors.HexColor("#6E655C"); CREME  = colors.HexColor("#FBF6EF")

def g(v, d=1):
    return f"{v:,.{d}f}".replace(",", "~").replace(".", ",").replace("~", ".")

S = lambda n, **k: ParagraphStyle(n, **k)
H1  = S("H1", fontName="Helvetica-Bold", fontSize=19, leading=22, textColor=MARROM, spaceAfter=2)
SUB = S("SUB", fontName="Helvetica", fontSize=9.6, leading=13, textColor=CINZA, spaceAfter=10)
H2  = S("H2", fontName="Helvetica-Bold", fontSize=12.5, leading=15, textColor=MARROM, spaceBefore=11, spaceAfter=5)
H3  = S("H3", fontName="Helvetica-Bold", fontSize=10.3, leading=13, textColor=TINTA, spaceBefore=8, spaceAfter=3)
P   = S("P", fontName="Helvetica", fontSize=9.2, leading=13, textColor=TINTA, spaceAfter=4)
PS  = S("PS", fontName="Helvetica", fontSize=8, leading=11, textColor=CINZA, spaceAfter=3)
NUN = S("NUN", fontName="Helvetica-Bold", fontSize=8.8, leading=12.3, textColor=VERM)
OKS = S("OK", fontName="Helvetica-Bold", fontSize=8.8, leading=12.3, textColor=VERDE)
CEL = S("CEL", fontName="Helvetica", fontSize=8.4, leading=10.8, textColor=TINTA)

story = []

def tab(dados, larg, cab=True, dest=None, fonte=8.5):
    t = Table(dados, colWidths=larg, repeatRows=1 if cab else 0)
    st = [("FONT",(0,0),(-1,-1),"Helvetica",fonte), ("TEXTCOLOR",(0,0),(-1,-1),TINTA),
          ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),3.2),
          ("BOTTOMPADDING",(0,0),(-1,-1),3.2), ("LEFTPADDING",(0,0),(-1,-1),5),
          ("RIGHTPADDING",(0,0),(-1,-1),5), ("LINEBELOW",(0,0),(-1,-2),0.4,LINHA)]
    if cab:
        st += [("FONT",(0,0),(-1,0),"Helvetica-Bold",fonte), ("BACKGROUND",(0,0),(-1,0),AREIA),
               ("TEXTCOLOR",(0,0),(-1,0),MARROM), ("LINEBELOW",(0,0),(-1,0),0.8,MARROM)]
    for r in (dest or []):
        st += [("BACKGROUND",(0,r),(-1,r),CREME), ("FONT",(0,r),(-1,r),"Helvetica-Bold",fonte)]
    t.setStyle(TableStyle(st)); return t

def caixa(txt, est, fundo, borda):
    t = Table([[Paragraph(txt, est)]], colWidths=[172*mm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),fundo),("BOX",(0,0),(-1,-1),0.9,borda),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return t
nunca = lambda t: caixa("NUNCA &nbsp;&nbsp;"+t, NUN, colors.HexColor("#FBEDEA"), VERM)
okbox = lambda t: caixa(t, OKS, colors.HexColor("#EDF5F0"), VERDE)
nota  = lambda t: caixa(t, P, AREIA, LINHA)

# ══════════════════════ CAPA
story.append(Paragraph("Receituário de produção", H1))
story.append(Paragraph(f"O Beco Gelato &nbsp;·&nbsp; revisão de {HOJE.strftime('%d/%m/%Y')} "
    f"&nbsp;·&nbsp; pote de {POTE} g &nbsp;·&nbsp; 7 sabores", SUB))
story.append(Paragraph("Esta revisão substitui todas as anteriores", H2))
story.append(Paragraph("Mudou bastante coisa desde o receituário anterior. O que está diferente:", P))
mud = [["O que mudou", "Antes", "Agora"],
 ["Gramatura do pote", "135 g (estimativa)", "140 g — 35 potes pesados em 16/10"],
 ["Preço de venda", "R$ 20,90 / 18,90", "R$ 20,50 / 18,70 — preço de rua"],
 ["Café e Brigadeiro", "duas receitas separadas", "UMA calda proteica, saborizada no fim"],
 ["Liga na calda proteica", "6 g/kg", "3 g/kg"],
 ["Mescla do Café", "por cima do pote", "ripada DENTRO dos 140 g"],
 ["Biscoito do Alfajor", "—", "POR CIMA do pote cheio, soma 15 g"],
 ["Alfajor", "não existia", "sabor de linha, 125 g… agora 135 g + biscoito"]]
story.append(tab(mud, [44*mm, 50*mm, 78*mm], fonte=8.3))

story.append(Paragraph("Os 7 sabores", H2))
tb = [["Sabor", "Linha", "Gelato/pote", "Finalização", "Sól.", "Prot.", "R$/kg"]]
for s in D["sabores"]:
    fin = g(s["massaPote"]-s["gelatoPote"],1)+" g" if s["fin"] else "—"
    if s["fin"] and not s["fin"][0]["adicional"]:
        fin = g(s["fin"][0]["noPote"],1)+" g (dentro)"
    elif s["fin"]:
        fin = g(s["fin"][0]["noPote"],1)+" g (por cima)"
    tb.append([s["nome"], s["linha"], g(s["gelatoPote"],0)+" g", fin,
               g(s["met"]["sol"],1)+"%", g(s["met"]["prot"],1)+"%",
               "R$ "+g(s["met"]["custoKg"],2)])
story.append(tab(tb, [40*mm, 20*mm, 24*mm, 32*mm, 17*mm, 17*mm, 22*mm], fonte=8.3))
story.append(Spacer(1,5))
story.append(okbox(f"Todo pote fecha em <b>{POTE} g de produto</b> — 150 g na balança com pote e tampa. "
  "A única exceção é o Alfajor: 135 g de gelato, o biscoito vai por cima e ele fecha em 150 g "
  "de produto, 160 g na balança."))
story.append(PageBreak())

# ══════════════════════ REGRAS
story.append(Paragraph("As regras que não se quebram", H1))
story.append(Paragraph("Dez linhas. Se alguma delas for quebrada, o lote sai diferente e "
                       "não dá para consertar depois.", SUB))
regras = [
 ("1", "Pesar tudo antes de ligar a máquina.", "Balança tarada a cada item."),
 ("2", "O pó entra no líquido em movimento, chovendo devagar.", "Pó no líquido parado vira bola seca por dentro que não dissolve mais."),
 ("3", "Gordura e pasta só depois do pó dissolvido.", "Gordura antes do pó envolve o grão e ele para de hidratar."),
 ("4", "Pasteurizar a 82–85 °C mexendo o fundo.", "Sem mexer, queima — e gosto de queimado não sai."),
 ("5", "Resfriar rápido de 85 para menos de 6 °C.", "Entre 60 e 20 °C bactéria cresce. Essa faixa se atravessa correndo."),
 ("6", "Maturar no mínimo 6 horas a 4 °C. Melhor 12.", "Calda morna na batedeira dá cristal grande."),
 ("7", "O que é ácido entra frio, depois da maturação.", "Pasteurizar ácido junto com leite talha a base."),
 ("8", "Encher o cilindro até a carga da máquina.", "Cilindro meio vazio incorpora o dobro de ar."),
 ("9", "Envasar na balança, nunca no olho.", "Medimos 5 potes de cada sabor: a Torta variou 23,5 g dentro do mesmo lote."),
 ("10","Preencher a folha de lote antes de sair.", "Sem registro não dá para achar o erro depois."),
]
rr = [["#", "A regra", "Por quê"]] + [[n, a, b] for n,a,b in regras]
story.append(tab(rr, [9*mm, 73*mm, 90*mm], fonte=8.3))
story.append(Spacer(1,6))
story.append(nunca("mudar uma receita sem avisar o Gabriel. Se faltar um ingrediente, "
                   "o lote espera — não se troca por parecido."))
story.append(PageBreak())

# ══════════════════════ CALDA ÚNICA
story.append(Paragraph("Calda única proteica", H1))
story.append(Paragraph("Café e Brigadeiro saem da mesma base. Validada em 13/10: 3 kg de base "
    "rendendo 1,5 kg de cada sabor. As proteínas dos dois divergem 0,14 ponto.", SUB))
story.append(Paragraph("Base proteica — por 1 kg de base", H2))
bs = [["Ingrediente", "Por kg"]] + [[n, g(v,1)+" g"] for n,v in D["baseProteica"]]
bs.append(["TOTAL", "1.000,0 g"])
story.append(tab(bs, [120*mm, 30*mm], dest=[len(bs)-1], fonte=8.4))
story.append(Paragraph("Saborização", H2))
sb = [["Sabor", "Base por kg de calda", "Saborizante", "Proteína"],
      ["Café Proteico", "943,2 g", "Pasta Café Selecta &nbsp; 56,8 g", "9,99%"],
      ["Brigadeiro", "961,5 g", "Cacau 22/24 &nbsp; 38,5 g", "10,13%"]]
story.append(tab(sb, [36*mm, 42*mm, 58*mm, 24*mm], fonte=8.4))
story.append(Spacer(1,5))
story.append(nunca("tentar corrigir a doçura na saborização. A estévia dessa base está em "
  "0,6 g por kg — numa porção de saborização isso é 1 parte em milhares e não dispersa. "
  "A doçura se define na base, antes da pasteurização."))
story.append(Spacer(1,5))
story.append(okbox("Se for fazer os dois no mesmo dia, bata a base para os dois de uma vez "
  "e só depois separe para saborizar. É esse o ganho da calda única."))
story.append(PageBreak())

# ══════════════════════ MIX OFICIAL
story.append(Paragraph("Mix Oficial", H1))
story.append(Paragraph("Feito na casa. Entra no Pistache e na Torta de Limão.", SUB))
tot = sum(v for _,v in D["mixOficial"])
mx = [["Componente", "Partes", "% do mix", "Para 1 kg de mix"]]
for n,v in D["mixOficial"]:
    mx.append([n, g(v,0), g(v/tot*100,1)+"%", g(v/tot*1000,1)+" g"])
mx.append(["TOTAL", g(tot,0), "100,0%", "1.000,0 g"])
story.append(tab(mx, [58*mm, 24*mm, 26*mm, 38*mm], dest=[len(mx)-1], fonte=8.5))
story.append(Spacer(1,6))
story.append(nunca("fazer o mix sem maltitol. Ele é 22,4% da fórmula — sem maltitol não existe mix, "
  "e sem mix não saem o Pistache nem a Torta de Limão."))
story.append(Spacer(1,5))
story.append(nota("<b>Como pesar:</b> maltitol, eritritol e polidextrose na balança comum. "
  "A <b>estévia é 3 partes em 999</b> — pesa na balança de precisão e mistura o lote seco "
  "com a mão por 30 segundos antes de guardar. Estévia mal distribuída faz metade do lote "
  "sair sem doçura e a outra metade amarga."))
story.append(PageBreak())

# ══════════════════════ FICHAS
for s in D["sabores"]:
    story.append(Paragraph(s["nome"], H1))
    sub = f"linha {s['linha']} &nbsp;·&nbsp; {g(s['gelatoPote'],0)} g de gelato por pote"
    if s["fin"]:
        f0 = s["fin"][0]
        sub += (f" + {g(f0['noPote'],1)} g de {f0['rotulo']} "
                + ("<b>por cima</b>" if f0["adicional"] else "<b>ripado dentro</b>"))
    sub += f" &nbsp;·&nbsp; venda R$ {g(s['preco'],2)}"
    story.append(Paragraph(sub, SUB))

    rc = [["Ingrediente", "Por kg de calda", "% da calda"]]
    for l in s["linhas"]:
        rc.append([l["nome"][:50], g(l["gkg"],1)+" g", g(l["pct"],2)+"%"])
    rc.append(["CALDA", g(s["soma"],1)+" g", "100,00%"])
    for l in s["fin"]:
        rc.append([l["nome"][:50]+"  · finalização", g(l["gkg"],1)+" g", "—"])
    story.append(tab(rc, [104*mm, 32*mm, 26*mm], dest=[len(s["linhas"])+1], fonte=8.3))

    m = s["met"]
    story.append(Paragraph("Parâmetros", H2))
    pr = [["Sólidos","Água","Gordura","Proteína","Açúcares","POD","PAC"],
          [g(m["sol"],2)+"%", g(m["agua"],2)+"%", g(m["gord"],2)+"%", g(m["prot"],2)+"%",
           g(m["acu"],2)+"%", g(m["pod"],0), g(m["pac"],0)]]
    story.append(tab(pr, [23*mm]*7, fonte=8.6))
    story.append(Spacer(1,4))
    story.append(Paragraph(f"<b>Janela de consumo {g(s['janela'][0])} a {g(s['janela'][1])} °C.</b> "
        f"A −8 °C está {g(s['frozen'],0)}% congelado. Servido fora dessa faixa fica duro ou mole — "
        "é temperatura, não receita.", P))

    lotes = [["Potes", "Calda a pesar"]]
    for n in (10, 30, 50):
        lotes.append([str(n), g(s["gelatoPote"]*n*D["fator"],0)+" g"])
    story.append(Paragraph("Lotes prontos", H2))
    story.append(tab(lotes, [26*mm, 36*mm], fonte=8.5))
    story.append(PageBreak())

# ══════════════════════ FOLHA DE LOTE
story.append(Paragraph("Folha de registro de lote", H1))
story.append(Paragraph("Uma por batida. Preencher antes de sair da cozinha.", SUB))
campos = [["Sabor","","Data",""],["Responsável","","Nº do ciclo",""],
 ["Calda pesada (g)","","Hora de início",""],
 ["Temp. máx. pasteurização","","Fim da pasteurização",""],
 ["Entrou na maturação","","Saiu da maturação",""],
 ["Horas de maturação","","Temp. da geladeira (°C)",""],
 ["Entrou na batedeira","","Hora da extração",""],
 ["Temp. de extração (°C)","","Carga do cilindro (kg)",""],
 ["POTES CHEIOS","","Peso de 1 pote cheio (g)",""],
 ["Sobra descartada (g)","","Observações",""]]
t = Table(campos, colWidths=[50*mm,36*mm,50*mm,36*mm], rowHeights=[9.6*mm]*len(campos))
t.setStyle(TableStyle([("FONT",(0,0),(-1,-1),"Helvetica",8.3),
  ("FONT",(0,0),(0,-1),"Helvetica-Bold",8.3),("FONT",(2,0),(2,-1),"Helvetica-Bold",8.3),
  ("TEXTCOLOR",(0,0),(-1,-1),TINTA),("GRID",(0,0),(-1,-1),0.5,LINHA),
  ("BACKGROUND",(0,0),(0,-1),AREIA),("BACKGROUND",(2,0),(2,-1),AREIA),
  ("BACKGROUND",(0,8),(-1,8),CREME),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
  ("LEFTPADDING",(0,0),(-1,-1),5)]))
story.append(t)
story.append(Paragraph("Medição de overrun — 2 minutos, em toda batida", H2))
story.append(Paragraph("1. Pesa um copo vazio. &nbsp; tara = ______ g<br/>"
  "2. Enche o copo <b>rasando</b> com a calda líquida e pesa. &nbsp; calda = ______ g<br/>"
  "3. Lava, enche o <b>mesmo copo rasando</b> com o gelato recém-extraído. &nbsp; gelato = ______ g<br/>"
  "4. <b>Overrun = (calda − gelato) ÷ gelato × 100 = ______ %</b>", P))
story.append(Spacer(1,4))
story.append(nota("Medido em 16/10, a partir de 5 potes de cada sabor: Café 14% · Torta 14% · "
  "Manga 19% · Brigadeiro 21% · Alfajor 22% · Pistache 24% · Sorbet Morango 47%. "
  "O cadastro usa 21% para todos — este protocolo existe para trocar a estimativa pelo número real."))

def rodape(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica", 7.2); canvas.setFillColor(CINZA)
    canvas.drawString(19*mm, 12*mm, f"O Beco Gelato · receituário de produção · revisão {HOJE.strftime('%d/%m/%Y')}")
    canvas.drawRightString(A4[0]-19*mm, 12*mm, str(doc.page))
    canvas.setStrokeColor(LINHA); canvas.setLineWidth(0.4)
    canvas.line(19*mm, 15.5*mm, A4[0]-19*mm, 15.5*mm); canvas.restoreState()

doc = BaseDocTemplate("O Beco Gelato - Receituario de Producao.pdf", pagesize=A4,
    leftMargin=19*mm, rightMargin=19*mm, topMargin=17*mm, bottomMargin=20*mm,
    title="O Beco Gelato — receituário de produção", author="O Beco Gelato")
doc.addPageTemplates([PageTemplate(id="pg",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")],
    onPage=rodape)])
doc.build(story)
print("receituário gerado")
