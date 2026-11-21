# HUB Beco — índice

Leia só este arquivo sempre. A partir dele: abra só a(s) área(s) relevante(s) e os arquivos de `memoria/` que ela declarar como dependência. `log/` só entra quando a pergunta for "isso já aconteceu antes". Número do dia (estoque, caixa) vem do banco do artifact Complexo Beco, nunca da memória.

## Foco atual (desde 04/11/2026)

**Vender, criar e abrir canal de venda.** Gabriel decidiu isso explicitamente: o negócio tem se preocupado com demanda que ainda não existe. Até ele mudar essa decisão: **Comercial & Parcerias B2B**, **Expansão de Pontos**, **Marca & Conteúdo** e **Tráfego & Performance** são as áreas que puxam proatividade primeiro — toda vez que a postura proativa de uma área entrar em jogo sem pedido específico, ela prioriza isso. As outras quatro áreas (Eventos, Loja/Ponto, Portfólio & Preço, Financeiro & Unit Economics) continuam existindo e respondem quando perguntadas, mas não propõem trabalho novo por conta própria enquanto esse foco valer — a demanda ainda não as justifica.

## memoria/

- `memoria/produtos.md` — marca, linhas, sabores, preços, canais, kits. Fatos estáveis, não o saldo do dia.
- `memoria/financeiro.md` — metas, parâmetros estáveis, margem mínima de revenda. Não o caixa do dia.
- `memoria/decisoes.md` — regras duras, padrão visual, benchmarks de referência (Oakberry, Bacio di Latte).
- `memoria/pendencias.md` — só pendência nascida de decisão do HUB, não duplica o Painel do Complexo Beco.
- `memoria/calendario-conteudo.md` — o plano semanal de conteúdo e venda direta ("Do momento ao hábito"): calendário dia a dia, rotina de Stories, painel de acompanhamento.
- `memoria/gtm.md` — visão consolidada de Go To Market (produto/mercado, posicionamento, objetivos, preço, marketing, vendas, distribuição, pós-venda, métricas, plano de ação), cada seção apontando pro arquivo/área fonte e com os gaps reais marcados. Não é fonte primária de nenhum fato — é o resumo que amarra os outros.

## areas/

- `areas/marketing.md` — Marca & Conteúdo. Consultar para Instagram, linha editorial, campanha.
- `areas/trafego.md` — Tráfego & Performance. Consultar para investimento/teste de anúncio.
- `areas/eventos.md` — Eventos & Ativações. Consultar para convite, ativação, cenário de evento.
- `areas/comercial-b2b.md` — Comercial & Parcerias B2B. Consultar para proposta, negociação, ponto parceiro.
- `areas/expansao.md` — Expansão de Pontos. Consultar para onde abrir ponto novo.
- `areas/loja.md` — Operação de Loja/Ponto. Consultar para execução no ponto de venda.
- `areas/portfolio.md` — Portfólio & Preço. Consultar para lançar/descontinuar/reposicionar sabor ou linha.
- `areas/financeiro-unit.md` — Financeiro & Unit Economics. Consultar para margem por canal/ponto.
- `areas/inteligencia-mercado.md` — Inteligência de Mercado & Tendências. Consultar para tendência de consumo, concorrente, preço de insumo-chave, notícia do setor. Não depende do Foco atual (sempre proativa) e é alimentada por rotina agendada (ver `schedule`).

## log/

- `log/YYYY-MM-decisoes.md` — append-only. Só ler quando a pergunta for sobre precedente.

## Registro — depois de toda análise com recomendação ou decisão

Não é opcional e não precisa de pergunta separada: toda vez que uma área (ver acima) devolver uma recomendação, prioridade ou decisão — não uma análise solta — registre nos dois lugares, com os mesmos dados:

1. **Acrescente** uma entrada em `log/YYYY-MM-decisoes.md` (nunca reescreva uma existente).
2. **Grave** na coleção `hub_log` do artifact Complexo Beco (`ArtifactData`, `action: "set"`, `doc_id` no formato `YYYY-MM-DD-<area>-<slug-curto>`), com os campos:
   - `data` (string `YYYY-MM-DD`), `area`, `decisao` (título curto) — sempre.
   - `situacao`, `oportunidade`, `prioridade`, `proximos_passos` (lista de `{passo, prazo}`), `o_que_falta` (lista de texto), `pendencia` (texto) — quando a resposta tiver essas partes (formato de saída de cada área).
   - `resultado` — **string vazia `""` enquanto não houver resultado**, nunca `"—"` nem omitido. Preencher quando Gabriel contar o que aconteceu.
   - `atualizado` (string ISO, `new Date().toISOString()`) — sempre que já existir outra entrada da mesma `area` no mesmo dia. É o que desempata qual aparece primeiro em "Em cima da mesa".

Se a conversa não tiver como gravar no banco (ex.: Project no claude.ai, sem ferramenta de arquivo/banco), devolva a entrada pronta, no mesmo formato, para Gabriel copiar — e avise que ela só entra de verdade quando alguém colar numa sessão com acesso ao repo e ao artifact.

**Quando a resposta muda o estado de uma entrada já registrada** (Gabriel confirma, recusa ou pede ajuste em algo que já estava no log) — isso não é uma análise nova, é a continuação da mesma: acrescente uma entrada curta no `log/` contando o que mudou, e no `hub_log` either (a) `update` o campo `pendencia` do doc original para `""` quando a pergunta em aberto foi respondida, ou (b) `set` um doc novo (`atualizado` obrigatório aqui) quando valer a pena um registro com data própria. Nunca apague ou reescreva os campos de análise (`situacao`, `oportunidade` etc.) de uma entrada existente.
