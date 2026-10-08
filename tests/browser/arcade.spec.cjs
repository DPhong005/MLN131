const {test,expect}=require('@playwright/test');
const glossary=require('../../data/glossary.json');
const claims=require('../../data/gameClaims.json');
const questions=require('../../data/questions.json');
async function enter(page,mode){await page.goto('/game.html?mode='+mode);await expect(page.locator('body')).toHaveClass(/ready/);await page.locator('#arcade-start').click();}
test('decode completes all rounds, supports correction and saves a result',async({page})=>{
 await enter(page,'decode');
 for(let n=0;n<8;n++){
  const clue=await page.locator('.arcade-clue').textContent();const item=glossary.find(x=>x.definition===clue);
  if(n===0){await page.locator('#decode-check').click();await expect(page.locator('#arcade-feedback')).toContainText('Chưa đúng');await page.locator('#decode-hint').click();}
  for(const word of item.term.split(/\s+/)){const buttons=page.locator('[data-piece]:not(:disabled)');let picked=false;for(const b of await buttons.all()){if(await b.textContent()===word){await b.click();picked=true;break;}}expect(picked).toBeTruthy();}
  await page.locator('#decode-check').click();await expect(page.locator('#arcade-feedback')).toContainText('Chính xác');await page.locator('#decode-next').click();
 }
 await expect(page.locator('.arcade-result')).toContainText('giải mã đủ 8');await page.goto('/games.html');await expect(page.locator('.arcade-game-card').first()).toContainText('Điểm tốt nhất');
});
test('mindmap accepts drag and keyboard placement, corrects mistakes and completes',async({page})=>{
 await enter(page,'mindmap');const entries=await page.locator('[data-concept]').evaluateAll(nodes=>nodes.map(x=>({id:x.dataset.concept,term:x.textContent})));
 for(let i=0;i<entries.length;i++){const x=entries[i],c=glossary.find(g=>g.term===x.term).chapterId;
  if(i===0){await page.locator(`[data-concept="${x.id}"]`).click();await page.locator(`[data-zone]:not([data-zone="${c}"])`).first().click();await expect(page.locator('#arcade-feedback')).toContainText('Chưa đúng');await page.locator(`[data-concept="${x.id}"]`).dragTo(page.locator(`[data-zone="${c}"]`));}
  else{await page.locator(`[data-concept="${x.id}"]`).focus();await page.keyboard.press('Enter');await page.locator(`[data-zone="${c}"]`).click();}
 }
 await expect(page.locator('#map-bank [data-concept]')).toHaveCount(0);await page.locator('#map-finish').click();await expect(page.locator('.arcade-result')).toContainText('Đã phân loại 6');
});
test('dossier finds exactly three false claims, shows sources and completes',async({page})=>{
 await enter(page,'verify');await page.locator('#verify-book').click();await expect(page.locator('#verify-sources a')).not.toHaveCount(0);
 for(const b of await page.locator('[data-claim]').all()){const text=await b.locator('p').textContent();const item=claims.find(c=>c.claim===text);if(!item.correct)await b.click();}
 await expect(page.locator('.claim-fixed')).toHaveCount(3);await page.locator('#verify-finish').click();await expect(page.locator('.arcade-result')).toContainText('tìm đủ 3');
});
test('hotseat provides aids and completes 15 increasingly difficult questions',async({page})=>{
 await enter(page,'hotseat');await page.locator('#help-fifty').click();await expect(page.locator('.eliminated')).toHaveCount(2);await page.locator('#help-audience').click();await expect(page.locator('#hotseat-aid')).toContainText('không phải bình chọn thật');await page.locator('#help-book').click();await expect(page.locator('#hotseat-timer')).toContainText('Tạm dừng');await page.locator('#resume-hotseat').click();await expect(page.locator('#help-book')).toBeDisabled();
 for(let n=0;n<15;n++){const text=await page.locator('.hotseat-question').textContent();const q=questions.find(q=>q.question===text);await page.locator(`[data-choice="${q.correct}"]`).click();await page.locator('#hotseat-next').click();}
 await expect(page.locator('.arcade-final-score')).toContainText('1500');await expect(page.locator('.arcade-result')).toContainText('đủ 15');
});
test('hotseat timeout ends the round and five correct answers secure 500 points',async({page})=>{
 await page.clock.install();await enter(page,'hotseat');await page.clock.runFor(30500);await expect(page.locator('#arcade-feedback')).toContainText('Hết thời gian');await page.locator('#hotseat-next').click();await expect(page.locator('.arcade-result')).toContainText('Hết thời gian');await page.locator('#arcade-replay').click();await page.locator('#hotseat-time').selectOption('0');await page.locator('#arcade-start').click();
 for(let n=0;n<5;n++){const text=await page.locator('.hotseat-question').textContent();const q=questions.find(q=>q.question===text);await page.locator(`[data-choice="${q.correct}"]`).click();await page.locator('#hotseat-next').click();}
 const text=await page.locator('.hotseat-question').textContent();const q=questions.find(q=>q.question===text);await page.locator(`[data-choice="${(q.correct+1)%4}"]`).click();await page.locator('#hotseat-next').click();await expect(page.locator('.arcade-final-score')).toContainText('500');
});
test('all four games fit mobile and can start without script errors',async({page})=>{
 await page.setViewportSize({width:390,height:844});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const mode of ['decode','mindmap','verify','hotseat']){await enter(page,mode);expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),mode).toBeTruthy();}
 expect(errors).toEqual([]);
});
