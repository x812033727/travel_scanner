"""奇聞檔案局素材池的本機語意近鄰（照原來如此事務所素材池的 semantic.py，路徑與輸入改成 curio）。

Local, advisory semantic neighbours. No automatic merge and no hosted inference.

Optional Python dependencies: numpy, onnxruntime, tokenizers. --prepare downloads
two pinned data files into the ignored pool cache and verifies their SHA-256.
Normal runs are offline; weights, embeddings and candidate text are never uploaded.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time
import urllib.request

os.environ.setdefault('OPENBLAS_NUM_THREADS', '2')
ROOT = Path(__file__).resolve().parents[4]
POOL = ROOT / 'docs/videos/history-curiosity/pool'
EXTERNAL = POOL / 'external/so-thats-why-cores.json'
MODEL = 'Xenova/paraphrase-multilingual-MiniLM-L12-v2'
REVISION = '2c4055b12046f11709e9df2c122e59ffbdc2f900'
FILES = {
    'onnx/model_quantized.onnx': '66fc00f5f29afcaff34092e1bdd20008ca3918265a82fb9695a551e510cc4ebc',
    'tokenizer.json': 'b60b6b43406a48bf3638526314f3d232d97058bc93472ff2de930d43686fa441',
}
CACHE = POOL / '.cache/semantic-v1'
MAX_LENGTH = 128  # Original sentence-transformer model's configured limit.


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(file, value):
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def read_cache(np, directory, namespace):
    metadata_file = directory / 'embeddings.json'
    if not metadata_file.exists():
        return {}
    metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
    if metadata.get('namespace') != namespace:
        return {}
    name = metadata.get('matrix_file', 'embeddings.npy')  # Read the initial cache too.
    if not re.fullmatch(r'embeddings(?:\.[0-9a-f]{64})?\.npy', name):
        raise ValueError('Invalid embedding cache filename')
    matrix_file = directory / name
    if not matrix_file.exists() or digest(matrix_file.read_bytes()) != metadata['matrix_sha256']:
        raise ValueError('Embedding cache pair mismatch')
    values = np.load(matrix_file, allow_pickle=False)
    keys = metadata['keys']
    if values.shape != (len(keys), 384) or len(set(keys)) != len(keys) or not np.isfinite(values).all():
        raise ValueError('Invalid embedding cache shape or values')
    if not np.allclose(np.linalg.norm(values, axis=1), 1, atol=1e-4):
        raise ValueError('Embedding cache is not normalized')
    return dict(zip(keys, values))


def save_cache(np, directory, namespace, cached):
    directory.mkdir(parents=True, exist_ok=True)
    keys = list(cached)
    temp = directory / f'embeddings.{os.getpid()}.next.npy'
    np.save(temp, np.array([cached[key] for key in keys], dtype=np.float32), allow_pickle=False)
    sha = digest(temp.read_bytes())
    matrix_file = directory / f'embeddings.{sha}.npy'
    temp.replace(matrix_file)
    # Metadata is the commit point. An interruption leaves the previous pair intact.
    metadata_temp = directory / f'embeddings.{os.getpid()}.next.json'
    write_json(metadata_temp, {'namespace': namespace, 'keys': keys, 'matrix_file': matrix_file.name, 'matrix_sha256': sha})
    metadata_temp.replace(directory / 'embeddings.json')


def prepare():
    for name, sha in FILES.items():
        target = CACHE / 'model' / name
        if target.exists() and digest(target.read_bytes()) == sha:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            f'https://huggingface.co/{MODEL}/resolve/{REVISION}/{name}',
            headers={'User-Agent': 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'},
        )
        partial = target.with_suffix(target.suffix + '.part')
        with urllib.request.urlopen(request, timeout=60) as response, partial.open('wb') as output:
            while chunk := response.read(1024 * 1024):
                output.write(chunk)
        if digest(partial.read_bytes()) != sha:
            raise ValueError(f'Hash mismatch for {name}; partial retained for diagnosis')
        partial.replace(target)
        print(json.dumps({'downloaded': name, 'verified_sha256': sha}), flush=True)


def run(args):
    if args.prepare:
        prepare()
        return
    import importlib.metadata
    import numpy as np
    import onnxruntime as ort
    from tokenizers import Tokenizer

    started = time.perf_counter()
    for name, sha in FILES.items():
        target = CACHE / 'model' / name
        if not target.exists() or digest(target.read_bytes()) != sha:
            raise ValueError('Missing or changed local model; run --prepare explicitly')
    input_file = ROOT / args.input
    input_bytes = input_file.read_bytes()
    snapshot = json.loads(input_bytes)
    records = snapshot['raw_records']
    if not records or any(not row.get('id') or not row.get('question') for row in records):
        raise ValueError('Input needs nonempty records, IDs and questions')
    if len({row['id'] for row in records}) != len(records):
        raise ValueError('Duplicate input IDs')
    # Produced episodes outside the bank have no finding; their title carries the case.
    texts = [' '.join(part for part in [row['question'], row.get('hook', ''), row.get('answer_target', '')] if part) for row in records]
    external = json.loads(EXTERNAL.read_text(encoding='utf-8'))['cores'] if args.cross_series and EXTERNAL.exists() else []
    texts += [core['question'] for core in external]
    keys = [digest(text.encode('utf-8')) for text in texts]
    namespace = digest(json.dumps([REVISION, FILES, MAX_LENGTH, 'mean-mask-l2-question-hook-answer-v1'], sort_keys=True).encode())
    cached = read_cache(np, CACHE, namespace)
    missing = list(dict.fromkeys(key for key in keys if key not in cached))
    text_by_key = dict(zip(keys, texts))
    options = ort.SessionOptions()
    options.intra_op_num_threads = args.threads
    options.inter_op_num_threads = 1
    session = ort.InferenceSession(str(CACHE / 'model/onnx/model_quantized.onnx'), options, providers=['CPUExecutionProvider']) if missing else None
    tokenizer = Tokenizer.from_file(str(CACHE / 'model/tokenizer.json'))
    pad_id = tokenizer.token_to_id('[PAD]')
    pad_token = '[PAD]'
    if pad_id is None:
        pad_id, pad_token = tokenizer.token_to_id('<pad>'), '<pad>'
    if pad_id is None:
        raise ValueError('Tokenizer has no known padding token')
    tokenizer.enable_truncation(max_length=MAX_LENGTH)
    tokenizer.enable_padding(pad_id=pad_id, pad_token=pad_token)
    truncated = []
    for offset in range(0, len(missing), args.batch_size):
        batch = missing[offset:offset + args.batch_size]
        encoded = tokenizer.encode_batch([text_by_key[key] for key in batch])
        for key, item in zip(batch, encoded):
            if item.overflowing:
                truncated.append(key)
        arrays = {
            'input_ids': np.array([x.ids for x in encoded], dtype=np.int64),
            'attention_mask': np.array([x.attention_mask for x in encoded], dtype=np.int64),
            'token_type_ids': np.array([x.type_ids for x in encoded], dtype=np.int64),
        }
        feed = {item.name: arrays[item.name] for item in session.get_inputs()}
        hidden = session.run(None, feed)[0]
        mask = arrays['attention_mask'][..., None]
        vectors = (hidden * mask).sum(axis=1) / np.clip(mask.sum(axis=1), 1, None)
        vectors = vectors / np.clip(np.linalg.norm(vectors, axis=1, keepdims=True), 1e-12, None)
        for key, vector in zip(batch, vectors):
            cached[key] = vector.astype(np.float32)
        if offset % (args.batch_size * 8) == 0:
            print(json.dumps({'encoded': min(offset + len(batch), len(missing)), 'pending': len(missing), 'elapsed_seconds': round(time.perf_counter() - started, 1)}), flush=True)
    save_cache(np, CACHE, namespace, cached)
    full = np.stack([cached[key] for key in keys])
    matrix = full[:len(records)]
    top_k = min(args.top_k, max(0, len(records) - 1))
    neighbours = []
    cross = []
    if external:
        other = full[len(records):]
        for start in range(0, len(records), 128):
            scores = matrix[start:start + 128] @ other.T
            for i, row_scores in enumerate(scores):
                at = start + i
                chosen = np.argsort(-row_scores, kind='stable')[:3]
                cross.append({'id': records[at]['id'], 'external': [{'id': external[int(j)]['id'], 'question': external[int(j)]['question'], 'cosine': round(float(row_scores[j]), 6)} for j in chosen]})
    for start in range(0, len(records), 128):
        scores = matrix[start:start + 128] @ matrix.T
        for i, row_scores in enumerate(scores):
            at = start + i
            row_scores[at] = -2
            chosen = np.argsort(-row_scores, kind='stable')[:top_k]
            neighbours.append({'id': records[at]['id'], 'neighbours': [{'id': records[int(j)]['id'], 'cosine': round(float(row_scores[j]), 6)} for j in chosen]})
    report = {
        'status': 'ADVISORY_NEIGHBOURS_NOT_MERGE_DECISIONS',
        'input': args.input, 'input_sha256': digest(input_bytes),
        'records': len(records), 'top_k': top_k, 'model': MODEL, 'revision': REVISION,
        'model_files': FILES, 'pooling': 'attention-mask mean, L2 normalized',
        'text': 'question + hook + answer_target (finding); external cores use their question only', 'max_tokens': MAX_LENGTH,
        'new_embeddings': len(missing), 'new_truncated_texts': len(truncated),
        'truncation_note': 'This run counts newly encoded texts only. Long historical answers can lose their tail; use source/lexical neighbours and editorial reading too.',
        'runtime_versions': {m: importlib.metadata.version(m) for m in ['numpy', 'onnxruntime', 'tokenizers']},
        'seconds': round(time.perf_counter() - started, 3), 'neighbours': neighbours,
        'cross_series': {'external_file': str(EXTERNAL.relative_to(ROOT)), 'top_k': 3, 'rows': cross} if external else None,
        'limits': 'Cosine similarity is not a duplicate probability. No fact check, automatic exclusion, or production approval. Text inference stays local.',
    }
    output = ROOT / args.output
    write_json(output, report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('neighbours', 'cross_series')}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--input', default='docs/videos/history-curiosity/pool/pool.json')
    parser.add_argument('--output', default='docs/videos/history-curiosity/pool/.cache/semantic-neighbours.json')
    parser.add_argument('--cross-series', action='store_true', help='also rank the so-thats-why cores against each curio record')
    parser.add_argument('--top-k', type=int, default=10)
    parser.add_argument('--batch-size', type=int, default=16)
    parser.add_argument('--threads', type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.top_k <= 100 or not 1 <= args.batch_size <= 64 or not 1 <= args.threads <= 8:
        parser.error('Invalid bounded top-k, batch size or thread count')
    run(args)
