import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import {fileURLToPath} from 'node:url';import {build} from 'esbuild';import {chromium} from 'playwright';
const dir=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(dir,'../..'),assets=path.join(root,'jev-atlas-assets');
fs.mkdirSync(assets,{recursive:true});
const pos=process.argv.indexOf('--import');
if(pos!==-1){
 const source=path.resolve(process.argv[pos+1]),raw=fs.readFileSync(source,'utf8');
 const match=raw.match(/<script>window\.DOCS=([\s\S]*?);<\/script>/);if(!match)throw Error('Expected standalone Jev Atlas export');
 const docs=JSON.parse(match[1]);fs.writeFileSync(path.join(dir,'content.json'),JSON.stringify(docs));
 let css=raw.match(/<style>([\s\S]*?)<\/style>/)[1];
 css=css.replace(/url\(data:font\/([^;]+);base64,([^)]+)\)/g,(_,ext,b64)=>{const buf=Buffer.from(b64,'base64'),name='font-'+crypto.createHash('sha256').update(buf).digest('hex').slice(0,14)+'.'+ext;fs.writeFileSync(path.join(assets,name),buf);return 'url(./'+name+')'});
 fs.writeFileSync(path.join(dir,'style.css'),css);
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||'/root/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome',args:['--no-sandbox']});const p=await browser.newPage();await p.goto('file://'+source);await p.waitForSelector('.model-card');
 const shell=await p.evaluate(()=>{document.querySelectorAll('script').forEach(x=>x.remove());document.querySelector('#progress').style.width='0%';return '<!doctype html>'+document.documentElement.outerHTML;});await browser.close();
 fs.writeFileSync(path.join(dir,'shell.html'),shell.replace(/<style>[\s\S]*?<\/style>/,'<link rel="stylesheet" href="jev-atlas-assets/style.css">'));
}
const docs=JSON.parse(fs.readFileSync(path.join(dir,'content.json'),'utf8'));fs.mkdirSync(path.join(assets,'docs'),{recursive:true});
for(const d of docs)fs.writeFileSync(path.join(assets,'docs',d.id+'.json'),JSON.stringify({html:d.html,text:d.text}));
fs.writeFileSync(path.join(assets,'search.json'),JSON.stringify(docs.filter(d=>d.group!=='来源').map(d=>({id:d.id,text:d.text}))));
const manifest=docs.map(({html,text,...d})=>d);
let shell=fs.readFileSync(path.join(dir,'shell.html'),'utf8');
shell=shell.replace('</body>','<script>window.DOCS='+JSON.stringify(manifest).replace(/</g,'\\u003c')+';</script><script type="module" src="jev-atlas-assets/app.js"></script><noscript><p style="padding:20px">浏览器未启用 JavaScript。可先浏览首页，或打开 <a href="https://github.com/linjh1118/BrainHao/tree/main/Topics/22_Jev/projects">Markdown 全文</a>。</p></noscript></body>');
fs.writeFileSync(path.join(root,'jev_atlas.html'),'<!-- index: Jev Atlas · 决策模型研究手册 | 2026-09-27 | 八个项目完整精读、模型结构、数据与 Benchmark，附交互教程与论文海报。 -->\n'+shell);
fs.copyFileSync(path.join(dir,'style.css'),path.join(assets,'style.css'));
await build({entryPoints:[path.join(dir,'app.js')],outdir:assets,bundle:true,splitting:true,minify:true,format:'esm',target:'es2020',chunkNames:'chunks/[name]-[hash]',legalComments:'eof'});
console.log('HTML bytes',fs.statSync(path.join(root,'jev_atlas.html')).size,'app bytes',fs.statSync(path.join(assets,'app.js')).size,'CSS bytes',fs.statSync(path.join(assets,'style.css')).size);

for(const file of fs.readdirSync(assets,{recursive:true})){const full=path.join(assets,file);if(fs.statSync(full).isFile()&&/\.(js|css)$/.test(full)){fs.writeFileSync(full,fs.readFileSync(full,'utf8').replace(/[ \t]+$/gm,''));}}
