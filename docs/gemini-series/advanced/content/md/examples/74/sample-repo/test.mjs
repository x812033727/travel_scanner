import test from 'node:test';
import assert from 'node:assert/strict';
import {displayLimit} from './apps/web/limit.mjs';
test('normal',()=>assert.equal(displayLimit(3),3));
test('upper',()=>assert.equal(displayLimit(20),10));
test('lower',()=>assert.equal(displayLimit(-2),0));
