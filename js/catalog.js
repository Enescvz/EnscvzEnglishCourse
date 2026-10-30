/** Data-view helpers for unreviewed *source* headwords. Never marks a lesson learned. */
export function filterCandidates(entries, {kind='all',level='all',query='',availability='all',page=0,pageSize=30}={}) {
  const needle=String(query).trim().toLocaleLowerCase('en-US');
  const filtered=entries.filter(x=>
    (kind==='all'||x.t===kind) &&
    (level==='all'||x.l===level) &&
    (availability==='all'||(availability==='lesson'?!!x.lesson:!x.lesson)) &&
    (!needle||x.w.includes(needle)));
  const count=filtered.length;
  const maxPage=Math.max(0,Math.ceil(count/pageSize)-1);
  const currentPage=Math.min(Math.max(0,Number(page)||0),maxPage);
  return {items:filtered.slice(currentPage*pageSize,(currentPage+1)*pageSize),count,page:currentPage,pageCount:maxPage+1};
}
