const state={slug:document.body.dataset.slug||'vienna-table',data:null};
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const money=n=>'€'+(n>=1000?(n/1000).toFixed(1)+'k':n.toLocaleString());

async function load(){
  const r=await fetch(`/demo/dashboard/${state.slug}`); state.data=await r.json(); render();
}
function render(){const d=state.data, r=d.restaurant;
  $('#restaurantName').textContent=r.name; $('#chatRestaurant').textContent=r.name+' AI'; $$('.chat-rest-name').forEach(x=>x.textContent=r.name); $('#restaurantHero').textContent=r.hero;
  $('#heroResolved').textContent=d.kpi.resolution_rate+'%'; $('#heroHours').textContent=d.kpi.hours_saved+'h'; $('#heroValue').textContent=money(d.kpi.estimated_value);
  $('#restaurantSelect').innerHTML=d.restaurants.map(x=>`<option value="${x.slug}" ${x.slug===state.slug?'selected':''}>${x.name} · ${x.city}</option>`).join('');
  const ks=[['Conversations',d.kpi.conversations,'Across all channels'],['Reservations created',d.kpi.reservations,d.kpi.guests+' guests booked'],['After-hours handled',d.kpi.after_hours,'No staff needed'],['Missed calls prevented',d.kpi.missed_calls_prevented,'Estimated'],['Resolution rate',d.kpi.resolution_rate+'%',d.kpi.handoffs+' safe handoffs'],['Staff time saved',d.kpi.hours_saved+' h','Estimated from handling time'],['Booking value',money(d.kpi.estimated_value),'AI-assisted'],['Active channels','3','Phone · WhatsApp · Web']];
  $('#kpiGrid').innerHTML=ks.map(k=>`<div class="kpi"><span>${k[0]}</span><strong>${k[1]}</strong><small>${k[2]}</small></div>`).join('');
  const max=Math.max(...d.weekly.map(x=>x.conversations)); $('#weeklyChart').innerHTML=d.weekly.map(x=>`<div class="bar-wrap"><div class="bar" style="height:${Math.round(x.conversations/max*165)}px"><div class="bar-value">${x.conversations}</div></div><span>${x.day}</span></div>`).join('');
  $('#channelList').innerHTML=d.channels.map(x=>`<div class="channel-row"><strong>${x.name}</strong><div class="track"><div class="fill" style="width:${x.share}%"></div></div><span>${x.share}%</span><div></div><small class="muted">${x.handled} handled · ${x.resolution}% resolved</small></div>`).join('');
  $('#activityList').innerHTML=d.activity.map(x=>`<div class="activity-row"><span class="muted">${x.time}</span><span class="channel">${x.channel}</span><div><strong>${x.event}</strong><div class="activity-detail">${x.detail}</div></div><div class="activity-value">${x.value}</div></div>`).join('');
  $('#scenarioRow').innerHTML=d.scenarios.map(x=>`<button class="scenario" data-message="${x.message.replaceAll('"','&quot;')}">${x.label}</button>`).join('');
  $('.scenario')?.addEventListener?.('noop',()=>{}); $$('.scenario').forEach(b=>b.onclick=()=>sendDemo(b.dataset.message));
  $('#reservationSummary').innerHTML=[['Tonight',d.reservations.length+' bookings','AI-assisted examples'],['Guests',d.reservations.reduce((a,x)=>a+x.party,0),'Across tonight'],['Booking value',money(d.reservations.reduce((a,x)=>a+x.value,0)),'Estimated'],['Channels','3','Unified book']].map(k=>`<div class="kpi"><span>${k[0]}</span><strong>${k[1]}</strong><small>${k[2]}</small></div>`).join('');
  $('#reservationTable').innerHTML=d.reservations.map(x=>`<tr><td><b>${x.time}</b></td><td>${x.name}</td><td>${x.party}</td><td>${x.seating}</td><td><span class="channel">${x.source}</span></td><td><span class="status">${x.status}</span></td><td>€${x.value}</td></tr>`).join('');
  $('#conversationCards').innerHTML=d.conversations.map(x=>`<div class="conversation-card"><div><b>${x.id}</b><div class="conversation-meta">${x.channel} · ${x.lang}</div></div><div><strong>${x.intent} · ${x.guest}</strong><p>${x.summary}</p></div><div><span class="status">${x.status}</span><p>${x.duration}</p></div></div>`).join('');
  $('#knowledgeName').textContent=r.name; $('#profileDetails').innerHTML=[['Concept',r.concept],['Location',r.address],['Phone',r.phone],['Hours',r.hours],['Language',r.language]].map(x=>`<div class="detail"><span>${x[0]}</span><b>${x[1]}</b></div>`).join('');
  $('#menuList').innerHTML=r.menu.map(x=>`<div class="menu-item"><div><b>${x.name}</b><span>${x.diet||'Standard'} · Allergens: ${x.allergens}</span></div><strong>€${x.price}</strong></div>`).join('');
  $('#policyList').innerHTML=r.policies.map(x=>`<div class="policy">✓ ${x}</div>`).join('');
  const icons={'Reservation system':'◫','POS':'▦','WhatsApp':'◉','Phone':'☎','Website':'⌂','Hotel PMS':'▤'}; $('#integrationGrid').innerHTML=r.integrations.map(x=>`<div class="integration"><div class="icon">${icons[x]||'◇'}</div><strong>${x}</strong><span>Demo adapter ready</span></div>`).join('');
}
function showView(name){$$('.view').forEach(v=>v.classList.remove('active')); $(`#view-${name}`).classList.add('active'); $$('.nav').forEach(n=>n.classList.toggle('active',n.dataset.view===name)); window.scrollTo({top:0,behavior:'smooth'});}
$$('.nav').forEach(n=>n.onclick=()=>showView(n.dataset.view)); $$('[data-jump]').forEach(b=>b.onclick=()=>showView(b.dataset.jump));
$('#restaurantSelect').onchange=e=>{state.slug=e.target.value; resetChat(); load();};
$('#resetDemo').onclick=()=>{state.slug='vienna-table'; resetChat(); load(); showView('overview');};
function addBubble(text,type){const el=document.createElement('div');el.className='bubble '+type;el.textContent=text;$('#chatLog').appendChild(el);$('#chatLog').scrollTop=$('#chatLog').scrollHeight;}
function resetChat(){const name=state.data?.restaurant?.name||'Vienna Table';$('#chatLog').innerHTML=`<div class="bubble bot">Hello — I’m the digital assistant for <span class="chat-rest-name">${name}</span>. I can help with reservations, menu questions, opening hours and guest requests.</div>`;$('#traceList').innerHTML='';$('#traceEmpty').classList.remove('hidden');$('#actionCard').hidden=true;}
async function sendDemo(message){if(!message.trim())return; addBubble(message,'user'); $('#demoInput').value=''; const r=await fetch(`/demo/chat/${state.slug}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message})});const out=await r.json(); setTimeout(()=>addBubble(out.reply,'bot'),180); $('#traceEmpty').classList.add('hidden'); $('#traceList').innerHTML=out.trace.map((t,i)=>`<div class="trace-step"><div class="step-num">${i+1}</div><div>${t}</div></div>`).join(''); $('#actionCard').hidden=false; $('#actionCard').innerHTML=`<span>FINAL ACTION</span><strong>${out.action.replaceAll('_',' ')}</strong><div style="font-size:12px;margin-top:5px;opacity:.8">Intent: ${out.intent} · synthetic execution</div>`;}
$('#demoChatForm').onsubmit=e=>{e.preventDefault();sendDemo($('#demoInput').value)};
$$('.channel-tab').forEach(b=>b.onclick=()=>{$$('.channel-tab').forEach(x=>x.classList.remove('active'));b.classList.add('active')});
load();
