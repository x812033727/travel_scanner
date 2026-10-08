// Media state is separate from the page so routing and recovery can be tested.
export const CAPTION_LANGUAGES = [
  ['zh-Hant', '繁體中文'], ['zh-Hans', '简体中文'], ['ja', '日本語'], ['ko', '한국어'],
];

export function replaceCues(track, entries, Cue = globalThis.VTTCue) {
  // Chromium exposes null cues while disabled. Read/remove only after enabling.
  track.mode = 'hidden';
  for (const cue of Array.from(track.cues ?? [])) track.removeCue(cue);
  for (const [start, end, text] of entries) track.addCue(new Cue(start, end, text));
}

export class MediaController {
  constructor(video, audio, { update = () => {}, timeout = 25000 } = {}) {
    this.video = video;
    this.audio = audio;
    this.update = update;
    this.timeout = timeout;
    this.voice = 'en';
    this.muted = false;
    this.volume = 1;
    this.rate = 1;
    this.loading = false;
    this.generation = 0;
    this.cancelLoad = null;
    this.listeners = [];
    const listen = (target, type, fn) => {
      target.addEventListener(type, fn);
      this.listeners.push(() => target.removeEventListener(type, fn));
    };
    for (const type of ['pause', 'seeking', 'waiting', 'ended']) {
      listen(video, type, () => audio.pause());
    }
    for (const type of ['play', 'playing', 'seeked']) {
      listen(video, type, () => this.resumeAlternate());
    }
    listen(video, 'loadedmetadata', () => { this.applySettings(); this.align(); });
    listen(audio, 'canplay', () => this.resumeAlternate());
    listen(audio, 'error', () => {
      if (this.voice !== 'en' && !this.loading) this.recoverEnglish();
    });
    listen(video, 'ratechange', () => { audio.playbackRate = this.rate; });
    listen(video, 'timeupdate', () => {
      if (!video.paused && !this.loading) this.align();
    });
    this.applySettings();
  }

  applySettings() {
    this.video.muted = this.muted || this.voice !== 'en';
    this.audio.muted = this.muted;
    this.video.volume = this.audio.volume = this.volume;
    this.video.defaultPlaybackRate = this.audio.defaultPlaybackRate = this.rate;
    this.video.playbackRate = this.audio.playbackRate = this.rate;
  }

  setMuted(muted) { this.muted = Boolean(muted); this.applySettings(); this.update(); }
  setVolume(volume) { this.volume = Math.max(0, Math.min(1, Number(volume))); this.applySettings(); }
  setRate(rate) { this.rate = Number(rate); this.applySettings(); this.update(); }

  clearAlternate() {
    this.audio.pause();
    this.audio.removeAttribute('src');
    this.audio.load();
  }

  selectLesson(lesson) {
    this.generation += 1;
    this.cancelLoad?.();
    this.video.pause();
    this.voice = 'en';
    this.loading = false;
    this.lesson = lesson;
    this.clearAlternate();
    this.video.src = lesson.master;
    this.video.load();
    this.applySettings();
    this.update('按播放開始。字幕與教學語音可分別選擇。');
  }

  align() {
    this.audio.playbackRate = this.rate;
    if (this.voice !== 'en' && this.audio.readyState > 0 &&
        Math.abs(this.audio.currentTime - this.video.currentTime) > 0.15) {
      this.audio.currentTime = this.video.currentTime;
    }
  }

  async resumeAlternate() {
    if (this.voice === 'en' || this.loading || this.video.paused || this.video.seeking) return;
    const generation = this.generation;
    this.align();
    try {
      await this.audio.play();
    } catch (error) {
      if (generation !== this.generation || this.voice === 'en' || this.video.paused) return;
      if (error.name === 'AbortError') return;
      if (error.name === 'NotAllowedError') {
        this.video.pause();
        this.update('請按播放，以啟動所選教學語音。');
      } else this.recoverEnglish();
    }
  }

  recoverEnglish() {
    this.voice = 'en';
    this.clearAlternate();
    this.applySettings();
    this.update('語音載入失敗，已切回英文；保留目前的靜音與音量設定。');
  }

  waitForAudio() {
    return new Promise((resolve, reject) => {
      const cleanup = () => {
        clearTimeout(timer);
        this.audio.removeEventListener('loadedmetadata', ready);
        this.audio.removeEventListener('error', fail);
        if (this.cancelLoad === cancel) this.cancelLoad = null;
      };
      const ready = () => { cleanup(); resolve(); };
      const fail = () => { cleanup(); reject(new Error('音軌無法載入')); };
      const cancel = () => { cleanup(); reject(new Error('載入已取消')); };
      const timer = setTimeout(fail, this.timeout);
      this.cancelLoad = cancel;
      this.audio.addEventListener('loadedmetadata', ready, { once: true });
      this.audio.addEventListener('error', fail, { once: true });
    });
  }

  async selectVoice(voice) {
    if (!this.lesson || !['en', ...CAPTION_LANGUAGES.map(([lang]) => lang)].includes(voice)) return;
    const generation = ++this.generation;
    this.cancelLoad?.();
    const wasPlaying = !this.video.paused;
    this.video.pause();
    this.clearAlternate();
    this.voice = voice;
    this.loading = true;
    this.applySettings();
    this.update('正在載入教學語音…');
    try {
      if (voice !== 'en') {
        const source = this.lesson.audio?.[voice];
        if (!source) throw new Error('缺少音軌');
        const ready = this.waitForAudio();
        this.audio.src = source;
        this.audio.load();
        await ready;
        if (generation !== this.generation) return;
        this.align();
      }
      this.update('已切換教學語音。英文對話維持英文。');
    } catch {
      if (generation !== this.generation) return;
      this.recoverEnglish();
    } finally {
      if (generation === this.generation) {
        this.loading = false;
        this.applySettings();
        this.update();
        if (wasPlaying) {
          try { await this.video.play(); }
          catch { this.update('按播放繼續。'); }
        }
      }
    }
  }

  destroy() {
    this.generation += 1;
    this.cancelLoad?.();
    for (const remove of this.listeners) remove();
    this.audio.pause();
  }
}
