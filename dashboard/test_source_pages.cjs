const assert = require('node:assert/strict');
const {paginate,pageAt,findNext,findPrevious} = require('./source-pages.js');
const texts = ['', 'one line', 'a\n'.repeat(1000), 'x'.repeat(9_600_000), 'x'.repeat(31999)+'🐕'+'y'.repeat(50000), '短い行\n'+'長'.repeat(100000)+'\n終わり\n'];
for(const text of texts){
  const pages=paginate(text);
  assert.equal(pages.map(p=>text.slice(p.start,p.end)).join(''),text);
  assert.ok(pages.every(p=>p.end-p.start<=32000));
  assert.ok(pages.every(p=>(text.slice(p.start,p.end).match(/\n/g)||[]).length<=160));
  for(const p of pages){
    assert.equal(pageAt(pages,p.start),pages.indexOf(p));
    if(p.end>p.start)assert.equal(pageAt(pages,p.end-1),pages.indexOf(p));
    assert.ok(!(/[\uD800-\uDBFF]/.test(text[p.end-1]||'')&&/[\uDC00-\uDFFF]/.test(text[p.end]||'')));
  }
}
console.log('6 source pagination cases passed: exact coverage, bounded size/lines, lookup and Unicode boundaries.');
const repeated='first HIT '+ 'x'.repeat(100000)+' second hit 🐕 '+ 'x'.repeat(100000)+' third HiT';
const first=findNext(repeated,'hit'),second=findNext(repeated,'hit',first.offset+first.length),third=findNext(repeated,'hit',second.offset+second.length);
assert.ok(first.offset<second.offset&&second.offset<third.offset);
assert.deepEqual(findNext(repeated,'hit',third.offset+third.length),first);
assert.deepEqual(findPrevious(repeated,'hit',third.offset),second);
assert.deepEqual(findPrevious(repeated,'hit',first.offset),third);
assert.equal(findNext('before [a]+ after','[a]+').offset,7);
assert.equal(findNext('İ 🐕 target','target').offset,5);
assert.equal(findNext(repeated,'not found'),null);
assert.equal(findNext(repeated,''),null);
console.log('5 search cases passed: every occurrence in a long line, wrap/previous, literal regex characters, original Unicode offsets and empty/missing queries.');
