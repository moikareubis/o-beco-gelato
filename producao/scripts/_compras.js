const { JSDOM } = require("jsdom"), fs = require("fs");
const w = new JSDOM(fs.readFileSync("Balanceador de Receitas.html","utf8"),
                    {runScripts:"dangerously", url:"https://x.test/"}).window;

const FAT  = w.eval("eiFator()");
const POTE = w.eval("eiPote()");
const ING  = w.eval("INGREDIENTS");
const EST  = w.eval("ESTOQUE_INS");
const EMB  = w.eval("EMB");
const R    = w.eval("RECIPES").filter(r=>r.lancamento);

/* O Mix Oficial e feito na casa. Para compras, o que interessa e o que se COMPRA,
   entao ele entra explodido nos componentes. */
const MIXC = {"POLIDEXTROSE":528,"MALTITOL":224,"ERITRITOL":163,"INULINA":81,"STEVIA":3};
const TOTMIX = Object.values(MIXC).reduce((a,b)=>a+b,0);

/* consumo em gramas por POTE de cada sabor, ja com a perda de processo e
   com o mix explodido nos insumos que ele compra de fato */
const consumo = {};   // consumo[sabor][insumo] = g por pote
R.forEach(r=>{
  const nome = r.nome.replace(" (LANCAMENTO)","");
  const fin  = (r.finalizacao||[]).reduce((a,l)=>a+Number(l.gramas),0)/1000;
  const caldaNoPote = (fin && !r.finAdicional) ? w.massaPote(r)/(1+fin) : w.gelatoPote(r);
  const acc = {};
  const add=(n,g)=>{ if(n==="AGUA") return; acc[n]=(acc[n]||0)+g; };
  r.linhas.forEach(l=>{
    const g = Number(l.gramas)/1000*caldaNoPote*FAT;
    if(/^MIX /.test(l.nome)) Object.entries(MIXC).forEach(([c,p])=>add(c, g*p/TOTMIX));
    else add(l.nome, g);
  });
  (r.finalizacao||[]).forEach(l=> add(l.nome, Number(l.gramas)/1000*caldaNoPote*FAT));
  consumo[nome]=acc;
});

/* ESTOQUE DE POTES PRONTOS — CONTAGEM FISICA DE 22/10/2026, ditada pelo Gabriel.
   325 potes. Substitui a contagem de 13/10 (262 potes).

   22/10/2026 — ATENCAO AO RISCO DE SUBTRAIR DUAS VEZES: esta contagem e POSTERIOR
   ao pedido 000007 (16/10), entao os 125 potes daquele pedido JA SAIRAM do numero
   contado. Por isso as linhas do 000007 na aba MOVIMENTO viraram tipo "HISTORICO"
   em vez de "VENDA": o SUMIFS do saldo so soma PRODUCAO e VENDA, de forma que o
   historico fica visivel sem ser descontado de novo.
   Regra geral: toda contagem fisica zera a conta. O que veio antes dela e historico. */
const POTES_CONTAGEM = {   // 22/10/2026 — contagem fisica
  "Pistache":46, "Café Proteico":40, "Alfajor":38, "Manga com Maracujá":60,
  "Brigadeiro Proteico":51, "Sorbet Morango":32, "Torta de Limão":58
};
const PEDIDO7 = {          // 16/10/2026 — O BECO, 125 potes
  "Brigadeiro Proteico":20, "Café Proteico":15, "Manga com Maracujá":15,
  "Pistache":20, "Torta de Limão":20, "Sorbet Morango":15, "Alfajor":20
};

/* O QUE EU SEI DE FORNECEDOR vem de conversa, nao do cadastro — o sistema nunca
   teve esse campo. Marquei a procedencia de cada linha para ele saber no que confiar. */
const FORN = {
  "CREMOBENE PREMIUM (LIGA NEUTRA)":      ["Biobene","Cremobene Premium","","conversa"],
  "PASTA PISTACCHIO 100% CALIFÓRNIA":     ["","","","—"],
  "PASTA FRAGOLA MEC3 (18047)":           ["MEC3","MEC3 18047","","ficha"],
  "PASTA BISCOTTINO MEC3 (14094)":        ["MEC3","MEC3 14094","","ficha"],
  "PASTA CAFÉ SELECTA (BALDE 2 KG)":      ["","Selecta","balde 2 kg","conversa"],
  "GUSTO LIMONE SICILIA (PÓ)":            ["MEC3","Gusto Limone Sicilia","","ficha"],
  "DELÍCIA DE AMENDOIM PROTEICO":         ["","","","—"],
  "DOCE DE LEITE VIÇOSA ZERO":            ["Viçosa","Viçosa Zero","pote 400 g","nota 39,90/400 g"],
  "CREME DE LEITE FRESCO 35% ZL (VERDE CAMPO LACFREE)": ["Verde Campo","Lacfree","500 g","nota 28,90/500 g"],
  "LEITE EM PO DESNATADO ZL (BATAVO PENSE ZERO)": ["Batavo","Pense Zero","","conversa"],
  "LEITE ZERO LACTOSE (INTEGRAL)":        ["Leitíssimo","","","conversa"],
  "ERITRITOL":                            ["","","1 kg","cotação Huakang 25 kg R$ 14,75"],
  "MALTITOL":                             ["","","","cotação Yusweet 25 kg R$ 17,95"],
  "POLIDEXTROSE":                         ["","","10 kg","cotação Bailong 25 kg R$ 12,85"],
  "BISCOITO ALFAJOR DE CHOCOLATE (ZERO LACTOSE)": ["","","caixa 4 un","nota 8,00/4 un"],
  "BASE MEC PROTEIN":                     ["MEC3","Base MEC Protein","","ficha"],
};

/* insumos usados em receita, ja explodidos */
const usados = new Set();
Object.values(consumo).forEach(a=>Object.keys(a).forEach(n=>usados.add(n)));

const out = {
  pote: POTE, fator: FAT,
  sabores: R.map(r=>r.nome.replace(" (LANCAMENTO)","")),
  consumo,
  insumos: [...usados].sort().map(n=>{
    const i = ING.find(x=>x.nome===n) || {};
    const fo = FORN[n] || ["","","",""];
    return { nome:n, custoKg:Number(i.custoKg||0), estoque:Number(EST[n]||0),
             fornecedor:fo[0], marca:fo[1], embalagem:fo[2], origem:fo[3] };
  }),
  embalagem: Object.entries(EMB).map(([k,e])=>({
    nome:k, porPote:Number(e.porPote||0), preco:Number(e.preco||0), saldo:Number(e.saldo||0)
  })),
  potesContagem: POTES_CONTAGEM,
  pedido7: PEDIDO7,
};

fs.writeFileSync("_compras.json", JSON.stringify(out,null,1));
console.log("ok — "+out.insumos.length+" insumos · "+out.sabores.length+" sabores · "+out.embalagem.length+" itens de embalagem");
const semForn = out.insumos.filter(i=>!i.fornecedor).length;
const semPreco= out.insumos.filter(i=>!i.custoKg).length;
console.log("   sem fornecedor: "+semForn+"   sem preço: "+semPreco);
