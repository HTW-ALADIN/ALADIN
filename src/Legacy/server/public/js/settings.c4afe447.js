(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["settings","replayoverview"],{1148:function(e,t,r){"use strict";var c=r("a691"),n=r("1d80");e.exports="".repeat||function(e){var t=String(n(this)),r="",a=c(e);if(a<0||a==1/0)throw RangeError("Wrong number of repetitions");for(;a>0;(a>>>=1)&&(t+=t))1&a&&(r+=t);return r}},"24ce":function(e,t,r){},"26d3":function(e,t,r){"use strict";r.r(t);var c=r("7a23"),n=Object(c["withScopeId"])("data-v-39171977");Object(c["pushScopeId"])("data-v-39171977");var a={class:"settings"};Object(c["popScopeId"])();var i=n((function(e,t,r,n,i,o){return Object(c["openBlock"])(),Object(c["createBlock"])("div",a)})),o={name:"Settings",setup:function(){return{}}};r("c335");o.render=i,o.__scopeId="data-v-39171977";t["default"]=o},"408a":function(e,t,r){var c=r("c6b6");e.exports=function(e){if("number"!=typeof e&&"Number"!=c(e))throw TypeError("Incorrect invocation");return+e}},"84c7":function(e,t,r){},b680:function(e,t,r){"use strict";var c=r("23e7"),n=r("a691"),a=r("408a"),i=r("1148"),o=r("d039"),s=1..toFixed,u=Math.floor,l=function(e,t,r){return 0===t?r:t%2===1?l(e,t-1,r*e):l(e*e,t/2,r)},d=function(e){var t=0,r=e;while(r>=4096)t+=12,r/=4096;while(r>=2)t+=1,r/=2;return t},p=s&&("0.000"!==8e-5.toFixed(3)||"1"!==.9.toFixed(0)||"1.25"!==1.255.toFixed(2)||"1000000000000000128"!==(0xde0b6b3a7640080).toFixed(0))||!o((function(){s.call({})}));c({target:"Number",proto:!0,forced:p},{toFixed:function(e){var t,r,c,o,s=a(this),p=n(e),f=[0,0,0,0,0,0],b="",v="0",O=function(e,t){var r=-1,c=t;while(++r<6)c+=e*f[r],f[r]=c%1e7,c=u(c/1e7)},j=function(e){var t=6,r=0;while(--t>=0)r+=f[t],f[t]=u(r/e),r=r%e*1e7},h=function(){var e=6,t="";while(--e>=0)if(""!==t||0===e||0!==f[e]){var r=String(f[e]);t=""===t?r:t+i.call("0",7-r.length)+r}return t};if(p<0||p>20)throw RangeError("Incorrect fraction digits");if(s!=s)return"NaN";if(s<=-1e21||s>=1e21)return String(s);if(s<0&&(b="-",s=-s),s>1e-21)if(t=d(s*l(2,69,1))-69,r=t<0?s*l(2,-t,1):s/l(2,t,1),r*=4503599627370496,t=52-t,t>0){O(0,r),c=p;while(c>=7)O(1e7,0),c-=7;O(l(10,c,1),0),c=t-1;while(c>=23)j(1<<23),c-=23;j(1<<c),O(1,1),j(2),v=h()}else O(0,r),O(1<<-t,0),v=h()+i.call("0",p);return p>0?(o=v.length,v=b+(o<=p?"0."+i.call("0",p-o)+v:v.slice(0,o-p)+"."+v.slice(o-p))):v=b+v,v}})},c335:function(e,t,r){"use strict";r("84c7")},d2b4:function(e,t,r){"use strict";r("24ce")},d34d:function(e,t,r){"use strict";r.r(t);r("b680");var c=r("7a23"),n=Object(c["withScopeId"])("data-v-25e308f5");Object(c["pushScopeId"])("data-v-25e308f5");var a={class:"replayOverview"},i={class:"replayList"},o=Object(c["createVNode"])("div",{class:"header"},[Object(c["createVNode"])("div",null,"Task"),Object(c["createVNode"])("div",null,"Duration"),Object(c["createVNode"])("div",null,"Date"),Object(c["createVNode"])("div",null,"Status")],-1),s={class:"list"},u={class:"replayTask"},l={class:"replayDuration"},d={class:"replayDate"},p={class:"replayStatus"};Object(c["popScopeId"])();var f=n((function(e,t,r,f,b,v){var O=Object(c["resolveComponent"])("router-link");return Object(c["openBlock"])(),Object(c["createBlock"])("div",a,[Object(c["createVNode"])("div",i,[o,Object(c["createVNode"])("div",s,[(Object(c["openBlock"])(!0),Object(c["createBlock"])(c["Fragment"],null,Object(c["renderList"])(f.replayList,(function(e){return Object(c["openBlock"])(),Object(c["createBlock"])(O,{class:"replayListEntry",key:e.hash,to:"/replay/".concat(e.hash)},{default:n((function(){return[Object(c["createVNode"])("div",u,Object(c["toDisplayString"])(e.task),1),Object(c["createVNode"])("div",l,Object(c["toDisplayString"])((e.duration/1e3/60).toFixed(2))+" Minuten",1),Object(c["createVNode"])("div",d,Object(c["toDisplayString"])(new Date(e.date).toUTCString()),1),Object(c["createVNode"])("div",p,Object(c["toDisplayString"])(e.completion),1)]})),_:2},1032,["to"])})),128))])])])})),b=(r("96cf"),r("1da1")),v=r("bc3a"),O=r.n(v),j={setup:function(){var e=Object(c["ref"])({});return Object(c["onMounted"])(Object(b["a"])(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,O.a.post("/api/fetchReplayOverview",{user:"dummy"});case 2:r=t.sent,e.value=JSON.parse(r.data).replayList;case 4:case"end":return t.stop()}}),t)})))),{replayList:e}}};r("d2b4");j.render=f,j.__scopeId="data-v-25e308f5";t["default"]=j}}]);
//# sourceMappingURL=settings.c4afe447.js.map