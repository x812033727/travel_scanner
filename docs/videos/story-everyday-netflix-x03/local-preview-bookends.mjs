// Local-only concept bookends. These are visibly marked as previews and never count as
// the owner's installed channel branding, which lives outside this repository.
import { existsSync } from "node:fs";

import { encodeArgs } from "../../../tools/video/assemble/drama.mjs";

export const INTRO_FRAMES = 150;
export const OUTRO_FRAMES = 630;
const FPS = 30;
const WIDTH = 1920;
const HEIGHT = 1080;
const FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc";
const COLOUR = "format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709";

const label = (text, x, y, size, color, extra = "") =>
  `drawtext=fontfile=${FONT}:text=${text}:fontcolor=${color}:fontsize=${size}:x=${x}:y=${y}${extra}`;

/** A 5 s opening after the hook, or a 21 s end-screen layout after the body. */
export function conceptBookendArgs(kind, outFile) {
  if (kind !== "intro" && kind !== "outro") throw new Error(`unknown concept bookend: ${kind}`);
  const intro = kind === "intro";
  const frames = intro ? INTRO_FRAMES : OUTRO_FRAMES;
  const bg = intro ? "0x14242b" : "0xf2eee4";
  const filters = intro ? [
    "drawbox=x=0:y=0:w=iw:h=20:color=0x36826d:t=fill",
    "drawbox=x=245:y=283:w=1430:h=5:color=0xb49a62:t=fill",
    label("Mokaair", "(w-text_w)/2", 330, 86, "0xf4eddd", ":alpha='min(1,max(0,(t-0.3)*2))'"),
    label("品牌故事", "(w-text_w)/2", 472, 92, "0xe0ba78", ":alpha='min(1,max(0,(t-0.6)*2))'"),
    label("日用品的意外轉身", "(w-text_w)/2", 614, 45, "0xf4eddd", ":alpha='min(1,max(0,(t-1.0)*2))'"),
    label("本機概念試看片  非正式片頭", "(w-text_w)/2", 945, 31, "0xd0dcda"),
    "fade=t=in:st=0:d=0.35",
    "fade=t=out:st=4.55:d=0.45",
  ] : [
    "drawbox=x=0:y=0:w=iw:h=18:color=0x36826d:t=fill",
    "drawbox=x=0:y=1010:w=iw:h=70:color=0x315a4e:t=fill",
    label("Mokaair", "(w-text_w)/2", 75, 72, "0x315a4e"),
    label("喜歡  分享  訂閱", "(w-text_w)/2", 430, 78, "0x315a4e", ":enable='between(t,1,4)'"),
    "drawbox=x=140:y=335:w=600:h=338:color=0x315a4e:t=6:enable='gte(t,4)'",
    "drawbox=x=1180:y=335:w=600:h=338:color=0x315a4e:t=6:enable='gte(t,4)'",
    label("◯", "(w-text_w)/2", 345, 300, "0x315a4e", ":enable='gte(t,4)'"),
    label("最符合觀眾喜好", 230, 715, 40, "0x315a4e", ":enable='gte(t,5)'"),
    label("最新上傳", 1365, 715, 40, "0x315a4e", ":enable='gte(t,5)'"),
    label("訂閱", "(w-text_w)/2", 715, 42, "0x315a4e", ":enable='gte(t,5)'"),
    label("本機概念片尾  影片卡與訂閱鈕須在 YouTube Studio 設定", "(w-text_w)/2", 1020, 27, "0xf4eddd", ":enable='gte(t,4)'"),
  ];
  const graph = `[0:v]${filters.join(",")},${COLOUR}[out]`;
  return encodeArgs(["-f", "lavfi", "-i", `color=c=${bg}:s=${WIDTH}x${HEIGHT}:r=${FPS}:d=${frames / FPS}`], graph, frames, outFile);
}

/** Check the local renderer dependency only when an actual preview is being made. */
export function assertConceptBookendFont() {
  if (!existsSync(FONT)) throw new Error(`the local preview concept font is missing: ${FONT}`);
}

/** Insert instrumental preview music under the concept cards without moving the spoken audio. */
export function bookendedAudioArgs(bodyAudio, musicFile, bodyFrames, hookFrames, outFile) {
  if (!Number.isInteger(bodyFrames) || !Number.isInteger(hookFrames) || hookFrames <= 0 || hookFrames >= bodyFrames) {
    throw new Error("the opening hook must end on a body scene boundary");
  }
  const hookSamples = hookFrames * 1600; // 48 kHz / 30 fps, an exact sample boundary.
  const bodySamples = bodyFrames * 1600;
  const graph = [
    "[0:a]asplit=2[body0][body1]",
    `[body0]atrim=end_sample=${hookSamples},asetpts=PTS-STARTPTS[hook]`,
    `[body1]atrim=start_sample=${hookSamples}:end_sample=${bodySamples},asetpts=PTS-STARTPTS[rest]`,
    "[1:a]asplit=2[music0][music1]",
    "[music0]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:5,asetpts=PTS-STARTPTS,volume=-13dB,afade=t=in:st=0:d=0.5,afade=t=out:st=4.5:d=0.5[intro]",
    "[music1]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:21,asetpts=PTS-STARTPTS,volume=-11dB,afade=t=in:st=0:d=0.8,afade=t=out:st=19.5:d=1.5[outro]",
    "[hook][intro][rest][outro]concat=n=4:v=0:a=1[all]",
  ].join(";");
  return [
    "-hide_banner", "-y", "-loglevel", "error", "-i", bodyAudio, "-stream_loop", "-1", "-i", musicFile,
    "-filter_complex", graph, "-map", "[all]", "-c:a", "aac", "-b:a", "384k", "-ar", "48000", outFile,
  ];
}
