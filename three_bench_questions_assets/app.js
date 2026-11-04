'use strict';
const $ = (s, root=document) => root.querySelector(s);
const $$ = (s, root=document) => Array.from(root.querySelectorAll(s));
const esc = value => String(value ?? '').replace(/[&<>"']/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const json = value => JSON.stringify(value,null,2);
const num = n => Number(n).toLocaleString('en-US');
const pretty = v => v === null || v === undefined || v === '' ? '未提供' : typeof v === 'object' ? json(v) : String(v);
const prose = t => `<div class="prose">${esc(pretty(t))}</div>`;
const code = t => `<pre>${esc(typeof t==='string'?t:json(t))}</pre>`;
const kv = (k,v) => `<div class="kv"><small>${esc(k)}</small><span>${esc(pretty(v))}</span></div>`;
const displayTitle = r => {const t=r.title.replaceAll('{forecast_due_date}',r.date).replaceAll('{resolution_date}','各结算日').split('\n')[0];return t.length>280?t.slice(0,280)+'…':t;};
const safeUrl = u => {try {const x=new URL(u);return ['https:','http:'].includes(x.protocol)?x.href:'#';}catch{return '#';}};
const link = (u,text) => `<a href="${esc(safeUrl(u))}" target="_blank" rel="noopener noreferrer">${esc(text)} ↗</a>`;
const hint = s => `<div class="hint">${s}</div>`;
let catalog, active='ile';
const states={}, indexes={}, loaded={}, pending={};
const config={
 ile:{title:'ILE · 金融研究的完整工作流',description:'7 大类、86 道任务。查看信息截止时间、原始任务要求、参考真值和逐项评分标准；数据湖检索服务与公开题包分开标注。',stats:()=>[[86,'金融研究任务'],[1472,'评分标准'],[7,'任务大类']],group:'题库',category:'任务大类'},
 futurex:{title:'FutureX · 对真实事件作出预测',description:'历史题与当期题分开浏览。保留原始选项、标准答案、数值容差及题目级别；在线题没有公开答案时明确标记。',stats:()=>[[catalog.summary.futurex.past,'历史已结算'],[catalog.summary.futurex.online,'当期在线'],[4,'难度级别']],group:'题库范围',category:'难度级别'},
 forecastbench:{title:'ForecastBench · 概率预测与多期限结算',description:'默认最新 LLM 批次；可切换全部历史与 Human 批次。相同来源与 ID 可能跨批次出现；一题可对应多个预测期限。',stats:()=>[[catalog.summary.forecastbench.latest.questions,'最新一轮题目'],[catalog.summary.forecastbench.latest.outputs,'最新概率输出'],[catalog.summary.forecastbench.rounds,'全部公开批次']],group:'评测批次',category:'题目来源'}
};
function options(values, allLabel='全部'){return `<option value="">${allLabel}</option>`+values.map(x=>`<option value="${esc(x)}">${esc(x)}</option>`).join('');}
async function fetchJson(path){const r=await fetch(path);if(!r.ok)throw Error(`文件读取失败 (${r.status})：${path}`);return r.json();}
async function ensureIndex(b){if(indexes[b])return indexes[b];if(!pending[b])pending[b]=fetchJson(`three_bench_questions_assets/data/${b}-index.json`).then(rows=>{indexes[b]=rows;rows.forEach(r=>r.searchText=[r.title,r.subtitle,r.id,r.question,r.category,r.subcategory].join(' ').toLowerCase());return rows;}).catch(e=>{delete pending[b];throw e;});return pending[b];}
function makePanel(b){
 const c=config[b],rows=indexes[b],p=$(`#panel-${b}`);
 const groups=[...new Set(rows.map(x=>x.group))];if(b==='forecastbench')groups.sort().reverse();
 states[b]={search:'',group:b==='forecastbench'?catalog.summary.forecastbench.latest.group:'',category:'',subcategory:'',status:'',page:0,key:null,view:'question',horizon:null,filtered:[],ticket:0};
 p.innerHTML=`<div class="bench-intro"><div><h2>${c.title}</h2><p>${c.description}</p></div><div class="mini-stats">${c.stats().map(([n,t])=>`<div><b>${num(n)}</b><small>${t}</small></div>`).join('')}</div></div>
 <div class="toolbar"><input type="search" data-filter="search" aria-label="搜索 ${b} 题目" placeholder="搜索题目、公司、代码或关键词…"><select data-filter="status" aria-label="答案或结算状态">${options([...new Set(rows.map(x=>x.status))],'全部答案状态')}</select><button class="reset">清除筛选</button><button class="export">导出筛选目录</button></div>
 <div class="explorer"><aside class="list-side"><div class="directory"><div class="directory-head"><b>分类目录</b><span>${num(rows.length)} 题</span></div><div class="category-tree" aria-label="分层题目目录"></div></div><div class="list-meta"><span class="count"></span><span>每页 30 题</span></div><div class="question-list" aria-label="题目列表"></div><div class="pagination"><button class="prev">← 上一页</button><span class="pagecount"></span><button class="next">下一页 →</button></div></aside><article class="detail" aria-label="题目详情"></article></div>`;
 renderTree(b);
 $$('[data-filter]',p).forEach(el=>el.addEventListener(el.tagName==='INPUT'?'input':'change',()=>{states[b][el.dataset.filter]=el.value;states[b].page=0;applyFilters(b);}));
 $('.reset',p).onclick=()=>{for(const field of ['search','group','category','subcategory','status']){states[b][field]=field==='group'&&b==='forecastbench'?catalog.summary.forecastbench.latest.group:'';const input=$(`[data-filter=${field}]`,p);if(input)input.value=states[b][field];}states[b].page=0;applyFilters(b);};
 $('.export',p).onclick=()=>download(`${b}-filtered-catalog.json`,states[b].filtered.map(({searchText,...r})=>r));
 $('.prev',p).onclick=()=>{states[b].page--;renderList(b);};$('.next',p).onclick=()=>{states[b].page++;renderList(b);};
 $('.question-list',p).onclick=e=>{const card=e.target.closest('[data-key]');if(card)selectQuestion(b,card.dataset.key);};
 applyFilters(b);
 states[b].page=Math.max(0,Math.floor(states[b].filtered.findIndex(r=>r.key===states[b].key)/30));renderList(b);
}
function treeKeys(b,r){return b==='ile'?{parent:r.category,child:r.subcategory}:{parent:r.group,child:r.category};}
function renderTree(b){
 const p=$(`#panel-${b}`),rows=indexes[b],tree=$('.category-tree',p),groups=new Map();
 rows.forEach(r=>{const {parent,child}=treeKeys(b,r);if(!groups.has(parent))groups.set(parent,new Map());const children=groups.get(parent);if(!children.has(child))children.set(child,[]);children.get(child).push(r);});
 let entries=[...groups.entries()];
 if(b==='ile'){
  const order=['选股与研究规划','信息提取与重建','经营与财务预测','估值与投资决策','事件与持仓跟踪','综合研究','市场预测'];
  entries.sort((a,z)=>order.indexOf(a[0])-order.indexOf(z[0]));
 }
 if(b==='forecastbench')entries.sort((a,z)=>z[0].localeCompare(a[0]));
 if(b==='futurex')entries.sort((a,z)=>['历史已结算','当期在线'].indexOf(a[0])-['历史已结算','当期在线'].indexOf(z[0]));
 const current=states[b];
 tree.innerHTML=entries.map(([parent,children],i)=>{
  const all=[...children.values()].flat(),parentSelected=b==='ile'?current.category===parent&&!current.subcategory:current.group===parent&&!current.category;
  const childHtml=[...children.entries()].sort((a,z)=>a[0].localeCompare(z[0])).map(([child,items])=>{
   const selected=b==='ile'?current.category===parent&&current.subcategory===child:current.group===parent&&current.category===child;
   return `<button class="tree-node tree-child ${selected?'selected':''}" data-tree-parent="${esc(parent)}" data-tree-child="${esc(child)}"><span class="tree-label">${esc(child||'未分类')}</span><span class="tree-count">${num(items.length)}</span></button>`;
  }).join('');
  return `<details class="tree-group" ${parentSelected||(!current.group&&!current.category&&!current.subcategory&&i===0)?'open':''}><summary><span>${esc(parent)}</span><small>${num(all.length)}</small></summary><button class="tree-node tree-all ${parentSelected?'selected':''}" data-tree-parent="${esc(parent)}"><span class="tree-label">全部题目</span><span class="tree-count">${num(all.length)}</span></button>${childHtml}</details>`;
 }).join('');
 tree.onclick=e=>{const node=e.target.closest('[data-tree-parent]');if(!node)return;const parent=node.dataset.treeParent,child=node.dataset.treeChild||'';if(b==='ile'){current.group='';current.category=parent;current.subcategory=child;}else{current.group=parent;current.category=child;current.subcategory='';}current.page=0;const details=node.closest('details');if(details)details.open=true;applyFilters(b);};
}
function syncTreeSelection(b){
 const p=$(`#panel-${b}`),tree=$('.category-tree',p),s=states[b];
 $$('.tree-node',tree).forEach(node=>{const parent=node.dataset.treeParent,child=node.dataset.treeChild||'';const selected=b==='ile'?(s.category===parent&&(child?s.subcategory===child:!s.subcategory)):(s.group===parent&&(child?s.category===child:!s.category));node.classList.toggle('selected',selected);});
}
function applyFilters(b){
 const s=states[b],terms=s.search.trim().toLowerCase().split(/\s+/).filter(Boolean);
 s.filtered=indexes[b].filter(r=>(!s.group||r.group===s.group)&&(!s.category||r.category===s.category)&&(!s.subcategory||r.subcategory===s.subcategory)&&(!s.status||r.status===s.status)&&terms.every(t=>r.searchText.includes(t)));
 if(!s.filtered.some(r=>r.key===s.key)){s.key=s.filtered.find(r=>b==='ile'&&r.id==='O01')?.key||s.filtered[0]?.key||null;s.horizon=null;}
 syncTreeSelection(b);renderList(b);renderDetail(b);
}
function renderList(b){
 const p=$(`#panel-${b}`),s=states[b],max=Math.max(1,Math.ceil(s.filtered.length/30));s.page=Math.max(0,Math.min(s.page,max-1));
 $('.count',p).textContent=`${num(s.filtered.length)} / ${num(indexes[b].length)} 条记录`;
 $('.pagecount',p).textContent=`${s.page+1} / ${max}`;$('.prev',p).disabled=s.page===0;$('.next',p).disabled=s.page>=max-1;
 $('.question-list',p).innerHTML=s.filtered.slice(s.page*30,s.page*30+30).map(r=>`<button class="qcard ${r.key===s.key?'selected':''}" data-key="${esc(r.key)}" aria-label="查看 ${esc(r.id)} ${esc(r.title.slice(0,70))}" aria-pressed="${r.key===s.key}"><div class="tags"><span>${esc(r.category)}</span><span>${esc(r.status)}</span></div><h3>${esc(displayTitle(r))}</h3><small>${esc(b==='ile'?r.id+' · '+r.subtitle:r.date.slice(0,10)+' · '+r.group)}</small></button>`).join('')||'<div class="empty">没有匹配题目。试试其他关键词或重置筛选。</div>';
 $('.question-list',p).scrollTop=0;
}
function updateHash(b,key){history.replaceState(null,'',`#${new URLSearchParams({bench:b,...(key?{key}:{})})}`);}
function selectQuestion(b,key){states[b].key=key;states[b].horizon=null;renderList(b);renderDetail(b);updateHash(b,key);}
async function rawFor(r){if(!loaded[r.file])loaded[r.file]=fetchJson('three_bench_questions_assets/data/'+r.file).catch(e=>{delete loaded[r.file];throw e;});const all=await loaded[r.file];return r.index===null?all:all[r.index];}
async function renderDetail(b){
 const s=states[b],d=$(`#panel-${b} .detail`),ticket=++s.ticket,r=s.filtered.find(x=>x.key===s.key);
 if(!r){d.innerHTML='<div class="empty">左侧筛选结果为空。</div>';return;}
 d.innerHTML='<div class="empty">正在读取原题…</div>';
 try{
 const raw=await rawFor(r);if(ticket!==s.ticket)return;
 d.innerHTML=`<div class="detail-head"><div class="kicker">${esc(b==='ile'?'INVESTOR’S LAST EXAM':b.toUpperCase())} / ${esc(r.id)}</div><h2>${esc(displayTitle(r))}</h2><div class="detail-tags"><span class="tag">${esc(r.category)}</span><span class="tag">${esc(r.group)}</span><span class="tag">${esc(r.status)}</span>${r.rubric_count?`<span class="tag">${r.rubric_count} 条评分标准</span>`:''}${r.outputs?`<span class="tag">${r.outputs} 项概率输出</span>`:''}</div></div>
 <div class="detail-actions">${link(r.source,'官方原始文件')}<button class="download">下载本题 JSON</button><button class="copy">复制本题链接</button></div><div class="status-line" aria-live="polite"></div>
 <nav class="detail-tabs" role="tablist" aria-label="题目内容"><button role="tab" data-view="question">题面与任务</button><button role="tab" data-view="answer">答案与结算</button><button role="tab" data-view="scoring">评分与格式</button><button role="tab" data-view="raw">原始字段</button></nav>
 ${['question','answer','scoring','raw'].map(v=>`<section class="content" role="tabpanel" data-content="${v}" hidden></section>`).join('')}`;
 $('.download',d).onclick=()=>download(`${b}-${r.id.replace(/[^a-zA-Z0-9_-]/g,'_')}.json`,raw);
 $('.copy',d).onclick=async()=>{const url=location.href.split('#')[0]+'#'+new URLSearchParams({bench:b,key:r.key});try{await navigator.clipboard.writeText(url);$('.status-line',d).textContent='已复制，可直接打开这道题。';}catch{$('.status-line',d).innerHTML=`本题链接：<a href="${esc(url)}">${esc(url)}</a>`;}};
 $$('[data-view]',d).forEach(btn=>btn.onclick=()=>{s.view=btn.dataset.view;showDetailView(b,r,raw);});
 showDetailView(b,r,raw);d.scrollTop=0;
 }catch(e){if(ticket===s.ticket)d.innerHTML=hint(esc(e.message));}
}
function showDetailView(b,r,raw){
 const s=states[b],d=$(`#panel-${b} .detail`);
 $$('[data-view]',d).forEach(btn=>btn.setAttribute('aria-selected',String(btn.dataset.view===s.view)));
 $$('[data-content]',d).forEach(panel=>panel.hidden=panel.dataset.content!==s.view);
 const panel=$(`[data-content=${s.view}]`,d);
 if(s.view==='raw')panel.innerHTML=hint('下方保留官方原始字段；“下载本题 JSON”可获得完整内容。')+code(raw);
 else if(b==='ile')panel.innerHTML=ileView(s.view,raw,r);
 else if(b==='futurex')panel.innerHTML=futurexView(s.view,raw,r);
 else panel.innerHTML=forecastView(s.view,raw,r,s);
 const horizon=$('.horizon-select',panel);if(horizon)horizon.onchange=()=>{s.horizon=horizon.value;showDetailView(b,r,raw);};
}
function details(title,value){return `<details><summary>${esc(title)}</summary>${code(value)}</details>`;}
function ileView(view,q,r){
 if(view==='question')return hint(`<b>这道题看什么：</b>${esc(r.subcategory)}。必须遵守题面规定的信息截止时间；评分材料含参考真值，正式作答时不能暴露给模型。`)+`<div class="kvgrid">${kv('公司 / 证券代码',q.company+' / '+q.ticker)}${kv('信息截止时间',q.cutoff)}${kv('官方任务分类',q.category_id+' · '+q.category_name)}${kv('提交方式',q.submission_mode)}</div><h3>完整题面 · 官方原文</h3>${prose(q.question)}<h3>可用工具</h3><div class="tool-list">${q.tools.map(t=>`<span class="tag">${esc(t.function?.name||t.name||'tool')}</span>`).join('')}</div>${details('查看 Solver 系统指令',q.solver_system_prompt)}`;
 if(view==='answer'){
 const truth=q.ground_truth||{},targets=truth.targets||[];
 if(truth.kind)return marketAnswer(truth);
 return hint('<b>公开参考真值与证据：</b>这些是官方评测端的答案依据，不是本次运行模型的回答。个别任务没有单一标准答案，应结合评分细则阅读。')+`<div class="kvgrid">${kv('真值模式',truth.truth_mode)}${kv('参考目标数',targets.length)}</div>`+targets.map((t,i)=>`<details ${i===0?'open':''}><summary>${i+1}. ${esc(t.metric||t.truth_id||'参考目标')} <span class="rubric-meta">${esc(pretty(t.value))} ${esc(t.unit||'')}</span></summary><div class="kvgrid">${kv('实体 / 期间',(t.entity||'')+' / '+(t.period||''))}${kv('公开时间',t.public_available_at)}${kv('证据数据集',t.dataset)}${kv('文档定位',t.document_version_id+' · '+(t.locator||''))}</div>${t.excerpt?'<h3>证据摘录</h3>'+prose(t.excerpt):''}${t.derivation?'<h3>推导过程</h3>'+code(t.derivation):''}</details>`).join('')+details('完整参考真值对象',truth);
 }
 return hint(`<b>评分颗粒度：</b>本题共 ${q.rubrics.length} 条标准，总分上限 ${q.max_score}。机械规则与语义判断分别保留原始类型和权重。`)+q.rubrics.map((x,i)=>`<details ${i===0?'open':''}><summary>${i+1}. ${esc(x.title||x.rubric_id)} <span class="rubric-meta">${esc(x.type)} · ${Number(x.max_score||0).toFixed(2)} 分</span></summary><h3>评判标准</h3>${prose(x.criterion)}<h3>通过条件</h3>${prose(x.pass_condition||(x.score_formula?'连续评分，使用下方公式。':'官方未单独提供'))}<div class="kvgrid">${kv('对应输出字段',x.primary_output_path)}${kv('权重 / 精确分值',x.weight+' / '+x.max_score_exact)}</div>${x.deterministic?details('机械检验参数',x.deterministic):''}${x.judge?details('语义评分依据',x.judge):''}${x.future_truth?details('未来真值依据',x.future_truth):''}${x.score_formula?'<h3>评分公式</h3>'+code(x.score_formula):''}${x.scoring_parameters?details('完整评分参数',x.scoring_parameters):''}</details>`).join('')+details('完整提交格式（Submission schema）',q.submission_schema)+details('评估政策',q.evaluation_policy)+details('Judge 系统指令',q.judge_system_prompt);
}
function marketAnswer(t){
 const values=t.kind==='point'?`<div class="kvgrid">${kv('基准日收盘价 / anchor_close',t.anchor_close)}${kv('目标日实际收盘价 / actual_close',t.actual_close)}${kv('误差尺度（百分点）',t.error_scale_pp)}${kv('历史日波动率',t.historical_daily_sigma)}</div>`:`<h3>实际指标 · ${esc(t.metric)}</h3>${prose(t.target_definition)}<div class="scrolltable"><table><thead><tr><th>证券 / 组合</th><th>实际指标值（官方原单位）</th></tr></thead><tbody>${Object.entries(t.realized_metrics||{}).map(([k,v])=>`<tr><td>${esc(k)}</td><td>${esc(v)}</td></tr>`).join('')}</tbody></table></div>`;
 return hint('<b>市场类任务的未来真实结果：</b>价格、回报或波动率用于事后评分；不是模型预测，也不是可提前使用的信息。')+`<div class="kvgrid">${kv('任务形式',t.kind)}${kv('基准日期',t.anchor_date)}${kv('目标日期',t.target_dates)}</div>`+values+`<h3>损失函数</h3>${code(t.loss_formula)}<h3>得分函数</h3>${code(t.score_formula)}`+details('完整参考真值与校准参数',t);
}
function futurexView(view,q,r){
 if(view==='question')return hint('<b>阅读顺序：</b>先看题目中的事件与选项，再看要求的最终输出格式。Level 为官方级别，题面中的所有限定条件原样保留。')+`<div class="kvgrid">${kv('级别',r.category)}${kv('事件结束时间（官方字段）',q.end_time)}${kv('题库',r.group)}${kv('题目 ID',q.id)}</div><h3>完整题面与输出要求</h3>${prose(q.prompt)}`;
 if(view==='answer')return q.ground_truth?hint('<b>官方历史答案：</b>以下为 Past 数据集的 ground_truth，不是模型预测。')+`<h3>标准答案</h3>${code(q.ground_truth)}<div class="kvgrid">${kv('数值容差 / std',q.std||'未提供；不可视为 0')}</div><h3>容差说明 / std_reason</h3>${prose(q.std_reason||'官方未提供')}`:hint('<b>本快照没有公开答案。</b>在线题即使事件日期已过，也不会据此自动填入答案。待官方公开后可更新快照。');
 return hint('本页保留题面规定的作答格式。不同题型的评分规则以官方 grader 为准；未运行模型、未生成准确率。')+`<h3>题面中的输出与评分要求</h3>${prose(q.prompt.slice(Math.max(0,q.prompt.indexOf('IMPORTANT:'))))}<h3>评分材料</h3><div class="kvgrid">${kv('ground_truth',q.ground_truth||'未公开')}${kv('std',q.std||'未提供')}</div>${link('https://github.com/Futurex-ai/Futurex-Eval','官方评测实现')}`;
}
function forecastView(view,item,r,s){
 const q=item.question,dates=Array.isArray(q.resolution_dates)?q.resolution_dates:[],chosen=dates.includes(s.horizon)?s.horizon:dates[0];
 const fullQuestion=q.question.replaceAll('{forecast_due_date}',item.forecast_due_date).replaceAll('{resolution_date}',chosen||'{resolution_date}');
 if(view==='question')return hint(`<b>预测对象：</b>对事件结果给出概率${dates.length?`；本题包含 ${dates.length} 个结算期限，需要分别输出概率`:'，不是直接填写 Yes / No'}。下方题面已代入预测日期${dates.length?'和所选结算日期':''}。`)+`<div class="kvgrid">${kv('预测提交日期',item.forecast_due_date)}${kv('信息冻结时间',q.freeze_datetime)}${kv('来源',q.source)}${kv('冻结时观测值',q.freeze_datetime_value)}</div>${dates.length?`<label>查看预测期限 <select class="horizon-select" aria-label="预测期限">${dates.map(x=>`<option ${x===chosen?'selected':''}>${esc(x)}</option>`).join('')}</select></label>`:''}<h3>完整题面</h3>${prose(fullQuestion)}<h3>背景资料</h3>${prose(q.background||'官方未提供')}<h3>来源简介</h3>${prose(q.source_intro)}<h3>题目原始来源</h3>${(q.url?.match(/https?:\/\/[^\s]+/g)||[]).map(u=>link(u,u)).join('<br>')}`;
 if(view==='answer')return hint('<b>官方结算记录：</b>resolved_to 为结算值；仅 resolved=true 视为已结算。缺失记录、未结算与数值 0 严格区分。')+`<div class="kvgrid">${kv('本快照状态',r.status)}${kv('预计输出数',r.outputs)}</div>`+(item.resolutions.length?`<div class="scrolltable"><table><thead><tr><th>结算日期</th><th>方向</th><th>已结算</th><th>结果 / 原字段</th></tr></thead><tbody>${item.resolutions.map(x=>`<tr><td>${esc(x.resolution_date)}</td><td>${esc(pretty(x.direction))}</td><td>${x.resolved===true?'是':'否'}</td><td>${esc(x.resolved===true?pretty(x.resolved_to):'未结算（原值：'+pretty(x.resolved_to)+'）')}</td></tr>`).join('')}</tbody></table></div>`:hint('该批次的公开数据中暂无本题结算记录。'))+`<h3>结算条件</h3>${prose(q.resolution_criteria)}${q.market_info_resolution_criteria&&q.market_info_resolution_criteria!=='N/A'?'<h3>市场详细结算条件</h3>'+prose(q.market_info_resolution_criteria):''}`;
 return hint('<b>作答形式：</b>预测每个目标事件发生的概率。公开基准以 Brier 类概率评分为基础，榜单聚合与显著性比较需使用官方实现；本页不把题数当作概率输出数。')+`<div class="kvgrid">${kv('预测日期',item.forecast_due_date)}${kv('结算期限',dates.length?dates:'由市场结算条件决定')}${kv('冻结值含义',q.freeze_datetime_value_explanation)}${kv('信息冻结时刻',q.freeze_datetime)}</div><h3>二元事件的单项 Brier 分数</h3>${code('(预测概率 p − 实际结果 y)²；越低越好。\n此公式说明单项评分，不代替官方榜单的聚合规则。')}<h3>官方规则与实现</h3>${link('https://github.com/forecastingresearch/forecastbench','ForecastBench 评测仓库')}`;
}
function download(name,data){const a=document.createElement('a'),u=URL.createObjectURL(new Blob([json(data)],{type:'application/json'}));a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
function renderScope(){const s=catalog.summary,m=catalog.snapshot;
 $('#panel-scope').innerHTML=`<div class="scopegrid"><section class="scope-card"><p class="eyebrow">DATA COVERAGE</p><h2>看板覆盖到哪一层？</h2><ul><li><b>ILE：</b>全部 86 题、1,472 条评分标准、参考真值、工具与提交格式。</li><li><b>FutureX：</b>${num(s.futurex.past)} 道 Past 历史题 + ${num(s.futurex.online)} 道 Online 当期题。</li><li><b>ForecastBench：</b>${s.forecastbench.rounds} 个日期批次（${s.forecastbench.llm_rounds} 个 LLM 批次），${num(s.forecastbench.records)} 条记录；按来源 + ID 去重为 ${num(s.forecastbench.unique_source_id)} 个对象。</li></ul><p>ForecastBench 最新 LLM 批次为 ${s.forecastbench.latest.date}：500 题、1,496 项概率输出。全部批次保留版本差异；不将重复记录计成独立事件。</p></section>
 <section class="scope-card"><p class="eyebrow">ACCESS BOUNDARY</p><h2>ILE 题包与远程数据湖</h2><span class="badge">公开题包已完整下载</span><p>官网发布的是可下载题包与评测程序；底层金融资料库仍为需认证的远程服务。邀请码不等同于 API Key，也不等同于已下载数据库。</p><p>本次没有激活邀请码、消耗授权额度或下载整个数据湖。页面展示的证据摘录来自公开题包，不能代表完整底层文档。真实模型评测另需完成 Portal 账户与 API 配置。</p>${link('https://github.com/Prophetlab/Investor-Last-Exam/blob/'+m.sources.find(x=>x.name==='ile').revision+'/QUICKSTART.md','ILE 官方接入说明')}</section>
 <section class="scope-card wide"><p class="eyebrow">REPRODUCIBLE SNAPSHOT</p><h2>固定版本与下载校验</h2><p>下载时间：${esc(m.downloaded_at)}。页面随附公开题目数据，按题或按批次读取原文。固定快照不会随上游变化自动改写。</p><div class="scrolltable"><table><thead><tr><th>资料</th><th>固定提交</th><th>已下载文件大小（字节）</th><th>官方来源</th></tr></thead><tbody>${m.sources.map(x=>`<tr><td>${esc(x.name)}</td><td><code>${esc(x.revision)}</code></td><td>${num(x.bytes)}</td><td>${link(x.url,'固定版本文件')}</td></tr>`).join('')}</tbody></table></div>${details('SHA-256 完整校验清单',m.sources.map(({name,bytes,sha256})=>({name,bytes,sha256})))}<a href="three_bench_questions_assets/data/download_manifest.json" download>下载来源与校验清单 ↓</a></section>
 <section class="scope-card wide"><h2>直接打开历史批次</h2><p>点击切换到 ForecastBench，并保留其他基准的筛选与阅读位置。</p><div class="date-row">${catalog.rounds.slice().reverse().map(x=>`<button data-round="${esc(x.group)}">${esc(x.group)} · ${num(x.questions)} 题</button>`).join('')}</div></section></div>`;
 $$('[data-round]').forEach(btn=>btn.onclick=async()=>{await switchBench('forecastbench');const s=states.forecastbench;s.group=btn.dataset.round;s.search='';s.category='';s.subcategory='';s.status='';s.page=0;$('#panel-forecastbench [data-filter=search]').value='';$('#panel-forecastbench [data-filter=status]').value='';applyFilters('forecastbench');});
}
async function switchBench(b){
 active=b;$$('.bench-tabs [role=tab]').forEach(x=>{x.setAttribute('aria-selected',String(x.dataset.bench===b));x.tabIndex=x.dataset.bench===b?0:-1;});$$('.bench-panel').forEach(x=>x.hidden=x.id!=='panel-'+b);updateHash(b,states[b]?.key);
 if(b==='scope'){$('#notice').textContent='';return;}
 $('#notice').textContent=indexes[b]?'':'正在读取完整题目目录…';
 try{await ensureIndex(b);if(!states[b])makePanel(b);if(active===b){$('#notice').textContent='';updateHash(b,states[b]?.key);}}catch(e){$('#notice').textContent=e.message;}
}
$('#theme').onclick=()=>{const dark=document.documentElement.dataset.theme==='dark';document.documentElement.dataset.theme=dark?'light':'dark';$('#theme').textContent=dark?'☾ 深色':'☀ 浅色';$('#theme').setAttribute('aria-label',dark?'切换到深色主题':'切换到浅色主题');};
$$('.bench-tabs [role=tab]').forEach(btn=>{btn.onclick=()=>switchBench(btn.dataset.bench);btn.onkeydown=e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const all=$$('.bench-tabs [role=tab]'),i=all.indexOf(btn),j=e.key==='Home'?0:e.key==='End'?all.length-1:(i+(e.key==='ArrowRight'?1:-1)+all.length)%all.length;all[j].focus();switchBench(all[j].dataset.bench);}};});
async function init(){try{catalog=await fetchJson('three_bench_questions_assets/data/catalog.json');renderScope();const hash=new URLSearchParams(location.hash.slice(1)),b=hash.get('bench'),key=hash.get('key');await switchBench(['ile','futurex','forecastbench','scope'].includes(b)?b:'ile');if(key&&states[active]){const s=states[active],r=indexes[active].find(x=>x.key===key);if(r){s.group=active==='ile'?'':r.group;applyFilters(active);s.key=key;s.page=Math.floor(s.filtered.findIndex(x=>x.key===key)/30);renderList(active);await renderDetail(active);updateHash(active,key);}}}catch(e){$('#notice').textContent=e.message;}}
init();
