# Produtos — memória central

Fatos decididos e estáveis — preço e saldo do dia moram no Complexo Beco, não aqui.

## Marca

- Nome: O Beco Gelato (grupo Beco: O Beco Saudável, O Beco Burger, O Beco Gelato).
- Frase decidida: "Gelato italiano, agora saudável e em pote."
- Categoria a ocupar: sobremesa. Categoria a evitar: sobremesa fit, sorvete saudável, nicho.
- Regra de escrita: o atributo fecha a peça, nunca abre. A peça começa pela sobremesa; "sem açúcar adicionado" entra no fim, como permissão para repetir.
- Premium por: matéria-prima e processo — artesanal no insumo, industrial no processo.
- Nunca dizer: "feito a mão".
- Pote: neutro e igual nos sete sabores; muda a cor da tampa, uma por linha.

## Linhas

| Linha | Posicionamento | Preço direto | Preço iFood |
|---|---|---|---|
| Fresh | fruta, refrescância, leveza, nutrição — a cara do dia | R$ 22,90 | R$ 25,90 |
| Special | sobremesa, matar a saudade do doce, mesa de família | R$ 25,90 | R$ 29,90 |
| Boost | proteica — treino, fitness, quem conta proteína | R$ 25,90 | R$ 29,90 |

## Sabores

| Sabor | Linha | Gramatura | Preço direto | Preço iFood |
|---|---|---|---|---|
| Sorbet Morango | Fresh | 120 g | R$ 22,90 | R$ 25,90 |
| Manga com Maracujá | Fresh | 140 g | R$ 22,90 | R$ 25,90 |
| Alfajor | Special | 150 g (135 g + 15 g de biscoito) | R$ 25,90 | R$ 29,90 |
| Brigadeiro Proteico | Boost | 140 g | R$ 25,90 | R$ 29,90 |
| Torta de Limão | Special | 140 g | R$ 25,90 | R$ 29,90 |
| Café Proteico | Boost | 140 g | R$ 25,90 | R$ 29,90 |
| Pistache | Special | 140 g | R$ 25,90 | R$ 29,90 |

Estoque e vendas acumuladas são dado do dia — ver Complexo Beco, não aqui.

## Canais

- **Ponto parceiro:** compra no preço de atacado: R$ 18,50 (Special e Boost) e R$ 17,50 (Fresh), confirmado por Gabriel em 23/11 (vale desde 26/10). Revende por até o preço do iFood: R$ 27,90 (Special e Boost) e R$ 25,90 (Fresh). Margem do parceiro: 33,7% e 32,4%. Papel: volume — paga menos por pote, mas leva muitos de uma vez, sem custo de atenção. Margem mínima do revendedor: 32%.
- **Loja da família (O Beco Saudável):** compra no mesmo preço de atacado, R$ 18,50 / R$ 17,50, desde o pedido 000009 (26/10). Antes era R$ 20,50 / R$ 18,70. Revende todos os sabores a R$ 25,90 (23/11): margem da loja de 28,6% no Special e Boost e 32,4% no Fresh.
- **iFood:** taxa de 12%. Papel: canal de busca, não de descoberta — quem abre o app já decidiu que quer sobremesa. Preço próprio (+14,4% sobre o direto) para a contribuição empatar com a retirada; isso quebra de propósito a regra de preço único, que foi escrita para gôndola física.
- **Direto/WhatsApp:** retirada ou entrega própria. O canal mais rentável — vale de R$ 2 a R$ 3 mais por pote que o iFood.
- **Regra de CTA:** WhatsApp primeiro, iFood depois. iFood é para quem não conhece; WhatsApp é para quem já conhece.

## Kits

- Regra que sustenta: no máximo 2 unidades do mesmo sabor por kit, sem restrição de linha.
- Custeio sempre na composição mais cara que a regra permite, nunca na média.
- Objetivo: fazer todos os sabores girarem — o desconto é o meio, nunca o fim. Comunicar pelo jogo de composição, nunca pelo preço ("10% em seis potes" não é oferta).
- Mistos: Dupla do Agora (2 potes, R$ 48,90, 5% desc.), Mood do Dia (4 potes, R$ 95,90, 7% desc., composição curada), Monte seu Mood (6 potes, R$ 138,90, 10% desc., composição livre do cliente).
- Por linha: Modo Refresca — linha Fresh (4 potes, R$ 84,90, teto de 4 potes, 2 sabores hoje), Modo Sofá — linha Special (6 potes, R$ 138,90, teto de 6, 3 sabores hoje), Modo Treino — linha Boost (4 potes, R$ 95,90, teto de 4, 2 sabores hoje).
- Nomes antigos (não usar mais, só referência interna): Kit Mood → Mood do Dia; Monte seu Kit → Monte seu Mood; Kit Fresh/Special/Boost → Modo Refresca/Sofá/Treino.
- Regra geral: uma linha com N sabores permite no máximo 2N potes num kit monolinha. Destrava o kit de 6 em Fresh e Boost: terceiro sabor em cada.

### Combos no iFood (criados 10/11, dentro do catálogo real)

Implementação específica do canal iFood — preços diferentes dos kits acima (que usam preço direto como base). Calculados com o Special/Boost valendo R$29,90 (preço correto documentado), mesmo o avulso no catálogo ainda estando em R$27,90 por decisão de Gabriel (10/11: "não, só os combos" — ver `hub/log`). Isso significa que o "preço cheio" mostrado no combo não bate exatamente com a soma dos avulsos reais — aceito conscientemente.

| Combo | Composição | Preço cheio (pior caso) | Preço no iFood |
|---|---|---|---|
| Dupla do Agora | 2 potes, livre (máx. 2 do mesmo sabor) | R$ 59,80 | R$ 54,90 |
| Mood do Dia | 4 potes, livre (máx. 2 do mesmo sabor) | R$ 119,60 | R$ 107,90 |
| Beco Completo | 7 potes, 1 de cada sabor + sacola térmica de brinde | R$ 201,30 | R$ 174,91 |

"Beco Completo" substitui "Monte seu Mood" (6 potes, livre) no iFood — é todos os 7 sabores, não uma escolha de 6. "Monte seu Mood" continua valendo como conceito pro canal direto/WhatsApp, se Gabriel quiser oferecer lá.

A sacola térmica do "Beco Completo" não é um item do cardápio — é brinde físico, incluído na montagem do pedido, descrito só no texto do combo.
