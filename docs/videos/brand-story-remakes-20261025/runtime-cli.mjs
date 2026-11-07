// Use the repository's ordinary CLI with the isolated, correctly named projects.
import path from "node:path";
import { main } from "../../../tools/video/cli.mjs";
import { requiredAssemblyArguments } from "./branding-pr1860/required-assembly.mjs";

const [root, command, ...args] = process.argv.slice(2);
const supported = new Set(["status", "lint", "narrative", "script", "tts", "check-audio", "keyframes", "render", "clips", "music", "assemble", "captions", "i18n-sheet", "i18n-merge", "qa", "package", "review-push", "review-pull", "media-status"]);
if (!root || !path.isAbsolute(root) || !supported.has(command)) {
  throw new Error("Usage: node runtime-cli.mjs <absolute runtime root> <ordinary video CLI command> [arguments]");
}
const resolvedRoot = path.resolve(root);
const commandArgs = command === "assemble" ? requiredAssemblyArguments(resolvedRoot, args) : args;
process.exitCode = await main([command, ...commandArgs], { root: resolvedRoot });
