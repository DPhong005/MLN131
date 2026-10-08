const fs = require('node:fs');
const path = require('node:path');
require('./build-pages');
const root = path.resolve(__dirname,'..');
const publicRoot = path.join(root,'public');
fs.mkdirSync(publicRoot,{recursive:true});
for (const file of ['ai-assistants.html','js/retrieval.mjs']) { const target=path.join(publicRoot,file); if(fs.existsSync(target)) fs.unlinkSync(target); }
function copy(file) { const source=path.join(root,file);const target=path.join(publicRoot,file);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(source,target); }
const routes = JSON.parse(fs.readFileSync(path.join(root,'data','routes.json'),'utf8'));
routes.forEach(route=>copy(route.file));
for (const file of ['css/site.css','js/app.js','js/state.mjs','js/arcade.mjs','assets/illustrations/society.svg','assets/illustrations/favicon.svg','assets/docs/cnxh-khoa-hoc-2021.pdf','header.html','footer.html']) copy(file);
const photoCredits = JSON.parse(fs.readFileSync(path.join(root,'data','photoCredits.json'),'utf8'));
const photoFiles = new Set(['textbook-cover.webp','hero-cutout-v2.webp', ...photoCredits.flatMap(photo=>[photo.image,photo.cutoutImage].filter(Boolean).map(file=>path.basename(file)))]);
const generatedPublic = path.join(publicRoot,'assets/illustrations/generated');
fs.mkdirSync(generatedPublic,{recursive:true});
for(const file of fs.readdirSync(generatedPublic)) if(!photoFiles.has(file)) fs.unlinkSync(path.join(generatedPublic,file));
for(const file of photoFiles) copy(`assets/illustrations/generated/${file}`);
for (const file of fs.readdirSync(path.join(root,'data'))) if(file.endsWith('.json'))copy(`data/${file}`);
console.log('Public website built. Internal files and legacy scripts are not served.');
