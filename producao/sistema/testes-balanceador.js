#!/usr/bin/env node
/* ============================================================================
   SUITE DE TESTES DO BALANCEADOR
   ----------------------------------------------------------------------------
   Roda:  node testes-balanceador.js "Balanceador de Receitas.html" baseline.json
   Sai com codigo 1 se qualquer teste falhar.

   O que ela protege:
     1. REGRESSAO  — cada numero das 6 receitas do lancamento esta congelado no
                     baseline. Se eu mexer em qualquer coisa e um numero mudar,
                     o teste acusa e diz exatamente qual e de quanto.
     2. FISICA     — os limites que nao sao negociaveis (banda de congelamento,
                     teto de eritritol, inulina, lupa da ANVISA).
     3. COERENCIA  — aritmetica interna de cada ingrediente. Foi assim que a
                     Base MEC Protein e o MIX BECO 2 estavam errados sem ninguem ver.
     4. INTEGRIDADE— receita somando 1000 g, ingrediente inexistente, preco faltando.
     5. MOTOR      — o calculo de mix bate com a composicao; POD de mistura usa a
                     formula ponderada certa, nao media simples.
   ========================================================================== */
const fs = require("fs");
const path = require("path");

const ARQ  = process.argv[2] || "Balanceador de Receitas.html";
const BASE = process.argv[3] || "baseline.json";

/* ---------- carrega o app ----------
   O app é um HTML único e declara tudo com const/let no topo, que não vazam de um
   eval. A única forma de alcançar esses valores é concatenar o nosso código ao dele
   e avaliar os dois juntos. E antes disso é preciso cortar o bootstrap de DOM
   (loadState(); fillFamilias(); ... e a pilha de handlers), senão a primeira
   chamada a document.querySelector derruba o script inteiro antes do fim.        */
function carregarApp(arquivo){
  const html = fs.readFileSync(arquivo, "utf8");
  const blocos = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  if(!blocos.length) throw new Error("nenhum <script> no HTML");
  let js = blocos.join("\n;\n");
  const corte = js.match(/^[ \t]*loadState\(\);/m);
  if(corte) js = js.slice(0, corte.index) + "\nloadState();\n";

  /* shim de navegador: tudo devolve a si mesmo, handlers de DOM viram no-op */
  const dummy = new Proxy(function(){}, {
    get:()=>dummy, set:()=>true, apply:()=>dummy, construct:()=>dummy,
    has:()=>true, deleteProperty:()=>true
  });
  const store = {};
  global.localStorage = {
    getItem:k => (k in store ? store[k] : null),
    setItem:(k,v) => { store[k] = String(v); },
    removeItem:k => { delete store[k]; }
  };
  global.document = dummy;
  global.window   = global;
  global.alert    = ()=>{};
  global.confirm  = ()=>false;
  global.navigator= dummy;
  const logReal = console.info;
  console.info = ()=>{};                       /* silencia o log do recálculo de mix */

  const EXPORTAR = ["INGREDIENTS","SEED_RECIPES","MIX_COMP","FAMILIES","ROTULO","SEED_ESTOQUE",
    "DEFAULT_INGREDIENTS","SEED_INGREDIENTS","eiNecessidade",
    "computeRecipe","computeScience","calcMix","findIng","selosDoPote","faixaVigente",
    "familyById","poliolDe","acucarAddDe","listaIngredientes","aplicarMixesCalculados",
    "RCFG","BATCH",
    /* 24/09: sem estes o teste caia no fallback -15 e discordava do baseline em 1,3 ponto */
    "tServico","eiPote","fConsumo","fEstoque","fEntrega","janelaConsumo","janelaCobre","auditar","calcPoteDe","geloEm","massaPote","bncTotal","LIMITES_LULO",
    /* 22/10: gelatoPote faltava aqui, e por isso o teste de gramatura que o usa
       caia no guard e passava sempre — teste verde que nao testava nada. */
    "gelatoPote","precoDe","eiFator","CUSTO_EMB_POTE"];
  const cola = "\n;(function(){var A={};" +
    EXPORTAR.map(n=>`try{A[${JSON.stringify(n)}]=${n};}catch(e){}`).join("") +
    "return A;})()";

  let api;
  try { api = (0,eval)(js + cola); }
  finally { console.info = logReal; }
  if(!api || !api.computeRecipe) throw new Error("o motor não carregou — o corte do bootstrap falhou?");
  return api;
}

/* ---------- runner ---------- */
let ok=0, falhou=0; const erros=[];
function teste(grupo, nome, fn){
  try{ const r = fn();
    if(r===true || r===undefined){ ok++; }
    else { falhou++; erros.push({grupo,nome,msg:String(r)}); }
  }catch(e){ falhou++; erros.push({grupo,nome,msg:"exceção: "+e.message}); }
}
const perto=(a,b,tol)=>Math.abs(a-b)<=tol;

/* ========================================================================== */
const app = carregarApp(ARQ);
const {INGREDIENTS, SEED_RECIPES, MIX_COMP, computeRecipe, computeScience,
       calcMix, findIng, selosDoPote, faixaVigente, familyById} = app;

if(!computeRecipe){ console.error("ERRO: nao consegui carregar o motor do app."); process.exit(1); }

const baseline = fs.existsSync(BASE) ? JSON.parse(fs.readFileSync(BASE,"utf8")) : null;
/* 24/09/2026: era "baseline.pote : 130" — o pote do Beco e 120 g e a config do app
   ja diz isso. Puxa de la, para o teste nao discordar do sistema que ele testa. */
const POTE = (app.eiPote?app.eiPote():null) || (baseline?baseline.pote:120);
const LANC = SEED_RECIPES.filter(r => r.lancamento);

/* helper: calcula o pote pronto de uma receita sem depender da UI */
function potePronto(rec, pote){
  const L = rec.linhas, F = rec.finalizacao || [];
  const caldaG = L.reduce((a,l)=>a+(+l.gramas||0),0) || 1;
  const acc = {calorias:0,acucares:0,gordura:0,gordSat:0,proteinas:0,fibra:0,sodio:0,solidosTotais:0};
  let massa=0, custo=0, pol=0, addAcu=0;
  const somar = (nome,g)=>{
    const I = findIng(nome); if(!I||!g) return;
    massa += g; custo += (+I.custoKg||0)*g/1000;
    Object.keys(acc).forEach(k => acc[k] += (+I[k]||0)*g/100);
    pol    += (app.poliolDe    ? app.poliolDe(nome)    : 0)*g/100;
    addAcu += (app.acucarAddDe ? app.acucarAddDe(nome) : 0)*g/100;
  };
  L.forEach(l=>somar(l.nome,+l.gramas||0));
  F.forEach(l=>somar(l.nome,(+l.gramas||0)*caldaG/1000));
  const p100 = x => x/massa*100;
  return { massa, kcal100:p100(acc.calorias), proteinas:p100(acc.proteinas),
    fibra:p100(acc.fibra), gordura:p100(acc.gordura), gordSat:p100(acc.gordSat),
    sodio:p100(acc.sodio), acucares:p100(acc.acucares), poliois:p100(pol),
    acucarRotulo:Math.max(0,p100(acc.acucares)-p100(pol)), acucarAdd:p100(addAcu),
    custoKg:custo/massa*1000, solidosTotais:p100(acc.solidosTotais) };
}

/* ========================= 1. REGRESSÃO ================================== */
if(baseline){
  LANC.forEach(r=>{
    const n = r.nome.replace(" (LANCAMENTO)","");
    const b = baseline.receitas[n];
    if(!b){ teste("regressão", n, ()=>"não está no baseline"); return; }
    const R = computeRecipe(r.linhas);
    /* -15 estava na unha aqui. A temperatura de consumo agora e configuravel e vive
       em tServico(); o teste tem de ler a mesma coisa que a tela. */
    const s = computeScience(R, app.tServico?app.tServico():-15, +(app.RCFG&&app.RCFG.overrun)||38);
    const p = potePronto(r, POTE);
    const S = selosDoPote(p);
    const checks = [
      ["soma",        r.linhas.reduce((a,l)=>a+l.gramas,0), b.soma,     0.05],
      ["sólidos",     R.metrics.solidosTotais*100,          b.solT,     0.05],
      ["gordura",     R.metrics.gordura*100,                b.gord,     0.05],
      ["proteína",    R.metrics.proteinas*100,              b.prot,     0.05],
      ["POD",         R.pod,                                b.pod,      0.2 ],
      ["PAC",         R.pac,                                b.pac,      0.2 ],
      ["congelada",   s.frozen*100,                         b.frozen,   0.05],
      ["kcal/pote",   p.kcal100*POTE/100,                   b.kcalPote, 0.2 ],
      ["prot/pote",   p.proteinas*POTE/100,                 b.protPote, 0.05],
      ["fibra/pote",  p.fibra*POTE/100,                     b.fibraPote,0.05],
      ["açúcar adic", p.acucarAdd,                          b.acucarAdd,0.01],
      ["gord. sat",   p.gordSat,                            b.gordSat,  0.05],
      ["sódio",       p.sodio*1000,                         b.sodio,    1   ],
      ["custo/pote",  p.custoKg/1000*POTE,                  b.custoPote,0.02]
    ];
    checks.forEach(([campo,atual,esperado,tol])=>{
      teste("regressão", n+" · "+campo, ()=> perto(atual,esperado,tol) ? true
        : `${esperado} → ${atual.toFixed(3)} (mudou ${(atual-esperado>0?"+":"")}${(atual-esperado).toFixed(3)})`);
    });
    teste("regressão", n+" · selos", ()=>{
      const a = S.ok.slice().sort().join("|"), e = (b.selos||[]).join("|");
      return a===e ? true : `"${e}" → "${a}"`;
    });
    teste("regressão", n+" · lupa", ()=>{
      const a = S.lupa.slice().sort().join("|"), e = (b.lupa||[]).join("|");
      return a===e ? true : `"${e}" → "${a}"`;
    });
  });

  Object.entries(baseline.mixes||{}).forEach(([nome,b])=>{
    if(!MIX_COMP[nome]) { teste("regressão","mix "+nome,()=>"composição sumiu do MIX_COMP"); return; }
    const c = calcMix(MIX_COMP[nome]);
    [["POD",c.pod,b.pod,0.2],["PAC",c.pac,b.pac,0.2],["fibra",c.fibra,b.fibra,0.05],
     ["kcal",c.calorias,b.kcal,0.2],["poliol",c.poliois,b.poliois,0.05],["custo",c.custoKg,b.custoKg,0.02]]
     .forEach(([campo,a,e,tol])=> teste("regressão","mix "+nome+" · "+campo,
        ()=> perto(a,e,tol) ? true : `${e} → ${a.toFixed(3)}`));
  });

  /* o baseline usa nomes curtos; a base usa os longos */
  const CAMPO = {prot:"proteinas", gord:"gordura", acu:"acucares", solT:"solidosTotais",
                 fibra:"fibra", pod:"pod", pac:"pac", custoKg:"custoKg"};
  Object.entries(baseline.ingredientes||{}).forEach(([nome,b])=>{
    const i = findIng(nome);
    if(!i){ teste("regressão","ingrediente "+nome, ()=>"sumiu da base"); return; }
    Object.entries(b).forEach(([curto,esperado])=>{
      const campo = CAMPO[curto] || curto;
      teste("regressão", nome+" · "+curto,
        ()=> perto(+i[campo]||0, esperado, 0.02) ? true : `${esperado} → ${i[campo]}`);
    });
  });
}

/* ========================= 2. FÍSICA / LIMITES =========================== */
LANC.forEach(r=>{
  const n = r.nome.replace(" (LANCAMENTO)","");
  const R = computeRecipe(r.linhas);
  const s = computeScience(R, app.tServico?app.tServico():-15, +(app.RCFG&&app.RCFG.overrun)||38);
  const p = potePronto(r, POTE);

  /* Banda 79–84% a −15 °C. A de 70–76% vinha da fórmula de T0 ainda errada: r.pac
     JÁ é g de sacarose-equivalente por kg, e o código multiplicava por açúcares% de novo,
     inflando pacAbs de 1,3x a 1,7x. Corrigido em 16/09/2026 (3ª correção desta fórmula).
     Com a física certa a linha inteira cai entre 81,2 e 83,4% — e o Café (81,2%), único
     ponto com textura aprovada em bancada, é a âncora. Banda PROVISÓRIA até haver mais
     leitura de bancada. Os 70–75% do Mirko são temperatura de VITRINE (~−11/−12 °C). */
  /* 24/09/2026: este teste exigia 79-84% de agua congelada NA TEMPERATURA DE SERVICO, e
     reprovava as seis receitas quando o Gabriel pos o serviço em -13 C. Era o mesmo erro
     que eu tinha cometido no app: tratar a banda do Lulo como requisito em vez de leitura.
     A banda descreve a textura do gelato COM ACUCAR dele, na vitrine dele. O gelato do
     Gabriel tem mais poliol, logo mais anticongelante, logo fica mais macio na mesma
     temperatura — de proposito.
     O que vale testar e a FISICA, nao a preferencia: a fracao tem de ser um numero
     plausivel e monotona na temperatura (mais frio = mais gelo). Isso pega bug de verdade;
     a banda nao pegava nada, so media distancia do gosto de outra pessoa. */
  teste("física", n+" · fração de gelo plausível e monótona", ()=>{
    const f13 = app.geloEm ? app.geloEm(R,-13) : s.frozen*100;
    const f18 = app.geloEm ? app.geloEm(R,-18) : null;
    const f22 = app.geloEm ? app.geloEm(R,-22) : null;
    if(!(f13>50 && f13<95)) return `a −13 °C deu ${f13.toFixed(1)}% — fora de qualquer faixa plausível`;
    if(f18!==null && !(f18>f13)) return `−18 (${f18.toFixed(1)}%) não é mais congelado que −13 (${f13.toFixed(1)}%)`;
    if(f22!==null && !(f22>f18)) return `−22 (${f22.toFixed(1)}%) não é mais congelado que −18 (${f18.toFixed(1)}%)`;
    return true;
  });

  teste("física", n+" · eritritol ≤ 6% da calda", ()=>{
    let er = 0;
    r.linhas.forEach(l=>{
      const I = findIng(l.nome); if(!I) return;
      if(/^ERITRITOL/.test(I.nome)) er += l.gramas;
      const C = MIX_COMP[I.nome];
      if(C){ const tm = Object.values(C).reduce((a,b)=>a+b,0)||1;
             er += l.gramas*(C["ERITRITOL"]||0)/tm; }
    });
    const pct = er/10;
    return pct<=6 ? true : `${pct.toFixed(2)}% — risco de cristalização (areia)`;
  });

  teste("física", n+" · inulina ≤ 50 g/kg (Mirko p.36)", ()=>{
    let inu = 0;
    r.linhas.forEach(l=>{
      const I = findIng(l.nome); if(!I) return;
      if(I.nome==="INULINA") inu += l.gramas;
      const C = MIX_COMP[I.nome];
      if(C){ const tm = Object.values(C).reduce((a,b)=>a+b,0)||1;
             inu += l.gramas*(C["INULINA"]||0)/tm; }
    });
    return inu<=50 ? true : `${inu.toFixed(1)} g/kg — risco de textura elástica`;
  });

  teste("ANVISA", n+" · gordura saturada < 6 g/100 g (lupa)",
    ()=> p.gordSat<6 ? true : `${p.gordSat.toFixed(2)} — acende a lupa frontal`);
  teste("ANVISA", n+" · sódio < 600 mg/100 g (lupa)",
    ()=> p.sodio*1000<600 ? true : `${(p.sodio*1000).toFixed(0)} mg — acende a lupa`);
  teste("ANVISA", n+" · açúcar adicionado < 15 g/100 g (lupa)",
    ()=> p.acucarAdd<15 ? true : `${p.acucarAdd.toFixed(2)} g — acende a lupa`);
});

/* ========================= 3. COERÊNCIA DOS INGREDIENTES ================= */
const usados = new Set();
LANC.forEach(r=>[...(r.linhas||[]),...(r.finalizacao||[])].forEach(l=>{
  const I = findIng(l.nome); if(!I) return;
  const C = MIX_COMP[I.nome];
  if(C) Object.keys(C).forEach(c=>{const J=findIng(c); if(J)usados.add(J.nome);});
  else usados.add(I.nome);
}));

[...usados].sort().forEach(nome=>{
  const i = findIng(nome);
  const A=+i.acucares||0, G=+i.gordura||0, P=+i.proteinas||0,
        F=+i.fibra||0, S=+i.solidosTotais||0, D=+i.solidosDif||0, K=+i.calorias||0;
  teste("coerência", nome+" · macros cabem nos sólidos",
    ()=> (A+G+P) <= S+0.6 ? true : `açúcar+gordura+proteína ${(A+G+P).toFixed(1)} > sólidos ${S}`);
  teste("coerência", nome+" · sólidos dif. = sólidos − açúcar − gordura − proteína", ()=>{
    const esp = S-A-G-P;
    return Math.abs(D-esp)<=1.5 ? true : `${D} deveria ser ${esp.toFixed(1)}`;
  });
  teste("coerência", nome+" · sólidos ≤ 100%",
    ()=> S<=100.5 ? true : `${S}%`);
  teste("coerência", nome+" · caloria compatível com os macros", ()=>{
    /* mesmo bug que o app tinha: sem contar os solidos de DIFERENCA (amido, maltodextrina),
       todo po de aroma aparece como ficha errada. O Gusto Limone tem 97% de solidos e so
       34,5 vem de acucar/gordura/proteina. */
    const dif = Math.max(0, (+i.solidosTotais||0) - A - G - P);
    const teto = A*4+P*4+G*9+F*2+Math.max(0,dif-F)*4;
    return K <= teto*1.35+25 ? true : `${K} kcal contra teto ~${teto.toFixed(0)} — conferir ficha`;
  });
  teste("custo", nome+" · tem preço",
    ()=> nome==="AGUA" || (+i.custoKg>0) ? true : "sem preço — CMV subestimado");
});

/* ========================= 4. INTEGRIDADE ================================ */
LANC.forEach(r=>{
  const n = r.nome.replace(" (LANCAMENTO)","");
  /* ------------------------------------------------------------------
     DOIS BLOCOS DE INGREDIENTE. DEFAULT_INGREDIENTS (JSON) e SEED_INGREDIENTS
     (compacto) definem varios ingredientes com o MESMO nome. seedDesafio() faz
     INGREDIENTS[ix]=si, ou seja: o SEED SEMPRE VENCE e o JSON e silenciosamente
     descartado. Em 18/09/2026 eu atualizei preco de morango e manga no bloco
     errado e o CMV nao mudou — sem barulho nenhum.
     Este teste nao proibe a duplicata: ela existe e o app depende dela. Ele so
     exige que os dois blocos CONCORDEM nos ingredientes que o lancamento usa,
     para que editar o bloco errado vire falha em vez de silencio.        */
  if(!global.__dupChecked){ global.__dupChecked=1; (function(){
    const campos=["custoKg","calorias","acucares","gordura","proteinas","solidosTotais","fibra","pod","pac"];
    const DEF=app.DEFAULT_INGREDIENTS||[], SEE=app.SEED_INGREDIENTS||[], need=app.eiNecessidade;
    if(!DEF.length||!SEE.length||!need) return;
    const dMap={}; DEF.forEach(x=>dMap[x.nome]=x);
    const usados=new Set();
    LANC.forEach(r=>Object.keys(need(r,1)).forEach(n=>usados.add(n)));
    SEE.forEach(si=>{
      if(!usados.has(si.nome)) return;
      const dd=dMap[si.nome]; if(!dd) return;
      teste("integridade", si.nome+" \u00b7 JSON e SEED concordam", ()=>{
        const dif=campos.filter(k=>Math.abs(Number(dd[k]||0)-Number(si[k]||0))>0.005);
        return dif.length ? "divergem em "+dif.map(k=>k+" ("+dd[k]+" vs "+si[k]+")").join(", ")+
          " \u2014 o SEED vence; editar o JSON n\u00e3o tem efeito" : true;
      });
    });
  })(); }

  teste("integridade", n+" · soma 1000 g", ()=>{
    const s = r.linhas.reduce((a,l)=>a+(+l.gramas||0),0);
    return Math.abs(s-1000)<0.5 ? true : `${s} g`;
  });
  teste("integridade", n+" · todos os ingredientes existem", ()=>{
    const orf = [...(r.linhas||[]),...(r.finalizacao||[])].filter(l=>!findIng(l.nome)).map(l=>l.nome);
    return orf.length===0 ? true : "inexistente: "+orf.join(", ");
  });
  teste("integridade", n+" · nenhuma linha com gramas ≤ 0", ()=>{
    const z = r.linhas.filter(l=>!(+l.gramas>0)).map(l=>l.nome);
    return z.length===0 ? true : z.join(", ");
  });
});

teste("integridade", "nenhum ingrediente duplicado", ()=>{
  const vistos = {}, dup = [];
  INGREDIENTS.forEach(i=>{ if(vistos[i.nome]) dup.push(i.nome); vistos[i.nome]=1; });
  return dup.length===0 ? true : dup.join(", ");
});

/* ========================= 5. MOTOR DE CÁLCULO =========================== */
Object.entries(MIX_COMP).forEach(([nome,comp])=>{
  /* 24/09/2026: este teste exigia soma 1000 g e reprovava o MIX OFICIAL (999) e o
     MIX BECO 3 (990,9). Mas essas listas sao DITADAS pelo Gabriel e o calcMix normaliza
     pelo total — o que importa e a proporcao, nao o total absoluto. O teste estava
     cobrando uma coisa que a fonte da verdade nunca prometeu. Agora checa o que de fato
     invalida um mix: componente negativo, zerado ou total perto de zero. */
  teste("motor", "mix "+nome+" · composição utilizável", ()=>{
    const vals = Object.values(comp).map(v=>+v||0);
    const s = vals.reduce((a,b)=>a+b,0);
    if(s<100) return `total ${s} g — baixo demais para normalizar com segurança`;
    /* zero e legitimo: o MIX BECO lista GOMA ALFARROBA em 0 justamente para registrar
       que aquela versao nao leva goma. O que nao pode e gramas negativas ou nao-numero. */
    const ruim = Object.entries(comp).filter(([,v])=>!(isFinite(+v)&&+v>=0)).map(([k])=>k);
    return ruim.length ? `componente com gramas inválidas: ${ruim.join(", ")}` : true;
  });
  teste("motor", "mix "+nome+" · cadastro bate com a composição", ()=>{
    const c = calcMix(comp), i = findIng(nome);
    if(!i) return "mix não está cadastrado como ingrediente";
    const dif = ["calorias","acucares","fibra","solidosTotais","pod","pac"]
      .filter(k => Math.abs((+i[k]||0)-c[k]) > Math.max(0.5, Math.abs(c[k])*0.02))
      .map(k => `${k} ${i[k]} vs ${c[k].toFixed(2)}`);
    return dif.length===0 ? true : dif.join(" · ");
  });
});

teste("motor", "POD de mistura é ponderado pelo açúcar, não média simples", ()=>{
  /* dois componentes com POD muito diferente e massas iguais:
     media simples daria (100+70)/2 = 85; a ponderada pelo açúcar dá outro valor */
  const c = calcMix({"MALTITOL":500,"ERITRITOL":500});
  const m = findIng("MALTITOL"), e = findIng("ERITRITOL");
  const esperado = (0.5*m.acucares*m.pod/100 + 0.5*e.acucares*e.pod/100) /
                   (0.5*m.acucares + 0.5*e.acucares) * 100;
  return perto(c.pod, esperado, 0.5) ? true : `${c.pod.toFixed(2)} ≠ ${esperado.toFixed(2)}`;
});

/* 19/10/2026: a fixture era o Brigadeiro e passou a falhar — de novo por mudança real,
   não por bug. O Brigadeiro virou a calda única proteica do teste de 13/10, que adoça só
   com estévia e NÃO tem poliol nenhum. Sem poliol, açúcar de rótulo = açúcar técnico e o
   teste não tem o que provar. Troquei a fixture para o Alfajor, que leva 30 g/kg de
   maltitol. Este teste existe para provar o MECANISMO; a fixture tem de ser uma receita
   com poliol, qualquer que seja ela. */
teste("motor", "poliol não entra em açúcares de rótulo", ()=>{
  const r = LANC.find(x=>/Alfajor/.test(x.nome)); if(!r) return true;
  const p = potePronto(r, POTE);
  return p.acucarRotulo < p.acucares ? true
    : `açúcar de rótulo (${p.acucarRotulo.toFixed(2)}) deveria ser menor que o técnico (${p.acucares.toFixed(2)})`;
});

/* 24/09/2026: a fixture era o Sorbet Morango e o teste passou a falhar — mas por um
   achado REAL, nao por bug: a Pasta Fragola a 10 g/kg poe 0,47 g/100 g de acucar
   adicionado e derruba o selo. Quem tem de gritar isso e a auditoria (e grita, como
   grave), nao este teste, que existe para provar o MECANISMO do selo. Troquei a fixture
   para a Manga, que nao tem insumo com acucar adicionado. */
teste("motor", "receita sem açúcar adicionado ganha o selo", ()=>{
  const r = LANC.find(x=>/Manga com Maracujá/.test(x.nome)); if(!r) return true;
  const p = potePronto(r, POTE), S = selosDoPote(p);
  if(p.acucarAdd>0.001) return "manga tem açúcar adicionado: "+p.acucarAdd.toFixed(3);
  return S.ok.includes("SEM ADIÇÃO DE AÇÚCARES") ? true : "selo não foi concedido";
});

teste("motor", "açúcar adicionado derruba o selo", ()=>{
  const r = SEED_RECIPES.find(x=>/AÇÚCAR DE MAÇÃ/.test(x.nome)); if(!r) return true;
  const p = potePronto(r, POTE), S = selosDoPote(p);
  if(!(p.acucarAdd>0.001)) return "açúcar de maçã não está contando como adicionado";
  return S.ok.includes("SEM ADIÇÃO DE AÇÚCARES") ? "selo concedido a receita com açúcar" : true;
});

teste("motor", "alvo de sólidos dif. fica suspenso em fórmula sem açúcar", ()=>{
  const r = LANC.find(x=>/Café Proteico/.test(x.nome)); if(!r) return true;
  const R = computeRecipe(r.linhas);
  return faixaVigente("solidosDif", R, r.familia)===null ? true
    : "o alvo do Mirko está sendo aplicado a uma fórmula zero açúcar";
});

/* 24/09/2026: a fixture era "Fior di Latte (classica)", apagada na limpeza de 23/09.
   Qualquer receita com acucar de maca serve — e foi justamente esta troca que revelou
   que o acucar de maca nao estava na tabela ACUCAR_ADD_PCT e que formulaSemAcucar
   decidia so pela fibra. Dois bugs reais achados por consertar uma fixture. */
teste("motor", "receita COM açúcar continua validada pelo Mirko", ()=>{
  const r = SEED_RECIPES.find(x=>/AÇÚCAR DE MAÇÃ/.test(x.nome)); if(!r) return true;
  const R = computeRecipe(r.linhas);
  const FV = faixaVigente("acucares", R, r.familia);
  return (FV && /Mirko/.test(FV.fonte)) ? true : "clássica não está mais no alvo do Mirko";
});

/* ==================== GRAMATURA POR SABOR ================================
   22/10/2026 — A suíte tinha 445 testes e NENHUM cobria a massa do pote por
   receita: todos usavam o eiPote() global. Quando o Gabriel me disse que o
   morango só chega a 120 g e eu gravei potePeso:120, os 445 passaram sem
   piscar — o que significa que a trava mais importante do projeto estava
   desprotegida justamente no número que mais me morde aqui.
   Histórico da gramatura: 130 → 120 → 135 → 140, e agora 120 só no morango.
   Cada mudança se propagou para CMV, receituário, lista de compras e rótulo.   */
teste("gramatura", "morango tem gramatura própria de 120 g", ()=>{
  const r = SEED_RECIPES.find(x=>/Sorbet Morango \(LANCAMENTO\)/.test(x.nome));
  if(!r) return "Sorbet Morango (LANCAMENTO) não está no SEED";
  return (+r.potePeso === 120) ? true
       : `morango deveria ter potePeso 120, tem ${r.potePeso||"(ausente — cai no global)"}`;
});
teste("gramatura", "alfajor segue 135 g de gelato + biscoito por fora", ()=>{
  const r = SEED_RECIPES.find(x=>/Alfajor \(LANCAMENTO\)/.test(x.nome));
  if(!r) return true;
  if(+r.potePeso !== 135) return `alfajor deveria ter potePeso 135, tem ${r.potePeso}`;
  return r.finAdicional === true ? true
       : "alfajor perdeu o finAdicional — o biscoito voltaria a deslocar calda";
});
teste("gramatura", "os outros cinco sabores usam o pote global", ()=>{
  const fora = LANC.filter(r => !/Sorbet Morango|Alfajor/.test(r.nome))
                   .filter(r => +r.potePeso > 0)
                   .map(r => r.nome.replace(" (LANCAMENTO)","")+" = "+r.potePeso);
  return fora.length ? "ganharam gramatura própria sem decisão de bancada: "+fora.join(", ")
                     : true;
});
teste("gramatura", "massaPote e gelatoPote respeitam o potePeso da receita", ()=>{
  if(!app.massaPote || !app.gelatoPote) return true;
  const mor = SEED_RECIPES.find(x=>/Sorbet Morango \(LANCAMENTO\)/.test(x.nome));
  const g = app.gelatoPote(mor), m = app.massaPote(mor);
  if(g !== 120) return `gelatoPote do morango deu ${g}, esperado 120`;
  return m === 120 ? true : `massaPote do morango deu ${m}, esperado 120 (não tem finalização)`;
});

/* ========================= RELATÓRIO ===================================== */
const linha = "─".repeat(78);
console.log("\n" + linha);
console.log("SUÍTE DE TESTES DO BALANCEADOR");
console.log(linha);
console.log(`arquivo:  ${path.basename(ARQ)}`);
console.log(`baseline: ${baseline ? path.basename(BASE)+" ("+baseline.gerado+")" : "AUSENTE — regressão não testada"}`);
console.log(`receitas: ${LANC.length} do lançamento · pote de ${POTE} g\n`);

if(erros.length){
  const porGrupo = {};
  erros.forEach(e => (porGrupo[e.grupo] = porGrupo[e.grupo]||[]).push(e));
  Object.entries(porGrupo).forEach(([g,list])=>{
    console.log(`  ${g.toUpperCase()} — ${list.length} falha(s)`);
    list.forEach(e => console.log(`    ✕ ${e.nome}\n        ${e.msg}`));
    console.log("");
  });
}

console.log(linha);
console.log(`  ${ok} passaram · ${falhou} falharam · ${ok+falhou} testes`);
console.log(linha + "\n");
process.exit(falhou ? 1 : 0);
