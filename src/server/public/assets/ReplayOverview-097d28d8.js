import{l,e as d,v as _,_ as p,r as u,c as i,b as s,F as v,n as h,o,h as y,w as f,t as a,p as m,a as k}from"./index-ac1dbb22.js";const w={setup(){const e=l({});return d(async()=>{const n=await _.post("/api/fetchReplayOverview",{user:"dummy"});e.value=JSON.parse(n.data).replayList}),{replayList:e}}};const S=e=>(m("data-v-fb79a4af"),e=e(),k(),e),x={class:"replayOverview"},D={class:"replayList"},L=S(()=>s("div",{class:"header"},[s("div",null,"Task"),s("div",null,"Duration"),s("div",null,"Date"),s("div",null,"Status")],-1)),O={class:"list"},b={class:"replayTask"},g={class:"replayDuration"},B={class:"replayDate"},I={class:"replayStatus"};function $(e,n,C,r,F,R){const c=u("router-link");return o(),i("div",x,[s("div",D,[L,s("div",O,[(o(!0),i(v,null,h(r.replayList,t=>(o(),y(c,{class:"replayListEntry",key:t.hash,to:`/replay/${t.hash}`},{default:f(()=>[s("div",b,a(t.task),1),s("div",g,a((t.duration/1e3/60).toFixed(2))+" Minuten",1),s("div",B,a(new Date(t.date).toUTCString()),1),s("div",I,a(t.completion),1)]),_:2},1032,["to"]))),128))])])])}const E=p(w,[["render",$],["__scopeId","data-v-fb79a4af"]]);export{E as default};