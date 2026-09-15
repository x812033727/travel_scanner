import test from 'node:test';
import assert from 'node:assert/strict';
import {title} from './src/title.mjs';
test('trim title',()=>assert.equal(title(' 海風 '),'海風'));
test('empty title',()=>assert.equal(title(null),'未命名'));
