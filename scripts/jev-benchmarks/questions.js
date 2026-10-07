// Browse frozen public records. Only the selected subset is downloaded.
const QM = __QUESTIONS_MANIFEST__;
const questionCache = new Map();
let questionRequest = 0;
let questionRows = [], questionMatches = [], questionPage = 0, questionPayload;
let activeQuestionBench = 'jevbench', activeQuestionSubset = '', activeQuestionId = '';
const questionSize = 20;
const pretty = value => typeof value === 'string' ? value : JSON.stringify(value, null, 2);
function questionUrl(id = '') {
  return '#questions/' + [activeQuestionBench, activeQuestionSubset, id].map(encodeURIComponent).join('/');
}
function questionFields(raw) {
  if (activeQuestionBench === 'nimble') return {id:raw.id, state:raw.input.state, question:raw.input.questions, gold:raw.reference};
  if (activeQuestionBench === 'jevals') {
    const task = questionPayload.task;
    let target = raw.target;
    if (task.primitive === 'choice' && Number.isInteger(target)) target = {index:target, label:task.options[target]};
    return {id:raw.item_id, state:raw.state, question:Object.fromEntries(Object.entries(task).filter(([key]) => ["primitive","instructions","options","criteria","scale","min","max","labels"].includes(key))), gold:target};
  }
  return {id:raw.id, state:raw.state, question:raw.question, gold:raw.expected};
}
function showQuestion(id, scroll = false) {
  const raw = questionRows.find(row => questionFields(row).id === id);
  if (!raw) return;
  const row = questionFields(raw);
  activeQuestionId = id;
  history.replaceState(null, '', questionUrl(id));
  $('question-detail').innerHTML = `<div class="row"><h3>原题全文 · ${esc(id)}</h3><a href="${esc(questionUrl(id))}">本题直达链接 ↗</a></div><p class="muted">下方保留原始语言与字段，不用摘要替代完整题面。</p><h4>输入 / State</h4><pre>${esc(pretty(row.state))}</pre><h4>问题、选项与判断标准 / Question</h4><pre>${esc(pretty(row.question))}</pre><details><summary>查看答案 / Gold</summary><pre>${esc(pretty(row.gold))}</pre></details>${activeQuestionBench === 'jevals' ? `<details><summary>子集元数据 / Task metadata</summary><pre>${esc(JSON.stringify(questionPayload.task,null,2))}</pre></details>` : ''}<details><summary>完整原始记录 / Raw JSON</summary><pre>${esc(JSON.stringify(raw,null,2))}</pre></details><button id="question-copy">复制原始 JSON</button>`;
  $('question-copy').onclick = async () => {
    try { await navigator.clipboard.writeText(JSON.stringify(raw,null,2)); $('question-copy').textContent = '已复制'; }
    catch { $('question-copy').textContent = '复制不可用，请展开 Raw JSON 手动复制'; }
  };
  document.querySelectorAll('[data-question-id]').forEach(button => button.closest('tr').classList.toggle('selected-question', button.dataset.questionId === id));
  if (scroll) $('question-detail').scrollIntoView({block:'start',behavior:'smooth'});
}
function renderQuestionRows() {
  const start = questionPage * questionSize;
  const rows = questionMatches.slice(start, start + questionSize);
  $('question-count').textContent = `${questionMatches.length.toLocaleString()} / ${questionRows.length.toLocaleString()} 题 · 第 ${questionPage+1} / ${Math.max(1,Math.ceil(questionMatches.length/questionSize))} 页`;
  $('question-prev').disabled = questionPage === 0;
  $('question-next').disabled = start + questionSize >= questionMatches.length;
  $('question-table').innerHTML = rows.map(raw => {
    const row = questionFields(raw);
    const state = pretty(row.state);
    const question = row.question.instructions || pretty(row.question);
    return `<tr class="${row.id === activeQuestionId ? 'selected-question' : ''}"><td><button data-question-id="${esc(row.id)}">${esc(row.id)}<br>展开全文 →</button></td><td><div class="question-preview">${esc(state.slice(0,350))}${state.length>350?'…':''}</div></td><td><div class="question-preview">${esc(question.slice(0,180))}${question.length>180?'…':''}</div></td><td><details><summary>答案</summary><pre>${esc(pretty(row.gold))}</pre></details></td></tr>`;
  }).join('') || '<tr><td colspan="4">没有匹配题目。请修改搜索词。</td></tr>';
  document.querySelectorAll('[data-question-id]').forEach(button => button.onclick = () => showQuestion(button.dataset.questionId,true));
}
async function openQuestions(bench = 'jevbench', subset = '', item = '') {
  const request = ++questionRequest;
  activeQuestionBench = bench;
  activeQuestionId = '';
  go('questions');
  $('questions').scrollIntoView({block:'start'});
  $('question-bench').value = bench;
  $('question-detail').innerHTML = '';
  $('question-table').innerHTML = '';
  $('question-search').value = '';
  $('question-search').disabled = true;
  $('question-prev').disabled = true;
  $('question-next').disabled = true;
  $('question-download').hidden = true;
  const meta = QM.benchmarks.find(b => b.id === bench);
  if (!meta) {
    const catalog = D.catalog.find(c => c.id === bench);
    $('question-subset').innerHTML = '<option>尚未接入</option>';
    $('question-subset').disabled = true;
    $('question-meta').innerHTML = `<b>这套评测的原题尚未接入本浏览器。</b>已有榜单不代表已有题库，也不表示上游没有公开数据。${catalog ? `<a href="${esc(S[catalog.source].url)}" target="_blank" rel="noopener">打开已核对来源 ↗</a>` : ''}`;
    $('question-count').textContent = '已接入：JevBench、Jevals、Nimble、Eikos。';
    history.replaceState(null,'','#questions/'+encodeURIComponent(bench));
    return;
  }
  const selectedSubset = meta.subsets.find(s => s.id === subset) || meta.subsets[0];
  activeQuestionSubset = selectedSubset.id;
  $('question-subset').disabled = false;
  $('question-subset').innerHTML = meta.subsets.map(s => `<option value="${esc(s.id)}">${esc(s.id)} · ${s.count.toLocaleString()}题</option>`).join('');
  $('question-subset').value = selectedSubset.id;
  $('question-meta').innerHTML = `<b>${esc(meta.name)} · ${meta.count.toLocaleString()}题 / ${meta.subsets.length}子集</b><p>${esc(meta.note)}</p><a href="${esc(meta.source)}" target="_blank" rel="noopener">固定版本与来源 ↗</a> · 接入日期 ${esc(QM.updated)}`;
  $('question-count').textContent = '正在加载原题…';
  history.replaceState(null,'',questionUrl(item));
  const path = 'jev-benchmark-data/questions/'+selectedSubset.file;
  try {
    let payload = questionCache.get(path);
    if (!payload) {
      const response = await fetch(path);
      if (!response.ok) throw new Error('HTTP '+response.status);
      payload = await response.json();
      questionCache.set(path,payload);
    }
    if (request !== questionRequest) return;
    questionPayload = payload;
    questionRows = payload.rows;
    questionMatches = questionRows;
    const index = questionRows.findIndex(raw => questionFields(raw).id === item);
    questionPage = index < 0 ? 0 : Math.floor(index/questionSize);
    $('question-search').disabled = false;
    $('question-download').hidden = false;
    $('question-download').href = path;
    renderQuestionRows();
    showQuestion(index < 0 ? questionFields(questionRows[0]).id : item);
  } catch(error) {
    if (request !== questionRequest) return;
    $('question-count').textContent = '加载失败：'+error.message+'。可重新选择子集重试。';
  }
}
$('question-bench').innerHTML = QM.benchmarks.map(b=>`<option value="${b.id}">${esc(b.name)} · ${b.count.toLocaleString()}题</option>`).join('') + '<optgroup label="其他评测 · 尚未接入原题">'+D.catalog.filter(c=>!QM.benchmarks.some(b=>b.id===c.id)).map(c=>`<option value="${esc(c.id)}">${esc(c.name)} · 未接入</option>`).join('')+'</optgroup>';
$('question-bench').onchange = () => openQuestions($('question-bench').value);
$('question-subset').onchange = () => openQuestions(activeQuestionBench,$('question-subset').value);
$('question-search').oninput = () => {
  const query = $('question-search').value.toLowerCase();
  questionMatches = questionRows.filter(raw => JSON.stringify(raw).toLowerCase().includes(query));
  questionPage=0;
  renderQuestionRows();
  if (questionMatches.length) showQuestion(questionFields(questionMatches[0]).id);
  else $('question-detail').innerHTML='';
};
$('question-prev').onclick = () => {questionPage--;renderQuestionRows();showQuestion(questionFields(questionMatches[questionPage*questionSize]).id);};
$('question-next').onclick = () => {questionPage++;renderQuestionRows();showQuestion(questionFields(questionMatches[questionPage*questionSize]).id);};
