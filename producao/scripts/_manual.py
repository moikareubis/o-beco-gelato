# -*- coding: utf-8 -*-
"""
MANUAL DO SISTEMA + REGISTRO DE DECISOES — O Beco Gelato
24/10/2026

Duas metades num documento:
  PARTE I  — o que o Balanceador de Receitas faz, como pensa e onde errar dói
  PARTE II — tudo que foi decidido, medido e corrigido nesta rodada de trabalho

Escrito para o Gabriel ler em seis meses e entender por que cada numero e o que e.
"""
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, KeepTogether)

HOJE = datetime.date(2026, 10, 24)

TINTA  = colors.HexColor("#1F1A17"); MARROM = colors.HexColor("#6B4A2F")
AREIA  = colors.HexColor("#F3EDE5"); LINHA  = colors.HexColor("#D8CEC1")
VERM   = colors.HexColor("#A3321E"); VERDE  = colors.HexColor("#2E6B4F")
CINZA  = colors.HexColor("#6E655C"); CREME  = colors.HexColor("#FBF6EF")
AMAR   = colors.HexColor("#FFF8E1")

S = lambda n, **k: ParagraphStyle(n, **k)
TIT = S("TIT", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=MARROM)
H1  = S("H1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=MARROM, spaceAfter=3)
SUB = S("SUB", fontName="Helvetica", fontSize=9.6, leading=13, textColor=CINZA, spaceAfter=9)
H2  = S("H2", fontName="Helvetica-Bold", fontSize=12.5, leading=15, textColor=MARROM, spaceBefore=12, spaceAfter=5)
H3  = S("H3", fontName="Helvetica-Bold", fontSize=10.3, leading=13, textColor=TINTA, spaceBefore=8, spaceAfter=3)
P   = S("P", fontName="Helvetica", fontSize=9.2, leading=13.2, textColor=TINTA, spaceAfter=4)
PS  = S("PS", fontName="Helvetica", fontSize=8, leading=11, textColor=CINZA, spaceAfter=3)
AL  = S("AL", fontName="Helvetica", fontSize=9, leading=12.6, textColor=VERM, spaceAfter=4)
OK  = S("OK", fontName="Helvetica", fontSize=9, leading=12.6, textColor=VERDE, spaceAfter=4)
CEL = S("CEL", fontName="Helvetica", fontSize=8.2, leading=10.6, textColor=TINTA)
CELB= S("CELB", fontName="Helvetica-Bold", fontSize=8.2, leading=10.6, textColor=TINTA)

story = []
def sp(h=4): story.append(Spacer(1, h*mm))
def p(t, st=P): story.append(Paragraph(t, st))
def h1(t, s=""):
    story.append(Paragraph(t, H1))
    if s: story.append(Paragraph(s, SUB))
def h2(t): story.append(Paragraph(t, H2))
def h3(t): story.append(Paragraph(t, H3))

def tab(dados, larg, cab=True, fonte=8.2, dest=None, bg=None):
    t = Table(dados, colWidths=larg, repeatRows=1 if cab else 0)
    st = [("FONT",(0,0),(-1,-1),"Helvetica",fonte), ("TEXTCOLOR",(0,0),(-1,-1),TINTA),
          ("VALIGN",(0,0),(-1,-1),"TOP"), ("TOPPADDING",(0,0),(-1,-1),3),
          ("BOTTOMPADDING",(0,0),(-1,-1),3), ("LEFTPADDING",(0,0),(-1,-1),5),
          ("RIGHTPADDING",(0,0),(-1,-1),5), ("LINEBELOW",(0,0),(-1,-2),0.4,LINHA)]
    if cab:
        st += [("FONT",(0,0),(-1,0),"Helvetica-Bold",fonte), ("BACKGROUND",(0,0),(-1,0),AREIA),
               ("TEXTCOLOR",(0,0),(-1,0),MARROM), ("LINEBELOW",(0,0),(-1,0),0.8,MARROM)]
    for r in (dest or []):
        st.append(("FONT",(0,r),(-1,r),"Helvetica-Bold",fonte))
    for r,c in (bg or []):
        st.append(("BACKGROUND",(0,r),(-1,r),c))
    t.setStyle(TableStyle(st))
    story.append(t)

def caixa(titulo, linhas, cor=AMAR, borda=MARROM):
    dentro=[[Paragraph("<b>"+titulo+"</b>", CELB)]]
    for l in linhas: dentro.append([Paragraph(l, CEL)])
    t=Table(dentro, colWidths=[165*mm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),cor),
        ("BOX",(0,0),(-1,-1),0.8,borda),("LEFTPADDING",(0,0),(-1,-1),7),
        ("RIGHTPADDING",(0,0),(-1,-1),7),("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    story.append(t); sp(3)

# ══════════════════════════════════ CAPA
sp(45)
p("O BECO GELATO", TIT)
sp(3)
p("Manual do sistema de balanceamento<br/>e registro de decisões", H1)
sp(6)
p("Documento interno · " + HOJE.strftime("%d/%m/%Y") +
  "<br/>Balanceador de Receitas · 537 mil caracteres · 236 funções · 139 ingredientes · 41 receitas", SUB)
sp(25)
caixa("PARA QUE SERVE ESTE DOCUMENTO", [
 "A PARTE I descreve o que o Balanceador faz, quais regras ele aplica e, principalmente, "
 "onde ele é fácil de usar errado. É o manual que faltava.",
 "A PARTE II registra o que foi decidido, medido e corrigido na rodada de trabalho de "
 "21 a 24 de outubro de 2026 — com o motivo de cada número, não só o número.",
 "Onde um dado é estimativa minha e não medição sua, está dito na linha."], CREME)
story.append(PageBreak())

# ══════════════════════════════════ PARTE I
h1("PARTE I · O SISTEMA", "Balanceador de Receitas — arquivo HTML único, roda offline no navegador, "
   "salva tudo no próprio aparelho")

h2("As dez telas")
tab([["TELA","O QUE RESOLVE"],
 ["Início","Painel de entrada: estoque de potes prontos, produção do dia, atalhos."],
 ["Bancada","O solver. Você diz o sabor e os alvos, ele monta a calda procurando a combinação "
            "que cai dentro das faixas. É a tela de criar receita nova."],
 ["Receita","O editor linha por linha. Métricas ao vivo: sólidos, gordura, proteína, açúcares, "
            "POD, PAC, janela de consumo, custo por quilo."],
 ["Custos","CMV por pote, food cost, margem, preço por canal e imposto do Simples."],
 ["Ingredientes","As 139 fichas: nutricional completa, custo por quilo, POD, PAC, sólidos, "
                 "açúcar adicionado e nome de rótulo."],
 ["Salvas","As 41 receitas gravadas, com as 7 do lançamento marcadas."],
 ["Estoque de insumos","Saldo por insumo e necessidade calculada a partir de um plano de produção."],
 ["Rótulo","Monta a lista de ingredientes em ordem decrescente (RDC 727), alérgenos, "
           "selos e a tabela nutricional do pote."],
 ["Dados","Exportar e importar o estado inteiro — é o seu backup."],
 ["Produção 2","Histórico de lotes e classificação de sabores."]], [34*mm,131*mm])
sp(2)
p("Quatro telas foram apagadas em 22/10 a seu pedido — Painel, Investimento, Produção &amp; Vitrine e "
  "Lançamentos. Os dados continuam no arquivo: só as telas saíram. O sistema virou ferramenta de "
  "receita, e o resto migrou para planilha.", PS)

h2("Como o motor pensa")
h3("Normalização por 1.000 g")
p("Toda métrica é calculada sobre 1 kg de calda. Se você jogar uma receita de 2.947 g sem normalizar, "
  "os números saem absurdos — sólidos de 92%, POD de 661. Não é bug, é a conta sendo feita sobre a "
  "escala errada.")

h3("POD e PAC")
p("<b>POD</b> é poder adoçante, <b>PAC</b> é poder anticongelante, ambos na escala em que a sacarose "
  "vale 100. O alvo da casa é <b>POD 170, faixa aceitável 160 a 180</b>. O PAC define onde o gelato "
  "fica servível: a <b>janela de consumo</b> é a faixa de temperatura em que 79 a 84% da água está "
  "congelada. Abaixo disso é espuma, acima é pedra.")
p("Gelato sem açúcar carrega mais anticongelante que um gelato normal, e é por isso que a janela da "
  "linha inteira fica entre −13 e −20 °C. Na prática isso é uma vantagem: o pote sai do freezer de "
  "casa já no ponto, sem os cinco minutos de espera.", PS)

h3("Açúcares: o campo técnico e o campo de rótulo")
caixa("A DISTINÇÃO QUE MAIS IMPORTA NO SISTEMA", [
 "<b>acucares</b> — campo TÉCNICO. Soma açúcar + poliol. É o que alimenta POD e PAC. "
 "Serve para formular.",
 "<b>acucarRotulo</b> — o que a ANVISA chama de açúcares totais. NÃO inclui poliol. "
 "É o que vai na tabela nutricional.",
 "<b>acucarAdd</b> — quanto de açúcar ADICIONADO entrou via insumo. É o que decide o selo.",
 "No Sorbet Morango a diferença é de 5,93 contra 16,29 — dez pontos de poliol. Mandar o técnico "
 "para a nutricionista produziria um rótulo declarando quase três vezes o açúcar real."], AMAR)

h3("A linha comercial não é o campo família")
p("<b>família</b> é a família de formulação e serve para escolher os alvos: 1 creme/leite, "
  "2 fruta/água, 3 proteica, 4 creme alcoólico, 5 sorbet alcoólico, 6 sorbet de chocolate.")
p("<b>linhaBeco()</b> é o que decide a linha de venda: família 2 vira <b>Fresh</b>; fora disso, "
  "proteína igual ou acima de 7,5% vira <b>Boost</b>, e o resto vira <b>Special</b>. "
  "O Pistache é família 3 e linha Special — é o exemplo que mostra que os dois conceitos não coincidem.")

h3("Alvos por linha")
tab([["LINHA","SÓLIDOS","ÁGUA","GORDURA","PROTEÍNA","AÇÚCARES"],
 ["Fresh (sorbet)","28–34%","66–72%","0–1,5%","0–2%","9–21%"],
 ["Special (creme ZL)","32–40%","60–68%","6–12%","2–7%","10–19%"],
 ["Boost (proteico)","36–40%","60–64%","4–6%","8–10%","10–20%"]],
 [36*mm,24*mm,22*mm,25*mm,25*mm,28*mm])

h3("Limites que vêm do curso do Lulo")
tab([["LIMITE","VALOR","POR QUE"],
 ["Proteína máxima","10%","acima disso a textura areia"],
 ["Whey","55 g/kg","limite de solubilidade e sabor"],
 ["Inulina","50 g/kg","acima disso dá desconforto intestinal"],
 ["Eritritol","40 g/dia","limiar de tolerância digestiva"],
 ["Maltitol","20 g/porção","idem, e é o poliol mais laxativo da lista"],
 ["Estévia","0,9 g/kg","acima disso aparece retrogosto"],
 ["Gordura na Boost","4–5% ideal, 6% máximo","gordura compete com proteína pela estrutura"]],
 [42*mm,38*mm,80*mm])

h2("Dois mecanismos de finalização, e a diferença custa dinheiro")
caixa("O ERRO QUE CUSTOU R$ 0,77 POR POTE DE CAFÉ", [
 "<b>finAdicional = true</b> (Alfajor): o biscoito vai POR CIMA do pote cheio. Ele SOMA. "
 "O pote tem 135 g de gelato mais 15 g de biscoito = 150 g de produto.",
 "<b>sem finAdicional</b> (Café): a mescla é ripada DENTRO do pote. Ela DESLOCA calda. "
 "O pote tem 140 g de produto, dos quais 125,6 g de calda e 14,4 g de mescla.",
 "Eu tratei os dois do mesmo jeito e o Café fechou em 156,1 g num pote de 140 g. "
 "Só apareceu quando conferi a planilha de CMV contra o número do sistema."], AMAR)

h2("Gramatura — o número que mais se propaga")
p("A massa do pote entra em CMV, receituário, lista de compras, consumo de embalagem, proteína por "
  "pote e rótulo. Mudou quatro vezes: 130 g de chute inicial, 120 g quando você pesou um pote de "
  "morango em 07/10, 135 g de estimativa minha em 09/10, e <b>140 g a partir da medição de 35 potes "
  "em 16/10</b>.")
tab([["SABOR","GELATO","PRODUTO","OBSERVAÇÃO"],
 ["Café, Pistache, Torta, Brigadeiro, Manga","140 g","140 g","padrão da casa"],
 ["Alfajor","135 g","150 g","biscoito de 15 g por cima"],
 ["Sorbet Morango","120 g","120 g","gramatura própria — o pote não fecha 140 g"]],
 [66*mm,22*mm,22*mm,55*mm], dest=[3])
sp(2)
p("Densidades medidas em 16/10, gelato em pote de 150 ml: Café 0,963 · Torta 0,961 · Manga 0,949 · "
  "Brigadeiro 0,909 · Alfajor 0,903 · Pistache 0,884 · Sorbet Morango 0,772.", PS)

h2("A suíte de testes")
p("<b>449 testes</b> rodam contra o arquivo e contra um baseline de 12/10. Comando: "
  "<font face='Courier'>node testes-balanceador.js</font>. Exige node e jsdom.")
p("Ela existe porque este sistema tem 236 funções entrelaçadas e mudança de ingrediente se propaga "
  "para lugares que ninguém lembra. Já pegou: poliol entrando em açúcar de rótulo, selo aparecendo "
  "em receita com açúcar adicionado, alvo de sólidos não-gordura ficando suspenso em fórmula sem "
  "açúcar, e a gramatura por sabor.")

h2("O que você pode pedir ao sistema")
tab([["PEDIDO","O QUE ELE DEVOLVE"],
 ["Monte uma calda de X","O solver da Bancada procura a combinação que cai nos alvos da família, "
  "respeitando os limites do Lulo. Você define a arquitetura do sabor; ele resolve as quantidades."],
 ["Escale esta receita para N potes ou N kg","Reescala mantendo proporção, já com a perda de processo "
  "e a gramatura certa daquele sabor."],
 ["Está na janela?","Calcula a faixa de temperatura em que o gelato fica servível e avisa se a "
  "receita cai fora."],
 ["Quanto custa?","CMV por pote separando insumo e embalagem, food cost, margem por canal, "
  "imposto do Simples."],
 ["Posso declarar o selo?","Verifica açúcar adicionado por insumo e devolve os selos que passam, "
  "os que quase passam e o que acende lupa frontal."],
 ["Monte o rótulo","Lista de ingredientes em ordem decrescente conforme a RDC 727, alérgenos "
  "herdados de cada insumo, e a tabela nutricional do pote."],
 ["O que preciso comprar?","Explode o plano de produção em necessidade por insumo, com o mix "
  "aberto nos cinco componentes que você compra de fato."],
 ["Audite esta receita","Aponta ingrediente sem preço, sem nome de rótulo, ingrediente composto "
  "sem lista interna, e métrica fora da faixa."],
 ["Troque o ingrediente X por Y","Recalcula tudo e mostra o que mudou — o que é a única forma "
  "honesta de decidir uma substituição."]], [48*mm,117*mm])

h2("As sete receitas do lançamento")
# 24/10 — ESTA TABELA FOI LIDA DO SISTEMA, NAO ESCRITA DE MEMORIA.
# Na primeira versao eu digitei os sete de cabeca e cinco estavam errados: o Pistache
# com POD 161 quando e 148, o Cafe com 167 quando e 180, o Alfajor com solidos 38,9
# quando sao 37,1. Num documento de referencia isso e pior que nao existir — e
# exatamente a reclamacao dele de que "toda hora a receita vem de uma forma".
tab([["SABOR","LINHA","FAM","SÓL.","GORD.","PROT.","POD","PAC","JANELA °C","R$/kg"],
 ["Sorbet Morango","Fresh","2","31,9%","0,4%","0,7%","232","388","−14,8 a −19,4","21,31"],
 ["Manga com Maracujá","Fresh","2","32,0%","0,4%","0,8%","227","389","−14,8 a −19,4","26,19"],
 ["Torta de Limão","Special","1","39,4%","6,5%","3,6%","170","352","−15,0 a −19,7","44,60"],
 ["Alfajor","Special","1","37,1%","6,1%","5,4%","148","369","−15,2 a −20,0","33,75"],
 ["Pistache","Special","3","38,2%","9,5%","6,2%","148","330","−13,8 a −18,2","60,55"],
 ["Café Proteico","Boost","3","39,3%","4,5%","10,0%","180","354","−15,1 a −19,8","40,61"],
 ["Brigadeiro Proteico","Boost","3","40,6%","5,4%","10,1%","161","332","−14,5 a −19,0","41,09"]],
 [40*mm,18*mm,10*mm,15*mm,15*mm,15*mm,13*mm,13*mm,28*mm,15*mm], fonte=7.6)
sp(2)
p("<b>Dois sabores estão fora do alvo de POD 160–180:</b> Pistache e Alfajor em 148, doze pontos "
  "abaixo do piso. Os dois estão aprovados em bancada e vendendo, o que significa que ou o alvo é "
  "conservador para sabores de pasta, ou os dois estão menos doces do que o resto da linha de "
  "propósito. O Café está no teto, em 180. Vale saber antes de mexer em qualquer um dos três.", AL)
sp(1)
p("Café e Brigadeiro compartilham a mesma base proteica — é uma calda única que se diferencia só na "
  "saborização. Por 1 kg de base: leite ZL 692,4 · Base MEC Protein 130 · leite em pó desnatado 120 · "
  "glicerol 30 · polidextrose 20 · Cremobene 3,1 · sal 1 · estévia 0,6.", PS)
p("<b>Mix oficial</b>, em 999 partes: polidextrose 528 · maltitol 224 · eritritol 163 · inulina 81 · "
  "estévia 3. É feito na casa, então para compras ele entra explodido nos cinco componentes.", PS)

h2("Onde o sistema é fácil de usar errado")
tab([["ARMADILHA","O QUE ACONTECE"],
 ["Não normalizar por 1.000 g","Métricas absurdas. Sempre normalize antes de chamar o motor."],
 ["Usar o campo acucares no rótulo","Declara poliol como açúcar. Use acucarRotulo."],
 ["Mapear linha pelo campo família","Pistache aparece como Boost quando é Special."],
 ["Assumir 140 g para todo sabor","Morango é 120 g e Alfajor é 135 + 15."],
 ["Confiar no saldo de ESTOQUE_INS","Treze insumos usados em receita estão com saldo zero por falta "
  "de lançamento, não por falta real."],
 ["Achar que existe cadastro de fornecedor","Não existe. O sistema nunca teve esse campo."]],
 [48*mm,117*mm])
story.append(PageBreak())

# ══════════════════════════════════ PARTE II
h1("PARTE II · O QUE FOI DECIDIDO", "Rodada de 21 a 24 de outubro de 2026")

h2("1 · Planilha de compras e estoque")
p("Criada a planilha <b>O Beco Gelato — Compras e Estoque.xlsx</b>, com oito abas: Leia-me, Plano, "
  "Fornecedores, Estoque de Insumos, Embalagem, Potes Prontos, Testes e Movimento. Amarelo é campo "
  "seu, branco é fórmula, cinza vem do Balanceador.")
p("<b>O que a planilha revelou:</b> o sistema nunca teve cadastro de fornecedor. Oito linhas foram "
  "preenchidas com o que apareceu em conversa, cada uma marcada com a procedência — nota fiscal, "
  "ficha técnica, menção de passagem ou cotação. As outras quinze ficaram em branco de propósito.")

h2("2 · Contagem física de 22/10 — 325 potes, R$ 6.496,90")
tab([["SABOR","POTES","SABOR","POTES"],
 ["Manga com Maracujá","60","Café Proteico","40"],
 ["Torta de Limão","58","Alfajor","38"],
 ["Brigadeiro Proteico","51","Sorbet Morango","32"],
 ["Pistache","46","TOTAL","325"]], [45*mm,20*mm,45*mm,20*mm], dest=[4])
sp(3)
caixa("DOIS FATOS QUE SÓ A CONTAGEM REVELOU", [
 "<b>188 potes de produção não lançada.</b> Havia 262 potes em 13/10; menos os 125 do pedido 000007 "
 "daria 137, e há 325. Você produziu 188 potes em nove dias e nada disso existia em registro. "
 "O Alfajor é o caso visível: estava em zero e agora tem 38.",
 "<b>O morango não fecha.</b> Eram 53, saíram 15, deveria haver 38 — e há 32. Faltam 6 potes. "
 "Degustação, amostra, perda ou venda não registrada: não há como saber qual."], AMAR)
p("A contagem zera a conta: por ser posterior ao pedido 000007, aquelas 125 saídas viraram tipo "
  "HISTÓRICO na aba Movimento, para não serem descontadas duas vezes. Toda contagem nova funciona assim.", PS)

h2("3 · Gramatura do morango corrigida para 120 g")
p("Você mediu: o pote de morango chega a 120 g e não fecha 140. Gravado como "
  "<font face='Courier'>potePeso:120</font> na receita; nenhum outro sabor foi afetado.")
tab([["O QUE MUDOU","ANTES","DEPOIS"],
 ["CMV do pote de morango","R$ 4,75","R$ 4,31"],
 ["Margem a R$ 18,70","73,8%","77,0%"],
 ["Morango por pote","91,0 g","77,8 g"],
 ["Morango no plano de 30 potes","2.723 g","2.334 g"]], [70*mm,32*mm,32*mm])
sp(3)
caixa("A SUÍTE TINHA 445 TESTES E NENHUM COBRIA ISSO", [
 "Gravei os 120 g, rodei a suíte e os 445 passaram sem piscar: todos usavam o pote global, nenhum "
 "testava a massa por receita. A gramatura é o número que mais se propaga neste projeto e estava "
 "sem trava.",
 "Escrevi quatro testes. Um deles passou de primeira por motivo errado — a função gelatoPote não "
 "estava na lista de exportação do harness, então o guard engolia o teste e ele ficava verde sem "
 "testar nada. Corrigido e validado ao contrário: removi o potePeso de uma cópia e a suíte acusou "
 "as duas falhas corretas. São 449 testes agora."], AMAR)

h2("4 · CMV por linha, insumo e embalagem separados")
p("Embalagem igual nos sete: R$ 1,67 por pote — pote com tampa R$ 1,07, colher R$ 0,26, lacre R$ 0,34. "
  "Toda a diferença entre sabores está no insumo.")
tab([["LINHA · SABOR","GELATO","INSUMO","EMBAL.","CMV","MARGEM","FOOD COST"],
 ["FRESH · R$ 18,70","","","","","",""],
 ["Manga com Maracujá","140 g","R$ 3,78","R$ 1,67","R$ 5,45","70,9%","29,1%"],
 ["Sorbet Morango","120 g","R$ 2,64","R$ 1,67","R$ 4,31","77,0%","23,0%"],
 ["SPECIAL · R$ 20,50","","","","","",""],
 ["Pistache","140 g","R$ 8,74","R$ 1,67","R$ 10,41","49,2%","50,8%"],
 ["Torta de Limão","140 g","R$ 6,44","R$ 1,67","R$ 8,11","60,5%","39,5%"],
 ["Alfajor","135 g","R$ 5,29","R$ 1,67","R$ 6,96","66,0%","34,0%"],
 ["BOOST · R$ 20,50","","","","","",""],
 ["Café Proteico","140 g","R$ 6,66","R$ 1,67","R$ 8,33","59,4%","40,6%"],
 ["Brigadeiro Proteico","140 g","R$ 5,93","R$ 1,67","R$ 7,60","62,9%","37,1%"]],
 [42*mm,17*mm,21*mm,21*mm,21*mm,21*mm,22*mm], dest=[1,4,8],
 bg=[(1,AREIA),(4,AREIA),(8,AREIA)])
sp(3)
p("<b>O Pistache é o problema isolado.</b> Food cost de 50,8% contra 34,0% do Alfajor, que está na "
  "mesma linha e no mesmo preço. Ele sozinho derruba a média da Special (58,6%) abaixo da Boost "
  "(61,1%) — ou seja, a linha dita especial é hoje menos rentável que a proteica.")
p("<b>A embalagem pesa mais no Fresh:</b> 38,8% do CMV do morango contra 16,0% do pistache. "
  "Toda redução de custo de embalagem vale mais na linha Fresh.")
p("Isto é CMV de insumo e embalagem apenas. Não tem mão de obra, energia, frete, imposto nem rateio "
  "dos R$ 5.000 de custo fixo mensal. A margem de contribuição real é bem menor.", PS)

h2("5 · Cotação de polióis — simulação")
p("Eritritol R$ 14,75/kg (Huakang), Maltitol R$ 17,95/kg (Yusweet), Polidextrose R$ 12,85/kg "
  "(Shandong Bailong), sacos de 25 kg, <b>FOB Recife</b>. Com o pote a R$ 0,73:")
tab([["","HOJE","COTAÇÃO","QUEDA"],
 ["Eritritol","R$ 53,76","R$ 14,75","−73%"],
 ["Maltitol","R$ 37,78","R$ 17,95","−52%"],
 ["Polidextrose","R$ 28,92","R$ 12,85","−56%"],
 ["Mix oficial","R$ 49,13","R$ 29,83","−39%"],
 ["Embalagem por pote","R$ 1,67","R$ 1,33","−20%"]], [52*mm,30*mm,30*mm,24*mm], dest=[4,5])
sp(3)
p("Economia média de <b>R$ 0,68 por pote</b>, mas assimétrica: Fresh ganha R$ 0,84 e R$ 0,96, "
  "Boost só R$ 0,38 — a base proteica usa pouco mix. <b>A cotação não resolve o Pistache</b>, "
  "que continua a 46,9% de food cost porque o custo dele é a pasta a R$ 450/kg.")
caixa("O FOB É O FURO DA COTAÇÃO", [
 "O frete não está nesses preços. Diluído nos 2.459 potes que os 75 kg atendem: frete de R$ 400 "
 "deixa R$ 0,52 de economia, R$ 800 deixa R$ 0,35, R$ 1.500 deixa R$ 0,07.",
 "Mesmo no pior caso não se perde dinheiro, mas o ganho pode virar metade do anunciado. "
 "Peça a cotação do frete Recife–Salvador para 75 kg antes de fechar.",
 "<b>A polidextrose é o limitante:</b> 25 kg dela rendem 2.459 potes, contra 7.581 do maltitol e "
 "9.622 do eritritol. Comprar um saco de cada deixaria maltitol e eritritol parados por mais de um "
 "ano — faz mais sentido dois ou três sacos de polidextrose e um de cada dos outros.",
 "Os 75 kg custam R$ 1.138,75 contra R$ 3.011,50 de hoje: R$ 1.872,75 de economia na compra, "
 "cerca de 4 meses no ritmo atual. Você está no Simples, então o ICMS incluso é custo mesmo — "
 "não há crédito a aproveitar."], AMAR)

h2("6 · Potes novos — Natucopos")
tab([["ITEM","QTD","UNITÁRIO","TOTAL","FRETE"],
 ["Pote (proposta 08/10)","1.000","R$ 0,4606","R$ 460,56","grátis"],
 ["Tampa de papel (08/10)","6.000","R$ 0,2665","R$ 1.599,24","grátis"],
 ["Pote (proposta 23/10)","5.000","R$ 0,3504","R$ 1.752,20","FOB"],
 ["TOTAL","","","R$ 3.812,00","6x de R$ 635,33"]],
 [48*mm,20*mm,26*mm,26*mm,34*mm], dest=[4])
sp(3)
p("<b>Pote + tampa sai a R$ 0,635</b>, não R$ 0,73 — você foi conservador. A embalagem completa cai "
  "de R$ 1,67 para R$ 1,235, economia de R$ 0,435 por pote, R$ 2.610 sobre os 6.000. Com frete de "
  "R$ 580 o pote+tampa chega exatamente nos R$ 0,73, então seu número não foi chute: foi "
  "conservadorismo bem calibrado.")

h3("Mas são três estoques de 2.000, não 6.000 fungíveis")
p("Os potes são de três linhas, 2.000 cada, e as tampas de três cores, uma por linha. Pote de uma "
  "linha não serve na outra. Contra o que você vende de verdade — 643 potes em seis pedidos:")
tab([["LINHA","DEMANDA REAL","COMPROU","2.000 POTES COBREM"],
 ["Fresh","26,1%","33,3%","7.655 potes de produção"],
 ["Special","36,5%","33,3%","5.472 potes de produção"],
 ["Boost","37,3%","33,3%","5.358 potes de produção"]], [34*mm,38*mm,30*mm,60*mm])
sp(3)
p("<b>A divisão igual está melhor do que parecia.</b> O gargalo é o Boost e a produção trava em "
  "5.358 potes, sobrando 642 — R$ 408, 11% da compra. Para uma divisão feita no escuro, é pouco.")
caixa("MAS O ALFAJOR PODE INVERTER ISSO", [
 "O Alfajor é Special e só existe há um pedido. No 000007, o único em que apareceu, a Special foi de "
 "36% para 48% da venda. Se esse for o novo patamar, a Special trava a produção em 4.167 potes e o "
 "imobilizado salta de 642 para 1.833 potes — de 11% para 31% da compra, de R$ 408 para R$ 1.164.",
 "<b>O pedido dos 5.000 tem 30 dias de produção.</b> Dá tempo de mudar a divisão das cores. Pelo mix "
 "agregado, 1.600 Fresh / 2.200 Special / 2.200 Boost liberaria 540 potes a mais de produção útil.",
 "A diferença entre 11% e 31% depende de uma coisa que só você sabe: se o Alfajor veio para ficar."], AMAR)

h3("O lacre é o gargalo absoluto")
tab([["ITEM","ESTOQUE","COBERTURA A ~600 POTES/MÊS"],
 ["Potes (700 antigos + 6.000)","6.700","11,2 meses"],
 ["Tampas de papel","6.000","10,0 meses"],
 ["Colheres","4.217","7,0 meses"],
 ["Lacres de sabor","717","1,2 mês"]], [60*mm,30*mm,60*mm], dest=[4],
 bg=[(4,colors.HexColor("#FFEBEE"))])
sp(3)
p("A tampa colorida identifica a <b>linha</b>, mas a Special tem três sabores dentro dela — ainda é "
  "preciso distinguir Pistache de Torta de Alfajor. Com 30 dias de produção mais 15 de entrega em "
  "qualquer pedido novo, o lacre precisa ser pedido esta semana. A colher vence em sete meses e vale "
  "no mesmo pedido, para não pagar frete duas vezes.")
story.append(PageBreak())

h2("7 · Receitas novas desta rodada")
h3("Gelato de Canela — pasta PreGel ST-58472 · 1 kg")
tab([["INGREDIENTE","g/kg"],["Leite zero lactose integral","617"],["Mix oficial","150"],
 ["Creme de leite 35% ZL","102"],["Leite em pó desnatado Batavo","60"],
 ["Pasta canela PreGel","30"],["Polidextrose","20"],["Glicerol","15"],
 ["Cremobene Premium","6"]], [70*mm,22*mm])
sp(2)
p("Sólidos 38,5% · gordura 6,5% · proteína 4,6% · POD 169 · PAC 349 · janela −14,7 a −19,3 °C · "
  "R$ 24,83/kg sem a pasta. É a arquitetura da Torta de Limão com canela no lugar do limão — "
  "POD 169 contra 170 e PAC 349 contra 352.")
p("<b>Método:</b> a pasta tem pH 1,5. Misture a seco o mix, o leite em pó, a polidextrose e o "
  "Cremobene; dissolva no leite com o creme a 40 °C; pasteurize a 82–85 °C; fora do fogo o glicerol; "
  "resfrie a 4 °C; e só com a calda já fria entre a pasta com o mixer. Ácido forte em leite quente "
  "com 4,6% de proteína coagula.")
p("<b>Não serve para venda:</b> 1,50 g de açúcar adicionado por 100 g. A canela real é só 4% da "
  "pasta — a 30 g/kg dá 1,2 g por quilo de calda, o resto do sabor vem dos aromas.", AL)

h3("Gelato de Pipoca — pó PreGel ST-40341 · 1 kg")
tab([["INGREDIENTE","ORIGINAL","COM MENOS CREME"],
 ["Leite zero lactose integral","611","639"],["Mix oficial","150","150"],
 ["Creme de leite 35% ZL","110","60"],["Leite em pó desnatado Batavo","58","80"],
 ["Pop Corn Industrial PreGel","30","30"],["Polidextrose","20","20"],
 ["Glicerol","15","15"],["Cremobene Premium","6","6"]], [70*mm,30*mm,38*mm])
sp(2)
p("Versão com menos creme: sólidos 39,60% · gordura 5,33% · POD 166 · PAC 362 · R$ 23,93/kg. "
  "A gordura cai de 6,95% para 5,33%, que é exatamente onde o Brigadeiro Proteico já está (5,44%) "
  "e você validou em bancada. Em pipoca, sabor de cereal torrado, gordura menor até ajuda.")
p("<b>Dois impedimentos para venda:</b> contém lactose (o último ingrediente é leite em pó desnatado) "
  "e tem 0,399 g de açúcar adicionado por 100 g. Na linha Boost, que já tem lactose, só o açúcar "
  "travaria. O sódio deu 117,8 mg/100 g — abaixo do Café (155) e do Brigadeiro (168): o sal da ficha "
  "assusta mas a 30 g/kg dilui.", AL)

h3("Sorbet Morango — escalas")
tab([["ALVO","CALDA","MORANGO","MIX","ÁGUA","ERITR.","GLIC.","PASTA","CREMOB."],
 ["21 potes","2.598 g","1.634","598","255","39","39","26","8"],
 ["30 potes","3.711 g","2.334","854","364","56","56","37","11"],
 ["3 kg de fruta","4.769 g","3.000","1.097","467","72","72","48","14"]],
 [26*mm,22*mm,22*mm,18*mm,18*mm,16*mm,16*mm,16*mm,18*mm])
sp(2)
p("Com 3 kg de morango dá <b>38 potes</b> de 120 g. Todas as escalas já incluem a perda de 3%.")

h2("8 · Verba mensal de teste — R$ 500")
p("Levantados 26 testes de bancada. O custo por quilo existe para 16 deles porque as receitas estão "
  "cadastradas; o volume só existe para quatro, que são os que você declarou em voz alta. Os outros "
  "22 ficaram com o quilo em branco de propósito — chutar ali estragaria justo a média que serve "
  "para fixar a verba.")
p("A verba de R$ 500 veio de dois caminhos independentes que bateram no mesmo lugar: 4% do "
  "faturamento dá R$ 515, e a conta de baixo para cima — 3 testes de 1,5 kg a R$ 37/kg, fator 1,5 de "
  "reteste, mais R$ 250 de pasta ou insumo novo — dá R$ 500.")
caixa("TESTE APROVADO QUE VIROU VENDA NÃO É DESPESA DE P&D", [
 "Oito das 26 linhas são dessa categoria: Torta v3, chocolate proteico, os três Cremobene, Alfajor. "
 "O insumo voltou como receita. O que sai do bolso é o que foi comido, dado em degustação ou jogado "
 "fora — e é isso que a linha de custo líquido separa.",
 "<b>Seis insumos sem preço travam cinco testes:</b> Pasta Gusto Pop-Corn, siriguela, goiaba, pasta "
 "de avelã 100%, iogurte integral e baunilha Vanilla Brasil."], CREME)

h2("9 · Correções que eu precisei fazer nesta rodada")
tab([["O QUE EU ERREI","COMO APARECEU"],
 ["Disse que 0,465 g/100 g de açúcar adicionado ficava “raspando no limite de 0,5”",
  "Misturei duas alegações. O limite de 0,5 é para “zero açúcares”, que fala de açúcares TOTAIS — e "
  "seu gelato nunca se encaixa nisso porque a lactose já põe 8 a 10 g. A sua alegação é “sem adição "
  "de açúcares”, e essa tem TOLERÂNCIA ZERO. O morango com Pasta Fragola não pode carregar o selo."],
 ["Dimensionei a receita de 21 potes de morango a 140 g por pote",
  "Mesmo tendo a densidade 0,772 medida na mão. Renderia 24 ou 25 potes. Você corrigiu."],
 ["A suíte passava um teste de gramatura sem testar nada",
  "gelatoPote não estava na lista de exportação do harness, então o guard retornava verdadeiro."],
 ["Minha reconstrução dos testes de bancada estava furada",
  "Eu tinha 13, você lembrou de 12 e 10 eu não tinha. Pior: cajú e goiaba eu havia marcado como "
  "“nunca foi à bancada” e você fez os dois. Eu inferia de onde o assunto aparecia na conversa, e "
  "assunto não é lote batido."]], [55*mm,110*mm])

h2("10 · O que fica em aberto")
tab([["PENDÊNCIA","POR QUE IMPORTA"],
 ["Frete Recife–Salvador para 75 kg","Única variável que ainda mexe materialmente na cotação"],
 ["Divisão das cores dos 5.000 potes","Janela de 30 dias para mudar; decide 11% ou 31% imobilizado"],
 ["Pedido de lacre e colher","Lacre tem 1,2 mês; prazo de reposição é 45 dias"],
 ["Preço do balde de canela e do saco de pipoca","Sem eles o CMV dessas duas não fecha"],
 ["Seis insumos sem preço","Travam o custeio de cinco testes"],
 ["Overrun do morango","A manga prova que a calda aguenta 0,949; o morango dá 0,772"],
 ["Um pote pesado após a batida","Separa “a perda é menor que 3%” de “o envase está leve”"],
 ["O morango entrega 120 g ao mesmo preço da manga","Decisão comercial sua, não técnica"],
 ["Mescla do Brigadeiro","Campo em branco; 764 g de granulado em estoque sem cadastro"],
 ["75 °C de bancada contra 82–85 °C do receituário","Divergência nunca resolvida"]],
 [62*mm,103*mm])

sp(6)
p("— fim —", PS)

# ══════════════════════════════════ RENDER
def rodape(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 7.2); canv.setFillColor(CINZA)
    canv.drawString(22*mm, 12*mm, "O Beco Gelato · Manual do sistema e registro de decisões · " +
                    HOJE.strftime("%d/%m/%Y"))
    canv.drawRightString(188*mm, 12*mm, "pág. %d" % doc.page)
    canv.setStrokeColor(LINHA); canv.setLineWidth(0.4)
    canv.line(22*mm, 16*mm, 188*mm, 16*mm)
    canv.restoreState()

OUT = "O Beco Gelato - Manual do Sistema e Decisoes.pdf"
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=22*mm, rightMargin=22*mm,
                      topMargin=18*mm, bottomMargin=22*mm, title="O Beco Gelato — Manual do Sistema e Decisões",
                      author="O Beco Gelato")
doc.addPageTemplates([PageTemplate(id="n",
    frames=[Frame(22*mm, 22*mm, 166*mm, 253*mm, id="f")], onPage=rodape)])
doc.build(story)
print("ok —", OUT)
