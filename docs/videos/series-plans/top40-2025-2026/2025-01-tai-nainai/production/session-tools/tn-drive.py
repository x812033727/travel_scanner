#!/usr/bin/env python3
"""《恁祖媽今年18》製作檔傳雲端硬碟（站主 2026-11-10，PR #2059：不再推分支）。

用法：python3 -B tn-drive.py stage e005|…|shared   用硬連結排出那一集的資料夾（不佔空間）
      python3 -B tn-drive.py push  e005|…|shared   stage 後用 todrive.sh 傳到
          videobackup:AI劇/恁祖媽今年18/第005集/製作檔/   （shared → AI劇/恁祖媽今年18/_共用/製作檔/）
      python3 -B tn-drive.py check e005|…|shared   只核對（給沒參與製作的代理）

哪些檔歸哪一集照 tn-bk.py 的 walk()／branches_of()（舊的分支規則：分集與共用各放什麼仍然適用）。
雲端硬碟裡的路徑跟舊分支一樣相對於 ~/mokaair-work/videos/：_scratchpad/…、tai-nainai-e00N/…、tai-nainai-import/…
"""
import importlib.util, os, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tnbk", HERE / "tn-bk.py"); tnbk = importlib.util.module_from_spec(spec); spec.loader.exec_module(tnbk)
TODRIVE = "/home/user/travel_scanner/docs/videos/ai-drama-drive/todrive.sh"
STAGE = Path("/tmp/claude-0/tn-drive-stage")  # 不放在 scratchpad 裡，免得 walk() 把它也算進去

def dest(br: str) -> str:
    return "videobackup:AI劇/恁祖媽今年18/" + ("_共用" if br == "shared" else f"第{br[1:]}集") + "/製作檔"

def stage(br: str) -> Path:
    root = STAGE / br
    if root.exists(): shutil.rmtree(root)
    keep, _ = tnbk.walk(); n = 0
    for local, bpath, is_link in keep:
        if br not in tnbk.branches_of(bpath): continue
        out = root / bpath; out.parent.mkdir(parents=True, exist_ok=True)
        if is_link or os.path.islink(local): os.symlink(os.readlink(local), out)
        else:
            try: os.link(local, out)
            except OSError: shutil.copy2(local, out)
        n += 1
    print(f"staged {br}: {n} files in {root}"); return root

if __name__ == "__main__":
    act, br = sys.argv[1], sys.argv[2]
    root = stage(br) if act in ("stage", "push", "check") else None
    if act == "push": sys.exit(subprocess.run(["bash", TODRIVE, str(root), dest(br)]).returncode)
    if act == "check": sys.exit(subprocess.run(["bash", TODRIVE, "--check", str(root), dest(br)]).returncode)
