"""Bundle editorial materials and thumbnails, without large review videos/audio."""
from pathlib import Path
import zipfile

root=Path(__file__).resolve().parents[1]
dest=root/'scripts-and-thumbnails.zip'
included=[]
for file in root.rglob('*'):
    if not file.is_file() or file==dest: continue
    relative=file.relative_to(root)
    if 'voice-cache' in relative.parts or '__pycache__' in relative.parts: continue
    if file.suffix.lower() in {'.mp4','.wav','.zip','.log','.pyc'}: continue
    if 'media' in relative.parts and file.suffix.lower() in {'.png','.jpg'}: continue
    if file.name=='speech-input.json': continue  # machine-specific cache paths
    included.append((file,relative))
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED) as output:
    for file,relative in included: output.write(file,relative.as_posix())
with zipfile.ZipFile(dest) as output:
    assert output.testzip() is None
print(f'{dest.name}: {len(included)} files, {dest.stat().st_size:,} bytes; MP4/WAV excluded.')

videos=root/'review-videos.zip'
media_files=[f for f in (root/'media').rglob('*') if f.is_file() and f.name in {'review.mp4','captions.srt'}]
assert len([f for f in media_files if f.suffix=='.mp4'])==18, 'Expected 6 long videos and 12 Shorts'
with zipfile.ZipFile(videos,'w',compression=zipfile.ZIP_STORED) as output:
    output.write(root/'README.md','README.md')
    for file in media_files: output.write(file,file.relative_to(root).as_posix())
with zipfile.ZipFile(videos) as output:
    assert output.testzip() is None
print(f'{videos.name}: 18 review videos plus SRT subtitles; {videos.stat().st_size:,} bytes.')
