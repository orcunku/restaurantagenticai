(function(){
 const root=document.querySelector('[data-ai-frontdesk]'); if(!root)return;
 const slug=root.dataset.restaurant; const log=root.querySelector('.afd-log'); const form=root.querySelector('form'); const input=root.querySelector('input');
 const uid=localStorage.afd_uid||(localStorage.afd_uid=crypto.randomUUID()); const sid=sessionStorage.afd_sid||(sessionStorage.afd_sid=crypto.randomUUID());
 function add(who,text){const d=document.createElement('div');d.className='afd-msg '+who;d.textContent=text;log.appendChild(d);log.scrollTop=log.scrollHeight;}
 form.addEventListener('submit',async(e)=>{e.preventDefault();const msg=input.value.trim();if(!msg)return;add('user',msg);input.value='';
   try{const r=await fetch('/api/chat/'+encodeURIComponent(slug),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,user_id:uid,session_id:sid})});const j=await r.json();add('bot',j.reply||'Fehler.');}
   catch(e){add('bot','Der digitale Assistent ist gerade nicht erreichbar.');}
 });
})();
