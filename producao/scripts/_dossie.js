const { JSDOM } = require("jsdom"), fs = require("fs");
const w = new JSDOM(fs.readFileSync("Balanceador de Receitas.html","utf8"),
                    {runScripts:"dangerously", url:"https://x.test/"}).window;

const FAT  = w.eval("eiFator()");
const POTE = w.eval("eiPote()");
const OVER = Number(w.eval("RCFG").overrun) || 21;
const EMB  = w.eval("CUSTO_EMB_POTE");
const IMP  = w.eval("IMPOSTO_SIMPLES");
const ING  = w.eval("INGREDIENTS");
const ROT  = w.eval("ROTULO");
const AADD = w.eval("ACUCAR_ADD_PCT");
const ingDe = n => ING.find(i=>i.nome===n) || {};

/* Mix Oficial e ingrediente composto feito na casa: a nutricionista precisa dele
   explodido nos componentes que a gente compra, nao como caixa-preta. */
const MIX_OFICIAL = [
  ["POLIDEXTROSE", 528], ["MALTITOL", 224], ["ERITRITOL", 163],
  ["INULINA", 81], ["STEVIA", 3]
];
/* Base proteica da calda unica (13/10), por 1 kg de base */
const BASE_PROT = [
  ["LEITE ZERO LACTOSE (INTEGRAL)", 692.4], ["BASE MEC PROTEIN", 130],
  ["LEITE EM PO DESNATADO ZL (BATAVO PENSE ZERO)", 120],
  ["GLICEROL (GLICERINA BIDESTILADA)", 30], ["POLIDEXTROSE", 20],
  ["CREMOBENE PREMIUM (LIGA NEUTRA)", 3.1], ["SAL", 1], ["STEVIA", 0.6]
];

/* A LINHA COMERCIAL NAO E O CAMPO familia. familia e a familia de FORMULACAO
   (1 creme/leite, 2 fruta/agua, 3 proteica) e serve para escolher os alvos.
   A linha que vai no rotulo sai de linhaBeco(): familia 2 -> fresh; fora isso,
   proteina >= 7,5% -> boost, senao special. O Pistache e familia 3 e linha SPECIAL. */
const FAMILIA_FORM = { 1:"creme / leite", 2:"fruta / agua", 3:"proteica" };

const EMBITENS = Object.entries(w.eval("EMB"))
  .map(([k,e])=>({nome:k, porPote:Number(e.porPote||0), preco:Number(e.preco||0)}))
  .filter(e=>e.porPote>0);

const out = { pote:POTE, fator:FAT, overrun:OVER, emb:EMB, embItens:EMBITENS, imposto:IMP,
              mixOficial:MIX_OFICIAL, baseProteica:BASE_PROT,
              sabores:[], ingredientes:[], pendencias:[] };

const usados = new Set();

w.eval("RECIPES").filter(r=>r.lancamento).forEach(r=>{
  const nome = r.nome.replace(" (LANCAMENTO)","");
  const m  = w.eval("computeRecipe")(r.linhas);
  const j  = w.eval("janelaConsumo")(Object.assign({},r,m));
  const sc = w.eval("computeScience")(m,-8,OVER);
  const P  = w.calcPoteDe(r.linhas, r.finalizacao||[]);
  const S  = w.selosDoPote(P);
  const lista = w.listaIngredientes(r.linhas, r.finalizacao||[], POTE);
  const gel  = w.gelatoPote(r);
  const massa = w.massaPote(r);
  const soma = r.linhas.reduce((a,l)=>a+Number(l.gramas),0);
  /* 21/10/2026 — QUANTA CALDA EXISTE DENTRO DO POTE. Nao e sempre gelatoPote.
     ALFAJOR (finAdicional): o biscoito vem POR CIMA, entao a calda ocupa os 135 g
       inteiros e o biscoito soma 15 g em cima -> caldaNoPote = gelatoPote.
     CAFE (mescla dentro): a delicia e ripada DENTRO dos 140 g, entao ela DESLOCA
       calda -> caldaNoPote = massaPote/(1+fin/1000) = 125,6 g, e a mescla pega os
       14,4 g que faltam para fechar 140.
     Eu usava gelatoPote nos dois casos e o Cafe fechava em 156,1 g de produto num
     pote de 140 g — R$ 0,77 de CMV a mais, que so apareceu quando conferi a planilha
     de CMV contra o numero do sistema. */
  const finTot = (r.finalizacao||[]).reduce((a,l)=>a+Number(l.gramas),0)/1000;
  const caldaNoPote = (finTot && !r.finAdicional) ? massa/(1+finTot) : gel;

  const linhas = r.linhas.map(l=>{
    usados.add(l.nome);
    const i = ingDe(l.nome);
    return { nome:l.nome, gkg:Number(l.gramas), pct:Number(l.gramas)/soma*100,
             noPote:Number(l.gramas)/1000*caldaNoPote,
             rotulo:(ROT[l.nome]||{}).r || l.nome.toLowerCase(),
             kcal:i.calorias };
  }).sort((a,b)=>b.gkg-a.gkg);

  const fin = (r.finalizacao||[]).map(l=>{
    usados.add(l.nome);
    const gPote = Number(l.gramas)/1000*caldaNoPote;
    return { nome:l.nome, gkg:Number(l.gramas), noPote:gPote,
             adicional: !!r.finAdicional,
             rotulo:(ROT[l.nome]||{}).r || l.nome.toLowerCase() };
  });

  out.sabores.push({
    nome,
    linha: (w.eval("linhaBeco")(m, r.familia, r.linhas) || "—").toUpperCase(),
    familia: r.familia, familiaForm: FAMILIA_FORM[r.familia] || "—",
    gelatoPote: gel, massaPote: massa, caldaNoPote,
    soma, linhas, fin,
    met: { sol:m.metrics.solidosTotais*100, agua:m.metrics.agua*100,
           gord:m.metrics.gordura*100, prot:m.metrics.proteinas*100,
           acu:m.metrics.acucares*100, solDif:m.metrics.solidosDif*100,
           pod:m.pod, pac:m.pac, kcalCalda:m.caloriasPer100,
           custoKg:m.custo/m.gramas*1000 },
    janela:[j[0],j[1]], frozen:sc.frozen*100,
    /* 21/10/2026 — ACUCAR DE ROTULO, NAO O TECNICO.
       calcPoteDe devolve DOIS campos de acucar e a diferenca e a razao de existir
       deste documento inteiro:
         .acucares     = tecnico, acucar + poliol, alimenta POD e PAC na formulacao
         .acucarRotulo = o que a ANVISA chama de acucares totais, sem os poliois
       Eu ia mandar o tecnico para a nutricionista. No Alfajor sao 15,59% contra
       10,03% de rotulo — 5,5 pontos de acucar que nao existem no produto.
       Carboidratos totais NAO sao calculados aqui de proposito: a convencao de
       incluir ou nao fibra e poliol e decisao dela, e chutar isso seria pior que
       deixar em branco. Vai cada componente medido, separado. */
    pote: { kcal:P.kcal100, acu:P.acucarRotulo, acuTecnico:P.acucares,
            poliois:P.poliois, acucarAdd:P.acucarAdd, prot:P.proteinas,
            gord:P.gordura, gordSat:P.gordSat,
            gordTrans: r.linhas.reduce((a,l)=>a+Number(ingDe(l.nome).gordTrans||0)*Number(l.gramas)/100,0)/soma*100,
            fibra:P.fibra, sodio:P.sodio*1000,
            solidosTotais:P.solidosTotais, custoKg:P.custoKg },
    selos:S, alerg:[...(lista.alerg||[])], temPoliol:!!lista.temPoliol,
    rdc727:(lista.itens||[]).map(i=>({r:i.r, pct:i.pct})),
    preco: w.precoDe(r.nome),
    cmv: P.custoKg/1000*massa*FAT + EMB
  });
});

/* ficha de cada ingrediente usado, mais o que a nutricionista precisa conferir */
[...usados].sort().forEach(n=>{
  const i = ingDe(n), r = ROT[n] || {};
  const conferir = [];
  if(r.comp)                 conferir.push("ingrediente COMPOSTO — pedir a lista interna ao fabricante");
  if(!ROT[n])                conferir.push("sem nome de rótulo definido");
  if(!Number(i.custoKg))     conferir.push("sem preço no cadastro");
  if(/^MIX /.test(n))        conferir.push("feito na casa — ver composição na seção do Mix Oficial");
  out.ingredientes.push({
    nome:n,
    rotulo: r.r || "—",
    alerg: r.al || [],
    composto: !!r.comp,
    obs: r.ver || "",
    acucarAdd: Number(AADD[n]||0),
    nut: { kcal:Number(i.calorias||0), acucares:Number(i.acucares||0),
           gordura:Number(i.gordura||0), gordSat:Number(i.gordSat||0),
           gordTrans:Number(i.gordTrans||0), proteinas:Number(i.proteinas||0),
           fibra:Number(i.fibra||0), solidosTotais:Number(i.solidosTotais||0),
           solidosDif:Number(i.solidosDif||0), sodio:Number(i.sodio||0)*1000,
           pod:Number(i.pod||0), pac:Number(i.pac||0) },
    custoKg:Number(i.custoKg||0),
    conferir
  });
  if(conferir.length) out.pendencias.push({ ingrediente:n, itens:conferir });
});

fs.writeFileSync("_dossie.json", JSON.stringify(out,null,1));
console.log("ok — "+out.sabores.length+" sabores · "+out.ingredientes.length+" ingredientes · "+out.pendencias.length+" com pendência");
out.sabores.forEach(s=>console.log("   "+s.nome.padEnd(22)+s.linha.padEnd(9)+
  "sol "+s.met.sol.toFixed(2)+"%  prot "+s.met.prot.toFixed(2)+"%  "+s.linhas.length+" ingredientes"+
  (s.fin.length?" + "+s.fin.length+" finalização":"")));
