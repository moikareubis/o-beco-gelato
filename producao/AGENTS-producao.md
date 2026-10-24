# O BECO GELATO — instruções para o agente

Leia este arquivo inteiro antes de mexer em qualquer coisa. Ele existe porque eu
(o agente anterior) cometi cada um dos erros listados aqui, e vários custaram
dinheiro ou foram para a mão de uma funcionária em papel impresso.

Última atualização: 24/10/2026.

---

## 1. O QUE É ESTE PROJETO

O Beco Gelato é uma marca de gelato de pote **zero lactose e sem adição de
açúcares**, operada por **Gabriel Sampaio** em Lauro de Freitas / Salvador (BA).
Produto na rua desde meados de setembro de 2026. Sete sabores no portfólio,
três linhas comerciais, venda em atacado para pontos parceiros e venda direta.

A fonte de verdade de tudo que é formulação é **um único arquivo HTML**:
`sistema/Balanceador de Receitas.html` — 537 mil caracteres, 236 funções, roda
offline no navegador, salva em localStorage. Não é um protótipo: é o sistema de
produção da empresa.

---

## 2. AS REGRAS DO GABRIEL — cite verbatim, não reinterprete

Estas frases são dele. Elas não são preferências negociáveis; são o contrato.

> "nenhum gelato pode ter retrogosto de remedio, amargor, ou gosto ruim"

> "a minha linha proteica contém lactose, só não contém na classico saudaveis e
> linha leve"

> "em momento nenhum eu falei que eu tinha problema com óleo de palma, com palma
> no rótulo, com palmiste, com glúten, isso é você que está trazendo"

> "Para de querer mudar a receita sem eu pedir."

> "quando eu digo que não quero mexer nela, é que eu não quero mudar a base.
> Retirar a base pronta e criar uma nova, entende? Mas posso mexer na quantidade."

> "NÃO VAI BISCOTINO, O BISCOITO É ADICIONADO POR FORA PRA FINALIZAR"

> "contanto que não entre lupa"

O que isso significa na prática:

- **As únicas restrições reais da linha são zero lactose e zero açúcar adicionado.**
  Glúten, óleo de palma e palmiste nunca foram restrições. Se você inventar uma
  restrição que ele não declarou, ele vai corrigir — e com razão.
- **Ele define a arquitetura do sabor; você balanceia dentro dela.** Mexer na
  quantidade é permitido. Trocar a base por outra não é.
- **Bancada ganha de tabela, sempre.** Se ele aprovou na bancada e a tabela
  discorda, a tabela está errada ou o alvo é conservador. Não "corrija" receita
  aprovada por argumento de planilha.
- **Nota fiscal não é decisão de formulação.** Ele comprar um insumo não autoriza
  você a colocá-lo numa receita.
- **Ficha técnica de amostra: cadastre e explique, nada mais.** Não proponha
  receita nem sabor novo a partir de uma ficha que ele mandou, a menos que ele
  peça.
- **Frutas chegam prontas para uso.** Não há mão de obra para limpar ou descascar.

### Formato de resposta que ele espera

- O mix oficial aparece como **uma linha só** ("x g de mix oficial"), nunca
  quebrado nos componentes — exceto em contexto de compras, onde o que importa é
  o que ele compra de fato.
- Ele quer **advisor estratégico**: questionar premissas, apontar incoerência e
  risco, dizer o que adiar. Não concordar automaticamente. Diferenciar fato
  verificado de hipótese e de opinião.
- Padrão visual das ferramentas: fundo branco sempre, sem tema escuro, verde da
  casa, uma família tipográfica, minimalista. Ele reclama de caixa alta e
  monoespaçada em rótulo — diz que dá cara retrô e cyberpunk.

---

## 3. COMO RODAR

```bash
npm install                       # só jsdom
node testes-balanceador.js        # 449 testes contra o baseline
```

Para ler ou manipular o sistema por fora do navegador, o padrão é jsdom:

```js
const { JSDOM } = require("jsdom"), fs = require("fs");
const w = new JSDOM(fs.readFileSync("Balanceador de Receitas.html","utf8"),
                    {runScripts:"dangerously", url:"https://x.test/"}).window;
const m = w.eval("computeRecipe")(linhas);
```

A `url` é obrigatória — sem ela o localStorage lança exceção e o arquivo não
carrega.

**Rode a suíte antes e depois de qualquer mudança no HTML.** Ela já pegou poliol
entrando em açúcar de rótulo, selo aparecendo em receita com açúcar adicionado,
alvo ficando suspenso em fórmula sem açúcar e gramatura por sabor.

---

## 4. AS ARMADILHAS DO MOTOR — leia antes de calcular qualquer coisa

### 4.1 Normalize por 1.000 g

`computeRecipe` calcula sobre `BATCH = 1000`. Passar uma receita de 2.947 g sem
normalizar devolve sólidos de 92%, POD 661 e janela de −391 °C. Não é bug: é a
conta certa sobre a escala errada.

```js
const soma = linhas.reduce((a,l)=>a+Number(l.gramas),0);
const norm = linhas.map(l=>({nome:l.nome, gramas:Number(l.gramas)/soma*1000}));
```

### 4.2 Três campos de açúcar, e confundi-los gera rótulo errado

| campo | o que é | para que serve |
|---|---|---|
| `acucares` | **técnico**: açúcar + poliol | alimenta POD e PAC, serve para formular |
| `acucarRotulo` | açúcares totais no sentido da ANVISA, **sem poliol** | tabela nutricional |
| `acucarAdd` | açúcar **adicionado** que entrou via insumo | decide o selo |

No Sorbet Morango é 5,93 contra 16,29 — dez pontos de poliol. Eu quase mandei o
técnico para a nutricionista, o que produziria um rótulo declarando quase três
vezes o açúcar real.

### 4.3 "Sem adição de açúcares" tem tolerância ZERO

Não existe limite de 0,5 g/100 g para essa alegação. O 0,5 é para **"zero
açúcares"**, que fala de açúcares *totais* — e o produto nunca se encaixa nisso,
porque a lactose do leite já põe 8 a 10 g/100 g. A alegação da casa é "sem adição
de açúcares", e qualquer açúcar adicionado a derruba.

Eu disse a ele que 0,465 g/100 g ficava "raspando no limite". Estava errado.
Dois sabores não podem carregar o selo: **Sorbet Morango** (Pasta Fragola a
10 g/kg → 0,465) e **Alfajor** (biscoito → 0,010).

### 4.4 A linha comercial não é o campo `familia`

`familia` é família de **formulação** e escolhe os alvos: 1 creme/leite,
2 fruta/água, 3 proteica, 4 creme alcoólico, 5 sorbet alcoólico, 6 sorbet de
chocolate.

A linha de **venda** sai de `linhaBeco()`: família 2 → Fresh; fora disso,
proteína ≥ 7,5% → Boost, senão Special.

O Pistache é família 3 e linha **Special**. Eu mapeei pelo campo `familia` e
publiquei o Pistache como Boost num documento.

### 4.5 Duas mecânicas de finalização, e a diferença é dinheiro

```js
function massaPote(r){
  const base = num(r&&r.potePeso) || eiPote();
  if(!(r&&r.finAdicional)) return base;
  const fin=(r.finalizacao||[]).reduce((a,l)=>a+num(l.gramas),0);
  return base*(1+fin/1000);
}
```

- `finAdicional:true` (**Alfajor**): o biscoito vai **por cima** do pote cheio.
  Ele **soma**. 135 g de gelato + 15 g de biscoito = 150 g de produto.
- sem `finAdicional` (**Café**): a mescla é ripada **dentro** e **desloca** calda.
  140 g de produto = 125,6 g de calda + 14,4 g de mescla.

Tratei os dois igual e o Café fechou em 156,1 g num pote de 140 g — R$ 0,77 de
CMV a mais. Só apareceu quando cruzei a planilha de CMV contra o sistema.

A quantidade de calda dentro do pote:

```js
const finTot = (r.finalizacao||[]).reduce((a,l)=>a+Number(l.gramas),0)/1000;
const caldaNoPote = (finTot && !r.finAdicional) ? massaPote(r)/(1+finTot) : gelatoPote(r);
```

### 4.6 Gramatura é por sabor, não global

| sabor | gelato | produto |
|---|---|---|
| Café, Pistache, Torta, Brigadeiro, Manga | 140 g | 140 g |
| Alfajor | 135 g | 150 g |
| **Sorbet Morango** | **120 g** | **120 g** |

A gramatura mudou quatro vezes (130 → 120 → 135 → 140) e cada mudança se
propagou para CMV, receituário, lista de compras, consumo de embalagem, proteína
por pote e rótulo. **Sempre confira `eiPote()` e `r.potePeso` em vez de assumir.**

O morango tem 120 g porque ele mediu: o pote cheio não fecha 140 g, por causa da
densidade. Eu dimensionei um lote a 140 g sabendo que a densidade era 0,772 e
errei o rendimento em 20%.

### 4.7 `formulaSemAcucar` — leia o código antes de confiar

Quando as linhas estão disponíveis, o açúcar adicionado é a resposta definitiva
(`add100 < 2` → true). A heurística de fibra é só fallback. A função já esteve
quebrada: detectava fórmula sem açúcar **pela fibra**, e quebrou quando a base
proteica adoçada com estévia chegou. O Brigadeiro ficou mal classificado por
dias, e a suíte não pegou porque a fixture era o Café.

### 4.8 O backup é v9 — corrigido em 24/10/2026

O export v8 gravava nove chaves e deixava de fora `RCFG` (gramatura do pote,
perda de processo, overrun, temperaturas) e `EMB` (preços e saldos de embalagem).
Restaurar num navegador limpo perdia a gramatura medida em 16/10 e todos os
saldos. Era o mesmo tipo de furo do `lotes:PROD` que custou a agenda de batidas
em 30/09.

**O v9 grava doze chaves de estado restaurável** — as nove antigas mais `cfg`,
`embalagem` e `bancada` — e um bloco `referencia` com as constantes do arquivo
(`ROTULO`, `ACUCAR_ADD_PCT`, `MIX_COMP`, `PRECO_VENDA`, `BNC_LINHAS`,
`CUSTO_EMB_POTE`, `IMPOSTO_SIMPLES`, alvos, limites do Lulo e a massa de pote
resolvida de cada receita de lançamento).

O bloco `referencia` **não é restaurado** — são `const` no HTML, e quem manda
nelas é o arquivo. Mas o import **compara e avisa**: se o backup foi feito com
preços, nomes de rótulo ou massa de pote diferentes dos que estão no HTML atual,
aparece um alerta nomeando o que divergiu. Um backup antigo restaurado sobre um
HTML novo já me deu CMV errado sem nenhum sintoma visível.

O import aceita v8 e v9. Num v8, o que não existe no arquivo simplesmente não é
tocado — a configuração atual fica intacta em vez de virar `undefined`.

⚠️ `dumpBackup()` devolve `cfg: RCFG` **por referência**, não cópia. Para o
botão não importa, porque serializa na hora do clique. Mas se você guardar o
objeto para usar depois, ele é uma referência viva — serialize primeiro. Eu
perdi tempo com um teste que falhava por isso e cheguei a achar que o código
estava errado.

---

## 5. NÚMEROS QUE IMPORTAM

### Parâmetros
- **POD alvo 170**, faixa 160–180. Banda de congelamento 79–84%.
- Perda de processo **3%** (`eiFator()` = 1,0309). **O bancada diz que está alto:**
  30 potes de pistache renderam 31, mesmo caso na torta. Um pote pesado após a
  batida resolveria.
- Imposto do Simples **4,5%**.
- Embalagem **R$ 1,67/pote**: pote com tampa 1,07 + colher 0,26 + lacre 0,34.

### As sete receitas do lançamento — lido do sistema em 24/10

| sabor | linha | fam | sól. | gord. | prot. | POD | PAC | janela °C | R$/kg |
|---|---|---|---|---|---|---|---|---|---|
| Sorbet Morango | Fresh | 2 | 31,9% | 0,4% | 0,7% | 232 | 388 | −14,8 a −19,4 | 21,31 |
| Manga com Maracujá | Fresh | 2 | 32,0% | 0,4% | 0,8% | 227 | 389 | −14,8 a −19,4 | 26,19 |
| Torta de Limão | Special | 1 | 39,4% | 6,5% | 3,6% | 170 | 352 | −15,0 a −19,7 | 44,60 |
| Alfajor | Special | 1 | 37,1% | 6,1% | 5,4% | **148** | 369 | −15,2 a −20,0 | 33,75 |
| Pistache | Special | 3 | 38,2% | 9,5% | 6,2% | **148** | 330 | −13,8 a −18,2 | 60,55 |
| Café Proteico | Boost | 3 | 39,3% | 4,5% | 10,0% | **180** | 354 | −15,1 a −19,8 | 40,61 |
| Brigadeiro Proteico | Boost | 3 | 40,6% | 5,4% | 10,1% | 161 | 332 | −14,5 a −19,0 | 41,09 |

**Não copie esta tabela de memória.** Na primeira versão do manual eu digitei os
sete de cabeça e cinco estavam errados. Leia do sistema.

Pistache e Alfajor estão com POD 148, doze pontos abaixo do piso, e os dois estão
aprovados em bancada e vendendo. Café está no teto. Isso é um fato em aberto, não
um defeito a corrigir sem conversar com ele.

### Mix oficial — 999 partes
POLIDEXTROSE 528 · MALTITOL 224 · ERITRITOL 163 · INULINA 81 · STEVIA 3.
Feito na casa. Para compras, explode nos cinco componentes.

### Base proteica da calda única — por 1 kg
Leite ZL 692,4 · Base MEC Protein 130 · leite em pó desnatado 120 · glicerol 30 ·
polidextrose 20 · Cremobene 3,1 · sal 1 · estévia 0,6.

Café e Brigadeiro compartilham esta base e se diferenciam só na saborização.
**Cremobene Premium a 3 g/kg na calda proteica** — metade da dose tabelada,
porque a proteína faz parte do trabalho estrutural. Ajuste de bancada dele.

### Preço e CMV
- Atacado: **Fresh R$ 18,70 · Special e Boost R$ 20,50**. Varejo sugerido:
  Fresh R$ 30,90 · Special e Boost R$ 32,90.
- Em 21/10 ele decidiu o caminho: **venda direta** em vez de virar canal forte de
  distribuição, porque o objetivo é loja própria. Preço por linha com piso:
  quem revende não pode vender abaixo do preço dele.

| sabor | insumo | embal. | CMV | margem | food cost |
|---|---|---|---|---|---|
| Sorbet Morango | 2,64 | 1,67 | 4,31 | 77,0% | 23,0% |
| Manga com Maracujá | 3,78 | 1,67 | 5,45 | 70,9% | 29,1% |
| Alfajor | 5,29 | 1,67 | 6,96 | 66,0% | 34,0% |
| Brigadeiro Proteico | 5,93 | 1,67 | 7,60 | 62,9% | 37,1% |
| Torta de Limão | 6,44 | 1,67 | 8,11 | 60,5% | 39,5% |
| Café Proteico | 6,66 | 1,67 | 8,33 | 59,4% | 40,6% |
| Pistache | 8,74 | 1,67 | 10,41 | 49,2% | 50,8% |

Isto é insumo e embalagem apenas. **Não tem mão de obra, energia, frete, imposto
nem rateio dos R$ 5.000 de custo fixo mensal.** Nunca apresente esses 49–77% como
margem real.

### Densidades medidas em 16/10 (gelato em pote de 150 ml)
Café 0,963 · Torta 0,961 · Manga 0,949 · Brigadeiro 0,909 · Alfajor 0,903 ·
Pistache 0,884 · **Sorbet Morango 0,772**.

Manga e Morango têm caldas fisicamente idênticas (sólidos 32,0 vs 31,9, PAC 389
vs 388) e deram overrun de 19% e 47%. **A diferença é processo, não receita** — a
manga é a prova de que a calda do morango aguenta 0,949.

---

## 6. ERROS QUE EU COMETI — não repita

| erro | como apareceu | lição |
|---|---|---|
| Usei R$ 20,90/18,90 quando os preços de rua eram 20,50/18,70 | A memória do projeto já tinha o número certo; eu confiei no cadastro e não cruzei | Toda margem de uma semana saiu otimista. Cruze preço contra nota. |
| Imprimi o Brigadeiro antigo no receituário | Ele: *"toda hora a receita vem de uma forma"* | Leia do sistema, não da conversa. |
| Contei pote e tampa dentro dos 150 g | Gerou uma objeção falsa de "não cabe o biscoito" | Pergunte se a gramatura é líquida. |
| Mandei açúcar técnico para a nutricionista | Sorbet Morango: 5,93 de rótulo contra 16,29 técnico | Use `acucarRotulo`. |
| Escrevi "todos zero lactose e sem açúcar adicionado" no dossiê | Dois dos sete não são | Verifique cada item antes de generalizar. |
| Dimensionei lote de morango a 140 g | Renderia 25 potes, não 21 | Use `r.potePeso`. |
| Tabela das sete receitas digitada de memória | Cinco de sete erradas | Leia do sistema. |
| Reconstruí a lista de testes de bancada por inferência | Ele lembrou de 12 e 10 eu não tinha; dois que marquei "nunca feito" ele tinha feito | Assunto na conversa não é lote batido. Pergunte. |
| Teste verde que não testava nada | `gelatoPote` não estava exportado no harness, o guard engolia | Valide o teste ao contrário: quebre de propósito e veja se acusa. |
| Passei 2.947 g sem normalizar | Sólidos 92,6%, POD 661, janela −391 °C | Normalize por 1.000. |

---

## 7. ESTADO ATUAL (24/10/2026)

### Estoque de produto acabado — contagem física de 22/10, 325 potes
Manga 60 · Torta 58 · Brigadeiro 51 · Pistache 46 · Café 40 · Alfajor 38 ·
Morango 32. Valor R$ 6.496,90.

Dois achados dessa contagem: **188 potes de produção não lançada** entre 13/10 e
22/10, e o **morango não fecha** — faltam 6 potes sem explicação (degustação,
amostra, perda ou venda não registrada).

### Embalagem — comprados 6.000 potes e 6.000 tampas (Natucopos, R$ 3.812 em 6x)
São **3 linhas, 2.000 potes cada**, e **3 cores de tampa**, uma por linha. Pote de
uma linha não serve na outra. Pote + tampa a R$ 0,635 (a segunda nota é FOB, o
frete não está incluso).

O **lacre é o gargalo absoluto: 717 unidades, 1,2 mês** contra 11 meses de pote.
Colher 4.217, 7 meses.

### Pendências abertas
- Frete Recife–Salvador para 75 kg de polióis (cotação FOB de 21/10)
- Divisão das cores dos 5.000 potes — janela de 30 dias para mudar
- Pedido de lacre e colher
- Preço do balde de canela PreGel e do saco de 8 kg de pipoca PreGel
- Seis insumos sem preço travam cinco testes: Gusto Pop-Corn, siriguela, goiaba,
  pasta de avelã 100%, iogurte integral, baunilha Vanilla Brasil
- Overrun do morango (processo, não receita)
- Um pote pesado após a batida, para resolver os 3% de perda
- Mescla do Brigadeiro: campo em branco, 764 g de granulado sem cadastro
- 75 °C de bancada contra 82–85 °C do receituário — divergência nunca resolvida
- Pote novo de 180 ml declarando 150 g: precisa ser decidido antes da nutricionista
  montar as tabelas
- Goiaba, cajú e siriguela: feitos em bancada, nunca cadastrados

### O que mudou no sistema em 22/10
Quatro telas apagadas a pedido dele — Painel, Investimento, Produção & Vitrine e
Lançamentos. **Os dados continuam no arquivo**; só as telas saíram. `custosCompute`
depende de `investTotals()` e `INVEST.cap.parcelas`, então a remoção preservou os
dados de propósito. O sistema virou ferramenta de receita e o resto migrou para
planilha.

---

## 8. O QUE ESTÁ NESTE PACOTE

```
AGENTS.md                      este arquivo
README.md                      mapa do pacote
sistema/
  Balanceador de Receitas.html fonte de verdade
  testes-balanceador.js        449 testes
  baseline.json                baseline de 12/10
  package.json                 só jsdom
dados/
  backup_beco_gelato_2026-10-24.json
                               formato nativo v9 — importável pela aba Dados.
                               12 chaves de estado + bloco referencia.
  _dossie.json                 extração para os documentos técnicos
  _compras.json                extração para a planilha de compras
scripts/
  _dossie.js  _compras.js      extratores (node + jsdom)
  _rec.py _nutri.py _manual.py geradores de PDF (reportlab)
  _xlsx.py _cmv.py _forn.py    geradores de planilha (openpyxl)
documentos/
  *.pdf  *.xlsx                saídas atuais
```

**Ordem de confiança:** o HTML é a verdade. Os JSON são extrações datadas. Os
documentos são fotografias de um momento — se divergirem do HTML, o HTML ganha.
