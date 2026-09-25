function hashSeed(s){let h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function mulberry32(a){return function(){a|=0;a=(a+0x6D2B79F5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
const DEFAULT_ZONES=["North Zone","South Zone","East Zone","West Zone","Central Zone"];
/* lat/lng, coastal / cyclone / flood-proneness are used to make hazard simulation geographically plausible.
   Swap CITIES for a real municipal boundary list + Bhuvan/OSM data when you move past the hackathon demo. */
const CITIES=[
 {name:"Jaipur",zones:["Pink City Core","Malviya Nagar","Vaishali Nagar","C-Scheme","Sanganer"],lat:26.9124,lng:75.7873},
 {name:"Mumbai",zones:["Andheri","Dadar","Bandra","Colaba","Powai"],lat:19.0760,lng:72.8777,coastal:true,floodProne:true},
 {name:"Delhi",zones:["Connaught Place","Dwarka","Saket","Rohini","Karol Bagh"],lat:28.7041,lng:77.1025},
 {name:"Bengaluru",zones:["Indiranagar","Whitefield","Koramangala","Jayanagar","Electronic City"],lat:12.9716,lng:77.5946},
 {name:"Hyderabad",zones:DEFAULT_ZONES,lat:17.3850,lng:78.4867},
 {name:"Ahmedabad",zones:DEFAULT_ZONES,lat:23.0225,lng:72.5714},
 {name:"Chennai",zones:DEFAULT_ZONES,lat:13.0827,lng:80.2707,coastal:true,cycloneProne:true,floodProne:true},
 {name:"Kolkata",zones:DEFAULT_ZONES,lat:22.5726,lng:88.3639,coastal:true,cycloneProne:true,floodProne:true},
 {name:"Surat",zones:DEFAULT_ZONES,lat:21.1702,lng:72.8311,coastal:true,floodProne:true},
 {name:"Pune",zones:DEFAULT_ZONES,lat:18.5204,lng:73.8567},
 {name:"Lucknow",zones:DEFAULT_ZONES,lat:26.8467,lng:80.9462},
 {name:"Kanpur",zones:DEFAULT_ZONES,lat:26.4499,lng:80.3319},
 {name:"Nagpur",zones:DEFAULT_ZONES,lat:21.1458,lng:79.0882},
 {name:"Indore",zones:DEFAULT_ZONES,lat:22.7196,lng:75.8577},
 {name:"Thane",zones:DEFAULT_ZONES,lat:19.2183,lng:72.9781,floodProne:true},
 {name:"Bhopal",zones:DEFAULT_ZONES,lat:23.2599,lng:77.4126},
 {name:"Patna",zones:DEFAULT_ZONES,lat:25.5941,lng:85.1376,floodProne:true},
 {name:"Vadodara",zones:DEFAULT_ZONES,lat:22.3072,lng:73.1812,floodProne:true},
 {name:"Ghaziabad",zones:DEFAULT_ZONES,lat:28.6692,lng:77.4538},
 {name:"Coimbatore",zones:DEFAULT_ZONES,lat:11.0168,lng:76.9558},
 {name:"Chandigarh",zones:DEFAULT_ZONES,lat:30.7333,lng:76.7794},
 {name:"Kochi",zones:DEFAULT_ZONES,lat:9.9312,lng:76.2673,coastal:true,cycloneProne:true,floodProne:true},
 {name:"Nashik",zones:DEFAULT_ZONES,lat:19.9975,lng:73.7898},
 {name:"Guwahati",zones:DEFAULT_ZONES,lat:26.1445,lng:91.7362,floodProne:true},
];
const WEATHER=["Clear","Light rain advisory","Heavy rainfall alert","Heat advisory","High wind alert","Clear"];
const STATUS_META={
 NORMAL:{cls:"normal",label:{en:"Normal",hi:"सामान्य"},word:{en:"STABLE",hi:"स्थिर"}},
 WATCH:{cls:"watch",label:{en:"Watch",hi:"निगरानी"},word:{en:"WATCHING",hi:"निगरानी में"}},
 EMERGING:{cls:"emerging",label:{en:"Emerging",hi:"उभरता"},word:{en:"EMERGING",hi:"उभरता जोखिम"}},
 CRITICAL:{cls:"critical",label:{en:"Critical",hi:"गंभीर"},word:{en:"CRITICAL",hi:"गंभीर"}},
};
let state={cityIndex:0,tick:0,viewOffset:0,lang:"en",notifyOn:false,lastNotifiedStatus:null,role:"resident",
 mapZoom:1,mapSelected:null,flashDismissedKey:null,replayPlaying:false,replayIndex:0};

function statusForRisk(r){if(r>=75)return"CRITICAL";if(r>=50)return"EMERGING";if(r>=28)return"WATCH";return"NORMAL";}
function riskFromSignals(rainfall,traffic,transit,complaints){return Math.round(rainfall*0.28+traffic*0.2+transit*0.24+complaints*0.28);}

function buildCityData(cityIndex,tick){
 const city=CITIES[cityIndex];
 const rand=mulberry32(hashSeed(city.name)+tick*97);
 const zones=city.zones.map((zname,i)=>{
  const rainfall=Math.round(rand()*100),traffic=Math.round(rand()*100),transit=Math.round(rand()*100),complaints=Math.round(rand()*100);
  const weather=WEATHER[Math.floor(rand()*WEATHER.length)];
  let risk=riskFromSignals(rainfall,traffic,transit,complaints);
  if(i===Math.floor(rand()*city.zones.length)&&rand()>0.55)risk=Math.min(96,risk+22);
  const status=statusForRisk(risk);
  const anomaly=(rainfall>55&&complaints>45)||(transit>60&&complaints>50)||risk>=70;
  /* extra civic signals: grid stress, traffic-light faults, rare gas-leak reports, air quality */
  const power=Math.round(Math.min(100,rainfall*0.55+traffic*0.15+rand()*35));
  const outage=power>66&&rand()>0.5;
  const trafficLightDown=rand()>0.93||(traffic>78&&rand()>0.72);
  const gasLeak=rand()>0.988;
  const aqi=Math.round(45+rand()*255);
  return{name:zname,risk,rainfall,traffic,transit,complaints,weather,status,anomaly,power,outage,trafficLightDown,gasLeak,aqi};
 });
 const avgRain=Math.round(zones.reduce((s,z)=>s+z.rainfall,0)/zones.length);
 const cycloneWatch=!!(city.cycloneProne&&avgRain>60&&rand()>0.6);
 const floodWarning=!!((city.coastal||city.floodProne)&&avgRain>56&&rand()>0.5);
 return{city:city.name,lat:city.lat,lng:city.lng,coastal:!!city.coastal,floodProne:!!city.floodProne,cycloneProne:!!city.cycloneProne,zones,cycloneWatch,floodWarning,avgRain};
}
function fmtTime(d){return (d||new Date()).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit',second:'2-digit'});}

/* ---- sparkline: last 6 readings for one zone, canvas mini chart ---- */
function zoneHistory(cityIndex,tick,zoneName,n){
 const out=[];
 for(let k=n-1;k>=0;k--){
  const d=buildCityData(cityIndex,tick-k);
  const z=d.zones.find(zz=>zz.name===zoneName);
  out.push(z?z.risk:0);
 }
 return out;
}
function drawSpark(canvas,values,color){
 const ctx=canvas.getContext("2d");
 const w=canvas.width,h=canvas.height;
 ctx.clearRect(0,0,w,h);
 const max=100,min=0;
 ctx.beginPath();
 values.forEach((v,i)=>{
  const x=(i/(values.length-1))*(w-4)+2;
  const y=h-2-((v-min)/(max-min))*(h-4);
  if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);
 });
 ctx.strokeStyle=color;ctx.lineWidth=1.6;ctx.stroke();
 const last=values[values.length-1];
 const lx=(w-4)+2, ly=h-2-((last-min)/(max-min))*(h-4);
 ctx.beginPath();ctx.arc(lx,ly,2.2,0,7);ctx.fillStyle=color;ctx.fill();
}

/* ---- translation helper ---- */
const T={
 en:{tag:"GROUNDED ON LIVE FEED DATA",tagline:"Civic intelligence OS — one glance, grounded in evidence",
  heroSub:"Fusing weather, traffic, transit and complaint signals into one grounded read of what's happening right now — with confidence and evidence, not just a color.",
  selectZone:"SELECT A ZONE",selectZonePrompt:"Pick a zone above to get a plain-language safety read.",
  safe:"Safe to go out",caution:"Caution advised",avoid:"Avoid non-essential travel"},
 hi:{tag:"लाइव डेटा पर आधारित",tagline:"नागरिक इंटेलिजेंस ओएस — एक नज़र में, प्रमाण के साथ",
  heroSub:"मौसम, यातायात, परिवहन और शिकायत संकेतों को मिलाकर अभी की स्थिति को स्पष्ट रूप से दिखाता है।",
  selectZone:"एक ज़ोन चुनें",selectZonePrompt:"सुरक्षा की जानकारी पाने के लिए ऊपर एक ज़ोन चुनें।",
  safe:"बाहर जाना सुरक्षित है",caution:"सावधानी बरतें",avoid:"अनावश्यक यात्रा से बचें"},
};
function t(k){return T[state.lang][k];}

/* =========================================================================
   INCIDENT / HAZARD / CORRELATION ENGINE
   Normalizes every zone-level + city-level signal into one common incident
   schema: {id,type,severity,zone,title,desc,time,source}. This is the piece
   a real backend would populate from IMD / NDMA / utility / 311 feeds —
   see backend/server.js for the wiring points.
   ========================================================================= */
const INCIDENT_META={
 waterlogging:{icon:"💧",label:"Waterlogging"},
 power:{icon:"⚡",label:"Power outage"},
 signal:{icon:"🚦",label:"Traffic light down"},
 gas_leak:{icon:"🔥",label:"Gas leak"},
 cyclone:{icon:"🌀",label:"Cyclone watch"},
 flood:{icon:"🌊",label:"Flood warning"},
 accident:{icon:"🚗",label:"Accident-prone road"},
};
function buildIncidents(data){
 const list=[];
 data.zones.forEach(z=>{
  if(z.rainfall>60)list.push({id:`wl-${z.name}`,type:"waterlogging",severity:z.rainfall>80?"critical":"watch",zone:z.name,title:`Waterlogging near ${z.name}`,desc:`Rainfall index ${z.rainfall}/100 — standing water likely on low-lying stretches.`,time:new Date(),source:"CityPulse civic feed (simulated)"});
  if(z.outage)list.push({id:`pw-${z.name}`,type:"power",severity:z.power>85?"critical":"watch",zone:z.name,title:`Power outage risk in ${z.name}`,desc:`Grid stress at ${z.power}/100, likely tied to heavy rain load-shedding or a possible wire fault. Avoid touching fallen or loose wires.`,time:new Date(),source:"Utility feed (simulated)"});
  if(z.trafficLightDown)list.push({id:`sg-${z.name}`,type:"signal",severity:"watch",zone:z.name,title:`Traffic signal not working — ${z.name}`,desc:`A traffic light in ${z.name} is reported down. Treat the junction as an all-way stop and drive carefully.`,time:new Date(),source:"Citizen + traffic feed (simulated)"});
  if(z.gasLeak)list.push({id:`gl-${z.name}`,type:"gas_leak",severity:"critical",zone:z.name,title:`Possible gas leak — ${z.name}`,desc:`Multiple reports of a gas smell near ${z.name}. Avoid open flames and ignition sources, ventilate if indoors, and contact your gas utility emergency line immediately.`,time:new Date(),source:"Citizen report (simulated)"});
  if(z.rainfall>60&&z.traffic>55)list.push({id:`ac-${z.name}`,type:"accident",severity:"watch",zone:z.name,title:`Elevated accident risk — ${z.name}`,desc:`Rain-slicked roads plus heavy traffic load are raising crash risk here.`,time:new Date(),source:"Correlation engine"});
 });
 if(data.cycloneWatch)list.unshift({id:`cy-${data.city}`,type:"cyclone",severity:"critical",zone:"Citywide",title:`Cyclone watch issued for ${data.city}`,desc:`Sustained high rainfall + wind signals across multiple zones. Coastal and low-lying residents should review evacuation routes and secure loose structures.`,time:new Date(),source:"IMD-style bulletin (simulated)"});
 if(data.floodWarning)list.unshift({id:`fl-${data.city}`,type:"flood",severity:"critical",zone:"Citywide",title:`Flood warning for ${data.city}`,desc:`City-wide average rainfall index is ${data.avgRain}/100. Low-lying and coastal zones face elevated flood risk in the next few hours.`,time:new Date(),source:"NDMA-style bulletin (simulated)"});
 return list;
}
function buildNewsFeed(data,incidents){
 const items=incidents.slice(0,6).map(inc=>({
  source:inc.source,badge:inc.severity,title:inc.title,body:inc.desc,time:fmtTime()
 }));
 if(!items.length)items.push({source:"CityPulse Citizen Desk",badge:"info",title:`${data.city} reading normal city-wide`,body:"No active hazard bulletins right now. This panel will surface real IMD / NDMA / utility alerts once backend/server.js is wired to a live API.",time:fmtTime()});
 items.push({source:"CityPulse Desk",badge:"info",title:"About this panel",body:"Headlines here are generated from the same live signal fusion as the rest of the dashboard for this demo. In production, replace buildNewsFeed() with a call to backend/server.js's /api/news route (NewsAPI.org + IMD + NDMA CAP alerts, filtered by city).",time:fmtTime()});
 return items;
}

/* ---- historical reference dataset (deterministic sample data, not tick-based) ---- */
function historicalProfile(cityIndex){
 const city=CITIES[cityIndex];
 const rand=mulberry32(hashSeed(city.name+"-history"));
 const years=[2021,2022,2023,2024,2025];
 const wet=city.floodProne||city.coastal;
 const zoneStats=city.zones.map(z=>{
  const floods=Math.round(rand()*(wet?7:2));
  const cyclones=Math.round(rand()*(city.cycloneProne?3:0));
  const accidents=3+Math.round(rand()*13);
  const powerCuts=2+Math.round(rand()*9);
  return{zone:z,floods,cyclones,accidents,powerCuts,total:floods+cyclones+accidents+powerCuts};
 }).sort((a,b)=>b.total-a.total);
 const yearly=years.map(y=>({year:y,events:Math.round(6+rand()*(wet?22:11))}));
 const top=zoneStats[0],second=zoneStats[1]||zoneStats[0];
 const timeline=[
  {year:2025,text:`Heavy-rainfall week pushed ${top.zone} into elevated risk multiple times — pattern consistent with this zone's ${top.floods}-flood-event history.`},
  {year:2024,text:`Signal and power outages clustered near ${second.zone} during peak monsoon weeks.`},
  {year:2023,text:city.cycloneProne?`Cyclone watch issued; low-lying parts of ${top.zone} received evacuation advisories.`:`Multi-day heavy rainfall raised accident rates near ${second.zone}.`},
  {year:2022,text:`Heat + storm sequence strained power infrastructure, leading to rolling outages in parts of the city.`},
  {year:2021,text:`Baseline year — establishes CityPulse's rolling 5-year historical reference window.`},
 ];
 return{years,zoneStats,yearly,timeline};
}

function render(){
 const data=buildCityData(state.cityIndex,state.tick+state.viewOffset);
 const sorted=[...data.zones].sort((a,b)=>b.risk-a.risk);
 const top=sorted[0], second=sorted[1];
 const flagCount=data.zones.filter(z=>z.anomaly).length;
 const avgRisk=Math.round(data.zones.reduce((s,z)=>s+z.risk,0)/data.zones.length);
 const cityStatus=statusForRisk(Math.max(top.risk*0.6+avgRisk*0.4));
 const lang=state.lang;

 document.getElementById("tagline").textContent=t("tagline");
 document.getElementById("hero-sub").textContent=t("heroSub");
 document.getElementById("hero-city").textContent=data.city+", India";
 const hs=document.getElementById("hero-status");
 hs.textContent=STATUS_META[cityStatus].word[lang]; hs.style.color=`var(--${STATUS_META[cityStatus].cls})`;
 document.getElementById("hero-zonecount").textContent=data.zones.length;
 document.getElementById("hero-flags").textContent=flagCount+(flagCount===1?" zone":" zones");
 const snap=document.getElementById("snap-banner"), timeEl=document.getElementById("hero-time");
 if(state.viewOffset===0){snap.classList.remove("show");timeEl.textContent=fmtTime();}
 else{snap.classList.add("show");const mins=state.viewOffset*15;timeEl.textContent=fmtTime(new Date(Date.now()+mins*60000))+" ("+mins+"m)";}

 const sigActive=k=>top[k]>50;
 const confidence=Math.round(([sigActive("rainfall"),sigActive("traffic"),sigActive("transit"),sigActive("complaints")].filter(Boolean).length/4)*100);
 const convergence=Math.min(100,flagCount*28+(top.risk>=70?18:0));
 const prevData=buildCityData(state.cityIndex,state.tick+state.viewOffset-1);
 const prevTop=prevData.zones.find(z=>z.name===top.name);
 const delta=prevTop?top.risk-prevTop.risk:0;
 const persistence=delta>4?"Rising":delta<-4?"Falling":"Stable";
 const forecast=Math.max(0,Math.min(100,Math.round(top.risk+delta)));

 document.getElementById("hero-mini").innerHTML=`
  <div class="mini-metric"><div class="label">CITY-WIDE AVG RISK</div><div class="val">${avgRisk}<small> /100</small></div></div>
  <div class="mini-metric"><div class="label">HIGHEST RISK ZONE</div><div class="val">${top.name}</div></div>
  <div class="mini-metric"><div class="label">CONFIDENCE</div><div class="val">${confidence}<small>%</small></div></div>
  <div class="mini-metric"><div class="label">15-MIN FORECAST</div><div class="val">${forecast}<small> (${persistence})</small></div></div>`;

 const pm=STATUS_META[top.status];
 document.getElementById("priority-box").innerHTML=`
  <div class="priority-top"><div><div class="priority-tag"><span class="dot" style="background:var(--critical);box-shadow:0 0 8px var(--critical);"></span>LIVE PRIORITY ALERT</div><h3>${top.name}</h3></div>
  <div class="priority-score"><div class="label">RISK SCORE</div><div class="num">${top.risk}</div></div></div>
  <div class="priority-grid">
   <div><div class="k">STATUS</div><div class="v" style="color:var(--${pm.cls})">${pm.label[lang].toUpperCase()}</div></div>
   <div><div class="k">CONDITION</div><div class="v">${top.weather}</div></div>
   <div><div class="k">KEY SIGNALS</div><div class="v">Rainfall ${top.rainfall} · Traffic ${top.traffic} · Transit ${top.transit} · Complaints ${top.complaints}</div></div>
   <div><div class="k">CONVERGENCE / FORECAST</div><div class="v">${convergence}/100 convergence · projected ${forecast} in 15m</div></div>
  </div>`;

 const nodes=[["Weather",top.rainfall],["Traffic",top.traffic],["Transit",top.transit],["Complaints",top.complaints]];
 document.getElementById("event-graph").innerHTML=nodes.map((n,i)=>`
  <div class="g-node ${n[1]>50?'active':''}"><div class="g-label">${n[0]}</div><div class="g-val">${n[1]}</div></div>
  ${i<nodes.length-1?'<div class="g-arrow">→</div>':''}`).join("");
 document.getElementById("conv-box").innerHTML=`<div>Convergence score for <strong>${top.name}</strong> — how many signals are moving together right now</div><div class="num">${convergence}/100</div>`;

 document.getElementById("zone-grid").innerHTML=sorted.map((z,idx)=>{const m=STATUS_META[z.status];return`
  <div class="zone-card"><div class="zone-card-top"><div class="zone-name">${z.name}</div><div class="badge b-${m.cls}">${m.label[lang].toUpperCase()}</div></div>
  <div class="zone-risk-row"><span class="num">${z.risk}</span><span class="of">/ 100 risk</span></div>
  <div class="risk-bar"><div class="risk-fill" style="width:${z.risk}%;background:var(--${m.cls});"></div></div>
  <div class="spark-row"><canvas width="90" height="26" id="spark-${idx}"></canvas><span class="forecast">trend</span></div>
  <div class="zone-signals">
   <div class="zone-signal-row"><span>Rainfall index</span><strong>${z.rainfall}</strong></div>
   <div class="zone-signal-row"><span>Traffic load</span><strong>${z.traffic}</strong></div>
   <div class="zone-signal-row"><span>Transit delay</span><strong>${z.transit}</strong></div>
   <div class="zone-signal-row"><span>Complaint volume</span><strong>${z.complaints}</strong></div>
   <div class="zone-signal-row"><span>Air quality index</span><strong>${z.aqi}</strong></div>
  </div>
  <div class="zone-flag" style="color:${z.anomaly?'var(--critical)':'var(--dim)'}"><span class="flag-dot" style="background:${z.anomaly?'var(--critical)':'var(--dim)'}"></span>${z.anomaly?"Anomaly detected":"No anomaly"}</div>
  </div>`;}).join("");
 sorted.forEach((z,idx)=>{
  const c=document.getElementById(`spark-${idx}`);
  if(c)drawSpark(c,zoneHistory(state.cityIndex,state.tick+state.viewOffset,z.name,6),z.risk>=50?"#ff9457":"#22e8c8");
 });

 const avg=k=>Math.round(data.zones.reduce((s,z)=>s+z[k],0)/data.zones.length);
 const sigs=[["Rainfall index","◐",avg("rainfall"),"brand"],["Traffic load","▣",avg("traffic"),"violet"],["Transit delay","◇",avg("transit"),"watch"],["Complaint volume","◈",avg("complaints"),"critical"]];
 document.getElementById("signals-grid").innerHTML=sigs.map(s=>`
  <div class="signal-card"><div class="signal-top"><div class="signal-icon" style="background:rgba(255,255,255,0.05);color:var(--${s[3]});">${s[1]}</div><div class="signal-label">${s[0]}</div></div>
  <div class="signal-value">${s[2]}</div><div class="signal-trend ${s[2]>50?'trend-up':'trend-flat'}">${s[2]>50?'▲ above baseline':'— near baseline'}</div></div>`).join("");

 const flaggedNames=data.zones.filter(z=>z.anomaly).map(z=>z.name);
 let brief;
 if(flaggedNames.length===0)brief=`<strong>${data.city}</strong> is reading stable across all ${data.zones.length} monitored zones right now.`;
 else{const list=flaggedNames.length>1?flaggedNames.slice(0,-1).join(", ")+" and "+flaggedNames.slice(-1):flaggedNames[0];
  brief=`In <strong>${data.city}</strong>, <strong>${top.name}</strong> is the zone to watch — rainfall and complaint volume are rising together (confidence ${confidence}%), projected to reach ${forecast}/100 within 15 minutes if the trend holds. ${flaggedNames.length>1?`${list} are also showing correlated movement.`:`No other zone shows the same pattern right now.`}`;}
 document.getElementById("brief-text").innerHTML=brief;

 window._top=top; window._second=second; window._data=data; window._confidence=confidence; window._convergence=convergence; window._sorted=sorted; window._forecast=forecast; window._flagCount=flagCount; window._avgRisk=avgRisk;
 buildSimUI(top);
 buildSafeZonePicker(data);
 checkNotify(cityStatus,data.city);
 renderRoleCard(data,top,sorted,confidence,convergence,forecast);
 renderAdvisory(data);
 buildRouteZonePickers(data);

 /* ---- new: hazard/news/map/reporting/avoid-now/historical/flash ---- */
 const incidents=buildIncidents(data);
 window._incidents=incidents;
 renderAvoidNow(data,incidents);
 renderHazardWatch(data,incidents);
 renderMap(data,incidents);
 renderReporting(data);
 renderSourceStatus();
 flashCheck(data,incidents);
 if(!state._histBuilt||state._histCity!==state.cityIndex){renderHistorical(state.cityIndex);state._histBuilt=true;state._histCity=state.cityIndex;}
}

/* ---- road network: 5-node graph shared by every city's zone layout ---- */
const ROAD_EDGES=[[0,1],[1,2],[2,3],[3,4],[4,0],[0,2],[1,3]];
function buildRoadGraph(data){
 const rand=mulberry32(hashSeed(data.city+"-roads"));
 return ROAD_EDGES.map(([a,b])=>{
  const dist=+(2+rand()*7).toFixed(1);
  const za=data.zones[a],zb=data.zones[b];
  const rainRisk=(za.rainfall>60&&za.traffic>55)||(zb.rainfall>60&&zb.traffic>55);
  const critical=za.status==="CRITICAL"||zb.status==="CRITICAL";
  const closed=rainRisk||critical;
  const reason=critical?"zone at critical risk":rainRisk?"rain-related accident risk":null;
  return{a,b,dist,closed,reason};
 });
}
function dijkstra(edges,n,start,end,avoidClosed){
 const adj=Array.from({length:n},()=>[]);
 edges.forEach(e=>{if(avoidClosed&&e.closed)return;adj[e.a].push({to:e.b,dist:e.dist});adj[e.b].push({to:e.a,dist:e.dist});});
 const dist=Array(n).fill(Infinity),prev=Array(n).fill(-1),visited=Array(n).fill(false);
 dist[start]=0;
 for(let i=0;i<n;i++){
  let u=-1;for(let j=0;j<n;j++)if(!visited[j]&&(u===-1||dist[j]<dist[u]))u=j;
  if(u===-1||dist[u]===Infinity)break; visited[u]=true;
  adj[u].forEach(({to,dist:d})=>{if(dist[u]+d<dist[to]){dist[to]=dist[u]+d;prev[to]=u;}});
 }
 if(dist[end]===Infinity)return null;
 const path=[];let cur=end;while(cur!==-1){path.unshift(cur);cur=prev[cur];}
 return{path,dist:+dist[end].toFixed(1)};
}
function buildRouteZonePickers(data){
 const f=document.getElementById("route-from"),tt=document.getElementById("route-to");
 const fv=f.value,tv=tt.value;
 const opts=data.zones.map((z,i)=>`<option value="${i}">${z.name}</option>`).join("");
 f.innerHTML=opts; tt.innerHTML=opts;
 if(fv!==""&&fv<data.zones.length)f.value=fv; if(tv!==""&&tv<data.zones.length&&tv!==fv)tt.value=tv; else tt.selectedIndex=Math.min(1,data.zones.length-1);
}
document.getElementById("route-find").addEventListener("click",()=>{
 const data=window._data; if(!data)return;
 const from=+document.getElementById("route-from").value, to=+document.getElementById("route-to").value;
 const el=document.getElementById("route-result");
 if(from===to){el.innerHTML=`<span class="tag">SAME ZONE</span><br>Pick two different zones.`;return;}
 const graph=buildRoadGraph(data);
 const direct=dijkstra(graph,data.zones.length,from,to,false);
 const safe=dijkstra(graph,data.zones.length,from,to,true);
 if(!direct){el.innerHTML=`No route found between these zones right now.`;return;}
 const directClosed=direct.path.slice(0,-1).some((n,i)=>graph.find(e=>(e.a===n&&e.b===direct.path[i+1])||(e.b===n&&e.a===direct.path[i+1]))?.closed);
 const pathHtml=p=>p.map((idx,i)=>`<span class="route-node">${data.zones[idx].name}</span>${i<p.length-1?'<span class="route-arrow">→</span>':''}`).join("");
 if(!directClosed){
  el.innerHTML=`<span class="tag">${t("tag")}</span><br>Route is clear <span class="clear-tag">NO CLOSURES</span><div class="route-path">${pathHtml(direct.path)}</div>Total distance: <strong>${direct.dist} km</strong>`;
 } else if(safe){
  const closedSeg=graph.find(e=>direct.path.slice(0,-1).some((n,i)=>(e.a===n&&e.b===direct.path[i+1])||(e.b===n&&e.a===direct.path[i+1]))&&e.closed);
  const extra=+(safe.dist-direct.dist).toFixed(1);
  el.innerHTML=`<span class="tag">${t("tag")}</span><br>Direct route blocked <span class="closure-tag">CLOSURE: ${closedSeg?.reason||"road risk"}</span>
   <div class="route-path">${pathHtml(direct.path)}</div>
   Suggested safe alternate <span class="clear-tag">RECOMMENDED</span>
   <div class="route-path">${pathHtml(safe.path)}</div>
   Alternate distance: <strong>${safe.dist} km</strong> (${extra>0?`+${extra} km vs the blocked direct route`:"same distance, just avoids the risk"})`;
 } else {
  el.innerHTML=`<span class="tag">${t("tag")}</span><br>Direct route has a closure and no safe alternate is currently open between these zones. Consider delaying travel.`;
 }
});

/* ---- daily citizen advisory ---- */
function renderAdvisory(data){
 const items=[];
 const wetZones=data.zones.filter(z=>z.rainfall>55||z.weather.toLowerCase().includes("rain"));
 const hotClear=data.zones.filter(z=>z.weather==="Clear"&&z.rainfall<25);
 const windZones=data.zones.filter(z=>z.weather.toLowerCase().includes("wind"));
 const accidentZones=data.zones.filter(z=>z.rainfall>60&&z.traffic>55);
 const outageZones=data.zones.filter(z=>z.outage);
 if(wetZones.length)items.push({icon:"🌂",text:`Rain is active near <strong>${wetZones.map(z=>z.name).join(", ")}</strong> — carry an umbrella and add extra travel time.`});
 if(hotClear.length>=Math.ceil(data.zones.length/2))items.push({icon:"💧",text:`Clear, dry conditions across most of the city — carry water and use sun protection if you're out for a while.`});
 if(windZones.length)items.push({icon:"💨",text:`High wind advisory near <strong>${windZones.map(z=>z.name).join(", ")}</strong> — secure loose outdoor items.`});
 if(accidentZones.length)items.push({icon:"🚧",text:`Rain-slicked roads are raising accident risk near <strong>${accidentZones.map(z=>z.name).join(", ")}</strong> — drive slower and leave extra following distance, or use the route planner below to avoid them.`});
 if(outageZones.length)items.push({icon:"⚡",text:`Heavy rain load is straining the grid near <strong>${outageZones.map(z=>z.name).join(", ")}</strong> — outages and downed-wire risk are elevated; avoid contact with any exposed wiring.`});
 if(!items.length)items.push({icon:"✅",text:"No specific advisory today — conditions are normal across the city."});
 document.getElementById("advisory-card").innerHTML=items.map(i=>`<div class="advisory-item"><span class="advisory-icon">${i.icon}</span><span>${i.text}</span></div>`).join("");
}

/* ---- role-based stakeholder views ---- */
function renderRoleCard(data,top,sorted,confidence,convergence,forecast){
 const el=document.getElementById("role-card");
 const role=state.role;
 if(role==="resident"){
  const v=verdictFor(top);
  el.innerHTML=`<div class="role-title"><span class="verdict-badge b-${top.status.toLowerCase()==='normal'?'normal':top.status.toLowerCase()}" style="background:transparent;border:1px solid var(--border);color:var(--text)">FOR RESIDENTS</span></div>
  <div class="role-body">Right now, <strong>${top.name}</strong> is the zone most worth watching in ${data.city}. If you're there: ${v.advice} Everywhere else in the city is reading closer to normal — use the "Is it safe right now?" check below for your specific zone.</div>`;
 } else if(role==="business"){
  const open=top.risk<35?{v:"Open normally",c:"normal"}:top.risk<60?{v:"Open with caution",c:"watch"}:{v:"Consider delaying opening",c:"critical"};
  el.innerHTML=`<div class="role-title"><span class="verdict-badge b-${open.c}">${open.v.toUpperCase()}</span></div>
  <div class="role-body">In <strong>${top.name}</strong>: traffic load is ${top.traffic}/100 and transit delay is ${top.transit}/100 — expect ${top.traffic>55?"reduced footfall and slower deliveries":"roughly normal customer flow"}. Complaint volume of ${top.complaints}/100 ${top.complaints>50?"suggests some local disruption customers may already know about.":"is unremarkable."} Forecast in 15 minutes: ${forecast}/100.</div>`;
 } else if(role==="official"){
  const watch3=sorted.slice(0,3);
  const closures=buildRoadGraph(data).filter(e=>e.closed);
  el.innerHTML=`<div class="role-title"><span class="verdict-badge" style="background:var(--brand-dim);color:var(--brand)">CITY OPERATIONS SUMMARY</span></div>
  <div class="role-body">City-wide average risk is <strong>${window._avgRisk}/100</strong> with <strong>${window._flagCount} of ${data.zones.length}</strong> zones showing correlated signal movement (${confidence}% confidence, ${convergence}/100 convergence). Top three zones by risk, in priority order:</div>
  <div class="dispatch-list">${watch3.map((z,i)=>`<div class="dispatch-row"><div class="dispatch-rank">${i+1}</div><div><strong>${z.name}</strong> — risk ${z.risk}, dominant signal: ${['rainfall','traffic','transit','complaints'].reduce((a,b)=>z[b]>z[a]?b:a,'rainfall')}</div></div>`).join("")}</div>
  <div class="role-body" style="margin-top:14px;">${closures.length?`<strong>${closures.length} active road closure(s)</strong> — see Plan your route above for affected segments.`:"No road segments currently closed."}</div>`;
 } else if(role==="emergency"){
  const queue=[...sorted].slice(0,3);
  const closures=buildRoadGraph(data).filter(e=>e.closed);
  el.innerHTML=`<div class="role-title"><span class="verdict-badge b-critical">DISPATCH PRIORITY QUEUE</span></div>
  <div class="role-body">Ranked by severity × signal convergence — highest confidence incidents first.</div>
  <div class="dispatch-list">${queue.map((z,i)=>{const dom=['rainfall','traffic','transit','complaints'].reduce((a,b)=>z[b]>z[a]?b:a,'rainfall');const type=dom==='rainfall'?"Possible flooding / drainage":dom==='traffic'?"Traffic incident":dom==='transit'?"Transit disruption":"Civic complaint cluster";return `<div class="dispatch-row"><div class="dispatch-rank">${i+1}</div><div><strong>${z.name}</strong> — risk ${z.risk}, likely type: ${type}${z.anomaly?" · multi-signal confirmed":""}</div></div>`;}).join("")}</div>
  <div class="role-body" style="margin-top:14px;">${closures.length?`<strong>Route around:</strong> ${closures.map(c=>`${data.zones[c.a].name}–${data.zones[c.b].name}`).join(", ")}`:"No road closures to route around right now."}</div>`;
 } else if(role==="journalist"){
  el.innerHTML=`<div class="role-title"><span class="verdict-badge" style="background:var(--panel-2);color:var(--muted);border:1px solid var(--border)">CITABLE SUMMARY</span></div>
  <div class="role-body">As of ${fmtTime()}, CityPulse recorded a risk score of <strong>${top.risk}/100</strong> for ${top.name} in ${data.city}, against a city-wide average of ${window._avgRisk}/100 across ${data.zones.length} monitored zones. ${window._flagCount} zone(s) show correlated signal movement. Use "Copy citable press brief" below for a ready-to-quote paragraph with the same numbers.</div>`;
 }
}
document.querySelectorAll(".role-tab").forEach(b=>b.addEventListener("click",()=>{
 document.querySelectorAll(".role-tab").forEach(x=>x.classList.remove("on"));
 b.classList.add("on"); state.role=b.dataset.role; render();
}));

/* ---- CSV export ---- */
document.getElementById("csv-export").addEventListener("click",()=>{
 const data=window._data; if(!data)return;
 const rows=[["Zone","Risk","Status","Rainfall","Traffic","TransitDelay","Complaints","AQI","Anomaly"]];
 data.zones.forEach(z=>rows.push([z.name,z.risk,z.status,z.rainfall,z.traffic,z.transit,z.complaints,z.aqi,z.anomaly]));
 const csv=rows.map(r=>r.join(",")).join("\n");
 const blob=new Blob([csv],{type:"text/csv"});
 const a=document.createElement("a");
 a.href=URL.createObjectURL(blob); a.download=`citypulse-${data.city.toLowerCase()}-${Date.now()}.csv`; a.click();
});

/* ---- copy press brief ---- */
document.getElementById("copy-brief").addEventListener("click",async()=>{
 const top=window._top,data=window._data;
 if(!top||!data)return;
 const text=`CityPulse civic data brief — ${data.city}, India — ${new Date().toLocaleString()}\n\n${top.name} recorded a risk score of ${top.risk}/100 (${top.status}), against a city-wide average of ${window._avgRisk}/100 across ${data.zones.length} zones. ${window._flagCount} zone(s) showed correlated signal movement (confidence ${window._confidence}%, convergence ${window._convergence}/100).\n\nSource: CityPulse civic signal dashboard (simulated feed data for demonstration). Correlations are possible links, not confirmed causation.`;
 try{await navigator.clipboard.writeText(text);const btn=document.getElementById("copy-brief");const orig=btn.textContent;btn.textContent="✓ Copied";setTimeout(()=>btn.textContent=orig,1800);}catch(e){alert(text);}
});

function buildSimUI(top){
 const g=document.getElementById("sim-grid");
 const fields=[["rainfall","Rainfall"],["traffic","Traffic"],["transit","Transit delay"],["complaints","Complaints"]];
 g.innerHTML=fields.map(([k,label])=>`
  <div class="sim-ctrl"><div class="sim-head"><label>${label}</label><span id="sv-${k}">${top[k]}</span></div>
  <input type="range" min="0" max="100" value="${top[k]}" id="sr-${k}"></div>`).join("");
 fields.forEach(([k])=>{document.getElementById(`sr-${k}`).addEventListener("input",e=>{document.getElementById(`sv-${k}`).textContent=e.target.value;});});
}
document.getElementById("sim-run").addEventListener("click",()=>{
 const vals={rainfall:+document.getElementById("sr-rainfall").value,traffic:+document.getElementById("sr-traffic").value,transit:+document.getElementById("sr-transit").value,complaints:+document.getElementById("sr-complaints").value};
 const risk=riskFromSignals(vals.rainfall,vals.traffic,vals.transit,vals.complaints);
 const status=statusForRisk(risk);
 document.getElementById("sim-risk").textContent=risk;
 document.getElementById("sim-status").textContent=STATUS_META[status].label[state.lang];
 document.getElementById("sim-status").style.color=`var(--${STATUS_META[status].cls})`;
});

/* ---- Ask CityPulse ---- */
function answerQuestion(q){
 const top=window._top,second=window._second,data=window._data,conf=window._confidence,conv=window._convergence;
 const ql=q.toLowerCase();
 let ans;
 if(ql.includes("compare")){
  ans=`<strong>${top.name}</strong> (risk ${top.risk}, ${top.status.toLowerCase()}) vs <strong>${second.name}</strong> (risk ${second.risk}, ${second.status.toLowerCase()}). ${top.name} runs ${top.risk-second.risk} points higher, driven mainly by ${top.complaints>second.complaints?"complaint volume":"transit disruption"}.`;
 } else if(ql.includes("why")||ql.includes("flag")){
  ans=top.anomaly?`${top.name} is flagged because ${[top.rainfall>50?"rainfall":null,top.traffic>50?"traffic":null,top.transit>50?"transit delay":null,top.complaints>50?"complaint volume":null].filter(Boolean).join(", ")} are all elevated in the same window — a ${conf}% confidence, ${conv}/100 convergence pattern.`:`${top.name} isn't currently flagged — signals are elevated individually but not moving together.`;
 } else {
  const cityMatch=data.zones.find(z=>ql.includes(z.name.toLowerCase()));
  if(cityMatch){ans=`${cityMatch.name} is currently reading ${cityMatch.risk}/100 (${cityMatch.status.toLowerCase()}). Rainfall ${cityMatch.rainfall}, traffic ${cityMatch.traffic}, transit delay ${cityMatch.transit}, complaints ${cityMatch.complaints}.`;}
  else{ans=`Right now in ${data.city}, ${top.name} has the highest risk (${top.risk}/100, ${top.status.toLowerCase()}), with ${conf}% confidence behind the flag. ${data.zones.filter(z=>z.anomaly).length} of ${data.zones.length} zones show a correlated pattern.`;}
 }
 document.getElementById("ai-answer").innerHTML=`<span class="tag">${t("tag")}</span><br>${ans}`;
}
document.getElementById("ai-ask").addEventListener("click",()=>{const v=document.getElementById("ai-input").value.trim();if(v)answerQuestion(v);});
document.getElementById("ai-input").addEventListener("keydown",e=>{if(e.key==="Enter"){const v=e.target.value.trim();if(v)answerQuestion(v);}});
document.querySelectorAll(".chip").forEach(c=>c.addEventListener("click",()=>{document.getElementById("ai-input").value=c.dataset.q;answerQuestion(c.dataset.q);}));

/* ---- Is it safe right now? citizen widget ---- */
function buildSafeZonePicker(data){
 const p=document.getElementById("safe-zone-picker");
 const current=p.value;
 p.innerHTML=data.zones.map(z=>`<option value="${z.name}">${z.name}</option>`).join("");
 if(current)p.value=current;
}
function verdictFor(zone){
 if(zone.risk<28)return{cls:"v-safe",text:t("safe"),advice:"Normal outdoor activity — no active signal correlation."};
 if(zone.risk<50)return{cls:"v-caution",text:t("caution"),advice:"Keep an eye on transit delays and local weather updates."};
 return{cls:"v-avoid",text:t("avoid"),advice:"Multiple signals elevated together — postpone non-essential trips if possible."};
}
document.getElementById("safe-check-btn").addEventListener("click",()=>{
 const name=document.getElementById("safe-zone-picker").value;
 const z=window._data.zones.find(zz=>zz.name===name);
 if(!z)return;
 const v=verdictFor(z);
 const el=document.getElementById("safe-verdict");
 el.className=`safe-verdict ${v.cls}`;
 el.innerHTML=`<span class="tag">${z.name.toUpperCase()} · RISK ${z.risk}/100</span><br><strong>${v.text}</strong><br>${v.advice}`;
});

/* ---- Listen (text-to-speech) ---- */
document.getElementById("listen-btn").addEventListener("click",()=>{
 if(!window.speechSynthesis)return;
 const verdict=document.getElementById("safe-verdict").innerText;
 const brief=document.getElementById("brief-text").innerText;
 const text=verdict&&!verdict.includes("Pick a zone")?verdict:brief;
 const u=new SpeechSynthesisUtterance(text);
 u.lang=state.lang==="hi"?"hi-IN":"en-IN";
 speechSynthesis.cancel();speechSynthesis.speak(u);
});

/* ---- browser notifications on CRITICAL ---- */
document.getElementById("notify-toggle").addEventListener("click",async()=>{
 if(!("Notification" in window)){alert("Notifications aren't supported in this browser.");return;}
 if(Notification.permission!=="granted"){const perm=await Notification.requestPermission();if(perm!=="granted")return;}
 state.notifyOn=!state.notifyOn;
 document.getElementById("notify-toggle").classList.toggle("active",state.notifyOn);
 document.getElementById("notify-toggle").textContent=state.notifyOn?"🔔 Alerts on":"🔔 Enable alerts";
});
function checkNotify(cityStatus,cityName){
 if(!state.notifyOn||Notification.permission!=="granted")return;
 if(cityStatus==="CRITICAL"&&state.lastNotifiedStatus!=="CRITICAL"){
  new Notification("CityPulse alert",{body:`${cityName} just crossed into CRITICAL — check the dashboard.`});
 }
 state.lastNotifiedStatus=cityStatus;
}

/* =========================================================================
   NEW FEATURE RENDERERS
   ========================================================================= */

/* ---- Avoid right now ---- */
function renderAvoidNow(data,incidents){
 const el=document.getElementById("avoid-grid");
 const closures=buildRoadGraph(data).filter(e=>e.closed);
 const riskyZones=data.zones.filter(z=>z.status==="CRITICAL"||z.status==="EMERGING");
 const cards=[];
 riskyZones.forEach(z=>{
  const reasons=[];
  if(z.rainfall>60)reasons.push("waterlogging risk");
  if(z.trafficLightDown)reasons.push("signal down");
  if(z.outage)reasons.push("possible power outage");
  if(z.gasLeak)reasons.push("gas leak reported");
  if(!reasons.length)reasons.push("multiple signals elevated");
  cards.push({title:`${z.name}`,reason:reasons.join(" · ")+` — risk ${z.risk}/100`,ok:false});
 });
 closures.forEach(c=>{cards.push({title:`${data.zones[c.a].name} ↔ ${data.zones[c.b].name} road`,reason:`Closed — ${c.reason}`,ok:false});});
 if(!cards.length)cards.push({title:"Nothing to avoid right now",reason:"All zones and monitored roads are reading normal.",ok:true});
 el.innerHTML=cards.slice(0,8).map(c=>`<div class="avoid-card ${c.ok?'ok':''}"><div class="a-title">${c.ok?'✅':'⛔'} ${c.title}</div><div class="a-reason">${c.reason}</div></div>`).join("");
}

/* ---- India hazard watch / news ----
   Renders instantly from the local signal-derived feed (never blocks the
   dashboard on a network call), then tries a real backend for live
   headlines and swaps them in if one answers in time. This is the
   "degrade gracefully" behaviour from the problem statement, not just a
   loading spinner — if the backend/API is down, the dashboard is already
   showing something useful. See backend/server.js's /api/news/:city route
   for the real NewsAPI.org wiring (needs NEWS_API_KEY). */
const NEWS_BACKEND_URL="http://localhost:4000"; // set to your deployed backend's URL, or "" to disable live fetch entirely
function renderNewsGrid(items,liveState){
 const badge=liveState==="live"?`<span class="news-live-tag live">🟢 LIVE</span>`:liveState==="checking"?`<span class="news-live-tag">🔄 Checking for live source…</span>`:`<span class="news-live-tag">⚪ Simulated demo feed</span>`;
 document.getElementById("news-grid").innerHTML=`<div class="news-live-row">${badge}</div>`+items.map(n=>`
  <div class="news-card sev-${n.badge}">
   <div class="news-top"><span class="news-source">${n.source}</span><span class="news-badge b-${n.badge==='critical'?'critical':n.badge==='watch'?'watch':'normal'}">${n.badge}</span></div>
   <div class="news-title">${n.url?`<a href="${n.url}" target="_blank" rel="noopener" style="color:inherit;text-decoration:none;">${n.title} ↗</a>`:n.title}</div>
   <div class="news-body">${n.body}</div>
   <div class="news-time">${n.time}</div>
  </div>`).join("");
}
function renderHazardWatch(data,incidents){
 const simulated=buildNewsFeed(data,incidents);
 renderNewsGrid(simulated,NEWS_BACKEND_URL?"checking":"simulated");
 if(!NEWS_BACKEND_URL)return;
 const requestCity=data.city;
 const ctrl=new AbortController();
 const timeout=setTimeout(()=>ctrl.abort(),2500);
 fetch(`${NEWS_BACKEND_URL}/api/news/${encodeURIComponent(requestCity)}`,{signal:ctrl.signal})
  .then(r=>{if(!r.ok)throw new Error(`status ${r.status}`);return r.json();})
  .then(payload=>{
   clearTimeout(timeout);
   if(window._data.city!==requestCity)return; // user already switched cities — drop stale response
   if(payload.simulated||!payload.items||!payload.items.length){renderNewsGrid(simulated,"simulated");return;}
   renderNewsGrid(payload.items,"live");
  })
  .catch(()=>{clearTimeout(timeout);if(window._data.city===requestCity)renderNewsGrid(simulated,"simulated");});
}

/* ---- Live incident SVG map ---- */
function zonePos(cityName,zoneName,idx,total){
 const rand=mulberry32(hashSeed(cityName+zoneName+"-pos"));
 const angle=(idx/total)*Math.PI*2+rand()*0.6;
 const radius=90+rand()*70;
 const cx=300+Math.cos(angle)*radius, cy=200+Math.sin(angle)*radius*0.72;
 return{x:cx,y:cy};
}
const SEV_COLOR={critical:"var(--critical)",watch:"var(--watch)",normal:"var(--normal)"};
function renderMap(data,incidents){
 const wrap=document.getElementById("map-svg-wrap");
 const positions=data.zones.map((z,i)=>({...z,pos:zonePos(data.city,z.name,i,data.zones.length)}));
 let svg=`<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">`;
 svg+=`<circle cx="300" cy="200" r="175" fill="none" stroke="var(--border)" stroke-dasharray="3 5" stroke-width="1"/>`;
 for(let i=0;i<positions.length;i++)for(let j=i+1;j<positions.length;j++){
  svg+=`<line x1="${positions[i].pos.x}" y1="${positions[i].pos.y}" x2="${positions[j].pos.x}" y2="${positions[j].pos.y}" stroke="var(--border-soft)" stroke-width="1"/>`;
 }
 positions.forEach(z=>{
  const m=STATUS_META[z.status];
  const r=14+z.risk/8;
  svg+=`<circle class="map-zone-circle" data-zone="${z.name}" cx="${z.pos.x}" cy="${z.pos.y}" r="${r}" fill="var(--${m.cls})" fill-opacity="0.28" stroke="var(--${m.cls})" stroke-width="2"/>`;
  svg+=`<text class="map-zone-label" x="${z.pos.x}" y="${z.pos.y+r+13}" text-anchor="middle">${z.name}</text>`;
 });
 incidents.filter(inc=>inc.zone!=="Citywide").forEach(inc=>{
  const z=positions.find(p=>p.name===inc.zone); if(!z)return;
  const meta=INCIDENT_META[inc.type]||{icon:"⚠️"};
  svg+=`<text class="map-incident-marker" data-inc="${inc.id}" x="${z.pos.x+16}" y="${z.pos.y-14}" font-size="16">${meta.icon}</text>`;
 });
 svg+=`</svg>`;
 wrap.innerHTML=svg;
 wrap.querySelector("svg").style.transform=`scale(${state.mapZoom})`;
 document.getElementById("map-legend").innerHTML=Object.entries(STATUS_META).map(([k,m])=>`<span><i style="background:var(--${m.cls})"></i>${m.label.en}</span>`).join("");

 wrap.querySelectorAll(".map-zone-circle").forEach(c=>c.addEventListener("click",()=>{
  const z=data.zones.find(zz=>zz.name===c.dataset.zone); if(!z)return;
  const zoneIncidents=incidents.filter(i=>i.zone===z.name);
  document.getElementById("map-info").innerHTML=`<span class="tag">${z.name.toUpperCase()} · RISK ${z.risk}/100</span><br>
   <strong>Status:</strong> ${STATUS_META[z.status].label.en} · <strong>Condition:</strong> ${z.weather}<br>
   <strong>Signals:</strong> rainfall ${z.rainfall}, traffic ${z.traffic}, transit ${z.transit}, complaints ${z.complaints}, AQI ${z.aqi}<br>
   ${zoneIncidents.length?`<strong>Active incidents:</strong> ${zoneIncidents.map(i=>i.title).join("; ")}`:"No active incidents in this zone."}`;
 }));
 wrap.querySelectorAll(".map-incident-marker").forEach(m=>m.addEventListener("click",()=>{
  const inc=incidents.find(i=>i.id===m.dataset.inc); if(!inc)return;
  document.getElementById("map-info").innerHTML=`<span class="tag">${(INCIDENT_META[inc.type]||{}).label||inc.type} · ${inc.zone.toUpperCase()}</span><br><strong>${inc.title}</strong><br>${inc.desc}<br><span style="color:var(--dim);font-size:11.5px;">Source: ${inc.source}</span>`;
 }));
}
document.getElementById("map-zoom-in").addEventListener("click",()=>{state.mapZoom=Math.min(2.2,state.mapZoom+0.2);applyMapZoom();});
document.getElementById("map-zoom-out").addEventListener("click",()=>{state.mapZoom=Math.max(0.6,state.mapZoom-0.2);applyMapZoom();});
document.getElementById("map-zoom-reset").addEventListener("click",()=>{state.mapZoom=1;applyMapZoom();});
function applyMapZoom(){const svg=document.querySelector("#map-svg-wrap svg");if(svg)svg.style.transform=`scale(${state.mapZoom})`;}

/* ---- Historical risk profile + replay ---- */
function renderHistorical(cityIndex){
 const h=historicalProfile(cityIndex);
 const maxTotal=Math.max(...h.zoneStats.map(z=>z.total),1);
 document.getElementById("hist-grid").innerHTML=h.zoneStats.map(z=>`
  <div class="hist-zone-card"><div class="hz-name">${z.zone}</div>
   <div class="hist-bar-row"><span style="width:60px;">Floods</span><div class="hist-bar-track"><div class="hist-bar-fill" style="width:${z.floods/maxTotal*100}%;background:var(--brand)"></div></div><span>${z.floods}</span></div>
   <div class="hist-bar-row"><span style="width:60px;">Cyclones</span><div class="hist-bar-track"><div class="hist-bar-fill" style="width:${z.cyclones/maxTotal*100}%;background:var(--violet)"></div></div><span>${z.cyclones}</span></div>
   <div class="hist-bar-row"><span style="width:60px;">Accidents</span><div class="hist-bar-track"><div class="hist-bar-fill" style="width:${z.accidents/maxTotal*100}%;background:var(--emerging)"></div></div><span>${z.accidents}</span></div>
   <div class="hist-bar-row"><span style="width:60px;">Power cuts</span><div class="hist-bar-track"><div class="hist-bar-fill" style="width:${z.powerCuts/maxTotal*100}%;background:var(--watch)"></div></div><span>${z.powerCuts}</span></div>
  </div>`).join("");
 const maxY=Math.max(...h.yearly.map(y=>y.events),1);
 document.getElementById("hist-yearly").innerHTML=h.yearly.map(y=>`
  <div class="hist-year-col"><div class="hist-year-bar" style="height:${Math.max(6,y.events/maxY*90)}px;" title="${y.events} logged events"></div><div class="hist-year-label">${y.year}</div></div>`).join("");
 document.getElementById("hist-timeline").innerHTML=h.timeline.map((tl,i)=>`
  <div class="hist-tl-item ${i===0?'active':''}" data-idx="${i}"><div class="hist-tl-year">${tl.year}</div><div>${tl.text}</div></div>`).join("");
 window._histTimeline=h.timeline;
 state.replayIndex=0;
}
document.getElementById("replay-btn").addEventListener("click",()=>{
 if(state.replayPlaying)return;
 const items=document.querySelectorAll(".hist-tl-item");
 if(!items.length)return;
 state.replayPlaying=true; state.replayIndex=0;
 const btn=document.getElementById("replay-btn"); btn.textContent="⏸ Playing…";
 const step=()=>{
  items.forEach((el,i)=>el.classList.toggle("active",i===state.replayIndex));
  state.replayIndex++;
  if(state.replayIndex>=items.length){state.replayPlaying=false;btn.textContent="▶ Replay";return;}
  setTimeout(step,1100);
 };
 step();
});

/* ---- Citizen reporting ---- */
function reportsKey(city){return `citypulse_reports_${city}`;}
function loadReports(city){try{return JSON.parse(localStorage.getItem(reportsKey(city))||"[]");}catch(e){return[];}}
function saveReports(city,list){try{localStorage.setItem(reportsKey(city),JSON.stringify(list));}catch(e){}}
const REPORT_TYPE_META={waterlogging:"💧 Waterlogging",road_damage:"🚧 Road damage",accident:"🚗 Accident",power:"⚡ Power outage",gas_leak:"🔥 Gas leak",transit:"🚌 Transit problem",signal:"🚦 Signal down",tree:"🌳 Fallen tree",gathering:"📢 Public gathering",garbage:"🗑️ Garbage",streetlight:"💡 Streetlight",other:"Other"};
function renderReporting(data){
 const zp=document.getElementById("report-zone");
 const cur=zp.value;
 zp.innerHTML=data.zones.map(z=>`<option value="${z.name}">${z.name}</option>`).join("");
 if(cur)zp.value=cur;
 const list=loadReports(data.city);
 const el=document.getElementById("report-list");
 if(!list.length){el.innerHTML=`<div class="report-empty">No citizen reports yet for ${data.city}. Be the first to report something above.</div>`;return;}
 el.innerHTML=list.slice().reverse().slice(0,12).map(r=>{
  const status=r.confirmations>=5?"verified":r.confirmations>=2?"corroborated":"unverified";
  const statusLabel=status==="verified"?"Verified":status==="corroborated"?"Corroborated":"Unverified";
  return `<div class="report-item" data-id="${r.id}">
   <div class="r-main"><strong>${REPORT_TYPE_META[r.type]||r.type}</strong> — ${r.zone}<span class="r-status ${status}">${statusLabel}</span>
    ${r.desc?`<div class="r-meta">${r.desc}</div>`:""}
    <div class="r-meta">${new Date(r.time).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})} · ${r.confirmations} citizen confirmation${r.confirmations===1?"":"s"}</div>
   </div>
   <button class="confirm-btn" data-confirm="${r.id}">👍 I see this too</button>
  </div>`;
 }).join("");
 el.querySelectorAll("[data-confirm]").forEach(b=>b.addEventListener("click",()=>{
  const id=b.dataset.confirm;
  const arr=loadReports(data.city);
  const rep=arr.find(r=>r.id===id); if(!rep)return;
  rep.confirmations=(rep.confirmations||0)+1;
  saveReports(data.city,arr);
  renderReporting(window._data);
 }));
}
document.getElementById("report-photo").addEventListener("change",e=>{
 const f=e.target.files[0];
 document.getElementById("photo-name").textContent=f?f.name:"Add photo (optional)";
 const prev=document.getElementById("report-photo-preview"); prev.innerHTML="";
 if(f){const url=URL.createObjectURL(f);prev.innerHTML=`<img src="${url}" alt="Report photo preview">`;}
});
document.getElementById("report-submit").addEventListener("click",()=>{
 const data=window._data; if(!data)return;
 const type=document.getElementById("report-type").value;
 const zone=document.getElementById("report-zone").value;
 const desc=document.getElementById("report-desc").value.trim().slice(0,240);
 const rep={id:`r${Date.now()}${Math.floor(Math.random()*999)}`,type,zone,desc,time:Date.now(),confirmations:0};
 const arr=loadReports(data.city); arr.push(rep); saveReports(data.city,arr);
 document.getElementById("report-desc").value="";
 document.getElementById("report-photo").value="";
 document.getElementById("photo-name").textContent="Add photo (optional)";
 document.getElementById("report-photo-preview").innerHTML="";
 renderReporting(data);
});

/* ---- data source status strip ---- */
function renderSourceStatus(){
 const sources=[
  {name:"Weather",ok:true},{name:"Traffic",ok:true},{name:"Transit",ok:true},
  {name:"Air quality",ok:Math.random()>0.08},{name:"Power grid",ok:Math.random()>0.1},
  {name:"Citizen reports",ok:true},{name:"News / hazard bulletins",ok:Math.random()>0.05},
 ];
 document.getElementById("source-status").innerHTML=sources.map(s=>`
  <div class="source-row"><span>${s.name}</span><span style="display:flex;align-items:center;gap:6px;color:${s.ok?'var(--normal)':'var(--watch)'}"><span class="source-dot" style="background:${s.ok?'var(--normal)':'var(--watch)'}"></span>${s.ok?"Live":"Degraded — last known"}</span></div>`).join("");
}

/* ---- flash alert for critical incidents ---- */
function flashCheck(data,incidents){
 const critical=incidents.find(i=>i.severity==="critical");
 const el=document.getElementById("flash-alert");
 if(!critical){el.classList.remove("show");return;}
 const key=critical.id;
 if(state.flashDismissedKey===key){el.classList.remove("show");return;}
 el.innerHTML=`<div class="flash-alert-msg"><span class="flash-alert-icon">${(INCIDENT_META[critical.type]||{}).icon||"⚠️"}</span><span><strong>${critical.title}</strong> — ${critical.desc}</span></div><button class="flash-alert-close" id="flash-dismiss">Dismiss</button>`;
 el.classList.add("show");
 document.getElementById("flash-dismiss").addEventListener("click",()=>{state.flashDismissedKey=key;el.classList.remove("show");});
 if(state.notifyOn&&Notification.permission==="granted"&&state._lastFlashKey!==key){
  new Notification("CityPulse critical alert",{body:critical.title});
 }
 state._lastFlashKey=key;
}

/* ---- language toggle ---- */
document.getElementById("lang-toggle").addEventListener("click",()=>{
 state.lang=state.lang==="en"?"hi":"en";
 document.getElementById("lang-toggle").textContent=state.lang==="en"?"हिन्दी":"English";
 render();
});

/* ---- city + time machine controls ---- */
const picker=document.getElementById("city-picker");
CITIES.forEach((c,i)=>{const o=document.createElement("option");o.value=i;o.textContent=c.name+", India";picker.appendChild(o);});
picker.addEventListener("change",e=>{state.cityIndex=+e.target.value;state.tick=0;state.viewOffset=0;state.mapZoom=1;state._histBuilt=false;setTimeSeg(0);render();});

function setTimeSeg(off){document.querySelectorAll("#time-seg button").forEach(b=>b.classList.toggle("on",+b.dataset.off===off));}
document.querySelectorAll("#time-seg button").forEach(b=>b.addEventListener("click",()=>{state.viewOffset=+b.dataset.off;setTimeSeg(state.viewOffset);render();}));

render();
setInterval(()=>{if(state.viewOffset===0){state.tick++;render();}},8000);
setInterval(()=>{if(state.viewOffset===0)document.getElementById("hero-time").textContent=fmtTime();},1000);
