'use strict';
// Bound DOM text even when a report embeds megabytes of JSON on one line.
// Pages cover the original string exactly and never split a UTF-16 pair.
const SourcePages = (() => {
  function paginate(text, maxLines = 160, maxChars = 32000) {
    if (maxLines < 1 || maxChars < 2) throw new RangeError('Invalid page limits');
    if (!text.length) return [{start:0,end:0,startLine:1,endLine:1}];
    const pages = []; let start = 0, startLine = 1;
    while (start < text.length) {
      let end = Math.min(start + maxChars, text.length);
      if (end < text.length && /[\uD800-\uDBFF]/.test(text[end-1]) && /[\uDC00-\uDFFF]/.test(text[end])) end--;
      const chunk = text.slice(start,end); let index = 0, count = 0, next;
      while ((next = chunk.indexOf('\n',index)) !== -1) {
        count++; index = next+1;
        if (count === maxLines) { end = start+index; break; }
      }
      const endLine = startLine + count - (text[end-1] === '\n' && end < text.length ? 1 : 0);
      pages.push({start,end,startLine,endLine}); start=end; startLine+=count;
    }
    return pages;
  }
  function pageAt(pages, offset) {
    let low=0,high=pages.length-1;
    while(low<high){const middle=Math.floor((low+high)/2);if(offset<pages[middle].end)high=middle;else low=middle+1;}
    return low;
  }
  function expression(query) {
    return new RegExp(query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'giu');
  }
  function findNext(text, query, from = 0) {
    if (!query) return null;
    const regex=expression(query);regex.lastIndex=from;
    let hit=regex.exec(text);
    if(!hit && from>0){regex.lastIndex=0;hit=regex.exec(text);}
    return hit?{offset:hit.index,length:hit[0].length}:null;
  }
  function findPrevious(text, query, before = text.length+1) {
    if (!query) return null;
    const regex=expression(query);let hit,last=null,previous=null;
    while((hit=regex.exec(text))!==null){
      last={offset:hit.index,length:hit[0].length};
      if(hit.index<before)previous=last;
    }
    return previous || last;
  }
  return {paginate,pageAt,findNext,findPrevious};
})();
if (typeof module !== 'undefined') module.exports = SourcePages;
