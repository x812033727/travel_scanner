# Portable paths and historical specification hashes

On 2026-10-13, the four opening specifications were scrubbed for a public
repository. Each had five `source_doc` fields naming one operator's Windows
profile. Those fields were redundant: `speech.mjs` already resolves an omitted
`source_doc` to `<sources>/<slug>/video.json`. No opening line, locale, scene,
voice, or source-content digest changed. The media delivered on 2026-10-12 and
its existing review receipts were not regenerated.

| Specification | Historical SHA-256, as reviewed and used for the delivered batch | Portable repository SHA-256 |
| --- | --- | --- |
| `intro-specs.json` | `bf69b87b95ae44a1a07189a2ca949d3368a5b3fee79cba8a7f20d7a79600fbb7` | `8d7c48cf25c5b8715a1ac48b5da812181ed2e12c19a3cf3b38a71ac5706b4573` |
| `u02-visual-specs.json` | `71162027df20a61e4a82febd5a23729baa22c764cbe9cc7929893b8d6df529bc` | `ea8786511495eb260d292bb94c746e8af72ae5109b5ba83e2041014079844c04` |
| `h03-pronunciation-specs.json` | `9ad54c2e7badc92bd9ce5c545ec22bf1c6fb99bd9b33b2a0b675c5b95d0b1685` | `2f28886d91506ae12db505641489ff990a49838c16ec0a99df1b869daded6a46` |
| `l08-wording-specs.json` | `5b4c67388376b59e3977f7ae130d15e2457ecac4681700ed2740b20ad6d06821` | `18be24839022f228938c373491b1ccbe6c93c3bf2f365961eea725eabc5fb1f3` |

Exact historical bytes are retained outside Git with their original hashes in
`<home>/mokaair-work/backup-receipts/curio-five-recuts-20261012-specs-pre-portability/`.
The dated `independent-review.md` and saved speech/revision receipts continue
to cite the **historical** hashes. They have not been rebound to the portable
copies. When inspecting or resuming an existing revision, supply the archived
historical specs to any tool that validates `old_spec_sha256` or
`new_spec_sha256`; do not silently replace a receipt's binding. A fresh run
with the portable specs must use explicit `--sources` and establish its own
new receipts.

The CLI defaults now resolve delivery and branding under the current user's
home directory; `--output-root`, `--brand-dir`, `--sources`, `--out`, `--model`
and `--python` remain available for restored or nonstandard locations. The
synthetic assembler smoke uses the system temporary directory by default.
