/* Original educational arithmetic, not a FLAC bitstream encoder/decoder. */
(function () {
  'use strict';
  const presets = {
    smooth: [100, 101, 103, 102, 104, 105],
    jump: [100, 101, -100, 103, -99, 105],
  };
  const stereo = { even: [6, 2], odd: [6, 3], negative: [-6, -3], edge: [-32768, 32767] };
  function encode(samples) {
    if (!samples.length || !samples.every(Number.isSafeInteger)) throw new Error('Integer samples required');
    return { first: samples[0], residuals: samples.slice(1).map((value, index) => value - samples[index]) };
  }
  function decode(packet) {
    const values = [packet.first];
    for (const residual of packet.residuals) values.push(values.at(-1) + residual);
    return values;
  }
  function encodeStereo(left, right) {
    return { mid: Math.floor((left + right) / 2), side: left - right };
  }
  function decodeStereo(mid, side, recoverParity = true) {
    const odd = Math.abs(side % 2);
    const sum = 2 * mid + (recoverParity ? odd : 0);
    return { left: Math.floor((sum + side) / 2), right: Math.floor((sum - side) / 2), restoredSum: sum, odd };
  }
  globalThis.losslessDemo = { presets, stereo, encode, decode, encodeStereo, decodeStereo };
}());
