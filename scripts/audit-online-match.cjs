// Start one local private match with separate host and guest browser sessions.
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const out=path.resolve(__dirname,'..');
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true,args:['--use-angle=metal','--enable-gpu']});
 const records=[];
 async function page(){const c=await b.newContext({viewport:{width:1366,height:768},deviceScaleFactor:1});await c.addInitScript(()=>localStorage.setItem('kr-controls-seen','1'));return await c.newPage();}
 async function capture(p,name){await p.waitForTimeout(600);const v=await p.evaluate(()=>({url:location.href,viewport:[innerWidth,innerHeight],dpr:devicePixelRatio,body:document.body.innerText,buttons:[...document.querySelectorAll('button')].filter(e=>e.checkVisibility({checkOpacity:true,checkVisibilityCSS:true})).map(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {text:e.innerText.trim(),x:r.x,y:r.y,w:r.width,h:r.height,font:s.fontSize}}),errors:window.__kr?.errors,game:window.__kr?.game?.state(),online:window.__kr?.game?.link ? !window.__kr.game.link.offline : null,inMatch:window.__kr?.game?.inMatch}));records.push({name,...v});fs.writeFileSync(path.join(out,'online-match-states.json'),JSON.stringify(records,null,2));await p.screenshot({path:path.join(out,`online-match-${name}.png`)});}
 try{
  const host=await page(); await host.goto('http://127.0.0.1:5320/');await host.waitForFunction(()=>window.__kr?.ready,null,{timeout:180000});await host.waitForTimeout(4000);
  await host.getByText('Friends',{exact:true}).click();await host.getByRole('button',{name:'Create lobby',exact:true}).click();
  await host.getByRole('button',{name:'Copy invite link'}).waitFor({timeout:120000});await capture(host,'host');
  const body=await host.locator('body').innerText();const match=body.match(/PRIVATE LOBBY[^\n]*\n([A-Z0-9]{4})/);if(!match)throw Error('Could not identify room code');const code=match[1];
  const guest=await page();await guest.goto(`http://127.0.0.1:5320/?join=${code}`);await guest.waitForFunction(()=>window.__kr?.ready,null,{timeout:180000});await guest.waitForTimeout(4000);await capture(guest,'invited');
  await guest.getByRole('button',{name:/Join lobby/i}).click();await guest.getByText('2 PLAYERS',{exact:false}).first().waitFor({timeout:120000});await capture(guest,'guest-joined');await capture(host,'host-two');
  await host.getByRole('button',{name:'Start match',exact:true}).click();
  await host.waitForFunction(()=>window.__kr?.game?.inMatch&&window.__kr.game.link?.offline===false,null,{timeout:180000});
  await guest.waitForFunction(()=>window.__kr?.game?.inMatch&&window.__kr.game.link?.offline===false,null,{timeout:180000});
  await host.waitForTimeout(3000);await capture(host,'host-warmup');await capture(guest,'guest-warmup');
  await host.evaluate(()=>window.__kr.game.startNow());
  await host.waitForFunction(()=>window.__kr.game.state()?.phase===1,null,{timeout:180000});
  await guest.waitForFunction(()=>window.__kr.game.state()?.phase===1,null,{timeout:180000});
  await capture(host,'host-flight');await capture(guest,'guest-flight');

 }finally{await b.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
