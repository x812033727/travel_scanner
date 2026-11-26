/**
 * Swappable `MusicDriver` interface + Fail-Fast error classification for
 * Mokaair's local Google Flow Music MCP (`mokaair-flow-music`).
 */

export class MusicDriverError extends Error {
  constructor(
    message,
    {
      code = "driver_error",
      statusCode = null,
      retryable = false,
      nextAction = "none",
      remediation = null,
      raw = null,
    } = {},
  ) {
    super(message);
    this.name = "MusicDriverError";
    this.code = code;
    this.statusCode = statusCode;
    this.retryable = Boolean(retryable);
    this.nextAction = nextAction;
    this.remediation = remediation;
    this.raw = raw;
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      statusCode: this.statusCode,
      retryable: this.retryable,
      nextAction: this.nextAction,
      remediation: this.remediation,
    };
  }
}

/**
 * Classifies Flow Music / Chrome CDP failures with strict Fail-Fast discipline:
 * auth expiry, rate limiting / 403, and UI selector drift NEVER auto-retry.
 */
export function classifyMusicError({ code, statusCode = null, message = "", raw = null } = {}) {
  const lower = String(message || "").toLowerCase();

  if (code === "chrome_not_found" || lower.includes("chrome executable")) {
    return new MusicDriverError(message || "Google Chrome was not found on this machine.", {
      code: "chrome_not_found",
      retryable: false,
      nextAction: "install_chrome",
      remediation: "Install Google Chrome or set MOKAAIR_CHROME_BIN to chrome.exe.",
      raw,
    });
  }

  if (statusCode === 401 || code === "auth_expired" || lower.includes("not signed in") || lower.includes("unauthorized")) {
    return new MusicDriverError(message || "Flow Music session is not signed in or has expired.", {
      code: "auth_expired",
      statusCode: statusCode || 401,
      retryable: false,
      nextAction: "relogin",
      remediation: "Run `npm run flow-music -- login` (or `--profile <name>`) and sign into www.flowmusic.app in Chrome.",
      raw,
    });
  }

  if (statusCode === 403 || statusCode === 429 || code === "rate_limited" || lower.includes("rate limit") || lower.includes("403")) {
    return new MusicDriverError(message || "Flow Music refused or rate-limited the request (403/429). Stopping Fail-Fast.", {
      code: "rate_limited",
      statusCode: statusCode || 429,
      retryable: false,
      nextAction: "cooldown_or_switch_profile",
      remediation: "Pause submissions, check account quota in www.flowmusic.app, or switch to another signed-in profile.",
      raw,
    });
  }

  if (code === "selector_drift" || lower.includes("composer input not found")) {
    return new MusicDriverError(message || "Flow Music web composer DOM changed (selector drift). Stopping Fail-Fast.", {
      code: "selector_drift",
      retryable: false,
      nextAction: "update_selectors",
      remediation: "Inspect www.flowmusic.app composer selectors in chrome-cdp-driver.mjs or generate manually and run music_download.",
      raw,
    });
  }

  return new MusicDriverError(message || "Flow Music driver failed.", {
    code: code || "driver_error",
    statusCode,
    retryable: false,
    nextAction: "inspect_error",
    raw,
  });
}

/**
 * Abstract contract implemented by `ChromeCdpMusicDriver` (and mock drivers in tests).
 */
export class MusicDriver {
  constructor({ name = "abstract" } = {}) {
    this.name = name;
  }

  async checkAuth(_opts) {
    throw new Error(`${this.name}: checkAuth() not implemented`);
  }

  async listProfiles(_opts) {
    throw new Error(`${this.name}: listProfiles() not implemented`);
  }

  async listRemoteClips(_opts) {
    throw new Error(`${this.name}: listRemoteClips() not implemented`);
  }

  async downloadClip(_opts) {
    throw new Error(`${this.name}: downloadClip() not implemented`);
  }

  async generateTrack(_opts) {
    throw new Error(`${this.name}: generateTrack() not implemented`);
  }
}
