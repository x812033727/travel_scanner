// Localized copy for the Flow & Flow Music MCP token scope lives outside messages/<locale>/admin.json
// for the same reason as lib/runpod-copy.ts: those five admin.json files are SHA-256 bound to
// docs/videos/long-form/review.json.

export type FlowMcpTokenCopy = {
  flowAccessLabel: string;
  flowAccessHelp: string;
  flowBadge: string;
  pairFlow: string;
};

const catalogs: Record<string, FlowMcpTokenCopy> = {
  "zh-TW": {
    flowAccessLabel: "可以呼叫 Flow / Flow Music MCP",
    flowAccessHelp: "勾選後，雲端環境可用這組權杖透過站台呼叫主機上的 Google Flow 與 Flow Music MCP（帳號 Cookie 留在主機，每次呼叫皆有審計紀錄）。",
    flowBadge: "Flow MCP",
    pairFlow: "這台電腦也要求透過站台呼叫 Google Flow 與 Flow Music MCP：允許後，它拿到的權杖能操作主機上的生圖、生片與配樂 MCP 工具。",
  },
  "zh-CN": {
    flowAccessLabel: "可以调用 Flow / Flow Music MCP",
    flowAccessHelp: "勾选后，云端环境可用这组令牌通过站点调用主机上的 Google Flow 与 Flow Music MCP（账号 Cookie 留在主机，每次调用均有审计记录）。",
    flowBadge: "Flow MCP",
    pairFlow: "这台电脑也请求通过站点调用 Google Flow 与 Flow Music MCP：允许后，它拿到的令牌可操作主机上的生图、生片与配乐 MCP 工具。",
  },
  en: {
    flowAccessLabel: "May call Flow / Flow Music MCP",
    flowAccessHelp: "Besides narration, cloud sessions with this token may call the host Google Flow and Flow Music MCP servers through this site (account cookies stay on the host; every tool call is audited).",
    flowBadge: "Flow MCP",
    pairFlow: "This computer also asks to call Google Flow and Flow Music MCP through the site: once allowed, its token can invoke Flow and Flow Music MCP tools on the host.",
  },
  ja: {
    flowAccessLabel: "Flow / Flow Music MCP を利用可",
    flowAccessHelp: "チェックすると、クラウド環境がこのトークンでサイト経由の Google Flow / Flow Music MCP を呼び出せます（アカウント Cookie はホストに留まり、呼び出しは監査記録されます）。",
    flowBadge: "Flow MCP",
    pairFlow: "この端末は Google Flow / Flow Music MCP の利用も要求しています。許可すると、ホスト上の Flow / Flow Music MCP ツールを呼び出せます。",
  },
  ko: {
    flowAccessLabel: "Flow / Flow Music MCP 호출 허용",
    flowAccessHelp: "선택하면 클라우드 환경이 이 토큰으로 사이트를 통해 호스트의 Google Flow 및 Flow Music MCP를 호출할 수 있습니다(계정 쿠키는 호스트에 유지되며 모든 호출이 감사 로그에 기록됩니다).",
    flowBadge: "Flow MCP",
    pairFlow: "이 컴퓨터는 사이트를 통한 Google Flow 및 Flow Music MCP 호출도 요청했습니다. 허용하면 호스트의 Flow / Flow Music MCP 도구를 사용할 수 있습니다.",
  },
};

export function flowMcpCopy(locale: string): FlowMcpTokenCopy {
  return catalogs[locale] ?? catalogs.en;
}
