// 票價：兒童半價，不足一元算一元。
export function fare(full, child = false) {
  return child ? Math.ceil(full / 2) : full;
}
