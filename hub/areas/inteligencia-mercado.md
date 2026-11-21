# Inteligência de Mercado & Tendências

## O que recebe

Pergunta sobre o que está acontecendo fora do negócio que pode afetar ele: tendência de consumo, movimento de concorrente, preço de mercado de insumo-chave, notícia do setor (abertura/fechamento de loja relevante, produto saindo de linha, mudança regulatória em rótulo/claim).

## Depende de

`memoria/decisoes.md` (regra dura 7 — claim nutricional só com ficha técnica fechada: toda tendência "zero açúcar"/"saudável" trazida aqui precisa passar por esse filtro antes de virar peça) e `memoria/produtos.md` (pra saber contra quais sabores/linhas cruzar um achado de insumo ou concorrente).

## Cruza com

Qualquer uma das outras 8 áreas pode receber um achado desta — ex.: achado de concorrente cruza com `areas/marketing.md` e `areas/portfolio.md`; achado de preço de insumo cruza com `areas/financeiro-unit.md` e com o CMV do Complexo Beco (`T.cmv`); achado de público/Geração Z cruza com `areas/trafego.md`.

## Nunca faz

- Não traz número de mercado sem fonte (link real, buscado na hora via `WebSearch`) — nunca de memória.
- Não vira peça comercial/claim nutricional direto — qualquer achado de tendência "saudável"/"zero" passa pela regra dura 7 antes.
- Não substitui o preço real de insumo quando o Gabriel já informou um (ex.: óleo de coco R$35/500ml, 21/11) — só contextualiza (é caro, barato, dentro da faixa de mercado).

## Formato de saída

situação → oportunidade e por quê → prioridade → próximos passos com prazo → o que falta saber → pendência

## Postura proativa

Esta é a única área que não depende do "Foco atual" (`INDEX.md`) pra ser proativa — ela não propõe gasto nem iniciativa nova, só mantém Gabriel informado, então roda independente de qual área está priorizada no momento. Alimentada por uma rotina agendada (cloud routine, ver `RemoteTrigger`/skill `schedule` — criada em 21/11/2026, semanal) que busca e registra achados sozinha, sem precisar de pergunta. Toda vez que uma busca ao vivo (`WebSearch`) trouxer algo relevante — tendência de consumo, concorrente, preço de insumo, notícia do setor — registra no formato de saída acima, mesmo sem ninguém ter perguntado.

## Primeiro achado (21/11/2026, demonstração manual)

- Tendência do setor: "indulgência permissiva" é o eixo do mercado de sorvete/gelato no Brasil — o consumidor quer doce, desde que o ingrediente seja melhor. Consumo de açúcar caiu 21,2% desde 2022. Zero açúcar ganhando espaço, formatos menores e sabores pra Geração Z em alta. Tensão regulatória: termos "zero"/"natural" podem passar impressão de mais saudável do que o produto é — relevante pra regra dura 7.
- Concorrente direto: Gelato Borelli tem 28 sabores zero no portfólio = 7,5% do faturamento total dela — benchmark concreto de quanto uma linha "zero" pode pesar.
- Preço de insumo: óleo de coco em varejo online hoje gira R$38–50/500ml — o R$35/500ml que Gabriel informou é competitivo, não subestimado.
