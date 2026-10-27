'use strict';
// Parse Markdown into tokens, then build only explicitly allowed DOM elements.
// Raw HTML, images, attributes and URL schemes never go through an HTML sink.
const MarkdownView = (() => {
  const tags = new Set(['p','h1','h2','h3','h4','h5','h6','ul','ol','li','blockquote','strong','em','s','table','thead','tbody','tr','th','td']);
  function normalize(base, relative) {
    const parts = base ? base.split('/') : [];
    for (const part of relative.split('/')) {
      if (!part || part === '.') continue;
      if (part === '..') { if (!parts.length) return null; parts.pop(); }
      else parts.push(part);
    }
    return parts.join('/');
  }
  function resolveLink(href, context) {
    if (!href || /[\x00-\x20\x7f\\]/.test(href)) return null;
    if (/^https?:\/\//i.test(href)) {
      try { const url = new URL(href); return url.username || url.password ? null : {kind:'external',href:url.href}; } catch (_) { return null; }
    }
    if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('/')) return null;
    const hash = href.indexOf('#'), rawPath = hash < 0 ? href : href.slice(0,hash);
    let path, anchor;
    try { path=decodeURIComponent(rawPath);anchor=hash<0?'':decodeURIComponent(href.slice(hash+1)); } catch (_) { return null; }
    if (/[\x00-\x1f\x7f\\?:#]/.test(path) || path.startsWith('/') || /[\x00-\x1f\x7f]/.test(anchor)) return null;
    let target = path ? normalize(context.path.split('/').slice(0,-1).join('/'),path) : context.path;
    if (target === null) return null;
    for (const link of context.connections || []) {
      if (target === link.from || target.startsWith(link.from+'/')) {
        const canonical=normalize(link.from.split('/').slice(0,-1).join('/'),link.to);
        if(canonical)target=canonical+target.slice(link.from.length);
      }
    }
    const file=context.files.find(f=>f.path===target);
    if(file)return {kind:'file',file,anchor};
    const contents=context.files.filter(f=>f.path.startsWith(target+'/'));
    if(contents.length && contents.every(f=>f.group===contents[0].group) && !anchor)return {kind:'directory',group:contents[0].group};
    return null;
  }
  function route(context, link) {
    const query=new URLSearchParams();
    if(link.file)query.set('file',link.file.path);
    if(link.anchor)query.set('anchor',link.anchor);
    return '#'+context.employee+'/'+(link.file?.group || link.group)+(query.size?'?'+query:'');
  }
  function render(text, context, document, Parser) {
    const parser=new Parser({html:true,linkify:false,typographer:false,breaks:false});
    const fragment=document.createDocumentFragment(), stack=[fragment], anchors=new Map();
    const element=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
    const append=e=>stack[stack.length-1].append(e);
    const textNode=text=>document.createTextNode(text);
    const anchor=(el,name)=>{
      if(!name)return;
      const count=anchors.get(name)||0;anchors.set(name,count+1);
      el.setAttribute('data-md-anchor',name+(count?'-'+count:''));
    };
    const headingName=text=>text.toLowerCase().replace(/[^\p{L}\p{N}_\- ]/gu,'').trim().replace(/ +/g,'-');
    // Frontmatter remains readable as data; it is never evaluated as config.
    const front=text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
    if(front){
      const details=element('details');details.className='md-frontmatter';details.append(element('summary','文書の設定（YAML）'),element('pre',front[1]));append(details);text=text.slice(front[0].length);
    }
    function tokens(items) {
      for(let i=0;i<items.length;i++){
        const token=items[i];
        if(token.type==='inline'){tokens(token.children||[]);continue;}
        if(token.type==='text'){append(textNode(token.content));continue;}
        if(token.type==='softbreak'){append(textNode('\n'));continue;}
        if(token.type==='hardbreak'){append(element('br'));continue;}
        if(token.type==='code_inline'){append(element('code',token.content));continue;}
        if(token.type==='fence'||token.type==='code_block'){
          const pre=element('pre');pre.setAttribute('tabindex','0');pre.append(element('code',token.content));append(pre);continue;
        }
        if(token.type==='hr'){append(element('hr'));continue;}
        if(token.type==='html_block'||token.type==='html_inline'){
          let raw=token.content;
          if(token.type==='html_inline' && /^<a\s+id=["']([\p{L}\p{N}_:.-]+)["']\s*>$/u.test(raw) && items[i+1]?.type==='html_inline' && items[i+1].content==='</a>'){raw+=items[++i].content;}
          const match=raw.trim().match(/^<a\s+id=["']([\p{L}\p{N}_:.-]+)["']\s*>\s*<\/a>$/u);
          if(match){const span=element('span');anchor(span,match[1]);append(span);}
          else append(element(token.type==='html_block'?'pre':'code',token.content));
          continue;
        }
        if(token.type==='image'){
          // Images are described, never fetched (including relative/data URLs).
          append(element('span','［画像：'+token.content+'］'));continue;
        }
        if(token.type==='link_open'){
          const href=token.attrGet('href'),link=resolveLink(href,context);
          const a=element(link?'a':'span');
          if(link){
            a.setAttribute('href',link.kind==='external'?link.href:route(context,link));
            if(link.kind==='external'){a.setAttribute('target','_blank');a.setAttribute('rel','noopener noreferrer');a.setAttribute('referrerpolicy','no-referrer');a.setAttribute('title','外部サイトを別タブで開く');}
          }else{a.className='md-unavailable-link';a.setAttribute('title','表示対象外のリンクです。原文で参照先を確認できます。');}
          append(a);stack.push(a);continue;
        }
        if(token.type==='link_close'){stack.pop();continue;}
        if(token.nesting===1 && tags.has(token.tag)){
          const el=element(token.tag);
          if(/^h[1-6]$/.test(token.tag))anchor(el,headingName(items[i+1]?.content||''));
          if(token.tag==='ol' && /^\d+$/.test(token.attrGet('start')||''))el.setAttribute('start',token.attrGet('start'));
          if(token.tag==='th'||token.tag==='td'){
            const align=token.attrGet('style')?.match(/^text-align:(left|center|right)$/)?.[1];
            if(align)el.className='md-align-'+align;
          }
          if(token.tag==='table'){
            const wrap=element('div');wrap.className='md-table-scroll';wrap.setAttribute('tabindex','0');wrap.setAttribute('role','region');wrap.setAttribute('aria-label','表（横スクロールできます）');append(wrap);wrap.append(el);stack.push(el);
          }else{append(el);stack.push(el);}
          continue;
        }
        if(token.nesting===-1 && tags.has(token.tag)){stack.pop();continue;}
        if(token.content)append(textNode(token.content));
      }
    }
    tokens(parser.parse(text,{}));
    return fragment;
  }
  return {render,resolveLink,route};
})();
if(typeof module!=='undefined')module.exports=MarkdownView;
