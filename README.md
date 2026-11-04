# O Beco Gelato

Fonte de tudo que a marca usa: as ferramentas de gestão, a apresentação e os materiais comerciais.

## A regra

**Repo = onde se edita. Artifact = onde se usa.**

As ferramentas do dia a dia rodam publicadas na claude.ai, com URL própria e banco de dados — é assim que elas abrem no celular e é assim que os dados sobrevivem entre sessões. O que mora aqui é a **fonte** delas.

Editar aqui, commitar, publicar de lá. Nunca editar o HTML publicado direto: o que está publicado é build, não código.

## O que tem em cada pasta

| Pasta | O que é | Publicado em |
| --- | --- | --- |
| `complexo/` | O painel operacional — 9 abas: Painel do HUB, Mapa de Bairros, Tabela Comercial, Camada B2B, Agenda de Ativação, Vendas, Centro de Custo, Preço e Rotas, Estoque e Insumos | Artifact `3jL2vGzJmqVT1oTDsAGvQu` |
| `deck/` | Apresentação para investidor — 9 slides, tipo Slides | Artifact `T1zFa5debGfVfoNHkmnBWH` |
| `docs/` | Plano de Guerra do Estágio 1 e demais documentos de estratégia | Artifact `MpJqToQ31bn8fBJYgqSJ2w` |
| `editorial/` | Briefing, temário e calendário de conteúdo | — |
| `hub/` | A camada de análise por área (HUB Beco) — memória central e playbooks | — (não é publicado; é lido em conversa) |

## O Complexo Beco

Página única, sem build e sem dependência externa. Dois detalhes que não são óbvios e que já quebraram a ferramenta uma vez:

1. **Nada de `eval()` nem `new Function()`.** A política de segurança onde o artifact roda bloqueia os dois. Qualquer coisa que monte código em texto e execute falha em silêncio.
2. **Conteúdo gerado mora na fonte (`SEEDCLI`, `SEEDEV`); o banco guarda só o que o usuário editou**, com sobrescrita por campo e marcação de removido (`{removido:true}`). Republicar nunca pode apagar edição de usuário.

O banco é a capacidade `db` do artifact: `claude.use("db")`, coleções lidas com `db.collection(path).get()`. A coleção `hub_log` é escrita pelo HUB (ver seção abaixo), não pelo Complexo Beco; a aba Painel do HUB só lê.

## O HUB Beco

O Complexo Beco registra e calcula; não analisa nem recomenda. O HUB Beco é a camada de análise por área (marketing, tráfego, eventos, comercial B2B, expansão, loja, portfólio, financeiro) que você alimenta em conversa — ele lê a memória central em `hub/memoria/`, os playbooks em `hub/areas/`, e os números do dia do Complexo Beco, sem duplicar nenhum dos dois. Desenho completo em [`docs/superpowers/specs/2026-11-03-hub-beco-design.md`](docs/superpowers/specs/2026-11-03-hub-beco-design.md).

Na aba "Painel do HUB", cada uma das 8 áreas é navegável — toque no card pra ver só o histórico dela. A aba "Vendas" registra potes por canal todo mês e alimenta tanto a meta do Painel do HUB quanto as visões mensal/trimestral/semestral/anual de faturamento.

## Estado em 24/10/2026

- Venda direta: Fresh R$ 22,90 · Special e Boost R$ 24,90
- Atacado, inalterado: R$ 18,70 e R$ 20,50 — já é ~18% abaixo do direto, então quem revende aplicando 25% respeita o piso sozinho
- Meta de novembro: 1.000 potes/mês, cobrindo custo fixo de R$ 5.000 e pró-labore
- Gramatura: 140 g por pote, exceto Sorbet Morango, que é 120 g
- Três linhas, nunca uma quarta: Fresh, Special, Boost
