import { Refused } from "./contract.mjs";
import { fileHash } from "./store.mjs";

/** All account UI work is serialized. A paused job holds the browser for its owner. */
export class Runner {
  constructor(store, driver) { this.store = store; this.driver = driver; this.status = "idle"; this.busy = false; }
  async tick() {
    if (this.busy || this.store.all().some((j) => j.state === "needs_action")) return;
    const job = this.store.all().find((j) => j.state === "queued");
    if (!job) return;
    this.busy = true; this.status = "working";
    this.store.patch(job.id, { state: "running", code: null });
    const checkpoint = (fields) => this.store.patch(job.id, fields);
    try {
      for (const f of job.manifest.files) {
        if (this.store.received(job, f.sha256) !== f.size || await fileHash(this.store.file(job, f.sha256)) !== f.sha256) throw new Refused("file_hash_mismatch");
      }
      await this.driver.connect();
      await this.driver.channel(job.manifest.channel_id);
      for (const step of job.steps) {
        const current = this.store.get(job.id);
        if (current.completed.includes(step)) continue;
        checkpoint({ current_step: step });
        if (step === "video") {
          if (current.video_id) await this.driver.openPrivate(current.video_id);
          else {
            if (current.upload_started) throw new Refused("video_id_required");
            await this.driver.upload(current, {
              started: () => checkpoint({ upload_started: true }),
              identified: (video_id) => checkpoint({ video_id }),
            });
            checkpoint({ completed: [...this.store.get(job.id).completed, "details"] });
          }
        } else {
          if (!current.video_id) throw new Refused("video_id_required");
          await this.driver.step(step, current);
        }
        checkpoint({ completed: [...this.store.get(job.id).completed, step] });
      }
      checkpoint({ state: "done", code: null, current_step: null });
    } catch (e) {
      checkpoint({ state: "needs_action", code: e instanceof Refused ? e.code : "studio_changed" });
    } finally { this.busy = false; this.status = "idle"; }
  }
}
