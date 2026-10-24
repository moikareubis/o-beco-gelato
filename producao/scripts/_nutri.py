# -*- coding: utf-8 -*-
"""Dossiê técnico para a nutricionista — O Beco Gelato."""
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

TINTA = colors.HexColor("#1F1A17"); MARROM = colors.HexColor("#6B4A2F")
AREIA = colors.HexColor("#F3EDE5"); LINHA  = colors.HexColor("#D8CEC1")
VERM  = colors.HexColor("#A3321E"); VERDE  = colors.HexColor("#2E6B4F")
CINZA = colors.HexColor("#6E655C"); CREME  = colors.HexColor("#FBF6EF")
AZUL  = colors.HexColor("#2B4C7E")

def g(v, d=1):
    return f"{v:,.{d}f}".replace(",", "~").replace(".", ",").replace("~", ".")

S = lambda n, **k: ParagraphStyle(n, **k)
H1  = S("H1", fontName="Helvetica-Bold", fontSize=18, leading=21, textColor=MARROM, spaceAfter=2)
SUB = S("SUB", fontName="Helvetica", fontSize=9.4, leading=13, textColor=CINZA, spaceAfter=10)
H2  = S("H2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=MARROM, spaceBefore=11, spaceAfter=5)
H3  = S("H3", fontName="Helvetica-Bold", fontSize=10, leading=13, textColor=TINTA, spaceBefore=8, spaceAfter=3)
P   = S("P", fontName="Helvetica", fontSize=9, leading=12.8, textColor=TINTA, spaceAfter=4)
PS  = S("PS", fontName="Helvetica", fontSize=7.8, leading=10.6, textColor=CINZA, spaceAfter=3)
AV  = S("AV", fontName="Helvetica-Bold", fontSize=8.7, leading=12, textColor=VERM)
OKS = S("OK", fontName="Helvetica-Bold", fontSize=8.7, leading=12, textColor=VERDE)
IN  = S("IN", fontName="Helvetica", fontSize=8.7, leading=12, textColor=AZUL)

story = []

def tab(dados, larg, cab=True, dest=None, fonte=8.2):
    t = Table(dados, colWidths=larg, repeatRows=1 if cab else 0)
    st = [("FONT",(0,0),(-1,-1),"Helvetica",fonte), ("TEXTCOLOR",(0,0),(-1,-1),TINTA),
          ("VALIGN",(0,0),(-1,-1),"MIDDLE"), ("TOPPADDING",(0,0),(-1,-1),3),
          ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),4.5),
          ("RIGHTPADDING",(0,0),(-1,-1),4.5), ("LINEBELOW",(0,0),(-1,-2),0.4,LINHA)]
    if cab:
        st += [("FONT",(0,0),(-1,0),"Helvetica-Bold",fonte), ("BACKGROUND",(0,0),(-1,0),AREIA),
               ("TEXTCOLOR",(0,0),(-1,0),MARROM), ("LINEBELOW",(0,0),(-1,0),0.8,MARROM)]
    for r in (dest or []):
        st += [("BACKGROUND",(0,r),(-1,r),CREME), ("FONT",(0,r),(-1,r),"Helvetica-Bold",fonte)]
    t.setStyle(TableStyle(st)); return t

def caixa(txt, est, fundo, borda, larg=172*mm):
    t = Table([[Paragraph(txt, est)]], colWidths=[larg])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),fundo),("BOX",(0,0),(-1,-1),0.9,borda),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    return t
aviso = lambda t: caixa(t, AV, colors.HexColor("#FBEDEA"), VERM)
okbox = lambda t: caixa(t, OKS, colors.HexColor("#EDF5F0"), VERDE)
info  = lambda t: caixa(t, IN, colors.HexColor("#EEF2F8"), AZUL)
nota  = lambda t: caixa(t, P, AREIA, LINHA)

# ══════════════════════ ABERTURA
story.append(Paragraph("Dossiê técnico dos gelatos", H1))
story.append(Paragraph(f"O Beco Gelato LTDA &nbsp;·&nbsp; CNPJ 66.901.942/0001-59 "
    f"&nbsp;·&nbsp; {HOJE.strftime('%d/%m/%Y')}<br/>"
    "Documento preparado para elaboração das fichas técnicas e tabelas nutricionais.", SUB))

story.append(Paragraph("O que tem neste documento", H2))
story.append(Paragraph(
  "São 7 sabores em 3 linhas comerciais, todos <b>zero lactose</b>. Cinco sustentam a alegação "
  "<b>sem adição de açúcares</b>; dois não — ver o aviso na página seguinte. "
  "Para cada sabor estão a formulação completa em g por kg de calda e em percentual, os "
  "parâmetros físico-químicos, a composição do pote pronto e a lista de ingredientes já "
  "ordenada por peso decrescente conforme a RDC 727/2022. Ao final há a ficha nutricional "
  "de cada um dos 25 insumos e uma lista do que precisa ser confirmado junto aos fabricantes.", P))

story.append(Paragraph("Como ler os números", H2))
leitura = [["Termo", "O que significa aqui"],
 ["Açúcares totais", "No sentido da ANVISA: NÃO inclui polióis. O cadastro interno guarda um segundo valor, 'técnico', que soma açúcar e poliol para calcular doçura e ponto de congelamento — esse não serve para rótulo."],
 ["Calda", "A mistura líquida pasteurizada, antes de ir à batedeira. Todas as formulações estão por 1 kg de calda."],
 ["Gelato", "A calda depois de batida, com ar incorporado. É o que vai no pote."],
 ["Pote", f"{POTE} g de produto. Com pote e tampa (10 g), 150 g na balança."],
 ["Overrun", "O ar incorporado na batedeira. O cadastro usa 21%; medições de 16/10 deram de 14% a 47% conforme o sabor."],
 ["Sólidos totais", "Tudo que não é água."],
 ["POD / PAC", "Poder de doçura e poder anticongelante, na escala em que sacarose = 100. Uso interno de formulação."],
 ["Janela de consumo", "Faixa de temperatura em que o gelato serve no ponto."]]
story.append(tab(leitura, [30*mm, 142*mm], fonte=8.2))

story.append(Spacer(1,6))
story.append(aviso("ORIGEM DOS DADOS — leia antes de usar.<br/><br/>"
  "Os valores nutricionais dos insumos vêm do cadastro interno do Beco, montado ao longo do "
  "tempo a partir de fichas técnicas de fabricante e de rótulos. <b>Eles não substituem o "
  "rótulo físico da embalagem.</b> Antes de fechar qualquer tabela, recomendo conferir cada "
  "insumo contra a embalagem em uso, porque fornecedor e formulação mudam sem aviso. "
  "A seção final lista os insumos em que essa conferência é mais crítica."))
story.append(PageBreak())

# ══════════════════════ VISÃO GERAL
story.append(Paragraph("Os 7 sabores", H1))
story.append(Paragraph("Visão geral das três linhas.", SUB))
vg = [["Sabor", "Linha", "Família de formulação", "Gelato/pote", "Finalização", "Alergênicos"]]
for s in D["sabores"]:
    fin = "—"
    if s["fin"]:
        f0 = s["fin"][0]
        fin = f"{g(f0['noPote'],1)} g " + ("(por cima)" if f0["adicional"] else "(dentro)")
    vg.append([s["nome"], s["linha"], s["familiaForm"], g(s["gelatoPote"],0)+" g",
               fin, ", ".join(s["alerg"]) or "—"])
story.append(tab(vg, [36*mm, 18*mm, 30*mm, 22*mm, 28*mm, 38*mm], fonte=7.9))

story.append(Paragraph("Composição do pote pronto — comparativo", H2))
cp = [["Sabor", "kcal", "Açúc.", "Polióis", "Aç.ad.", "Prot.", "Gord.", "G.sat.", "Fibra", "Sódio"]]
for s in D["sabores"]:
    p = s["pote"]; k = s["massaPote"]/100
    cp.append([s["nome"][:18], g(p["kcal"]*k,0), g(p["acu"]*k,1), g(p["poliois"]*k,1),
               g(p["acucarAdd"]*k,2), g(p["prot"]*k,1), g(p["gord"]*k,1),
               g(p["gordSat"]*k,1), g(p["fibra"]*k,1), g(p["sodio"]*k,0)])
story.append(tab(cp, [34*mm]+[15.3*mm]*9, fonte=7.6))
story.append(Spacer(1,3))
story.append(Paragraph("Valores por pote. No Alfajor o pote são 150 g (135 g de gelato + 15 g de "
  "biscoito por cima); nos demais, 140 g. <b>Açúc.</b> são os açúcares totais no sentido da "
  "ANVISA — não incluem os polióis, que vão na coluna seguinte.", PS))
story.append(Spacer(1,5))
story.append(info("<b>Carboidratos totais não estão calculados aqui, de propósito.</b> A convenção "
  "de incluir ou não fibras e polióis na linha de carboidratos é decisão da profissional "
  "responsável, e eu preferi entregar cada componente medido separadamente a arbitrar isso. "
  "Os sólidos totais de cada sabor estão na ficha individual e fecham a conta."))

story.append(Paragraph("Alegações pretendidas", H2))
al = [["Sabor", "Selos que a formulação sustenta", "Advertência frontal (lupa)"]]
for s in D["sabores"]:
    al.append([s["nome"], " · ".join(s["selos"]["ok"]) or "—",
               " · ".join(s["selos"]["lupa"]) or "nenhuma"])
story.append(tab(al, [40*mm, 92*mm, 40*mm], fonte=8))
story.append(Spacer(1,5))
story.append(info("Os selos acima saem do cálculo da formulação, não de análise laboratorial. "
  "A decisão final sobre o que pode ser declarado é da nutricionista responsável."))
story.append(Spacer(1,6))
story.append(aviso("DOIS SABORES NÃO SUSTENTAM 'SEM ADIÇÃO DE AÇÚCARES'.<br/><br/>"
  "<b>Sorbet Morango</b> — 0,470 g/100 g. Vêm da Pasta Fragola MEC3, usada a 10 g/kg, "
  "que é 47% açúcar adicionado.<br/>"
  "<b>Alfajor</b> — 0,010 g/100 g. Vêm do biscoito de alfajor, que declara 0,1 g/100 g "
  "de açúcares adicionados no próprio rótulo.<br/><br/>"
  "Os outros cinco estão em zero absoluto. A alegação exige zero, sem tolerância, então "
  "esses dois precisam de decisão: trocar o insumo, ou vender sem o selo. "
  "O Gabriel já está ciente dos dois casos."))
story.append(PageBreak())

# ══════════════════════ INGREDIENTES COMPOSTOS
story.append(Paragraph("Ingredientes feitos na casa", H1))
story.append(Paragraph("Dois insumos das formulações não são comprados prontos — são preparados "
    "no Beco. Para a rotulagem eles precisam aparecer desdobrados nos componentes.", SUB))

story.append(Paragraph("Mix Oficial", H2))
story.append(Paragraph("Usado no Pistache e na Torta de Limão. Mistura seca de polióis e fibras "
    "que substitui o açúcar.", P))
tot = sum(v for _,v in D["mixOficial"])
mx = [["Componente", "Partes", "% do mix", "Por 1 kg de mix"]]
for n,v in D["mixOficial"]:
    mx.append([n, g(v,0), g(v/tot*100,2)+"%", g(v/tot*1000,1)+" g"])
mx.append(["TOTAL", g(tot,0), "100,00%", "1.000,0 g"])
story.append(tab(mx, [54*mm, 22*mm, 26*mm, 34*mm], dest=[len(mx)-1], fonte=8.3))

story.append(Paragraph("Base proteica", H2))
story.append(Paragraph("Usada no Café Proteico e no Brigadeiro Proteico. Uma única calda "
    "pasteurizada, saborizada no final.", P))
bs = [["Ingrediente", "Por 1 kg de base", "% da base"]]
for n,v in D["baseProteica"]:
    bs.append([n, g(v,1)+" g", g(v/1000*100,2)+"%"])
bs.append(["TOTAL", "1.000,0 g", "100,00%"])
story.append(tab(bs, [92*mm, 32*mm, 26*mm], dest=[len(bs)-1], fonte=8.3))
story.append(Spacer(1,4))
sb = [["Sabor", "Base por kg de calda", "Saborizante", "Proteína final"],
      ["Café Proteico", "943,2 g", "Pasta Café Selecta 56,8 g", "9,99%"],
      ["Brigadeiro Proteico", "961,5 g", "Cacau 22/24 38,5 g", "10,13%"]]
story.append(tab(sb, [40*mm, 36*mm, 56*mm, 28*mm], fonte=8.3))
story.append(PageBreak())

# ══════════════════════ FICHAS POR SABOR
for s in D["sabores"]:
    story.append(Paragraph(s["nome"], H1))
    sub = f"linha {s['linha']} &nbsp;·&nbsp; família de formulação: {s['familiaForm']}"
    sub += f" &nbsp;·&nbsp; pote de {g(s['massaPote'],0)} g"
    story.append(Paragraph(sub, SUB))

    story.append(Paragraph("Formulação — por 1 kg de calda", H2))
    rc = [["Ingrediente", "Nome de rótulo", "g/kg", "% calda", "g no pote"]]
    for l in s["linhas"]:
        rc.append([l["nome"][:38], l["rotulo"][:30], g(l["gkg"],1), g(l["pct"],2)+"%",
                   g(l["noPote"],2)])
    rc.append(["CALDA", "", g(s["soma"],1), "100,00%", g(s["gelatoPote"],1)])
    for l in s["fin"]:
        rc.append([l["nome"][:38]+" ·fin", l["rotulo"][:30], g(l["gkg"],1), "—",
                   g(l["noPote"],2)])
    story.append(tab(rc, [56*mm, 48*mm, 20*mm, 22*mm, 24*mm],
                     dest=[len(s["linhas"])+1], fonte=7.7))

    m = s["met"]
    story.append(Paragraph("Parâmetros físico-químicos da calda", H2))
    pr = [["Sólidos totais","Água","Gordura","Proteína","Açúcares","Sólidos dif.","POD","PAC"],
          [g(m["sol"],2)+"%", g(m["agua"],2)+"%", g(m["gord"],2)+"%", g(m["prot"],2)+"%",
           g(m["acu"],2)+"%", g(m["solDif"],2)+"%", g(m["pod"],0), g(m["pac"],0)]]
    story.append(tab(pr, [21.5*mm]*8, fonte=7.9))
    story.append(Spacer(1,3))
    story.append(Paragraph(f"Janela de consumo {g(s['janela'][0])} a {g(s['janela'][1])} °C · "
        f"{g(s['frozen'],0)}% de água congelada a −8 °C · overrun de cadastro {D['overrun']}%", PS))

    story.append(Paragraph(f"Pote pronto — {g(s['massaPote'],0)} g", H2))
    p = s["pote"]; k = s["massaPote"]/100
    pp = [["Componente", "por 100 g", f"por pote ({g(s['massaPote'],0)} g)"],
          ["Valor energético", g(p["kcal"],0)+" kcal", g(p["kcal"]*k,0)+" kcal"],
          ["Açúcares totais (rótulo)", g(p["acu"],2)+" g", g(p["acu"]*k,1)+" g"],
          ["   dos quais adicionados", g(p["acucarAdd"],2)+" g", g(p["acucarAdd"]*k,2)+" g"],
          ["Polióis", g(p["poliois"],2)+" g", g(p["poliois"]*k,1)+" g"],
          ["Fibras alimentares", g(p["fibra"],2)+" g", g(p["fibra"]*k,1)+" g"],
          ["Proteínas", g(p["prot"],2)+" g", g(p["prot"]*k,1)+" g"],
          ["Gorduras totais", g(p["gord"],2)+" g", g(p["gord"]*k,1)+" g"],
          ["   das quais saturadas", g(p["gordSat"],2)+" g", g(p["gordSat"]*k,1)+" g"],
          ["   das quais trans", g(p["gordTrans"],2)+" g", g(p["gordTrans"]*k,2)+" g"],
          ["Sódio", g(p["sodio"],1)+" mg", g(p["sodio"]*k,0)+" mg"],
          ["Sólidos totais", g(p["solidosTotais"],2)+" g", g(p["solidosTotais"]*k,1)+" g"]]
    story.append(tab(pp, [56*mm, 30*mm, 34*mm], dest=[11], fonte=8.2))
    story.append(Spacer(1,3))
    story.append(Paragraph("Açúcares totais no sentido da ANVISA: não incluem os polióis, "
        "que aparecem na linha própria. O valor técnico usado internamente para calcular "
        f"POD e PAC é {g(p['acuTecnico'],2)} g/100 g e soma os dois.", PS))

    story.append(Paragraph("Lista de ingredientes — RDC 727/2022", H2))
    txt = ", ".join(f"{i['r']}" for i in s["rdc727"])
    story.append(Paragraph(f"<b>Ingredientes:</b> {txt}.", P))
    pcts = " · ".join(f"{i['r']} {g(i['pct'],1)}%" for i in s["rdc727"])
    story.append(Paragraph(f"Percentuais no produto pronto: {pcts}", PS))
    if s["alerg"]:
        story.append(Paragraph(f"<b>ALÉRGICOS: CONTÉM {', '.join(s['alerg'])}.</b>", P))
    if s["temPoliol"]:
        story.append(Paragraph("Contém polióis — avaliar a advertência de efeito laxativo "
            "conforme a dose por porção.", PS))
    story.append(PageBreak())

# ══════════════════════ FICHA DOS INSUMOS
story.append(Paragraph("Ficha nutricional dos insumos", H1))
story.append(Paragraph(f"Os {len(D['ingredientes'])} insumos usados nas 7 formulações. "
    "Valores por 100 g do insumo, como estão no cadastro interno.", SUB))
fi = [["Insumo", "kcal", "Açúc.", "Gord.", "G.sat.", "Prot.", "Fibra", "Sól.tot.", "Sódio", "Aç.ad."]]
for i in D["ingredientes"]:
    n = i["nut"]
    fi.append([i["nome"][:34], g(n["kcal"],0), g(n["acucares"],1), g(n["gordura"],1),
               g(n["gordSat"],1), g(n["proteinas"],1), g(n["fibra"],1),
               g(n["solidosTotais"],1), g(n["sodio"],0), g(i["acucarAdd"],1)])
story.append(tab(fi, [52*mm]+[13.3*mm]*9, fonte=7))
story.append(Spacer(1,4))
story.append(Paragraph("<b>Aç.ad.</b> = percentual do insumo que conta como açúcar adicionado "
  "para efeito do selo. <b>Sól.tot.</b> = sólidos totais, o que não é água. Sódio em mg/100 g.", PS))

story.append(Paragraph("Nomes de rótulo e alergênicos", H2))
nr = [["Insumo", "Como aparece no rótulo", "Alergênicos"]]
for i in D["ingredientes"]:
    nr.append([i["nome"][:36], i["rotulo"][:40], ", ".join(i["alerg"]) or "—"])
story.append(tab(nr, [58*mm, 72*mm, 42*mm], fonte=7.4))
story.append(PageBreak())

# ══════════════════════ PENDÊNCIAS
story.append(Paragraph("O que precisa ser confirmado", H1))
story.append(Paragraph("Pontos em que o cadastro interno não basta e a informação precisa vir "
    "do fabricante ou da embalagem física.", SUB))

comp = [i for i in D["ingredientes"] if i["composto"]]
if comp:
    story.append(Paragraph("Ingredientes compostos", H2))
    story.append(Paragraph("Estes insumos são eles próprios formulações. Para a lista de "
        "ingredientes do rótulo final eles precisam ser desdobrados nos seus componentes, "
        "e essa lista só o fabricante tem.", P))
    for i in comp:
        story.append(Paragraph(f"<b>{i['nome']}</b>", H3))
        story.append(Paragraph(i["obs"] or "Pedir a lista de ingredientes ao fabricante.", P))

story.append(Paragraph("Demais pendências", H2))
pd = [["Insumo", "O que falta"]]
for p_ in D["pendencias"]:
    if any("COMPOSTO" in x for x in p_["itens"]) and len(p_["itens"])==1:
        continue
    pd.append([p_["ingrediente"][:40], "; ".join(x for x in p_["itens"] if "COMPOSTO" not in x)])
if len(pd) > 1:
    story.append(tab(pd, [62*mm, 110*mm], fonte=8))
else:
    story.append(Paragraph("Nenhuma além dos compostos acima.", P))

story.append(Paragraph("Pontos de atenção para a rotulagem", H2))
at = [["Tema", "Situação"],
 ["Peso líquido", f"Hoje o pote declara {POTE} g de gelato. Há uma troca de embalagem prevista para 180 ml declarando 150 g — confirmar com o Gabriel qual embalagem vale para as fichas."],
 ["Overrun", "O ar incorporado varia de 14% a 47% entre os sabores (medição de 16/10). Isso não muda a composição por 100 g, mas muda o peso do pote cheio. O protocolo de medição por lote começou agora."],
 ["Biscoito do Alfajor", "Contém glúten e declara 'pode conter amêndoas, amendoim, avelã, castanha-de-caju, derivados de trigo, pistache, soja'. Ele vai por cima do gelato e é 10% do peso do pote — entra integralmente na tabela e nos alérgicos."],
 ["Polióis", "Maltitol, eritritol e polidextrose estão em quase todas as formulações. Avaliar a advertência de efeito laxativo conforme a dose por porção declarada."],
 ["Zero lactose", "Toda a linha usa leite e derivados zero lactose. Confirmar os laudos dos fornecedores de leite, creme e leite em pó."],
 ["Vida de prateleira", "Ainda não definida. Não há estudo de estabilidade."]]
story.append(tab(at, [34*mm, 138*mm], fonte=8))

story.append(Spacer(1,6))
story.append(okbox("Qualquer dúvida sobre as formulações, o Gabriel tem o sistema de "
  "balanceamento com todos os cálculos abertos e pode gerar os números em qualquer "
  "recorte que for útil — por 100 g, por porção, por lote de produção."))

def rodape(canvas, doc):
    canvas.saveState(); canvas.setFont("Helvetica", 7.2); canvas.setFillColor(CINZA)
    canvas.drawString(19*mm, 12*mm, f"O Beco Gelato · dossiê técnico · {HOJE.strftime('%d/%m/%Y')}")
    canvas.drawRightString(A4[0]-19*mm, 12*mm, str(doc.page))
    canvas.setStrokeColor(LINHA); canvas.setLineWidth(0.4)
    canvas.line(19*mm, 15.5*mm, A4[0]-19*mm, 15.5*mm); canvas.restoreState()

doc = BaseDocTemplate("O Beco Gelato - Dossie Tecnico Nutricionista.pdf", pagesize=A4,
    leftMargin=19*mm, rightMargin=19*mm, topMargin=17*mm, bottomMargin=20*mm,
    title="O Beco Gelato — dossiê técnico para nutricionista", author="O Beco Gelato")
doc.addPageTemplates([PageTemplate(id="pg",
    frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")],
    onPage=rodape)])
doc.build(story)
print("dossiê gerado")
