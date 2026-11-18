// The words of the extra YouTube channels on the settings tab and of the channel picker on the
// upload card (docs/videos/YOUTUBE-REPORTS.md §頻道; apps/api/app/video_youtube/connection.py).
// They live here rather than in messages/<locale>/admin.json for the reason youtube-reports-copy.ts
// gives: those five files are bound by SHA-256 in docs/videos/long-form/review.json.

const en = {
  title: "Other channels",
  help: "Every channel signs in with the OAuth client above. Add a channel with a short code, then link it and pick that channel's account on Google's screen.",
  none: "No other channel yet.",
  defaultName: "Main channel",
  linked: "Linked",
  broken: "Needs relinking",
  notLinked: "Not linked",
  link: "Link",
  relink: "Link again",
  verify: "Check",
  unlink: "Unlink",
  unlinkConfirm: "Unlink {name}? Its reports kept on the site are deleted with the grant.",
  unlinked: "Unlinked.",
  verified: "Checked.",
  addTitle: "Add a channel",
  key: "Code",
  keyHelp: "2–32 lowercase letters, digits or hyphens, starting with a letter; videos refer to it.",
  label: "Name",
  add: "Add",
  added: "Added. Link it next.",
  needsClient: "Save the OAuth client above first.",
  loadError: "The channels could not be read: {message}",
  pickerLabel: "Channel",
  pickerHelp: "Which channel this video goes to. It cannot change once the video is on YouTube.",
  pickerSaved: "This video now goes to {name}.",
};

type Copy = typeof en;

const zhTW: Copy = {
  title: "其他頻道",
  help: "每個頻道都用上面的 OAuth 用戶端登入。先用一個代號新增頻道，再按連結，在 Google 的畫面選那個頻道的帳號。",
  none: "還沒有其他頻道。",
  defaultName: "主頻道",
  linked: "已連結",
  broken: "要重新連結",
  notLinked: "未連結",
  link: "連結",
  relink: "重新連結",
  verify: "檢查",
  unlink: "解除連結",
  unlinkConfirm: "要解除 {name} 的連結嗎？站上保存的這個頻道的報表會跟授權一起刪掉。",
  unlinked: "已解除連結。",
  verified: "檢查完成。",
  addTitle: "新增頻道",
  key: "代號",
  keyHelp: "2–32 個小寫英文字母、數字或連字號，第一個字是字母；影片用它指定頻道。",
  label: "名稱",
  add: "新增",
  added: "已新增，接著按連結。",
  needsClient: "請先在上面存好 OAuth 用戶端。",
  loadError: "讀不到頻道：{message}",
  pickerLabel: "頻道",
  pickerHelp: "這支影片要上哪個頻道；影片上了 YouTube 之後就不能換。",
  pickerSaved: "這支影片改上 {name}。",
};

const zhCN: Copy = {
  title: "其他频道",
  help: "每个频道都用上面的 OAuth 客户端登录。先用一个代号新增频道，再按连接，在 Google 的页面选那个频道的账号。",
  none: "还没有其他频道。",
  defaultName: "主频道",
  linked: "已连接",
  broken: "需要重新连接",
  notLinked: "未连接",
  link: "连接",
  relink: "重新连接",
  verify: "检查",
  unlink: "解除连接",
  unlinkConfirm: "要解除 {name} 的连接吗？站上保存的这个频道的报表会和授权一起删除。",
  unlinked: "已解除连接。",
  verified: "检查完成。",
  addTitle: "新增频道",
  key: "代号",
  keyHelp: "2–32 个小写英文字母、数字或连字符，第一个字是字母；视频用它指定频道。",
  label: "名称",
  add: "新增",
  added: "已新增，接着按连接。",
  needsClient: "请先在上面保存 OAuth 客户端。",
  loadError: "读不到频道：{message}",
  pickerLabel: "频道",
  pickerHelp: "这支视频要上哪个频道；视频上了 YouTube 之后就不能换。",
  pickerSaved: "这支视频改上 {name}。",
};

const ja: Copy = {
  title: "ほかのチャンネル",
  help: "どのチャンネルも上の OAuth クライアントでログインします。短いコードでチャンネルを追加してから連携し、Google の画面でそのチャンネルのアカウントを選んでください。",
  none: "ほかのチャンネルはまだありません。",
  defaultName: "メインチャンネル",
  linked: "連携済み",
  broken: "再連携が必要",
  notLinked: "未連携",
  link: "連携",
  relink: "再連携",
  verify: "確認",
  unlink: "連携を解除",
  unlinkConfirm: "{name} の連携を解除しますか？サイトに保存したこのチャンネルのレポートも削除されます。",
  unlinked: "連携を解除しました。",
  verified: "確認しました。",
  addTitle: "チャンネルを追加",
  key: "コード",
  keyHelp: "英小文字・数字・ハイフンで 2〜32 文字、先頭は英字。動画はこのコードでチャンネルを指定します。",
  label: "名前",
  add: "追加",
  added: "追加しました。次に連携してください。",
  needsClient: "先に上の OAuth クライアントを保存してください。",
  loadError: "チャンネルを読み込めません：{message}",
  pickerLabel: "チャンネル",
  pickerHelp: "この動画をどのチャンネルに上げるか。YouTube に上がった後は変えられません。",
  pickerSaved: "この動画は {name} に上げます。",
};

const ko: Copy = {
  title: "다른 채널",
  help: "모든 채널은 위의 OAuth 클라이언트로 로그인합니다. 짧은 코드로 채널을 추가한 뒤 연결을 누르고, Google 화면에서 그 채널의 계정을 고르세요.",
  none: "다른 채널이 아직 없습니다.",
  defaultName: "메인 채널",
  linked: "연결됨",
  broken: "다시 연결 필요",
  notLinked: "연결 안 됨",
  link: "연결",
  relink: "다시 연결",
  verify: "확인",
  unlink: "연결 해제",
  unlinkConfirm: "{name}의 연결을 해제할까요? 사이트에 보관한 이 채널의 리포트도 함께 삭제됩니다.",
  unlinked: "연결을 해제했습니다.",
  verified: "확인했습니다.",
  addTitle: "채널 추가",
  key: "코드",
  keyHelp: "영문 소문자·숫자·하이픈 2–32자, 첫 글자는 영문. 동영상은 이 코드로 채널을 지정합니다.",
  label: "이름",
  add: "추가",
  added: "추가했습니다. 이어서 연결하세요.",
  needsClient: "먼저 위의 OAuth 클라이언트를 저장하세요.",
  loadError: "채널을 읽지 못했습니다: {message}",
  pickerLabel: "채널",
  pickerHelp: "이 동영상을 올릴 채널. YouTube에 올라간 뒤에는 바꿀 수 없습니다.",
  pickerSaved: "이 동영상은 {name}에 올립니다.",
};

export type YoutubeChannelsCopy = Copy;
const catalogs: Record<string, Copy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function youtubeChannelsCopy(locale: string): YoutubeChannelsCopy {
  return catalogs[locale] ?? en;
}

/** The code a new channel may have; "default" is the main channel's. */
export const CHANNEL_KEY_PATTERN = /^[a-z][a-z0-9-]{1,31}$/;
