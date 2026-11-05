"""Optional local regression checks; no downloads or model inference."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import semantic

try:
    import numpy as np
except ImportError:
    np = None


@unittest.skipIf(np is None, 'Optional numpy runtime is not installed')
class CacheIntegrity(unittest.TestCase):
    def vector(self, index):
        value = np.zeros(384, dtype=np.float32)
        value[index] = 1
        return value

    def test_interrupted_metadata_commit_preserves_previous_pair(self):
        with tempfile.TemporaryDirectory(prefix='curio-semantic-') as temp:
            directory = Path(temp)
            semantic.save_cache(np, directory, 'v1', {'a': self.vector(0)})
            original = Path.replace

            def interrupted(source, target):
                if Path(target).name == 'embeddings.json':
                    raise OSError('simulated interruption before metadata commit')
                return original(source, target)

            with patch.object(Path, 'replace', interrupted):
                with self.assertRaisesRegex(OSError, 'simulated interruption'):
                    semantic.save_cache(np, directory, 'v1', {'a': self.vector(0), 'b': self.vector(1)})
            self.assertEqual(set(semantic.read_cache(np, directory, 'v1')), {'a'})
            semantic.save_cache(np, directory, 'v1', {'a': self.vector(0), 'b': self.vector(1)})
            self.assertEqual(set(semantic.read_cache(np, directory, 'v1')), {'a', 'b'})
            self.assertEqual(semantic.read_cache(np, directory, 'v2'), {})

    def test_tampered_bytes_and_invalid_matrices_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix='curio-semantic-') as temp:
            directory = Path(temp)
            semantic.save_cache(np, directory, 'v1', {'a': self.vector(0)})
            meta_file = directory / 'embeddings.json'
            metadata = json.loads(meta_file.read_text())
            matrix = directory / metadata['matrix_file']
            matrix.write_bytes(matrix.read_bytes() + b'corruption')
            with self.assertRaisesRegex(ValueError, 'pair mismatch'):
                semantic.read_cache(np, directory, 'v1')
            for values, keys in [
                (np.zeros((1, 383)), ['a']),
                (np.full((1, 384), float('nan')), ['a']),
                (np.zeros((1, 384)), ['a']),
                (np.stack([self.vector(0), self.vector(1)]), ['a', 'a']),
            ]:
                np.save(matrix, values, allow_pickle=False)
                metadata.update(matrix_sha256=semantic.digest(matrix.read_bytes()), keys=keys)
                semantic.write_json(meta_file, metadata)
                with self.assertRaises(ValueError):
                    semantic.read_cache(np, directory, 'v1')
            metadata['matrix_file'] = '../outside.npy'
            semantic.write_json(meta_file, metadata)
            with self.assertRaisesRegex(ValueError, 'filename'):
                semantic.read_cache(np, directory, 'v1')


if __name__ == '__main__':
    unittest.main()
