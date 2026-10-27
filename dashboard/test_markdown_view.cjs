'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict');
const MarkdownView=require('./markdown-view.js'),Parser=require('./vendor/markdown-it.min.js');
// Minimal DOM implementing only the APIs the renderer is allowed to use.
class Element {
  constructor(tag){this.tag=tag;this.children=[];this.attrs={};this.value='';}
  append(...children){this.children.push(...children);}
  set textContent(text){this.value=text;this.children=[];}
  get textContent(){return this.value+this.children.map(c=>c.textContent).join('');}
  setAttribute(k,v){this.attrs[k]=v;}
}
const document={createElement:tag=>new Element(tag),createDocumentFragment:()=>new Element('#fragment'),createTextNode:text=>{const n=new Element('#text');n.textContent=text;return n;}};
const files=[{path:'AGENTS.md',group:'definition'},{path:'interview.md',group:'interview'},{path:'.claude/skills/work-001/SKILL.md',group:'definition'},{path:'.claude/skills/work-001/references/rules.md',group:'definition'},{path:'inputs/memo.md',group:'inputs'}];
const context={employee:'sales',path:'AGENTS.md',files,connections:[{from:'.agents/skills/work-001',to:'../../.claude/skills/work-001'}]};
const render=text=>MarkdownView.render(text,context,document,Parser);
function all(node){return [node,...node.children.flatMap(all)];}
const tags=node=>all(node).map(x=>x.tag);
test('headings, nested lists, table, quote, inline/fenced code, emphasis, strike',()=>{
 const root=render('# Title\n\n- one\n  - two\n\n1. first\n\n| a | b |\n| --- | ---: |\n| **bold** | `code` |\n\n> quote *em* ~~old~~\n\n```js\n<script>raw</script>\n```');
 for(const tag of ['h1','ul','ol','li','table','th','td','strong','em','s','blockquote','pre','code'])assert.ok(tags(root).includes(tag),tag);
 assert.equal(all(root).filter(x=>x.tag==='ul').length,2);
 assert.ok(root.textContent.includes('<script>raw</script>'));
});
test('raw HTML never creates executable or styled elements',()=>{
 const root=render('<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>\n\n<iframe src="https://evil"></iframe>\n\n<span style="color:red" onclick="bad()">raw</span>');
 for(const tag of ['script','img','iframe','style'])assert.ok(!tags(root).includes(tag));
 assert.ok(root.textContent.includes('<script>'));
 assert.ok(all(root).every(x=>Object.keys(x.attrs).every(k=>!/^on|style/.test(k))));
});
test('images never load remote, data, or local sources',()=>{
 const root=render('![remote](https://evil/x.png) ![local](inputs/a.png) ![data](data:image/png;base64,AA==)');
 assert.ok(!tags(root).includes('img'));assert.ok(all(root).every(x=>!x.attrs.src));
});
test('dangerous protocols, controls, encoded traversal and unlisted paths blocked',()=>{
 for(const href of ['javascript:alert(1)','JaVaScRiPt:alert(1)','data:text/html,a','vbscript:x','file:///tmp/a','//evil/x','https://a/\nfoo','https://a\\b','%6aavascript%3aalert(1)','%2f%2fevil/x','%2e%2e/AGENTS.md','../minutes/AGENTS.md','private.md','inputs/a%00.md','?file=private'])assert.equal(MarkdownView.resolveLink(href,context),null,href);
});
test('entity-encoded unsafe links do not become anchors',()=>{
 const root=render('[bad](javascript&#58;alert%281%29) [bad2](data:text/html,evil)');
 assert.ok(all(root).every(x=>x.tag!=='a'));
});
test('relative links resolve from the actual Skill directory',()=>{
 const c={...context,path:'.claude/skills/work-001/SKILL.md'};
 assert.equal(MarkdownView.resolveLink('../../../AGENTS.md#emp-001',c).file.path,'AGENTS.md');
 assert.equal(MarkdownView.resolveLink('references/rules.md',c).file.path,'.claude/skills/work-001/references/rules.md');
 assert.equal(MarkdownView.resolveLink('../../../../AGENTS.md',c),null);
});
test('Codex Skill alias maps only to catalogued canonical files',()=>{
 assert.equal(MarkdownView.resolveLink('.agents/skills/work-001/SKILL.md',context).file.path,'.claude/skills/work-001/SKILL.md');
 assert.equal(MarkdownView.resolveLink('.agents/skills/work-001/private.md',context),null);
});
test('directory links route to the group of actual files',()=>{
 assert.deepEqual(MarkdownView.resolveLink('inputs/',context),{kind:'directory',group:'inputs'});
 assert.equal(MarkdownView.resolveLink('unknown/',context),null);
});
test('explicit anchors and heading anchors cannot collide with app IDs',()=>{
 const root=render('<a id="main"></a>\n\n# 日本語の見出し\n\n<a id="main" onclick="bad()"></a>');
 assert.ok(all(root).some(x=>x.attrs['data-md-anchor']==='main'));
 assert.ok(all(root).some(x=>x.attrs['data-md-anchor']==='日本語の見出し'));
 assert.ok(all(root).every(x=>!x.attrs.id));
 assert.equal(all(root).filter(x=>x.attrs['data-md-anchor']==='main').length,1);
});
test('internal link uses viewer route, preserving fragment',()=>{
 const root=render('[go](interview.md#質問)');const a=all(root).find(x=>x.tag==='a');
 assert.equal(a.attrs.href,'#sales/interview?file=interview.md&anchor=%E8%B3%AA%E5%95%8F');
});
test('external links require HTTP(S) and isolate the opened tab',()=>{
 const root=render('[site](https://example.com/a)');const a=all(root).find(x=>x.tag==='a');
 assert.equal(a.attrs.href,'https://example.com/a');assert.equal(a.attrs.target,'_blank');assert.equal(a.attrs.rel,'noopener noreferrer');
 assert.equal(MarkdownView.resolveLink('https://user:pass@example.com',context),null);
});
test('YAML frontmatter remains visible as plain data',()=>{
 const root=render('---\nname: work\ndescription: <script>evil</script>\n---\n\n# Skill');
 assert.ok(tags(root).includes('details'));assert.ok(tags(root).includes('h1'));assert.ok(root.textContent.includes('description: <script>evil</script>'));assert.ok(!tags(root).includes('script'));
});
test('reference links, escaped pipes and raw inline HTML retain readable content',()=>{
 const root=render('[manual][ref]\n\n[ref]: interview.md\n\n| name | note |\n| --- | --- |\n| a\\|b | `<x>` |\n\nHello <b>bold</b>.');
 assert.ok(all(root).some(x=>x.tag==='a'&&x.attrs.href.includes('interview')));assert.ok(root.textContent.includes('a|b'));assert.ok(root.textContent.includes('<b>'));
});
