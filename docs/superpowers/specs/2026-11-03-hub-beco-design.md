# HUB Beco — desenho

## O que é

Uma camada de inteligência de negócio para o Beco Gelato: você alimenta (convites, resultados, dúvidas, decisões) conversando com Claude, e cada área analisa o que recebe e devolve orientação prática — o que está acontecendo, que oportunidade faz sentido e por quê, o que priorizar agora, próximos passos com prazo sugerido, o que falta saber, e o que ficou pendente.

Não é um app novo com telas. É conversa + uma estrutura de arquivos que dá à conversa memória entre sessões e um jeito de cada área pensar sem reinventar contexto toda vez.

## Por que

Hoje cada decisão (evento, campanha, negociação) é pensada do zero, sem memória central de preço/custo/meta/regra e sem registro do que já foi decidido e por quê. O Complexo Beco (dashboard já existente) registra e calcula, mas não analisa nem recomenda. O HUB fecha essa lacuna sem duplicar o que o dashboard já faz.

## Relação com o que já existe

- **Complexo Beco** (artifact `3jL2vGzJmqVT1oTDsAGvQu`, fonte em `complexo/` — pasta renomeada de `cerebro/` para abrir espaço para o HUB) continua sendo o registro operacional do dia a dia: estoque, financeiro, metas do mês, pendências táticas. O HUB **lê** esses dados quando precisa de número atual; não os duplica. O HUB também **escreve** nele: toda decisão registrada no log entra na coleção `hub_log` do artifact, para alimentar a aba "Painel do HUB" (ver seção própria abaixo).
- **Balanceador** continua sendo a única fonte de fórmula/formulação. O HUB nunca propõe receita nem reabre decisão de bancada — regra dura herdada do `AGENTS.md` atual.
- **AGENTS.md / README.md** do repo precisam de uma atualização: o nome `cerebro/` passa a ser do HUB; o que hoje é chamado de "segundo cérebro" no README (o dashboard) passa a ser chamado apenas de "Complexo Beco".

## Estrutura de arquivos

```
hub/
  INDEX.md                 — mapa de 1 linha por arquivo: o que é, quando consultar. Único arquivo lido sempre.
  memoria/
    produtos.md             — linhas, sabores, preços, canais (fatos decididos, não a planilha toda)
    financeiro.md           — metas, ponto de equilíbrio, regras de margem (fatos estáveis; número do dia vem do Complexo Beco)
    decisoes.md             — decisões/regras duras já tomadas e por quê
    pendencias.md           — só pendências nascidas de decisão do HUB que ainda não foram para o Painel do Complexo Beco
  areas/
    marketing.md            — Marca & Conteúdo
    trafego.md               — Tráfego & Performance
    eventos.md                — Eventos & Ativações
    comercial-b2b.md          — Comercial & Parcerias B2B
    expansao.md                — Expansão de Pontos
    loja.md                     — Operação de Loja/Ponto
    portfolio.md                 — Portfólio & Preço
    financeiro-unit.md            — Financeiro & Unit Economics
  log/
    YYYY-MM-decisoes.md      — append-only; uma entrada por decisão relevante, com campo "resultado" preenchido depois
```

Áreas fora do escopo inicial, de propósito: Pessoas/RH e Jurídico/Compliance. Entram quando o volume justificar um playbook próprio.

## Formato de cada `areas/*.md`

Todo playbook de área segue o mesmo template, curto (o objetivo é ler pouco, não documentar tudo):

1. **O que essa área recebe** — que tipo de pedido cai aqui.
2. **O que ela precisa de `memoria/`** — quais arquivos consultar, nunca "todos".
3. **Com quem ela cruza** — quando a resposta exige olhar outra área (ex.: `eventos.md` sempre cruza com `financeiro.md` e `produtos.md` antes de montar cenário).
4. **O que ela nunca faz** — regras duras específicas da área.
5. **Formato de saída** — situação → oportunidade e por quê → prioridade → próximos passos com prazo → o que falta saber → pendência.
6. **Postura proativa** — a área não espera só ser alimentada. Quando você pedir orientação sem trazer nada pronto ("o que eu faço agora em marketing"), ela propõe estratégia, campanha ou movimento de crescimento por conta própria, usando a memória da marca e referência de mercado (ex. como Oakberry cresce sem ser franquia) — não só reage ao que chega.

O cruzamento entre áreas (regra 3) é a única forma de orquestração: não existe um arquivo "orquestrador" central além do `INDEX.md`.

## Fluxo de uma pergunta (consumo de tokens)

1. Lê `hub/INDEX.md` (sempre; é pequeno).
2. A partir do índice, identifica 1–2 áreas relevantes e lê só esses `areas/*.md`.
3. Lê só os arquivos de `memoria/` que essa área declara como dependência (regra 2 do template).
4. Se a pergunta precisa de número do dia (estoque, caixa), consulta um caminho específico do banco do Complexo Beco — nunca a página inteira do artifact.
5. `log/` só é lido quando a pergunta é do tipo "isso já aconteceu antes" — não entra por padrão.

Isso é o que mantém o custo de token baixo: o padrão é ler 3–4 arquivos pequenos, não a estrutura toda.

## Loop de decisão → execução → resultado

Toda decisão relevante registrada em `log/YYYY-MM-decisoes.md`: data, área, o que foi decidido, premissa usada, resultado (vazio até você contar o que aconteceu). Quando uma área responde a uma pergunta parecida com uma já registrada, ela pode citar o precedente — só quando for pertinente.

## Visibilidade: Painel do HUB

Conversa resolve para decidir, mas não para acompanhar ao longo do tempo — o que sai dela some no histórico do chat. Por isso toda decisão registrada no log também é escrita, pela mesma interação, no banco do próprio artifact Complexo Beco (coleção `hub_log`), não só no markdown do repo. O Complexo Beco ganha uma 11ª aba, **"Painel do HUB"**, que lê essa coleção e mostra: a timeline das últimas decisões/análises por área (data, área, decisão, resultado quando já houver) e um resumo de meta/progresso reaproveitando os números que a aba "Novembro" já calcula — sem duplicar estado.

O markdown (`hub/log/*.md`) continua existindo e sendo a cópia barata que Claude relê em conversa; o banco do artifact é o espelho que você vê no navegador/celular sem precisar me perguntar. Toda escrita de decisão grava nos dois.

## Acesso remoto (fora desta sessão de código)

O markdown de `hub/` mora no repo git, que esta sessão de código lê — mas você acessa Claude no dia a dia pelo app/site do claude.ai, não por aqui. Para isso funcionar remotamente: os arquivos de `hub/` (menos `log/`, que cresce e não precisa estar sempre carregado) entram como conhecimento de um **Project no claude.ai** dedicado ao Beco Gelato. Você abre esse Project de qualquer celular/computador e conversa com as áreas normalmente; a "Postura proativa" (seção acima) funciona igual, porque está escrita nos próprios arquivos do playbook, não em algo específico desta sessão.

Isso cria uma responsabilidade nova: toda vez que `hub/memoria/*.md` ou `hub/areas/*.md` mudar no repo (aqui ou numa sessão futura), o conhecimento do Project precisa ser atualizado também — os dois podem divergir se um for editado sem o outro. A aba "Painel do HUB" (seção anterior) não depende disso: ela lê direto do banco do artifact, então funciona do celular com ou sem o Project estar atualizado.

## Fora do escopo desta fase

- Qualquer automação que leia Instagram/anúncios sozinha (o "alimento" continua sendo você, em conversa).
- Reformular o Complexo Beco ou o Balanceador.
- Pessoas/RH e Jurídico/Compliance como áreas ativas.

## Próximo passo

Depois da sua revisão deste spec, vira plano de implementação (writing-plans): criar os arquivos, popular `memoria/` a partir do backup de 2026-11-03, escrever os 8 playbooks de área, e atualizar `AGENTS.md`/`README.md` para refletir o rename de `cerebro/` → `complexo/`.
