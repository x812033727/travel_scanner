/**
 * Zero-dependency binary image header dimension reader & 16:9 / 9:16 verifier.
 *
 * Defends against Google Flow's notorious silent `1:1` aspect reset when
 * switching back from Video mode to Image mode (FLOW-PRODUCTION-RULES.md §4.3).
 * Supports PNG, JPEG (SOF0..SOF3), and WebP (VP8 / VP8L / VP8X).
 */

import fs from "node:fs";

const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

export function readImageDimensionsFromBuffer(buf) {
  if (!Buffer.isBuffer(buf) || buf.length < 16) {
    throw new Error("Image buffer is empty or truncated.");
  }

  // PNG: 8-byte signature + 4-byte length + "IHDR" + 4-byte width + 4-byte height
  if (buf.length >= 24 && buf.subarray(0, 8).equals(PNG_SIG)) {
    const chunkType = buf.subarray(12, 16).toString("ascii");
    if (chunkType !== "IHDR") {
      throw new Error(`Invalid PNG header: expected IHDR, got "${chunkType}".`);
    }
    const width = buf.readUInt32BE(16);
    const height = buf.readUInt32BE(20);
    return { format: "png", width, height };
  }

  // JPEG: 0xFF 0xD8 SOI marker, then scan segments until SOF0/1/2/3/5/6/7/9/10/11/13/14/15
  if (buf[0] === 0xff && buf[1] === 0xd8) {
    let offset = 2;
    while (offset + 4 < buf.length) {
      if (buf[offset] !== 0xff) {
        offset += 1;
        continue;
      }
      while (offset < buf.length && buf[offset] === 0xff) offset += 1;
      if (offset >= buf.length) break;
      const marker = buf[offset];
      offset += 1;

      // Standalone markers without length
      if (marker === 0xd8 || marker === 0xd9 || (marker >= 0xd0 && marker <= 0xd7) || marker === 0x01) {
        continue;
      }

      if (offset + 2 > buf.length) break;
      const segLen = buf.readUInt16BE(offset);
      if (segLen < 2 || offset + segLen > buf.length) break;

      const isSof =
        (marker >= 0xc0 && marker <= 0xc3) ||
        (marker >= 0xc5 && marker <= 0xc7) ||
        (marker >= 0xc9 && marker <= 0xcb) ||
        (marker >= 0xcd && marker <= 0xcf);

      if (isSof && offset + 7 < buf.length) {
        const height = buf.readUInt16BE(offset + 3);
        const width = buf.readUInt16BE(offset + 5);
        return { format: "jpeg", width, height };
      }
      offset += segLen;
    }
    throw new Error("Could not find SOF dimension segment in JPEG buffer.");
  }

  // WebP: RIFF....WEBP
  if (
    buf.length >= 30 &&
    buf.subarray(0, 4).toString("ascii") === "RIFF" &&
    buf.subarray(8, 12).toString("ascii") === "WEBP"
  ) {
    const chunk = buf.subarray(12, 16).toString("ascii");
    if (chunk === "VP8X" && buf.length >= 30) {
      const width = 1 + (buf[24] | (buf[25] << 8) | (buf[26] << 16));
      const height = 1 + (buf[27] | (buf[28] << 8) | (buf[29] << 16));
      return { format: "webp", width, height };
    }
    if (chunk === "VP8 " && buf.length >= 30) {
      const width = buf.readUInt16LE(26) & 0x3fff;
      const height = buf.readUInt16LE(28) & 0x3fff;
      return { format: "webp", width, height };
    }
    if (chunk === "VP8L" && buf.length >= 25) {
      const b0 = buf[21];
      const b1 = buf[22];
      const b2 = buf[23];
      const b3 = buf[24];
      const width = 1 + (((b1 & 0x3f) << 8) | b0);
      const height = 1 + (((b3 & 0x0f) << 10) | (b2 << 2) | ((b1 & 0xc0) >> 6));
      return { format: "webp", width, height };
    }
  }

  throw new Error("Unsupported or unrecognized image format (expected PNG, JPEG, or WebP).");
}

export function readImageDimensions(filePath) {
  const buf = fs.readFileSync(filePath);
  return readImageDimensionsFromBuffer(buf);
}

/**
 * Verifies a generated Flow still matches the required resolution & aspect ratio.
 * Explicitly flags square (`1:1`) resets as `aspect_drift_1_1`.
 */
export function verifyStillDimensions(
  filePath,
  {
    expectedWidth = 1376,
    expectedHeight = 768,
    allowScaledRatio = false,
    ratioTolerance = 0.03,
  } = {},
) {
  let dims;
  try {
    dims = readImageDimensions(filePath);
  } catch (err) {
    return {
      ok: false,
      reason: "unreadable_image",
      error: err.message,
      width: null,
      height: null,
      expectedWidth,
      expectedHeight,
    };
  }

  const { width, height, format } = dims;
  const actualRatio = height > 0 ? width / height : 0;
  const expectedRatio = expectedHeight > 0 ? expectedWidth / expectedHeight : 0;

  // Catch Flow's silent 1:1 square reset when non-square output was required
  if (Math.abs(expectedRatio - 1) > 0.1 && Math.abs(actualRatio - 1) <= 0.05) {
    return {
      ok: false,
      reason: "aspect_drift_1_1",
      format,
      width,
      height,
      actualRatio: Number(actualRatio.toFixed(4)),
      expectedWidth,
      expectedHeight,
      expectedRatio: Number(expectedRatio.toFixed(4)),
      message: `Flow silently reset aspect to 1:1 (${width}x${height}) instead of ${expectedWidth}x${expectedHeight}. Re-select widescreen aspect and regenerate.`,
    };
  }

  const exactMatch = width === expectedWidth && height === expectedHeight;
  const ratioMatch =
    expectedRatio > 0 && Math.abs(actualRatio - expectedRatio) / expectedRatio <= ratioTolerance;

  if (exactMatch || (allowScaledRatio && ratioMatch && width >= expectedWidth && height >= expectedHeight)) {
    return {
      ok: true,
      reason: exactMatch ? "exact_match" : "scaled_ratio_match",
      format,
      width,
      height,
      actualRatio: Number(actualRatio.toFixed(4)),
      expectedWidth,
      expectedHeight,
      expectedRatio: Number(expectedRatio.toFixed(4)),
    };
  }

  return {
    ok: false,
    reason: ratioMatch ? "unexpected_resolution" : "aspect_mismatch",
    format,
    width,
    height,
    actualRatio: Number(actualRatio.toFixed(4)),
    expectedWidth,
    expectedHeight,
    expectedRatio: Number(expectedRatio.toFixed(4)),
    message: `Image dimensions ${width}x${height} do not match expected ${expectedWidth}x${expectedHeight}.`,
  };
}
