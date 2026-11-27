/**
 * Abstract `FlowDriver` contract and standardized RFC 9457 / exit-code error
 * classifier (strict Fail-Fast policy for Google Flow account safety).
 *
 * Route A ships `GflowCliDriver`. Because the orchestrator and MCP server only
 * talk to this interface, a future `NativeCdpDriver` can be plugged in without
 * touching any guard, ledger, post-processing, or MCP tool schema.
 */

export const NON_RETRYABLE_EXIT_CODES = new Set([
  2,  // usage error
  3,  // auth / reauth required
  11, // configuration / profile locked / invalid option
  17, // model-mode incompatibility
  22, // tier / 403 refusal (NEVER retry: raises WAF heat)
  23, // selector drift / unavailable model (NEVER retry)
  28, // unreachable UI arm (NEVER retry)
  32, // reference not found
  36, // Flow host migrated unsupported request
  37, // insufficient credits
  45, // credit cap exceeded
]);

export class FlowDriverError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = "FlowDriverError";
    this.code = details.code || "driver_error";
    this.exitCode = details.exitCode ?? null;
    this.retryable = Boolean(details.retryable);
    this.charged = details.charged || "no"; // "no" | "maybe" | "yes"
    this.nextAction = details.nextAction || "none";
    this.operationId = details.operationId || null;
    this.remediation = details.remediation || null;
    this.raw = details.raw || null;
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      exitCode: this.exitCode,
      retryable: this.retryable,
      charged: this.charged,
      nextAction: this.nextAction,
      operationId: this.operationId,
      remediation: this.remediation,
    };
  }
}

/**
 * Classifies a driver failure from structured RFC 9457 JSON + process exit code.
 * Enforces Mokaair's strict Fail-Fast rule:
 *   - Any `charged` of `"maybe"` or `"yes"` is NEVER auto-retried (must reconcile).
 *   - Any auth/tier-403/selector-drift/budget error is NEVER auto-retried.
 */
export function isUnbilledWafRejection(errObj = {}, stderr = "") {
  if (errObj?.operation_id) return false;
  const hay = [errObj?.type, errObj?.title, errObj?.detail, stderr]
    .filter(Boolean)
    .join(" ");
  return /waf-rejection|PUBLIC_ERROR_UNUSUAL_ACTIVITY/i.test(hay);
}

export function classifyDriverError({ exitCode = 1, json = null, stderr = "", command = "" } = {}) {
  const errObj = json?.error && typeof json.error === "object" ? json.error : json || {};
  const wafUnbilled = isUnbilledWafRejection(errObj, stderr);
  const charged = wafUnbilled
    ? "no"
    : ["no", "maybe", "yes"].includes(errObj.charged)
      ? errObj.charged
      : exitCode === 9
        ? "maybe"
        : "no";

  let retryable = Boolean(errObj.retryable);
  if (wafUnbilled || NON_RETRYABLE_EXIT_CODES.has(exitCode)) {
    retryable = false;
  }
  if (charged === "maybe" || charged === "yes") {
    retryable = false;
  }

  let nextAction = errObj.next_action || "none";
  if (exitCode === 3) nextAction = "reauth";
  else if (wafUnbilled) nextAction = "cooldown";
  else if (charged === "maybe" || charged === "yes") nextAction = "reconcile";
  else if (exitCode === 37 || exitCode === 45) nextAction = "fix_input";

  const title = errObj.title || errObj.type || `gflow exited with code ${exitCode}`;
  const detail = errObj.detail || (stderr ? stderr.trim().slice(0, 500) : "");
  const message = detail ? `${title}: ${detail}` : title;

  return new FlowDriverError(message, {
    code: errObj.type || `exit_${exitCode}`,
    exitCode,
    retryable,
    charged,
    nextAction,
    operationId: errObj.operation_id || null,
    remediation:
      errObj.remediation_hint ||
      (exitCode === 3
        ? "Run `npm run flow -- login` in a visible desktop session to renew Google Flow authentication."
        : exitCode === 22 || exitCode === 23 || exitCode === 28
          ? "Stop immediately (do NOT auto-retry to protect account heat). Upgrade gflow-cli (`uv tool upgrade gflow-cli`) or inspect Flow UI."
          : exitCode === 37
            ? "Account credits are insufficient for this model. Check balance with `flow_status`."
            : null),
    raw: { command, exitCode, json, stderr: stderr.slice(0, 1000) },
  });
}

/**
 * Base class documenting the required `FlowDriver` contract.
 */
export class FlowDriver {
  constructor({ name = "abstract" } = {}) {
    this.name = name;
  }

  async checkAuth() {
    throw new Error(`${this.name}: checkAuth() not implemented`);
  }

  async getCredits() {
    throw new Error(`${this.name}: getCredits() not implemented`);
  }

  async createProject() {
    throw new Error(`${this.name}: createProject() not implemented`);
  }

  async uploadAsset() {
    throw new Error(`${this.name}: uploadAsset() not implemented`);
  }

  async generateImage() {
    throw new Error(`${this.name}: generateImage() not implemented`);
  }

  async generateVideo() {
    throw new Error(`${this.name}: generateVideo() not implemented`);
  }

  async extendVideo() {
    throw new Error(`${this.name}: extendVideo() not implemented`);
  }

  async createCharacter() {
    throw new Error(`${this.name}: createCharacter() not implemented`);
  }

  async listCharacters() {
    throw new Error(`${this.name}: listCharacters() not implemented`);
  }

  async listProfiles() {
    throw new Error(`${this.name}: listProfiles() not implemented`);
  }

  async listRemoteVideos() {
    throw new Error(`${this.name}: listRemoteVideos() not implemented`);
  }

  async downloadMedia() {
    throw new Error(`${this.name}: downloadMedia() not implemented`);
  }

  async upscaleImage() {
    throw new Error(`${this.name}: upscaleImage() not implemented`);
  }

  async getVersion() {
    return null;
  }

  getLoginCommand() {
    throw new Error(`${this.name}: getLoginCommand() not implemented`);
  }
}
