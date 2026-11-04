"""Reproducible local FLAC sample roundtrip; no listening or quality benchmark."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
POOL = ROOT / 'docs/videos/so-thats-why/pool'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def first_frame_assignment(data):
    if data[:4] != b'fLaC':
        raise ValueError('Missing native FLAC marker')
    offset = 4
    while True:
        flag = data[offset]
        size = int.from_bytes(data[offset + 1:offset + 4], 'big')
        offset += 4 + size
        if flag & 128:
            break
    if data[offset] != 255 or data[offset + 1] & 254 != 248:
        raise ValueError('Unexpected first frame sync')
    return data[offset + 3] >> 4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error('ffmpeg is required')
    out = POOL / '.cache/media-probe'
    out.mkdir(parents=True, exist_ok=True)
    # One second of original deterministic integer PCM, including signed extremes
    # and odd L+R cases. Decode equality is over samples, not container metadata.
    samples = [(0, 1), (1, 0), (-1, 0), (0, -1), (32767, -32768),
               (-32768, 32767), (1234, 1235), (-1234, -1235)]
    for i in range(48000 - len(samples)):
        left = round(9000 * math.sin(2 * math.pi * 440 * i / 48000))
        right = left + (i % 7) - 3
        samples.append((left, right))
    pcm = b''.join(struct.pack('<hh', *pair) for pair in samples)
    input_file = out / 'input.s16le'
    input_file.write_bytes(pcm)
    version = subprocess.run([args.ffmpeg, '-version'], check=True,
                             capture_output=True, text=True).stdout.splitlines()[0]
    results = []
    for mode, assignment in [('indep', 1), ('mid_side', 10)]:
        encoded, decoded = out / f'{mode}.flac', out / f'{mode}.s16le'
        encode = [args.ffmpeg, '-v', 'error', '-y', '-f', 's16le', '-ar', '48000',
                  '-ac', '2', '-i', str(input_file), '-c:a', 'flac', '-ch_mode', mode,
                  '-map_metadata', '-1', str(encoded)]
        subprocess.run(encode, check=True, capture_output=True)
        subprocess.run([args.ffmpeg, '-v', 'error', '-y', '-i', str(encoded),
                        '-c:a', 'pcm_s16le', '-f', 's16le', str(decoded)],
                       check=True, capture_output=True)
        encoded_bytes, decoded_bytes = encoded.read_bytes(), decoded.read_bytes()
        actual = first_frame_assignment(encoded_bytes)
        if decoded_bytes != pcm or actual != assignment:
            raise AssertionError(f'Roundtrip or first-frame mode mismatch: {mode}')
        results.append({'requested_mode': mode, 'first_frame_channel_assignment': actual,
                        'decoded_pcm_sha256': sha(decoded_bytes), 'exact_pcm_match': True,
                        'encoded_bytes': len(encoded_bytes),
                        'encoded_sha256': sha(encoded_bytes)})
    receipt = {
        'status': 'PASS_SAMPLE_ROUNDTRIP_ONLY',
        'tested_on': datetime.now(timezone.utc).isoformat(), 'ffmpeg': version,
        'script_sha256': sha(Path(__file__).read_bytes()),
        'batch_sha256': sha((POOL / 'batches/wave5-digital-media.json').read_bytes()),
        'core_ids': ['M5008', 'M5009'],
        'source': 'https://www.rfc-editor.org/rfc/rfc9639.html',
        'source_sections': ['4.2', '4.3', '4.4', '9.1.3'],
        'input': {'frames': len(samples), 'sample_rate': 48000, 'channels': 2,
                  'format': 'signed 16-bit little-endian PCM', 'bytes': len(pcm),
                  'sha256': sha(pcm), 'odd_stereo_sum_pairs': sum((l + r) % 2 for l, r in samples)},
        'results': results,
        'limits': 'Two encoder modes on one synthetic signal. Only first-frame channel assignment inspected; complete decoded samples compared. Does not prove all inputs/codecs, predictor selection, perceptual quality, optimal settings, or a finished demo. No playback or paid media calls.'}
    (POOL / 'reviews/wave5-media-probe.json').write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
