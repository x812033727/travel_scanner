import tempfile,unittest
from pathlib import Path
from release_hold import acquire,verify,clear
class HoldTests(unittest.TestCase):
    def test_ownership_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'hold';a='a'*40;b='b'*40
            original=acquire('/release/a',a,path)
            self.assertEqual(original,acquire('/release/a',a,path))
            self.assertLessEqual(len(path.read_bytes().splitlines()[0]),600)
            with self.assertRaises(AssertionError):acquire('/release/b',b,path)
            with self.assertRaises(AssertionError):clear('/release/b',b,path)
            self.assertEqual(original,verify('/release/a',a,path))
            clear('/release/a',a,path)
            with self.assertRaises(FileNotFoundError):verify('/release/a',a,path)
    def test_replaced_hold_not_cleared(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'hold';acquire('/release/b','b'*40,path)
            with self.assertRaises(AssertionError):verify('/release/a','a'*40,path)
            self.assertTrue(path.exists())
if __name__=='__main__':unittest.main()
