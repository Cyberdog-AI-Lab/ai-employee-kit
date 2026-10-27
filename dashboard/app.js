'use strict';

const $ = (id) => document.getElementById(id);
const groups = {overview:'仕事の全体像',inputs:'入力資料',definition:'担当・手順',outputs:'最新の成果物',interview:'ヒアリング',reference:'版・関連資料'};
const labels = {'AGENTS.md':'社員の役割と境界','CLAUDE.md':'Claude Codeへの入口','SKILL.md':'具体的な仕事の手順','interview.md':'質問と回答の記録','sample.json':'版と成果物の対応','bundle-manifest.json':'配布ファイルの一覧','definition.md':'定義と確認方法'};
let employees = [], current = null, view = 'overview', chosen = null, content = '', lines = [], pages = [], lineOffsets = [], page = 0, hit = null, searchQuery = '';
let requestVersion = 0, controller = null, catalogController = null, catalogError = '';

function node(tag, text, className) {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
}
function size(bytes) { return bytes >= 1048576 ? `${(bytes / 1048576).toFixed(1)} MB` : bytes >= 1024 ? `${(bytes / 1024).toFixed(1)} KB` : `${bytes} B`; }
function go(group, file = '', employee = current?.id || 'sales', options = {}) {
  const params=new URLSearchParams();if(file)params.set('file',file);
  if(options.mode)params.set('mode',options.mode);if(options.anchor)params.set('anchor',options.anchor);
  const hash = `#${employee}/${group}${params.size ? '?'+params : ''}`;
  if (location.hash === hash) render(); else location.hash = hash;
}
function showNotice(message) { $('notice').textContent = message; $('notice').hidden = !message; }
async function checkedFetch(url, options = {}) {
  const response = await fetch(url, {cache:'no-store', ...options});
  if (!response.ok) {
    let message = `読込に失敗しました (${response.status})`;
    try { message = (await response.json()).error || message; } catch (_) { /* HTTP status remains useful */ }
    throw new Error(message);
  }
  return response;
}

async function loadCatalog() {
  catalogController?.abort(); catalogController = new AbortController();
  $('refresh').disabled = true; $('fatal').hidden = true;
  try {
    const data = await (await checkedFetch('/api/catalog', {signal:catalogController.signal})).json();
    employees = data.employees; catalogError = '';
    render();
  } catch (error) {
    if (error.name !== 'AbortError') {
      $('fatal').textContent = location.protocol === 'file:'
        ? 'ローカルサーバーを起動してください。リポジトリで python3 dashboard/serve.py を実行し、http://127.0.0.1:8765 を開きます。'
        : `一覧を読み込めません。サーバーの起動を確認し「再読込」を押してください。${error.message}`;
      $('fatal').hidden = false; catalogError = $('fatal').textContent;
    }
  } finally { $('refresh').disabled = false; }
}

function renderNavigation() {
  const navigation = $('employees'); navigation.replaceChildren();
  employees.forEach((person, index) => {
    const button = node('button', undefined, 'employee-button');
    button.setAttribute('aria-current', String(person.id === current.id));
    button.dataset.employee = person.id;
    button.append(node('span', String(index+1).padStart(2,'0'), 'number'));
    const label = node('span', person.title, 'label');
    label.append(node('span', person.id, 'case-label')); button.append(label);
    button.addEventListener('click', () => go('overview', '', person.id)); navigation.append(button);
  });
  document.querySelectorAll('[data-view]').forEach((button) => button.setAttribute('aria-current', String(button.dataset.view === view)));
}

function render() {
  if (!employees.length) return;
  const [route, query = ''] = location.hash.slice(1).split('?');
  const [id, requestedView] = route.split('/');
  current = employees.find((p) => p.id === id) || employees[0];
  view = Object.hasOwn(groups, requestedView) ? requestedView : 'overview';
  controller?.abort(); requestVersion++;
  clearPreview();
  $('preview-wrap').hidden = true; $('source-wrap').hidden = true; $('markdown-wrap').hidden = true;
  $('markdown-wrap').replaceChildren();clearTimeout(searchTimer);
  $('file-filter').value = '';
  document.body.classList.toggle('exploring',view!=='overview');
  renderNavigation();
  $('employee').hidden = Boolean(current.error);
  $('fatal').hidden = !current.error;
  if (current.error) { $('fatal').textContent = `${current.id}を読み込めません。${current.error}`; return; }
  showNotice(catalogError || (current.problems.length ? `確認が必要なファイルがあります：${current.problems.join(' / ')}` : ''));
  $('location').textContent = `AI社員ラボ / ${current.id} / ${groups[view]}`;
  $('eyebrow').textContent = `${String(employees.indexOf(current)+1).padStart(2,'0')} / ${current.id.toUpperCase()} · 架空サンプル`;
  $('title').textContent = current.title;
  $('purpose').textContent = current.purpose;
  $('acceptance').textContent = current.human_acceptance ? '検収状態は記録を確認' : '人の確認前';
  $('overview').hidden = view !== 'overview'; $('explorer').hidden = view === 'overview';
  if (view === 'overview') renderOverview();
  else {
    $('group-title').textContent = groups[view];
    const files = current.files.filter((f) => f.group === view);
    const parameters = new URLSearchParams(query), requested = parameters.get('file');
    chosen = files.find((f) => f.path === requested) || (view === 'outputs' ? files.find((f) => f.preview_url) : null) || files[0] || null;
    $('viewer-actions').hidden = !chosen;
    renderFiles();
    if (chosen) selectFile(chosen,parameters.get('mode'),parameters.get('anchor'));
    else { $('file-title').textContent = '表示できるファイルがありません'; $('file-path').textContent = ''; $('viewer-status').textContent = '資料とsample.jsonを確認し、一覧を再読込してください。';  }
  }
}

function renderOverview() {
  $('flow').replaceChildren();
  const specs = [
    ['inputs','資料を渡す',`${current.files.filter(f=>f.group==='inputs').length}ファイルの入力原本`],
    ['definition','仕事を任せる','役割をAGENTS、手順をSkillに'],
    ['outputs','人が確かめる',`${current.files.filter(f=>f.group==='outputs').length}ファイルの最新成果`]
  ];
  specs.forEach(([group,title,detail],i)=>{
    const button=node('button',undefined,'flow-card'); button.dataset.step=group;
    button.append(node('span',`0${i+1}`,'step-number'));
    const body=node('span',title,'flow-title');body.append(node('span',detail,'flow-sub'));button.append(body);
    button.addEventListener('click',()=>go(group));$('flow').append(button);
  });
  $('questions').replaceChildren();
  current.questions.slice(0,4).forEach((q,i)=>{
    const article=node('article',undefined,'question');
    const heading=node('h4');heading.append(node('span',`Q${i+1}`),document.createTextNode(q.question));
    article.append(heading,node('p',q.answer));$('questions').append(article);
  });
  $('parameters').replaceChildren();
  Object.entries(current.parameters).forEach(([key,value])=>$('parameters').append(node('dt',key),node('dd',String(value))));
  $('run-id').textContent=`実行ID：${current.run_id}`;
  $('report-open').disabled=!current.files.some(f=>f.preview_url);
}

function renderFiles() {
  const all=current.files.filter(f=>f.group===view), query=$('file-filter').value.toLocaleLowerCase();
  const files=all.filter(f=>f.path.toLocaleLowerCase().includes(query));
  $('file-count').textContent=`${files.length} / ${all.length}`;
  const list=$('file-list');list.replaceChildren(); let folder=null;
  files.forEach(file=>{
    let dir=file.path.split('/').slice(0,-1).join('/') || '社員フォルダ';
    if(dir.startsWith('outputs/')) dir='最新の実行結果';
    if(dir!==folder){list.append(node('div',dir,'file-folder'));folder=dir;}
    const button=node('button',undefined,'file-button');button.dataset.path=file.path;
    button.setAttribute('aria-current',String(chosen?.path===file.path));
    button.append(node('span',file.name,'file-label'),node('small',`${labels[file.name] || file.path.split('.').pop().toUpperCase()} · ${size(file.size)}`));
    button.addEventListener('click',()=>go(view,file.path));list.append(button);
  });
  if(!files.length)list.append(node('p','該当するファイルはありません。','source-note'));
  $('connections').replaceChildren();
  if(view==='definition' && current.connections.length){
    $('connections').append(node('strong','CodexとClaude Codeで同じ手順を共有'));
    current.connections.forEach(c=>$('connections').append(node('p',`${c.from} → ${c.to}`)));
  }
}

const isMarkdown=file=>/\.(md|markdown)$/i.test(file?.path||'');
async function selectFile(file, mode, anchor) {
  chosen=file; content='';lines=[];pages=[];lineOffsets=[];page=0;hit=null;searchQuery='';
  $('file-title').textContent=file.name; $('file-path').textContent=`sample/${current.id}/${file.path}`;
  $('file-type').textContent=file.path.split('.').pop().toUpperCase();
  $('preview-mode').hidden=!file.preview_url; $('source-mode').hidden=!file.text; $('markdown-mode').hidden=!isMarkdown(file);
  $('download').href=file.download_url; $('download').download=file.name;
  $('open-window').href=isMarkdown(file)?MarkdownView.route({employee:current.id},{file}):file.preview_url||file.source_url;
  $('open-window').hidden=!file.text;
  $('text-search').value='';$('match-count').textContent='';
  if(isMarkdown(file) && mode!=='source') await showSource(true,anchor);
  else if(file.preview_url && mode!=='source') await showPreview(); else if(file.text) await showSource();
  else status('この形式は原本をダウンロードして確認できます。');
}

function status(message,error=false){$('viewer-status').textContent=message;$('viewer-status').classList.toggle('error',error);}
function setMode(preview, markdown=false){
  $('preview-mode').setAttribute('aria-pressed',String(preview));$('source-mode').setAttribute('aria-pressed',String(!preview&&!markdown));$('markdown-mode').setAttribute('aria-pressed',String(markdown));
  $('preview-wrap').hidden=true;$('source-wrap').hidden=true;$('markdown-wrap').hidden=true;
  if(!preview)clearPreview();
}
function clearPreview(){
  const previous=$('report-frame');
  if(previous.hasAttribute('src')){
    const fresh=previous.cloneNode(false);fresh.removeAttribute('src');previous.replaceWith(fresh);
  }
}
async function showPreview(){
  if(!chosen?.preview_url)return;
  controller?.abort();controller=new AbortController();const version=++requestVersion;
  setMode(true);status('レポートを読み込んでいます…');
  try{
    await checkedFetch(chosen.preview_url,{method:'HEAD',signal:controller.signal});
    if(version!==requestVersion)return;
    $('preview-wrap').hidden=false;
    const previous=$('report-frame'), frame=previous.cloneNode(false);
    frame.onload=()=>{if(version===requestVersion)status('保存済みHTMLを表示しています。新しい業務実行や人の検収を行ったものではありません。');};
    // Set src before attachment: the initial frame navigation must not add
    // about:blank entries to the dashboard's shared Back/Forward history.
    frame.src=chosen.preview_url;previous.replaceWith(frame);
  }catch(error){if(version===requestVersion && error.name!=='AbortError')status(error.message,true);}
}
async function showSource(markdown=false,anchor=''){
  if(!chosen?.text)return;
  controller?.abort();controller=new AbortController();const version=++requestVersion;
  setMode(false,markdown);status(`全文を読み込んでいます… (${size(chosen.size)})`);
  try{
    const raw=await (await checkedFetch(chosen.source_url,{signal:controller.signal})).arrayBuffer();
    let text;
    try{text=new TextDecoder('utf-8',{fatal:true}).decode(raw);}catch(_){throw new Error('UTF-8で読み込めません。原本をダウンロードして文字コードを確認してください。');}
    if(version!==requestVersion)return;
    content=text;
    if(markdown){
      const context={employee:current.id,path:chosen.path,files:current.files,connections:current.connections};
      const article=$('markdown-wrap');article.replaceChildren(MarkdownView.render(content,context,document,markdownit));
      article.hidden=false;article.scrollTop=0;
      status('Markdownを整形表示しています。全文ソースで原文を確認できます。');
      if(anchor){
        const target=[...article.querySelectorAll('[data-md-anchor]')].find(el=>el.dataset.mdAnchor===anchor);
        if(target){article.scrollTop=target.getBoundingClientRect().top-article.getBoundingClientRect().top+article.scrollTop-18;}
        else status('指定の見出しは見つかりません。文書全体を表示しています。');
      }
      return;
    }
    lines=content.split('\n');pages=SourcePages.paginate(content);
    let offset=0;lineOffsets=lines.map(line=>{const start=offset;offset+=line.length+1;return start;});
    page=0;hit=null;searchQuery='';
    $('source-wrap').hidden=false;renderPage();
    status(`${lines.length.toLocaleString()}行の全文を読み込みました。原文は編集しません。`);
  }catch(error){if(version===requestVersion && error.name!=='AbortError')status(error.message,true);}
}
function renderPage(){
  const part=pages[page];
  // Untrusted Markdown, CSV, HTML and JSON are always a text node, never markup.
  const source=$('source-content');source.replaceChildren();
  if(hit && hit.offset>=part.start && hit.offset<part.end){
    const end=Math.min(hit.offset+hit.length,part.end),mark=node('mark',content.slice(hit.offset,end));
    mark.id='search-hit';
    source.append(document.createTextNode(content.slice(part.start,hit.offset)),mark,document.createTextNode(content.slice(end,part.end)));
    requestAnimationFrame(()=>{source.scrollTop=Math.max(0,mark.getBoundingClientRect().top-source.getBoundingClientRect().top+source.scrollTop-source.clientHeight/3);});
  }else source.textContent=content.slice(part.start,part.end);
  source.scrollTop=0;
  $('line-range').textContent=`${part.startLine.toLocaleString()}–${part.endLine.toLocaleString()}行 / 全${lines.length.toLocaleString()}行 · ${page+1}/${pages.length}ページ`;
  $('page-prev').disabled=page===0;$('page-next').disabled=page===pages.length-1;
}
function searchText(){
  searchQuery=$('text-search').value;hit=SourcePages.findNext(content,searchQuery);
  if(hit)page=SourcePages.pageAt(pages,hit.offset);
  if(pages.length)renderPage();renderMatches();
}
function renderMatches(){
  let line=0;
  if(hit){let low=0,high=lineOffsets.length-1;while(low<high){const mid=Math.ceil((low+high)/2);if(lineOffsets[mid]<=hit.offset)low=mid;else high=mid-1;}line=low+1;}
  $('match-count').textContent=!searchQuery?'':hit?`一致：${line.toLocaleString()}行目・${(hit.offset+1).toLocaleString()}文字目`:'一致なし';
  $('find-prev').disabled=!hit;$('find-next').disabled=!hit;
}
function moveMatch(direction){
  if(searchQuery!==$('text-search').value){searchText();return;}
  if(!hit)return;
  hit=direction>0?SourcePages.findNext(content,searchQuery,hit.offset+hit.length):SourcePages.findPrevious(content,searchQuery,hit.offset);
  if(hit)page=SourcePages.pageAt(pages,hit.offset);
  renderPage();renderMatches();
}

document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>go(button.dataset.view)));
$('hearing-open').addEventListener('click',()=>go('interview','interview.md'));
$('metadata-open').addEventListener('click',()=>go('reference','sample.json'));
$('report-open').addEventListener('click',()=>go('outputs'));
$('refresh').addEventListener('click',loadCatalog);
$('file-filter').addEventListener('input',renderFiles);
$('preview-mode').addEventListener('click',()=>go(view,chosen.path,current.id));
$('markdown-mode').addEventListener('click',()=>go(view,chosen.path,current.id));
$('source-mode').addEventListener('click',()=>go(view,chosen.path,current.id,{mode:'source'}));
$('page-prev').addEventListener('click',()=>{if(page>0){page--;renderPage();}});
$('page-next').addEventListener('click',()=>{if(page+1<pages.length){page++;renderPage();}});
let searchTimer;
$('text-search').addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(searchText,200);});
$('find-next').addEventListener('click',()=>moveMatch(1));$('find-prev').addEventListener('click',()=>moveMatch(-1));
$('text-search').addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();clearTimeout(searchTimer);if(searchQuery!==$('text-search').value)searchText();else moveMatch(event.shiftKey?-1:1);}});
$('present').addEventListener('click',()=>{const on=document.body.classList.toggle('presenting');document.documentElement.classList.toggle('projection',on);$('present').setAttribute('aria-pressed',String(on));try{localStorage.setItem('employee-showcase-projection',String(on));}catch(_){/* optional preference */}});
try{if(localStorage.getItem('employee-showcase-projection')==='true'){$('present').click();}}catch(_){/* local files may disable storage */}
window.addEventListener('hashchange',render);
loadCatalog();
