# -*- coding: utf-8 -*-
"""
PLANILHA DE COMPRAS E ESTOQUE — O BECO GELATO
22/10/2026

Tres coisas que o Gabriel pediu, numa planilha so:
  1. fornecedores com insumos e valores atuais
  2. estoque atual x necessario
  3. estoque de potes prontos e quantos sairam

REGRA DE COR, igual as outras planilhas do projeto:
  AMARELO = ele edita
  BRANCO  = formula, nao mexer
  CINZA   = dado vindo do Balanceador (atualiza rodando este script de novo)

O consumo por pote ja vem com o Mix Oficial EXPLODIDO nos componentes.
Para formular, o mix e um ingrediente. Para comprar, o que existe e
polidextrose, maltitol, eritritol, inulina e stevia em saco.
"""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

D = json.load(open("_compras.json", encoding="utf-8"))
POTE, FAT = D["pote"], D["fator"]
SAB = D["sabores"]
CONS = D["consumo"]
INS = D["insumos"]
EMB = D["embalagem"]

VERDE = "1B5E20"; ESCURO = "263238"; AMAR = "FFF9C4"
CINZA = "ECEFF1"; CAB = "37474F"; VERM = "FFCDD2"; VERDEC = "C8E6C9"
B = Side(style="thin", color="B0BEC5")
BOX = Border(left=B, right=B, top=B, bottom=B)
wb = Workbook()

def head(ws, titulo, sub=""):
    ws["A1"] = titulo
    ws["A1"].font = Font(bold=True, size=15, color=VERDE)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=9, italic=True, color="546E7A")
    return 4

def cab(ws, row, cols):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=i, value=c)
        x.font = Font(bold=True, size=9, color="FFFFFF")
        x.fill = PatternFill("solid", fgColor=CAB)
        x.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        x.border = BOX
    ws.row_dimensions[row].height = 30

def larg(ws, ls):
    for i, w in enumerate(ls, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def amarelo(c):
    c.fill = PatternFill("solid", fgColor=AMAR); c.border = BOX
def cinza(c):
    c.fill = PatternFill("solid", fgColor=CINZA); c.border = BOX

# ───────────────────────────────── 1. LEIA-ME
ws = wb.active; ws.title = "LEIA-ME"
larg(ws, [3, 100])
ws["B2"] = "O BECO GELATO — COMPRAS E ESTOQUE"
ws["B2"].font = Font(bold=True, size=18, color=VERDE)
ws["B3"] = "22 de outubro de 2026"
ws["B3"].font = Font(size=10, color="546E7A")

TXT = [
 ("", ""),
 ("h", "O QUE TEM AQUI"),
 ("p", "PLANO DE PRODUCAO — voce diz quantos potes de cada sabor pretende fazer. Tudo o resto se recalcula a partir daqui."),
 ("p", "FORNECEDORES — cada insumo, de quem vem, embalagem e preco por quilo."),
 ("p", "ESTOQUE INSUMOS — o que tem contra o que o plano exige, com a falta e o custo de cobrir a falta."),
 ("p", "EMBALAGEM — pote, colher e lacre, e quantos potes cada saldo ainda fecha."),
 ("p", "POTES PRONTOS — estoque de produto acabado por sabor, com entradas e saidas."),
 ("p", "TESTES — cada calda que voce bateu para testar ou para comer, com o custo, e a verba mensal de P&D."),
 ("p", "MOVIMENTO — onde voce lanca cada producao e cada venda. E a unica aba que precisa de disciplina diaria."),
 ("", ""),
 ("h", "A COR DIZ SE PODE MEXER"),
 ("p", "AMARELO — campo seu. Digite."),
 ("p", "BRANCO — formula. Se sobrescrever, quebra a conta."),
 ("p", "CINZA — numero que veio do Balanceador de Receitas. Nao edite aqui: mude na receita e me peca para gerar a planilha de novo."),
 ("", ""),
 ("h", "O QUE EU NAO TENHO — leia antes de confiar na aba FORNECEDORES"),
 ("p", "O sistema nunca teve campo de fornecedor. Nenhum. Eu tenho o preco de cada insumo, mas nao tenho de quem voce compra."),
 ("p", "Preenchi 8 linhas com o que apareceu nas nossas conversas e marquei a procedencia de cada uma na coluna ORIGEM:"),
 ("p", "   'nota' = saiu de uma nota fiscal que voce me mandou. Confiavel."),
 ("p", "   'ficha' = saiu da ficha tecnica do produto, entao o fabricante esta certo mas o distribuidor pode ser outro."),
 ("p", "   'conversa' = voce mencionou de passagem. Confira."),
 ("p", "   'cotacao' = e a cotacao nova de 21/10, ainda nao comprada."),
 ("p", "As outras 15 linhas estao em branco de proposito. Inventar fornecedor seria pior que deixar vazio."),
 ("", ""),
 ("h", "DUAS COISAS QUE A PLANILHA ASSUME"),
 ("p", "PERDA DE PROCESSO DE 3%. E o que esta no Balanceador, e o proprio bancada diz que esta alto: voce fez 30 potes de pistache e sairam 31, mesmo caso na torta de limao. Se a perda real for 1%, esta planilha pede 2% mais insumo do que voce precisa. Nao e erro grave para compras — sobra e melhor que faltar — mas quando voce pesar um pote eu corrijo o numero."),
 ("p", "POTE DE 140 g. Media de 35 potes pesados em 16/10. O Alfajor e a excecao: 135 g de gelato mais 15 g de biscoito por cima."),
 ("", ""),
 ("h", "O ESTOQUE DE POTES PRONTOS PARTE DA CONTAGEM DE 22/10 — 325 POTES"),
 ("p", "Contagem fisica ditada em 22/10/2026: Manga com Maracuja 60 · Torta de Limao 58 · Brigadeiro 51 · Pistache 46 · Cafe 40 · Alfajor 38 · Sorbet Morango 32."),
 ("p", "Essa contagem ZERA A CONTA. Ela e posterior ao pedido 000007 (16/10), entao aqueles 125 potes ja sairam do numero contado — as linhas do pedido na aba MOVIMENTO ficaram com tipo HISTORICO para nao serem descontadas duas vezes. Toda contagem nova funciona assim."),
 ("p", "DOIS FATOS QUE A CONTAGEM REVELOU. Primeiro: entre 13/10 (262 potes) e 22/10 a producao implicita foi de 188 potes, e nada disso estava lancado em lugar nenhum. Segundo: o morango nao fecha — eram 53, sairam 15, deveria haver 38 e ha 32. Faltam 6 potes, e pode ser degustacao, amostra, perda ou venda nao registrada; nao da para saber qual."),
 ("p", "A partir de hoje, lance cada producao e cada saida na aba MOVIMENTO. E so assim que a proxima contagem vai poder ser conferida em vez de apenas substituir a anterior."),
 ("", ""),
 ("h", "A ABA TESTES TEM O MESMO PROBLEMA, POR OUTRO MOTIVO"),
 ("p", "O sistema nunca registrou lote de teste. Nenhum. As 17 linhas que estao lá sao reconstruidas das nossas conversas, e cada uma carrega a coluna EVIDENCIA com a frase ou o fato que sustenta a linha."),
 ("p", "O custo por quilo eu tenho para quase todas, porque as receitas estao cadastradas. O que falta e o VOLUME: eu so sei os kg que voce declarou em voz alta — 1,5 kg do pistache meia a meia, 750 g da base neutra, 1 kg do melagrana e 1 kg da canela. Os outros ficaram em branco de proposito, porque chutar quilo ali estragaria exatamente a media que voce quer usar para fixar a verba."),
]
r = 5
for tipo, t in TXT:
    if tipo == "h":
        ws.cell(row=r, column=2, value=t).font = Font(bold=True, size=11, color=ESCURO)
    elif tipo == "p":
        c = ws.cell(row=r, column=2, value=t)
        c.font = Font(size=10); c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[r].height = max(15, 14 * (len(t) // 95 + 1))
    r += 1

# ───────────────────────────────── 2. PLANO DE PRODUCAO
ws = wb.create_sheet("PLANO")
r0 = head(ws, "PLANO DE PRODUCAO",
          "Quantos potes de cada sabor voce quer produzir no periodo. Esta aba comanda ESTOQUE INSUMOS e EMBALAGEM.")
larg(ws, [26, 14, 14, 16, 16])
ws.cell(row=r0, column=1, value="PERIODO DO PLANO").font = Font(bold=True, size=10)
amarelo(ws.cell(row=r0, column=2, value="30 dias"))
r = r0 + 2
cab(ws, r, ["SABOR", "POTES\nA PRODUZIR", "CALDA\nNECESSARIA (kg)", "PRECO DE\nVENDA (R$)", "RECEITA\nPREVISTA (R$)"])
PRECO = {"Pistache": 20.50, "Torta de Limão": 20.50, "Brigadeiro Proteico": 20.50,
         "Café Proteico": 20.50, "Alfajor": 20.50, "Manga com Maracujá": 18.70,
         "Sorbet Morango": 18.70}
PADRAO = {"Pistache": 30, "Torta de Limão": 30, "Brigadeiro Proteico": 30,
          "Café Proteico": 30, "Alfajor": 30, "Manga com Maracujá": 30,
          "Sorbet Morango": 30}
pl = {}
r += 1
for s in SAB:
    ws.cell(row=r, column=1, value=s).border = BOX
    amarelo(ws.cell(row=r, column=2, value=PADRAO.get(s, 30)))
    g = sum(CONS[s].values())
    c = ws.cell(row=r, column=3, value=f"=B{r}*{g/1000:.4f}")
    c.number_format = "0.00"; c.border = BOX
    amarelo(ws.cell(row=r, column=4, value=PRECO.get(s, 20.50)))
    ws.cell(row=r, column=4).number_format = '"R$" #,##0.00'
    c = ws.cell(row=r, column=5, value=f"=B{r}*D{r}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    pl[s] = r
    r += 1
ws.cell(row=r, column=1, value="TOTAL").font = Font(bold=True)
for col, fmt in ((2, "0"), (3, "0.00"), (5, '"R$" #,##0.00')):
    L = get_column_letter(col)
    c = ws.cell(row=r, column=col, value=f"=SUM({L}{r0+3}:{L}{r-1})")
    c.font = Font(bold=True); c.number_format = fmt
    c.fill = PatternFill("solid", fgColor=VERDEC); c.border = BOX
PLANO_LIN = pl
TOT_POTES = r

ws.cell(row=r + 2, column=1,
    value="A calda necessaria ja inclui a perda de 3% e exclui a agua das receitas de fruta.").font = Font(size=9, italic=True, color="546E7A")

# ───────────────────────────────── 3. FORNECEDORES
ws = wb.create_sheet("FORNECEDORES")
r0 = head(ws, "FORNECEDORES E PRECOS",
          "O sistema nunca teve cadastro de fornecedor. Preenchi o que saiu das conversas e marquei a procedencia. As linhas vazias sao para voce.")
larg(ws, [50, 20, 20, 16, 15, 15, 12, 24, 14, 30])
r = r0
cab(ws, r, ["INSUMO", "FORNECEDOR", "MARCA", "EMBALAGEM",
            "R$/kg ATUAL", "R$/kg COTADO", "ECONOMIA", "CONTATO / TELEFONE",
            "PRAZO (dias)", "ORIGEM DO DADO / OBS"])
COTADO = {"ERITRITOL": 14.75, "MALTITOL": 17.95, "POLIDEXTROSE": 12.85}
r += 1
F_LIN = {}
for i in INS:
    n = i["nome"]
    ws.cell(row=r, column=1, value=n).border = BOX
    amarelo(ws.cell(row=r, column=2, value=i["fornecedor"]))
    amarelo(ws.cell(row=r, column=3, value=i["marca"]))
    amarelo(ws.cell(row=r, column=4, value=i["embalagem"]))
    c = ws.cell(row=r, column=5, value=i["custoKg"])
    c.number_format = '"R$" #,##0.00'; cinza(c)
    ct = COTADO.get(n)
    c = ws.cell(row=r, column=6, value=ct if ct else None)
    c.number_format = '"R$" #,##0.00'; amarelo(c)
    c = ws.cell(row=r, column=7, value=f'=IF(F{r}="","",E{r}-F{r})')
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    amarelo(ws.cell(row=r, column=8))
    amarelo(ws.cell(row=r, column=9))
    o = i["origem"] or ""
    c = ws.cell(row=r, column=10, value=o)
    c.font = Font(size=9, italic=True,
                  color=("2E7D32" if o.startswith("nota") else "546E7A"))
    c.border = BOX
    if not i["fornecedor"]:
        ws.cell(row=r, column=2).fill = PatternFill("solid", fgColor=VERM)
    F_LIN[n] = r
    r += 1

r += 1
ws.cell(row=r, column=1, value="COTACAO DE 21/10/2026 — AINDA NAO COMPRADA").font = Font(bold=True, size=10, color=ESCURO)
r += 1
for t in ["Eritritol — Huakang — saco 25 kg — R$ 14,75/kg — ICMS 12% incluso",
          "Maltitol — Yusweet — saco 25 kg — R$ 17,95/kg — ICMS 4% incluso",
          "Polidextrose — Shandong Bailong — saco 25 kg — R$ 12,85/kg — ICMS 12% incluso",
          "",
          "Com os tres, o Mix Oficial cai de R$ 49,13 para R$ 29,83/kg e o CMV medio cai cerca de R$ 0,35 por pote.",
          "Pendente antes de fechar: ficha tecnica dos tres, granulometria do eritritol e data de fabricacao / validade.",
          "A polidextrose e o limitante: 25 kg dao cerca de 2.380 potes, contra 7.300 do maltitol e 9.160 do eritritol."]:
    c = ws.cell(row=r, column=1, value=t); c.font = Font(size=9, color="546E7A")
    r += 1

# ───────────────────────────────── 4. ESTOQUE INSUMOS
ws = wb.create_sheet("ESTOQUE INSUMOS")
r0 = head(ws, "ESTOQUE ATUAL x NECESSARIO",
          "O necessario vem da aba PLANO. Atualize a coluna ATUAL depois de cada contagem.")
larg(ws, [50, 16, 16, 16, 16, 15, 17, 30])
r = r0
cab(ws, r, ["INSUMO", "ESTOQUE\nATUAL (g)", "NECESSARIO\nPLANO (g)", "SALDO\n(g)",
            "COMPRAR\n(kg)", "R$/kg", "CUSTO DA\nCOMPRA (R$)", "SITUACAO"])
r += 1
E_LIN = {}
for i in INS:
    n = i["nome"]
    ws.cell(row=r, column=1, value=n).border = BOX
    amarelo(ws.cell(row=r, column=2, value=round(i["estoque"], 1)))
    ws.cell(row=r, column=2).number_format = "#,##0.0"
    # necessario = soma, por sabor, de (potes do plano) x (g por pote deste insumo)
    partes = []
    for s in SAB:
        g = CONS[s].get(n)
        if g:
            partes.append(f"PLANO!B{PLANO_LIN[s]}*{g:.4f}")
    c = ws.cell(row=r, column=3, value=("=" + "+".join(partes)) if partes else 0)
    c.number_format = "#,##0.0"; c.border = BOX
    c = ws.cell(row=r, column=4, value=f"=B{r}-C{r}")
    c.number_format = "#,##0.0"; c.border = BOX
    # 22/10 — ROUNDUP a 3 casas, nao 2. Com 2 casas a stevia (R$ 3.100/kg) pedia
    # 0,02 kg no lugar de 0,015 e o custo saia R$ 62 contra R$ 44 — R$ 18 de erro
    # numa linha de 14 gramas. Em insumo caro, o arredondamento e o erro.
    c = ws.cell(row=r, column=5, value=f"=IF(D{r}>=0,0,ROUNDUP(-D{r}/1000,3))")
    c.number_format = "#,##0.000"; c.border = BOX
    c = ws.cell(row=r, column=6, value=f"=FORNECEDORES!E{F_LIN[n]}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    c = ws.cell(row=r, column=7, value=f"=E{r}*F{r}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    c = ws.cell(row=r, column=8,
        value=f'=IF(B{r}=0,"SEM ESTOQUE",IF(D{r}<0,"FALTA","ok"))')
    c.border = BOX; c.font = Font(size=9, bold=True)
    E_LIN[n] = r
    r += 1
ws.cell(row=r, column=1, value="TOTAL A COMPRAR").font = Font(bold=True)
c = ws.cell(row=r, column=7, value=f"=SUM(G{r0+1}:G{r-1})")
c.font = Font(bold=True); c.number_format = '"R$" #,##0.00'
c.fill = PatternFill("solid", fgColor=VERDEC); c.border = BOX

r += 2
for t in ["O Mix Oficial nao aparece como linha: ele e feito na casa. O que esta aqui sao os cinco insumos que voce compra de fato — polidextrose, maltitol, eritritol, inulina e stevia — ja na proporcao do mix (528/224/163/81/3).",
          "A agua tambem nao aparece, por motivo obvio.",
          "A coluna NECESSARIO ja inclui a perda de 3%.",
          "A coluna COMPRAR e a necessidade liquida, nao o pedido. Ninguem compra 15 g de stevia nem 0,67 kg de doce de leite: voce compra o pacote fechado. Use a coluna como piso e arredonde para a embalagem do fornecedor."]:
    c = ws.cell(row=r, column=1, value=t)
    c.font = Font(size=9, italic=True, color="546E7A")
    r += 1

# ───────────────────────────────── 5. EMBALAGEM
ws = wb.create_sheet("EMBALAGEM")
r0 = head(ws, "EMBALAGEM",
          "Quantos potes cada saldo ainda fecha. O menor numero da coluna ALCANCE e o seu gargalo real de producao.")
larg(ws, [34, 13, 14, 16, 17, 16, 18, 30])
r = r0
cab(ws, r, ["ITEM", "POR POTE", "SALDO\n(un)", "ALCANCE\n(potes)", "NECESSARIO\nPLANO (un)",
            "COMPRAR\n(un)", "CUSTO (R$)", "OBS"])
OBS_E = {
 "Pote 150 ml com tampa": "R$ 0,47 negociado em 08/10 — so vale depois que este estoque acabar",
 "Lacre de sabor": "GARGALO — menor alcance dos tres",
 "Pote 80 ml (amostra)": "amostra, nao entra no pote de venda",
 "Colher de amostra": "amostra, nao entra no pote de venda",
}
r += 1
ini = r
for e in EMB:
    ws.cell(row=r, column=1, value=e["nome"]).border = BOX
    c = ws.cell(row=r, column=2, value=e["porPote"]); cinza(c)
    amarelo(ws.cell(row=r, column=3, value=e["saldo"]))
    ws.cell(row=r, column=3).number_format = "#,##0"
    c = ws.cell(row=r, column=4, value=f'=IF(B{r}=0,"—",FLOOR(C{r}/B{r},1))')
    c.number_format = "#,##0"; c.border = BOX; c.font = Font(bold=True)
    c = ws.cell(row=r, column=5, value=f"=B{r}*PLANO!B{TOT_POTES}")
    c.number_format = "#,##0"; c.border = BOX
    c = ws.cell(row=r, column=6, value=f"=MAX(0,E{r}-C{r})")
    c.number_format = "#,##0"; c.border = BOX
    c = ws.cell(row=r, column=7, value=f"=F{r}*{e['preco']}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    c = ws.cell(row=r, column=8, value=OBS_E.get(e["nome"], ""))
    c.font = Font(size=9, italic=True, color="546E7A"); c.border = BOX
    if e["nome"] == "Lacre de sabor":
        ws.cell(row=r, column=4).fill = PatternFill("solid", fgColor=VERM)
    r += 1
ws.cell(row=r, column=1, value="CUSTO DE EMBALAGEM").font = Font(bold=True)
c = ws.cell(row=r, column=7, value=f"=SUM(G{ini}:G{r-1})")
c.font = Font(bold=True); c.number_format = '"R$" #,##0.00'
c.fill = PatternFill("solid", fgColor=VERDEC); c.border = BOX
r += 2
ws.cell(row=r, column=1,
  value="Custo de embalagem por pote hoje: R$ 1,67 (pote 1,07 + colher 0,26 + lacre 0,34). Com o pote a R$ 0,47 cai para R$ 1,07.").font = Font(size=9, italic=True, color="546E7A")

# ───────────────────────────────── 6. POTES PRONTOS
ws = wb.create_sheet("POTES PRONTOS")
r0 = head(ws, "ESTOQUE DE PRODUTO ACABADO",
          "Saldo = contagem + entradas - saidas. As entradas e saidas vem da aba MOVIMENTO. Faca uma contagem fisica hoje e corrija a coluna CONTAGEM.")
larg(ws, [26, 15, 18, 14, 14, 14, 16, 16, 28])
r = r0
ws.cell(row=r, column=1, value="DATA DA CONTAGEM").font = Font(bold=True, size=10)
amarelo(ws.cell(row=r, column=2, value="22/10/2026"))
c = ws.cell(row=r, column=3, value="contagem física — 325 potes")
c.font = Font(size=9, italic=True, color="2E7D32")
r += 2
cab(ws, r, ["SABOR", "CONTAGEM\n(potes)", "ENTRADAS\n(producao)", "SAIDAS\n(vendas)",
            "SALDO\n(potes)", "PRECO\n(R$)", "VALOR EM\nESTOQUE (R$)",
            "RECEITA JA\nVENDIDA (R$)", "OBS"])
r += 1
ini = r
CONT = D["potesContagem"]; P7 = D["pedido7"]
for s in SAB:
    ws.cell(row=r, column=1, value=s).border = BOX
    amarelo(ws.cell(row=r, column=2, value=CONT.get(s, 0)))
    c = ws.cell(row=r, column=3,
        value=f'=SUMIFS(MOVIMENTO!$D:$D,MOVIMENTO!$C:$C,A{r},MOVIMENTO!$B:$B,"PRODUCAO")')
    c.number_format = "#,##0"; c.border = BOX
    c = ws.cell(row=r, column=4,
        value=f'=SUMIFS(MOVIMENTO!$D:$D,MOVIMENTO!$C:$C,A{r},MOVIMENTO!$B:$B,"VENDA")')
    c.number_format = "#,##0"; c.border = BOX
    c = ws.cell(row=r, column=5, value=f"=B{r}+C{r}-D{r}")
    c.number_format = "#,##0"; c.border = BOX; c.font = Font(bold=True)
    c = ws.cell(row=r, column=6, value=f"=PLANO!D{PLANO_LIN[s]}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    c = ws.cell(row=r, column=7, value=f"=E{r}*F{r}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    c = ws.cell(row=r, column=8, value=f"=D{r}*F{r}")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    OBS_P = {"Sorbet Morango": "caiu de 53 (13/10) para 32 — ver nota abaixo",
             "Alfajor": "0 em 13/10, 38 agora — foi produzido no meio"}
    c = ws.cell(row=r, column=9, value=OBS_P.get(s, ""))
    c.font = Font(size=9, italic=True, color="546E7A"); c.border = BOX
    r += 1
ws.cell(row=r, column=1, value="TOTAL").font = Font(bold=True)
for col, fmt in ((2, "#,##0"), (3, "#,##0"), (4, "#,##0"), (5, "#,##0"),
                 (7, '"R$" #,##0.00'), (8, '"R$" #,##0.00')):
    L = get_column_letter(col)
    c = ws.cell(row=r, column=col, value=f"=SUM({L}{ini}:{L}{r-1})")
    c.font = Font(bold=True); c.number_format = fmt
    c.fill = PatternFill("solid", fgColor=VERDEC); c.border = BOX
r += 2
for t, cor in [
  ("A contagem de 22/10 zera a conta: ela e posterior ao pedido 000007, entao os 125 potes daquele pedido JA ESTAO fora deste numero. Por isso as linhas do 000007 na aba MOVIMENTO estao com tipo HISTORICO — ficam visiveis mas nao sao descontadas de novo. Toda contagem fisica nova funciona assim: o que veio antes dela passa a ser historico.", "546E7A"),
  ("ENTRE 13/10 E 22/10 A PRODUCAO IMPLICITA FOI DE 188 POTES: 262 contados em 13/10, menos 125 vendidos no 000007, daria 137 — e ha 325. Nada dessa producao foi lancada em lugar nenhum.", "546E7A"),
  ("O MORANGO NAO FECHA. Eram 53 em 13/10 e sairam 15 no pedido 000007, o que deixaria 38 mesmo sem produzir nada. Ha 32. Faltam 6 potes, e as explicacoes possiveis sao degustacao, amostra, perda ou venda nao registrada. Nao da para saber qual — e por isso que o controle de saida precisa comecar.", "C62828")]:
    c = ws.cell(row=r, column=1, value=t)
    c.font = Font(size=9, italic=True, color=cor)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = max(15, 13 * (len(t) // 130 + 1))
    r += 1

# ───────────────────────────────── 7. TESTES E VERBA
# 22/10/2026 — O sistema nunca registrou lote de teste. Nenhum. O que esta aqui e
# reconstruido do que o Gabriel contou nas nossas conversas, e por isso cada linha
# carrega a coluna EVIDENCIA. Onde ele declarou o volume, esta preenchido; onde nao,
# o campo fica amarelo e vazio — nao inventei quantidade para fechar conta.
ws = wb.create_sheet("TESTES")
r0 = head(ws, "TESTES DE BANCADA E VERBA MENSAL",
          "Reconstruido das nossas conversas — o sistema nunca registrou lote de teste. Confira a coluna EVIDENCIA antes de confiar na linha.")
larg(ws, [15, 11, 34, 30, 11, 12, 13, 10, 13, 13, 14, 16, 30])
r = r0
cab(ws, r, ["DATA", "MES", "TESTE", "POR QUE", "CALDA\n(kg)", "R$/kg",
            "CUSTO DA\nCALDA", "POTES\nENVASADOS", "CUSTO\nEMBALAGEM",
            "CUSTO\nTOTAL", "RESULTADO", "DESTINO", "EVIDENCIA"])

#  data, mes, teste, motivo, kg, R$/kg, potes, resultado, destino, evidencia
#  R$/kg preenchido = receita cadastrada no Balanceador (celula CINZA).
#  R$/kg vazio = ou a receita nunca foi cadastrada, ou o insumo-chave esta sem
#  preco no sistema (celula AMARELA, ele preenche). A coluna EVIDENCIA diz qual.
LG = "lista do Gabriel, 22/10/2026"
T = [
 # ---- sabores novos que o Gabriel listou em 22/10
 ("","","Sorbet Melagrana (romã) · oficial","Sabor novo com a pasta MEC3 de romã",
  1.0,None,None,"REPROVADO","descarte",LG+" — \"ficou bem ruim o sabor\"; receita não cadastrada"),
 ("","","Melagrana · ajuste / reprocesso base leite","Salvar a calda reprovada",
  None,None,None,"PENDENTE","consumo próprio",LG+" — pediu o reprocesso para base leite"),
 ("","","Sorbet de Cajú","Sabor novo da linha Fresh",
  None,None,None,"PENDENTE","consumo próprio",LG+" — receita não cadastrada"),
 ("","","Sorbet de Goiaba","Sabor novo da linha Fresh",
  None,None,None,"PENDENTE","consumo próprio",LG+" — GOIABA está sem preço no sistema"),
 ("","","Sorbet de Siriguela","Sabor novo da linha Fresh",
  None,None,None,"PENDENTE","consumo próprio",LG+" — SIRIGUELA (polpa) está sem preço"),
 ("","","Avelã com açúcar de maçã","Exercício da apostila do Lulo",
  None,None,None,"PENDENTE","consumo próprio",LG+" — PASTA DE AVELA 100% está sem preço; o Gianduia do Lulo (R$ 6,94/kg) é o mais próximo cadastrado"),
 ("","","Baunilha tradicional","Par de prova da baunilha proteica",
  None,26.42,None,"PENDENTE","consumo próprio",LG+" — cadastrada como Baunilha · SPECIAL"),
 ("","","Baunilha proteica","Linha Boost — o pedido era 15 g de proteína",
  None,47.85,None,"PENDENTE","consumo próprio",LG+" — cadastrada como Baunilha Proteica · BOOST (entrega 13 g, não 15)"),
 ("","","Biscoito","Sabor novo com a pasta Biscottino",
  None,None,None,"PENDENTE","consumo próprio",LG+" — receita não cadastrada; a pasta tem preço (R$ 192,34/kg)"),
 ("","","Yogurt","Sabor novo de base iogurte",
  None,7.20,None,"PENDENTE","consumo próprio",LG+" — custo do Lulo · Iogurte (redução polióis); IOGURTE INTEGRAL está sem preço"),
 ("","","Pipoca","Sabor novo com a pasta Gusto Pop-Corn",
  None,None,None,"PENDENTE","consumo próprio",LG+" — PASTA GUSTO POP-CORN MEC3 está sem preço, o custo não fecha"),
 ("","","Latíssimo","Sabor novo de base leite",
  None,23.04,None,"REPROVADO","consumo próprio",LG+" — \"estava ruim\"; custo do Fior di Latte ZL como referência"),
 ("","","Latíssimo · ajuste da receita","Corrigir o Latíssimo que saiu ruim",
  None,23.04,None,"PENDENTE","consumo próprio",LG),
 # ---- testes que eu levantei das conversas anteriores
 ("24/09/2026","set/2026","Torta de Limão · v3 LULO","Subir os parâmetros para a faixa do Lulo",
  None,44.60,None,"APROVADO","virou venda","aprovou em bancada: \"ficou sensacional\""),
 ("24/09/2026","set/2026","Brigadeiro Proteico · versão que não pegava ponto","Linha Boost com 12 g de proteína",
  None,56.19,None,"REPROVADO","descarte","não pegava ponto — substituída pelo chocolate proteico"),
 ("24/09/2026","set/2026","Chocolate Proteico (virou o Brigadeiro oficial)","Substituir a versão que não pegava ponto",
  None,41.09,None,"APROVADO","virou venda","aprovado no mesmo dia, tomou o nome Brigadeiro"),
 ("","set/2026","Gelato de Ninho · mix antigo + creme 17%","Validar a textura do mix antigo",
  None,None,None,"APROVADO","consumo próprio","aprovou a textura: \"ficou muito boa\""),
 ("","set/2026","Mix com inulina","Comparar o mix com e sem inulina",
  None,None,None,"APROVADO","consumo próprio","\"com a inulina no mix tirou o melhor resultado de bancada\""),
 ("","out/2026","Café Proteico · v6 CREMOBENE","Fornecedor do núcleo Arkeo parou de fornecer",
  None,54.03,None,"APROVADO","virou venda","Cremobene entrou em uso oficial depois deste teste"),
 ("","out/2026","Sorbet Morango · CREMOBENE","Mesma troca de estabilizante",
  None,21.47,None,"APROVADO","virou venda","idem"),
 ("","out/2026","Manga com Maracujá · CREMOBENE","Mesma troca de estabilizante",
  None,26.25,None,"APROVADO","virou venda","idem"),
 ("","out/2026","Alfajor · estévia 0,45","Primeiro sabor novo pós-lançamento",
  None,33.75,None,"APROVADO","virou venda","\"receita validada e funcional\" — 20 potes no pedido 000007"),
 ("","out/2026","Pistache · 2 pastas novas, meia a meia","Comparar duas pastas de pistache novas",
  1.5,22.03,None,"PENDENTE","consumo próprio","\"vou fazer 1.5kg de pistache pra saborizar metade metade\""),
 ("","out/2026","Pistache · base neutra para dose de pasta","Achar a dose certa da pasta nova",
  0.75,22.03,None,"PENDENTE","consumo próprio","pediu a dose de pasta para 750 g de base"),
 ("22/10/2026","out/2026","Canela · pasta PreGel ST-58472","Sabor novo, pasta recém-chegada",
  1.0,24.83,None,"PENDENTE","consumo próprio","balanceado em 22/10 — não serve para venda (1,5 g de açúcar adicionado)"),
 ("","","Alfajor · estévia 0,30","Baixar a estévia de 0,45 para 0,30",
  None,33.75,None,"A FAZER","—","pendência aberta desde o cadastro do alfajor"),
]
r += 1
ini_t = r
for data, mes, teste, motivo, kg, rkg, potes, res, dest, ev in T:
    amarelo(ws.cell(row=r, column=1, value=data))
    amarelo(ws.cell(row=r, column=2, value=mes))
    ws.cell(row=r, column=3, value=teste).border = BOX
    ws.cell(row=r, column=4, value=motivo).border = BOX
    ws.cell(row=r, column=4).font = Font(size=9)
    amarelo(ws.cell(row=r, column=5, value=kg))
    ws.cell(row=r, column=5).number_format = "#,##0.000"
    c = ws.cell(row=r, column=6, value=rkg)
    c.number_format = '"R$" #,##0.00'
    (cinza if rkg else amarelo)(c)
    c = ws.cell(row=r, column=7, value=f"=IF(OR(E{r}=\"\",F{r}=\"\"),\"\",E{r}*F{r})")
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    amarelo(ws.cell(row=r, column=8, value=potes))
    c = ws.cell(row=r, column=9, value=f'=IF(H{r}="","",H{r}*1.67)')
    c.number_format = '"R$" #,##0.00'; c.border = BOX
    c = ws.cell(row=r, column=10, value=f"=N({chr(71)}{r})+N(I{r})")
    c.number_format = '"R$" #,##0.00'; c.border = BOX; c.font = Font(bold=True)
    amarelo(ws.cell(row=r, column=11, value=res))
    amarelo(ws.cell(row=r, column=12, value=dest))
    c = ws.cell(row=r, column=13, value=ev)
    c.font = Font(size=9, italic=True, color="546E7A"); c.border = BOX
    r += 1
for _ in range(14):                      # linhas em branco para os próximos testes
    for col in range(1, 14):
        amarelo(ws.cell(row=r, column=col))
    ws.cell(row=r, column=7, value=f"=IF(OR(E{r}=\"\",F{r}=\"\"),\"\",E{r}*F{r})").number_format = '"R$" #,##0.00'
    ws.cell(row=r, column=9, value=f'=IF(H{r}="","",H{r}*1.67)').number_format = '"R$" #,##0.00'
    ws.cell(row=r, column=10, value=f"=N(G{r})+N(I{r})").number_format = '"R$" #,##0.00'
    for col in (7, 9, 10):
        ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="FFFFFF")
        ws.cell(row=r, column=col).border = BOX
    r += 1
fim_t = r - 1

ws.cell(row=r, column=3, value="TOTAL GASTO EM TESTE").font = Font(bold=True)
c = ws.cell(row=r, column=10, value=f"=SUM(J{ini_t}:J{fim_t})")
c.font = Font(bold=True); c.number_format = '"R$" #,##0.00'
c.fill = PatternFill("solid", fgColor=VERDEC); c.border = BOX
r += 1
ws.cell(row=r, column=3, value="   do qual virou venda (não foi perda)").font = Font(size=9, italic=True)
c = ws.cell(row=r, column=10, value=f'=SUMIF(L{ini_t}:L{fim_t},"virou venda",J{ini_t}:J{fim_t})')
c.number_format = '"R$" #,##0.00'; c.border = BOX
r += 1
ws.cell(row=r, column=3, value="   CUSTO LÍQUIDO DE TESTE (consumo + descarte)").font = Font(bold=True, size=9)
c = ws.cell(row=r, column=10, value=f"=J{r-2}-J{r-1}")
c.font = Font(bold=True); c.number_format = '"R$" #,##0.00'
c.fill = PatternFill("solid", fgColor=AMAR); c.border = BOX
TOT_TESTE = r

# ---- bloco da verba
r += 3
ws.cell(row=r, column=1, value="VERBA MENSAL DE TESTE").font = Font(bold=True, size=13, color=VERDE)
r += 1
ws.cell(row=r, column=1,
  value="Dois jeitos de definir. Escolha um, preencha o amarelo e ignore o outro.").font = Font(size=9, italic=True, color="546E7A")
r += 2
VB = [
 ("A — PERCENTUAL DO FATURAMENTO", None, None, True),
 ("Faturamento médio mensal (R$)", 12879.10, "pedidos 000001 a 000005 (R$ 10.370,60) + 000007 (R$ 2.508,50). O 000006 não tem valor no sistema.", False),
 ("% destinado a P&D", 0.04, "3% é o patamar usual em alimentos; 5% se defende para quem ainda está montando portfólio. 4% é o meio.", False),
 ("VERBA DO MÊS", "=B{p1}*B{p2}", None, False),
 ("", None, None, True),
 ("B — DE BAIXO PARA CIMA, pelo que você realmente faz", None, None, True),
 ("Testes novos por mês", 3, "você tem 13 sabores em fila só na lista de 22/10", False),
 ("Calda por teste (kg)", 1.5, "seu volume de bancada tem sido 0,75 a 1,5 kg", False),
 ("Custo médio da calda (R$/kg)", 37.00, "média dos 16 testes que têm custo nesta aba", False),
 ("Fator de reteste", 1.5, "Latíssimo e Melagrana precisaram de segunda rodada — meio teste a mais, na média", False),
 ("   subtotal de calda", "=B{t1}*B{t2}*B{t3}*B{t4}", None, False),
 ("Insumo ou pasta nova por mês (R$)", 250.00, "pasta nova é o que custa de verdade: pistache R$ 450/kg, baunilha R$ 1.380/kg", False),
 ("VERBA PELA CONTA DE BAIXO", "=B{t5}+B{t6}", None, False),
 ("", None, None, True),
 ("CONTROLE DO MÊS", None, None, True),
 ("Mês de referência", "out/2026", None, False),
 ("Verba escolhida (R$)", 500.00, "as duas contas batem na mesma faixa: 4% dá R$ 515, a conta de baixo dá R$ 500. Arredondei para 500.", False),
 ("Gasto no mês", "=SUMIF($B${ini}:$B${fim},$B{pm},$J${ini}:$J${fim})", None, False),
 ("Saldo", '=IF(B{pv}="","escolha a verba acima",B{pv}-B{pg})', None, False),
]
larg2 = None
base = r
pos = {}
for i, (lab, val, obs, is_h) in enumerate(VB):
    rr = base + i
    pos[lab] = rr
    if is_h:
        if lab:
            ws.cell(row=rr, column=1, value=lab).font = Font(bold=True, size=10, color=ESCURO)
        continue
    ws.cell(row=rr, column=1, value=lab).font = Font(size=10)
    cell = ws.cell(row=rr, column=2)
    if isinstance(val, str) and val.startswith("="):
        f = (val.replace("{p1}", str(pos["Faturamento médio mensal (R$)"]))
                .replace("{p2}", str(pos["% destinado a P&D"]))
                .replace("{t1}", str(pos.get("Testes novos por mês", 0)))
                .replace("{t2}", str(pos.get("Calda por teste (kg)", 0)))
                .replace("{t3}", str(pos.get("Custo médio da calda (R$/kg)", 0)))
                .replace("{t4}", str(pos.get("Fator de reteste", 0)))
                .replace("{t5}", str(pos.get("   subtotal de calda", 0)))
                .replace("{t6}", str(pos.get("Insumo ou pasta nova por mês (R$)", 0)))
                .replace("{ini}", str(ini_t)).replace("{fim}", str(fim_t))
                .replace("{pm}", str(pos.get("Mês de referência", 0)))
                .replace("{pv}", str(pos.get("Verba escolhida (R$)", 0)))
                .replace("{pg}", str(pos.get("Gasto no mês", 0))))
        cell.value = f; cell.border = BOX; cell.font = Font(bold=True)
    else:
        cell.value = val; amarelo(cell)
    cell.number_format = "0.0%" if "%" in lab else '"R$" #,##0.00' if "R$" in lab else "General"
    if obs:
        o = ws.cell(row=rr, column=3, value=obs)
        o.font = Font(size=9, italic=True, color="546E7A")
r = base + len(VB) + 2
for t in ["Como ler o CUSTO LÍQUIDO: teste que foi aprovado e virou produto de venda não é despesa de P&D — o insumo voltou como receita. O que sai do seu bolso é o que você comeu, deu de degustação ou jogou fora.",
          "O que falta para esta aba virar controle de verdade: o volume de cada teste. Eu só tenho o que você declarou — 1,5 kg do pistache meia a meia, 750 g da base neutra, 1 kg do melagrana e 1 kg da canela. Os outros 22 estão com o quilo em branco porque chutar ali estragaria exatamente a média que você quer usar para fixar a verba. Preencha a coluna CALDA (kg) de cor amarela e o custo aparece sozinho.",
          "SEIS INSUMOS SEM PREÇO TRAVAM CINCO TESTES: Pasta Gusto Pop-Corn MEC3 (pipoca), Siriguela polpa, Goiaba, Pasta de Avelã 100%, Iogurte integral e Baunilha Vanilla Brasil. Enquanto não tiverem preço no cadastro, o custo desses testes não fecha — nem aqui nem no CMV se algum virar produto.",
          "Daqui para frente: toda vez que bater uma calda que não vai para venda, lance a linha aqui com os kg. Em dois meses a verba se define sozinha com o número real, em vez de benchmark."]:
    c = ws.cell(row=r, column=1, value=t)
    c.font = Font(size=9, italic=True, color="546E7A")
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = max(15, 13 * (len(t) // 120 + 1))
    r += 1

dv_r = DataValidation(type="list", formula1='"APROVADO,REPROVADO,PENDENTE,A FAZER"', allow_blank=True)
dv_d = DataValidation(type="list", formula1='"consumo próprio,degustação,descarte,virou venda,—"', allow_blank=True)
ws.add_data_validation(dv_r); ws.add_data_validation(dv_d)
dv_r.add(f"K{ini_t}:K{fim_t}")
dv_d.add(f"L{ini_t}:L{fim_t}")
ws.freeze_panes = f"A{ini_t}"

# ───────────────────────────────── 8. MOVIMENTO
ws = wb.create_sheet("MOVIMENTO")
r0 = head(ws, "MOVIMENTO DE POTES PRONTOS",
          "Uma linha por producao e uma linha por venda, com data a partir de 22/10/2026. Esta aba alimenta POTES PRONTOS automaticamente.")
larg(ws, [14, 16, 26, 12, 24, 40])
r = r0
cab(ws, r, ["DATA", "TIPO", "SABOR", "POTES", "CLIENTE / PEDIDO", "OBS"])
dv_t = DataValidation(type="list",
    formula1='"PRODUCAO,VENDA,PERDA,AMOSTRA,DEGUSTACAO,TESTE,HISTORICO"', allow_blank=True)
dv_s = DataValidation(type="list", formula1='"' + ",".join(SAB) + '"', allow_blank=True)
ws.add_data_validation(dv_t); ws.add_data_validation(dv_s)
r += 1
# 22/10 — tipo HISTORICO, nao VENDA: a contagem fisica de 22/10 e posterior a este
# pedido, entao estes 125 potes ja sairam do saldo contado. Lancar como VENDA
# descontaria duas vezes. Fica aqui como registro, fora da conta.
LANC = [("16/10/2026", "HISTORICO", s, n, "Pedido 000007 — O BECO",
         "anterior à contagem de 22/10 — não entra no saldo") for s, n in P7.items()]
for d, t, s, n, cl, o in LANC:
    amarelo(ws.cell(row=r, column=1, value=d))
    amarelo(ws.cell(row=r, column=2, value=t))
    amarelo(ws.cell(row=r, column=3, value=s))
    amarelo(ws.cell(row=r, column=4, value=n))
    ws.cell(row=r, column=4).number_format = "#,##0"
    amarelo(ws.cell(row=r, column=5, value=cl))
    amarelo(ws.cell(row=r, column=6, value=o))
    r += 1
for _ in range(120):
    for col in range(1, 7):
        amarelo(ws.cell(row=r, column=col))
    r += 1
dv_t.add(f"B{r0+1}:B{r-1}")
dv_s.add(f"C{r0+1}:C{r-1}")
ws.freeze_panes = f"A{r0+1}"

for s in wb.worksheets:
    s.sheet_view.showGridLines = False

OUT = "O Beco Gelato - Compras e Estoque.xlsx"
wb.save(OUT)
print("ok —", OUT)
print("abas:", ", ".join(s.title for s in wb.worksheets))
