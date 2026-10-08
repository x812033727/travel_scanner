import { CAPTION_LANGUAGES, MediaController, replaceCues } from './controller.mjs';

const $ = (selector) => document.querySelector(selector);
const video = $('#player');
const audio = $('#alternate');
const catalog = window.LESSONS;
const formatTime = (value) => `${Math.floor(value / 60)}:${String(Math.floor(value % 60)).padStart(2, '0')}`;

if (!Array.isArray(catalog) || !catalog.length) {
  $('#launch-help').textContent = '找不到集數資料。請確認 lessons.js 與影片資料夾已完整解壓縮。';
  throw new Error('LESSONS must contain at least one episode');
}
if (location.protocol === 'file:') throw new Error('Use the included localhost launcher');
$('#launch-help').hidden = true;
let current;
const tracks = CAPTION_LANGUAGES.map(([lang, label]) => video.addTextTrack('subtitles', label, lang));
const controller = new MediaController(video, audio, { update(message) {
  $('#voice').value = controller.voice;
  $('#voice').disabled = controller.loading;
  $('#loading').hidden = !controller.loading;
  $('#mute-audio').textContent = controller.muted ? '恢復聲音' : '靜音';
  $('#mute-audio').setAttribute('aria-pressed', String(controller.muted));
  if (message) $('#status').textContent = message;
} });

function renderCaptions() {
  const language = $('#captions').value;
  // Keep browser tracks hidden: translated CC has its own reserved area, outside
  // both the burned-in English picture and the playback controls.
  const entries = current?.captions?.[language] ?? [];
  $('#caption-text').textContent = entries
    .filter(([start, end]) => start <= video.currentTime && video.currentTime < end)
    .map(([, , text]) => text).join('\n');
  $('#caption-text').lang = language === 'off' ? '' : language;
}

function renderTime() {
  const duration = Number.isFinite(video.duration) ? video.duration : 600;
  $('#seek').max = duration;
  $('#seek').value = video.currentTime;
  const label = `${formatTime(video.currentTime)} / ${formatTime(duration)}`;
  $('#time').textContent = label;
  $('#seek').setAttribute('aria-valuetext', label);
  renderCaptions();
}

function selectDay(day) {
  current = catalog.find((lesson) => lesson.day === Number(day)) ?? catalog[0];
  $('#episode').value = current.day;
  $('#lesson-title').textContent = current.title;
  $('#day-label').textContent = `DAY ${String(current.day).padStart(2, '0')} / ${window.SERIES?.episodeCount ?? 60}`;
  video.setAttribute('aria-label', `第 ${current.day} 集機場英文：${current.title}，10 分鐘`);
  $('#previous').disabled = current === catalog[0];
  $('#next').disabled = current === catalog.at(-1);
  controller.selectLesson(current);
  for (const track of tracks) replaceCues(track, current.captions?.[track.language] ?? []);
  renderCaptions();
  renderTime();
  $('#files').replaceChildren();
  for (const file of current.files ?? []) {
    const link = document.createElement('a');
    link.href = file.url;
    link.download = file.name;
    link.textContent = file.name;
    $('#files').append(link);
  }
  $('#chapters').replaceChildren();
  // Chapter timings belong to the final production timeline, never a fixed
  // prototype timeline. Omit the chapter bar when a catalog has no chapters.
  for (const chapter of current.chapters ?? []) {
    const button = document.createElement('button');
    button.textContent = chapter.title;
    button.addEventListener('click', () => seek(chapter.start));
    $('#chapters').append(button);
  }
  history.replaceState(null, '', `#day${current.day}`);
}

function seek(time) {
  if (video.readyState < 1) return;
  video.currentTime = Math.max(0, Math.min(Number(time), video.duration));
  controller.align();
  renderTime();
}

for (const lesson of catalog) {
  const option = document.createElement('option');
  option.value = lesson.day;
  option.textContent = `Day ${String(lesson.day).padStart(2, '0')}｜${lesson.title}`;
  $('#episode').append(option);
}
$('#episode').addEventListener('change', () => selectDay($('#episode').value));
for (const [id, delta] of [['previous', -1], ['next', 1]]) {
  $(`#${id}`).addEventListener('click', () => {
    const lesson = catalog[catalog.indexOf(current) + delta];
    if (lesson) selectDay(lesson.day);
  });
}
$('#voice').addEventListener('change', () => controller.selectVoice($('#voice').value));
$('#captions').addEventListener('change', renderCaptions);
$('#speed').addEventListener('change', () => controller.setRate($('#speed').value));
$('#mute-audio').addEventListener('click', () => controller.setMuted(!controller.muted));
$('#volume').addEventListener('input', () => controller.setVolume($('#volume').value));
$('#seek').addEventListener('input', () => seek($('#seek').value));
$('#play').addEventListener('click', async () => {
  if (controller.loading) return;
  if (video.paused) {
    try { await video.play(); }
    catch { $('#status').textContent = '影片無法播放。請確認本集檔案完整，並使用提供的本機網址。'; }
  } else video.pause();
});
for (const event of ['play', 'pause', 'ended']) video.addEventListener(event, () => {
  $('#play').textContent = video.paused ? '播放' : '暫停';
  $('#play').setAttribute('aria-label', video.paused ? '播放' : '暫停');
});
for (const event of ['timeupdate', 'loadedmetadata', 'seeked']) video.addEventListener(event, renderTime);
video.addEventListener('error', () => {
  $('#status').textContent = '影片載入失敗。請確認本集影片檔案已完整解壓縮。';
});
$('#fullscreen').hidden = !document.fullscreenEnabled;
$('#fullscreen').addEventListener('click', async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await $('#screen').requestFullscreen();
  } catch { $('#status').textContent = '此瀏覽器目前無法開啟全螢幕。'; }
});
document.addEventListener('fullscreenchange', () => {
  $('#fullscreen').textContent = document.fullscreenElement ? '離開全螢幕' : '全螢幕';
});
selectDay(Number(location.hash.replace('#day', '')));
window.addEventListener('pagehide', () => controller.destroy(), { once: true });
