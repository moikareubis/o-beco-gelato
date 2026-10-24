# O Beco Gelato — pacote de transferência

Gerado em 24/10/2026 para levar o projeto a outro ambiente de trabalho.

## Comece aqui

1. **`AGENTS.md`** — leia inteiro antes de mexer em qualquer coisa. Contém as
   regras do Gabriel em citação literal, as oito armadilhas do motor, os números
   que importam, os dez erros que o agente anterior cometeu e o estado atual.
2. `documentos/O Beco Gelato - Manual do Sistema e Decisoes.pdf` — o mesmo
   conteúdo em formato de leitura, com as decisões da rodada de 21 a 24/10.

## Subir o ambiente

```bash
cd sistema
npm install            # instala jsdom, a única dependência
node testes-balanceador.js
```

Esperado: **449 passaram · 0 falharam**. Se falhar, pare e investigue antes de
seguir — a suíte compara contra `baseline.json` e qualquer divergência significa
que o motor mudou de comportamento.

Para os geradores de documento:

```bash
pip install reportlab openpyxl
```

## Abrir o sistema

`sistema/Balanceador de Receitas.html` abre direto no navegador, sem servidor.
Funciona offline. Os dados ficam no localStorage daquele navegador.

Para restaurar os dados: aba **Dados** → *Importar backup* →
`dados/backup_beco_gelato_2026-10-24.json`.

O backup é **v9** (corrigido em 24/10/2026). Restaura doze chaves de estado,
incluindo `cfg` — gramatura do pote, perda de processo, overrun e temperaturas —
e `embalagem`, com preços e saldos. O v8 antigo deixava essas duas de fora e
perdia a gramatura medida em 16/10 numa troca de navegador.

As constantes do arquivo (`ROTULO`, `ACUCAR_ADD_PCT`, `MIX_COMP`, `PRECO_VENDA`,
`BNC_LINHAS`, alvos e limites) vão num bloco `referencia` apenas para registro: o
import **compara e avisa** se divergirem, mas não sobrescreve, porque quem manda
nelas é o HTML. Detalhe em `AGENTS.md` §4.8.

## Ler o sistema por fora do navegador

```js
const { JSDOM } = require("jsdom"), fs = require("fs");
const w = new JSDOM(fs.readFileSync("Balanceador de Receitas.html","utf8"),
                    {runScripts:"dangerously", url:"https://x.test/"}).window;

const R = w.eval("RECIPES").filter(r=>r.lancamento);   // as 7 do lançamento
const m = w.eval("computeRecipe")(R[0].linhas);        // normalize antes! §4.1
```

A `url` é obrigatória: sem ela o localStorage lança e o arquivo não carrega.

`scripts/_dossie.js` e `scripts/_compras.js` são exemplos completos de extração.

## Regenerar os documentos

```bash
node scripts/_dossie.js    &&  python3 scripts/_rec.py      # receituário
node scripts/_dossie.js    &&  python3 scripts/_nutri.py    # dossiê nutricionista
node scripts/_dossie.js    &&  python3 scripts/_xlsx.py     # planilha nutricionista
node scripts/_dossie.js    &&  python3 scripts/_cmv.py      # CMV por produto
node scripts/_compras.js   &&  python3 scripts/_forn.py     # compras e estoque
                               python3 scripts/_manual.py   # manual e decisões
```

Os geradores esperam rodar no mesmo diretório do HTML. Ajuste os caminhos ou
copie o HTML para junto deles.

## Ordem de confiança dos arquivos

1. **`sistema/Balanceador de Receitas.html`** — a verdade.
2. `dados/*.json` — extrações datadas. Podem estar velhas.
3. `documentos/*` — fotografias de um momento. Se divergirem do HTML, o HTML ganha.

## Convenção de datas

O projeto trabalha com datas no formato brasileiro (dd/mm/aaaa) e os comentários
no código citam a data da decisão. Comentário datado no código é registro de
por que algo é como é — **não apague**.
