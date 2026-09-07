export type SearchableDocument = {manufacturer:string;title:string;source_url:string};
export function filterDocuments<T extends SearchableDocument>(documents:T[], query:string, manufacturer:string){
 const terms=query.trim().toLowerCase().split(/\s+/).filter(Boolean);
 return documents.filter(d=>(manufacturer==='all'||d.manufacturer===manufacturer)&&terms.every(t=>`${d.title} ${d.manufacturer} ${d.source_url}`.toLowerCase().includes(t)));
}
