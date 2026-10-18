// 一個 job 最多重試幾次。
export function retries(kind) {
  return kind === 'resize' ? 1 : 0;
}
