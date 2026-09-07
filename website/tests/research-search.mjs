import assert from 'node:assert/strict';
import {filterDocuments} from '../lib/research-search.ts';
const docs=[{manufacturer:'sibre',title:'SHI 75',source_url:'https://example.com/a'},{manufacturer:'twiflex',title:'MU3 Caliper',source_url:'https://example.com/b'}];
assert.equal(filterDocuments(docs,'  SHI  75 ','all').length,1);
assert.equal(filterDocuments(docs,'mu3','sibre').length,0);
assert.equal(filterDocuments(docs,'','all').length,2);
assert.equal(filterDocuments(docs,'nonexistent','all').length,0);
assert.equal(filterDocuments(docs,'','twiflex')[0].title,'MU3 Caliper');
console.log('Search behavior checks passed');
