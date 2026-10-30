# MiniMax H3 pod image

What a RunPod pod runs when `minimax-h3-runpod` asks the site for one
(`.agents/skills/minimax-h3-runpod/SKILL.md`).

| File | What it is |
| --- | --- |
| `Dockerfile` | Python 3.12, CUDA 12.8 PyTorch, ComfyUI, VideoHelperSuite and SeedVR2 at pinned commits |
| `entrypoint.sh` | Starts the gate, fetches the models, then starts ComfyUI on loopback |
| `gate.py` | Bearer-token gate on port 8188; forwards only five routes |
| `fetch_models.py`, `models.lock`, `make_lock.py` | Models on the network volume at pinned revisions, hash-checked |
| `workflows/`, `profiles.json` | API-format graphs with `$name` placeholders, and the sampling profiles |
| `smoke.py` | CI check: every workflow node exists with its required inputs |

The graphs come from the Colab notebooks that ran on 2026-10-28 and 2026-10-30, not from Comfy-Org
`workflow_templates`, because those are the graphs the measurements in `three-stage.md` belong to.

## First-time setup (owner)

1. Merge to main. `.github/workflows/runpod-h3-image.yml` publishes to GHCR and prints the digest in
   the job summary. Make the `runpod-h3` package public in GitHub (Packages → runpod-h3 → Package
   settings): the broker passes no registry credentials.
2. On `/admin/settings`, RunPod card (under 影片): API key, GPU, data center, network volume id, and
   the image exactly as printed, `ghcr.io/...@sha256:...`.
3. In a session: `node tools/video/cli.mjs login --runpod`, and allow it on the admin card.

The first pod downloads 109.7 GiB (15 files) to the volume, so the volume needs that much free.
Later pods verify by marker file and start in minutes. A failed fetch keeps the gate up so the
runner can report why.

## Changing a pin

- Models: `python ops/runpod/make_lock.py > ops/runpod/models.lock`, and review the diff.
- ComfyUI or nodes: change the commit in `Dockerfile`; CI's smoke check runs on the pull request.
- The image digest on the admin card does not change by itself: paste the new one after merging.
