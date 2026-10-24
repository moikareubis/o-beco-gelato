# -*- coding: utf-8 -*-
"""Planilha para a nutricionista. Fórmulas vivas — ela muda um insumo e tudo recalcula."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = json.load(open("_dossie.json", encoding="utf-8"))
POTE = D["pote"]

MARROM = "6B4A2F"; AREIA = "F3EDE5"; CREME = "FBF6EF"; CINZA = "6E655C"
NEG = Font(bold=True, color="1F1A17", size=10)
CAB = Font(bold=True, color="FFFFFF", size=10)
TIT = Font(bold=True, color=MARROM, size=13)
PEQ = Font(size=8, color=CINZA, italic=True)
FCAB = PatternFill("solid", fgColor=MARROM)
FDEST = PatternFill("solid", fgColor=AREIA)
FTOT = PatternFill("solid", fgColor=CREME)
BFINA = Border(bottom=Side(style="thin", color="D8CEC1"))

wb = Workbook()

def cabecalho(ws, linha, titulos, larguras=None):
    for i, t in enumerate(titulos, start=1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font = CAB; c.fill = FCAB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    if larguras:
        for i, w_ in enumerate(larguras, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w_
    ws.row_dimensions[linha].height = 28

# ═══════════════ 1. LEIA-ME
ws = wb.active; ws.title = "LEIA-ME"
ws.column_dimensions["A"].width = 28; ws.column_dimensions["B"].width = 105
ws["A1"] = "O Beco Gelato — dados para ficha técnica e tabela nutricional"; ws["A1"].font = TIT
ws["A2"] = "Revisão de 21/10/2026"; ws["A2"].font = PEQ
linhas = [
 ("", ""),
 ("O que tem aqui", "Sete sabores de linha, todos zero lactose. Uma aba por sabor, mais a aba INSUMOS com a ficha de cada ingrediente e a aba RESUMO com o comparativo."),
 ("ATENÇÃO — selo de açúcar", "Cinco dos sete sabores sustentam 'sem adição de açúcares' com zero absoluto. DOIS NÃO: Sorbet Morango (0,470 g/100 g, vindos da Pasta Fragola a 10 g/kg, que é 47% açúcar adicionado) e Alfajor (0,010 g/100 g, vindos do biscoito). A alegação exige zero sem tolerância. Coluna 'Aç. adic.' na aba RESUMO."),
 ("As fórmulas são vivas", "As abas de sabor calculam a composição puxando da aba INSUMOS com PROCV. Se você corrigir um valor na INSUMOS, todos os sabores que usam aquele insumo se atualizam sozinhos."),
 ("", ""),
 ("ORIGEM DOS DADOS", "Os valores nutricionais vêm do cadastro interno do Beco, montado a partir de fichas técnicas e rótulos ao longo do tempo. NÃO substituem o rótulo físico da embalagem em uso. A coluna CONFERIR na aba INSUMOS marca onde essa verificação é mais crítica."),
 ("", ""),
 ("Calda", "A mistura líquida pasteurizada, antes da batedeira. Todas as formulações estão por 1 kg de calda."),
 ("Gelato", "A calda depois de batida, com ar incorporado. É o que vai no pote."),
 ("Pote", f"{POTE} g de produto. Com pote e tampa (10 g), 150 g na balança. Exceção: o Alfajor tem 135 g de gelato mais 15 g de biscoito por cima, fechando 150 g."),
 ("Açúcares totais", "No sentido da ANVISA: NÃO incluem polióis. O cadastro guarda um segundo valor, 'técnico', que soma açúcar e poliol — serve para calcular doçura e ponto de congelamento, não para rótulo. As duas colunas estão separadas."),
 ("Carboidratos totais", "NÃO calculados aqui, de propósito. A convenção de incluir ou não fibras e polióis é decisão sua. Cada componente medido está separado e os sólidos totais fecham a conta."),
 ("Overrun", "O ar incorporado na batedeira. O cadastro usa 21% para todos; medição de 16/10 deu de 14% a 47% conforme o sabor. Não altera a composição por 100 g, altera o peso do pote cheio."),
 ("", ""),
 ("Contato", "Gabriel Sampaio — O Beco Gelato LTDA — CNPJ 66.901.942/0001-59"),
]
r = 3
for a, b in linhas:
    ws.cell(row=r, column=1, value=a).font = NEG
    c = ws.cell(row=r, column=2, value=b)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if a in ("ORIGEM DOS DADOS", "ATENÇÃO — selo de açúcar"):
        ws.cell(row=r, column=1).fill = FDEST; c.fill = FDEST
    ws.row_dimensions[r].height = 30 if b else 8
    r += 1

# ═══════════════ 2. INSUMOS
ws = wb.create_sheet("INSUMOS")
ws["A1"] = "Ficha nutricional dos insumos — valores por 100 g"; ws["A1"].font = TIT
ws["A2"] = "Editar aqui atualiza todas as abas de sabor automaticamente."; ws["A2"].font = PEQ
cols = ["Insumo","Nome de rótulo","Alergênicos","kcal","Açúcares téc.","% açúcar adicionado",
        "Gorduras","Gord. saturadas","Gord. trans","Proteínas","Fibras","Sólidos totais",
        "Sódio (mg)","R$/kg","CONFERIR"]
cabecalho(ws, 4, cols, [38,34,22,8,12,13,10,12,11,10,8,12,11,9,46])
r = 5
for i in D["ingredientes"]:
    n = i["nut"]
    ws.cell(row=r, column=1, value=i["nome"])
    ws.cell(row=r, column=2, value=i["rotulo"])
    ws.cell(row=r, column=3, value=", ".join(i["alerg"]) or "—")
    for col, v in [(4,n["kcal"]),(5,n["acucares"]),(6,i["acucarAdd"]),(7,n["gordura"]),
                   (8,n["gordSat"]),(9,n["gordTrans"]),(10,n["proteinas"]),(11,n["fibra"]),
                   (12,n["solidosTotais"]),(13,n["sodio"]),(14,i["custoKg"])]:
        c = ws.cell(row=r, column=col, value=round(v,3)); c.number_format = "0.00"
    c = ws.cell(row=r, column=15, value="; ".join(i["conferir"]) or "")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if i["conferir"]:
        for col in range(1,16): ws.cell(row=r, column=col).fill = FDEST
    for col in range(1,16): ws.cell(row=r, column=col).border = BFINA
    r += 1
ws.freeze_panes = "B5"
ws.auto_filter.ref = f"A4:O{r-1}"

# ═══════════════ 3. COMPOSTOS
ws = wb.create_sheet("COMPOSTOS")
ws["A1"] = "Ingredientes preparados na casa"; ws["A1"].font = TIT
ws["A2"] = "Precisam aparecer desdobrados nos componentes na lista de ingredientes do rótulo."
ws["A2"].font = PEQ
r = 4
for titulo, itens, unid in [("MIX OFICIAL — usado no Pistache e na Torta de Limão", D["mixOficial"], "partes"),
                            ("BASE PROTEICA — usada no Café e no Brigadeiro", D["baseProteica"], "g por kg de base")]:
    ws.cell(row=r, column=1, value=titulo).font = NEG; r += 1
    cabecalho(ws, r, ["Componente", unid, "% do total", "Por 1 kg"], [44,14,12,14])
    r += 1
    tot = sum(v for _, v in itens); ini = r
    for n, v in itens:
        ws.cell(row=r, column=1, value=n)
        ws.cell(row=r, column=2, value=round(v,2)).number_format = "0.00"
        ws.cell(row=r, column=3, value=f"=B{r}/SUM(B${ini}:B${ini+len(itens)-1})").number_format = "0.00%"
        ws.cell(row=r, column=4, value=f"=C{r}*1000").number_format = "0.0"
        r += 1
    ws.cell(row=r, column=1, value="TOTAL").font = NEG
    ws.cell(row=r, column=2, value=f"=SUM(B{ini}:B{r-1})").font = NEG
    ws.cell(row=r, column=4, value=1000).font = NEG
    for col in range(1,5): ws.cell(row=r, column=col).fill = FTOT
    r += 3
ws.cell(row=r, column=1, value="Saborização da base proteica").font = NEG; r += 1
cabecalho(ws, r, ["Sabor","Base por kg de calda","Saborizante","g/kg","Proteína final"], [26,20,30,10,14])
r += 1
for a_ in [["Café Proteico", 943.2, "Pasta Café Selecta", 56.8, "9,99%"],
           ["Brigadeiro Proteico", 961.5, "Cacau 22/24", 38.5, "10,13%"]]:
    for i, v in enumerate(a_, start=1): ws.cell(row=r, column=i, value=v)
    r += 1

# ═══════════════ 4. UMA ABA POR SABOR
NI = len(D["ingredientes"])
def procv(col, linha_ing):
    return f"IFERROR(VLOOKUP($A{linha_ing},INSUMOS!$A$5:$N${4+NI},{col},FALSE),0)"

for s in D["sabores"]:
    nome = s["nome"][:28]
    ws = wb.create_sheet(nome)
    ws["A1"] = s["nome"]; ws["A1"].font = TIT
    ws["A2"] = (f"linha {s['linha']} · família de formulação: {s['familiaForm']} · "
                f"pote de {s['massaPote']:.0f} g")
    ws["A2"].font = PEQ

    cols = ["Ingrediente","Nome de rótulo","g por kg de calda","% da calda","g no pote",
            "kcal","Açúc. téc.","Aç. adic.","Gord.","G.sat.","G.trans","Prot.","Fibra",
            "Sól.tot.","Sódio mg"]
    cabecalho(ws, 4, cols, [38,32,14,11,11,9,10,10,9,9,9,9,9,10,10])
    ini = 5; r = ini
    todas = s["linhas"] + [{"nome":l["nome"], "rotulo":l["rotulo"], "gkg":l["gkg"],
                            "pct":None, "noPote":l["noPote"]} for l in s["fin"]]
    for l in todas:
        ws.cell(row=r, column=1, value=l["nome"])
        ws.cell(row=r, column=2, value=l["rotulo"])
        ws.cell(row=r, column=3, value=round(l["gkg"],3)).number_format = "0.0"
        ws.cell(row=r, column=4, value=f"=C{r}/SUM(C${ini}:C${ini+len(s['linhas'])-1})").number_format = "0.00%"
        ws.cell(row=r, column=5, value=round(l["noPote"],3)).number_format = "0.00"
        # contribuicao de cada insumo ao pote, via PROCV na aba INSUMOS
        for col, icol in [(6,4),(7,5),(9,7),(10,8),(11,9),(12,10),(13,11),(14,12),(15,13)]:
            ws.cell(row=r, column=col, value=f"={procv(icol,r)}*$E{r}/100").number_format = "0.000"
        ws.cell(row=r, column=8, value=f"={procv(6,r)}*$E{r}/100/100").number_format = "0.000"
        for col in range(1,16): ws.cell(row=r, column=col).border = BFINA
        r += 1
    fim = r - 1
    ws.cell(row=r, column=1, value="TOTAL NO POTE").font = NEG
    ws.cell(row=r, column=3, value=f"=SUM(C{ini}:C{ini+len(s['linhas'])-1})").number_format = "0.0"
    ws.cell(row=r, column=5, value=f"=SUM(E{ini}:E{fim})").number_format = "0.00"
    for col in range(6,16):
        ws.cell(row=r, column=col, value=f"=SUM({get_column_letter(col)}{ini}:{get_column_letter(col)}{fim})")
        ws.cell(row=r, column=col).number_format = "0.00"
    for col in range(1,16):
        ws.cell(row=r, column=col).fill = FTOT; ws.cell(row=r, column=col).font = NEG
    tot_r = r
    r += 2

    ws.cell(row=r, column=1, value="POR 100 g DE PRODUTO").font = NEG; r += 1
    cabecalho(ws, r, ["Componente","Valor","Unidade"], [38,14,12]); r += 1
    massa = s["massaPote"]
    comp = [("Valor energético", f"=F{tot_r}/{massa}*100", "kcal"),
            ("Açúcares totais (rótulo)", s["pote"]["acu"], "g"),
            ("   dos quais adicionados", f"=H{tot_r}/{massa}*100", "g"),
            ("Polióis", s["pote"]["poliois"], "g"),
            ("Fibras alimentares", f"=M{tot_r}/{massa}*100", "g"),
            ("Proteínas", f"=L{tot_r}/{massa}*100", "g"),
            ("Gorduras totais", f"=I{tot_r}/{massa}*100", "g"),
            ("   das quais saturadas", f"=J{tot_r}/{massa}*100", "g"),
            ("   das quais trans", f"=K{tot_r}/{massa}*100", "g"),
            ("Sódio", f"=O{tot_r}/{massa}*100", "mg"),
            ("Sólidos totais", f"=N{tot_r}/{massa}*100", "g"),
            ("Açúcares técnicos (uso interno)", s["pote"]["acuTecnico"], "g")]
    for a_, v, u in comp:
        ws.cell(row=r, column=1, value=a_)
        c = ws.cell(row=r, column=2, value=v if isinstance(v, str) else round(v,3))
        c.number_format = "0.00"
        ws.cell(row=r, column=3, value=u)
        if "técnico" in a_:
            for col in range(1,4): ws.cell(row=r, column=col).font = PEQ
        r += 1
    r += 1

    ws.cell(row=r, column=1, value="PARÂMETROS DA CALDA").font = NEG; r += 1
    m = s["met"]
    for a_, v, u in [("Sólidos totais", m["sol"], "%"), ("Água", m["agua"], "%"),
                     ("Gordura", m["gord"], "%"), ("Proteína", m["prot"], "%"),
                     ("POD", m["pod"], ""), ("PAC", m["pac"], ""),
                     ("Janela de consumo", f"{s['janela'][0]:.1f} a {s['janela'][1]:.1f}", "°C"),
                     ("Água congelada a −8 °C", s["frozen"], "%")]:
        ws.cell(row=r, column=1, value=a_)
        ws.cell(row=r, column=2, value=v if isinstance(v, str) else round(v,2)).number_format = "0.00"
        ws.cell(row=r, column=3, value=u); r += 1
    r += 1

    ws.cell(row=r, column=1, value="LISTA DE INGREDIENTES — RDC 727/2022").font = NEG; r += 1
    ws.cell(row=r, column=1, value="Ingredientes: " + ", ".join(i["r"] for i in s["rdc727"]) + ".")
    ws.cell(row=r, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    ws.row_dimensions[r].height = 46; r += 1
    if s["alerg"]:
        ws.cell(row=r, column=1, value="ALÉRGICOS: CONTÉM " + ", ".join(s["alerg"]) + ".").font = NEG
        r += 1
    ws.cell(row=r, column=1, value="Selos: " + (" · ".join(s["selos"]["ok"]) or "—")); r += 1
    ws.cell(row=r, column=1, value="Lupa frontal: " + (" · ".join(s["selos"]["lupa"]) or "nenhuma"))
    ws.freeze_panes = "A5"

# ═══════════════ 5. RESUMO
ws = wb.create_sheet("RESUMO")
ws["A1"] = "Comparativo dos 7 sabores — por pote"; ws["A1"].font = TIT
ws["A2"] = "Alfajor em pote de 150 g; demais em 140 g."; ws["A2"].font = PEQ
cols = ["Sabor","Linha","Pote (g)","kcal","Açúcares","Polióis","Aç. adic.","Proteínas",
        "Gorduras","G. sat.","Fibras","Sódio (mg)","Selos","Lupa"]
cabecalho(ws, 4, cols, [24,11,10,9,11,10,11,11,10,9,9,11,40,20])
r = 5
for s in D["sabores"]:
    p = s["pote"]; k = s["massaPote"]/100
    vals = [s["nome"], s["linha"], round(s["massaPote"],0), round(p["kcal"]*k,0),
            round(p["acu"]*k,1), round(p["poliois"]*k,1), round(p["acucarAdd"]*k,2),
            round(p["prot"]*k,1), round(p["gord"]*k,1), round(p["gordSat"]*k,1),
            round(p["fibra"]*k,1), round(p["sodio"]*k,0),
            " · ".join(s["selos"]["ok"]) or "—", " · ".join(s["selos"]["lupa"]) or "nenhuma"]
    for i, v in enumerate(vals, start=1):
        c = ws.cell(row=r, column=i, value=v)
        if isinstance(v,(int,float)) and i>3: c.number_format = "0.0"
        c.border = BFINA
    r += 1
ws.freeze_panes = "B5"

wb.save("O Beco Gelato - Dados para Nutricionista.xlsx")
print("planilha gerada — abas:", ", ".join(wb.sheetnames))
