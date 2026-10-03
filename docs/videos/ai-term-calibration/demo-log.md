# 示範紀錄：校準（Calibration）

2026-10-03 在乾淨的 Python 虛擬環境執行，scikit-learn 1.9.1、numpy 2.4.6。資料是 scikit-learn 內建的手寫數字（`load_digits`，不需下載），問題是「這張手寫數字是不是 8」。一半訓練、一半測試，`random_state=0`，同一版本重跑會得到同一組數字。

選手寫數字而不是官方範例的合成資料，是因為觀眾想像得到「認一張圖」；不選醫療或金融資料，是頻道立場第 7 條。

## 可以講的數字

| 模型 | 測試題數 | 整體答對率 | 說「99% 以上確定」的次數 | 那些答案的答對率 |
| --- | --- | --- | --- | --- |
| 樸素貝氏（GaussianNB），未校準 | 899 | 51.7% | 868 | 52.1% |
| 同一個模型，isotonic 校準後 | 899 | 90.3% | 450 | 99.6%（錯 2 題） |
| 邏輯斯迴歸，未另外校準 | 899 | 95.0% | 722 | 99.4% |

- 失敗的樣子：未校準的樸素貝氏有 868 題說「幾乎肯定」，其中錯了一半；說「九成以上」的全部 883 題錯了 424 題。
- 校準不是萬能：校準後信心在 0.8–0.9 的 101 題，平均信心 0.831，實際答對 97%，反而低估自己。
- 準確不等於校準：邏輯斯迴歸整體答對 95%，可是信心 0.9–0.99 那 101 題只答對 86.1%，信心 0.7–0.8 那 18 題只答對 44.4%。
- 用站上預設門檻（0.9 以上採用、介於中間給人看）分三級時，未校準模型幾乎每一題都落在「直接採用」。

旁白只說「一個常見的簡單模型」「校準之後」；模型與方法的名稱只放字卡。

## 腳本

```python
"""Calibration demo for the ai-term-calibration brief. Deterministic: fixed seeds, bundled data."""
import json, sys
import numpy as np, sklearn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss

X, y = load_digits(return_X_y=True)
y = (y == 8).astype(int)  # question: is this handwritten digit an 8?
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.5, random_state=0, stratify=y)
models = {
    "naive_bayes": GaussianNB(),
    "naive_bayes_calibrated": CalibratedClassifierCV(GaussianNB(), method="isotonic", cv=5),
    "logistic": LogisticRegression(max_iter=5000),
}
bins = [(0.0, 0.1), (0.1, 0.5), (0.5, 0.9), (0.9, 1.0001)]
out = {"sklearn": sklearn.__version__, "numpy": np.__version__, "dataset": "load_digits, positive = digit 8",
       "n_train": int(len(ytr)), "n_test": int(len(yte)), "positives_test": int(yte.sum()), "models": {}}
for name, m in models.items():
    m.fit(Xtr, ytr)
    p = m.predict_proba(Xte)[:, 1]
    conf = np.maximum(p, 1 - p)              # confidence in whatever it answered
    pred = (p >= 0.5).astype(int)
    correct = pred == yte
    rows = []
    for lo, hi in [(0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 0.9), (0.9, 0.99), (0.99, 1.0001)]:
        sel = (conf >= lo) & (conf < hi)
        rows.append({"conf_range": [lo, min(hi, 1.0)], "n": int(sel.sum()),
                     "mean_conf": round(float(conf[sel].mean()), 3) if sel.any() else None,
                     "accuracy": round(float(correct[sel].mean()), 3) if sel.any() else None})
    # act / confirm / hold with the site's default thresholds (0.9 / 0.5) on P(yes)
    act = (p >= 0.9) | (p <= 0.1)
    hold = (p > 0.4) & (p < 0.6)
    yes_claims = p >= 0.9
    out["models"][name] = {
        "accuracy": round(float(correct.mean()), 3),
        "brier": round(float(brier_score_loss(yte, p)), 4),
        "reliability_by_confidence": rows,
        "said_yes_at_0.9_plus": {"n": int(yes_claims.sum()), "actually_8": int(yte[yes_claims].sum())},
        "confident_answers_0.9_plus": {"n": int(act.sum()), "wrong": int((~correct[act]).sum())},
        "near_coin_flip_0.4_0.6": int(hold.sum()),
    }
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
```

## 輸出（逐字）

```json
{
 "sklearn": "1.9.1",
 "numpy": "2.4.6",
 "dataset": "load_digits, positive = digit 8",
 "n_train": 898,
 "n_test": 899,
 "positives_test": 87,
 "models": {
  "naive_bayes": {
   "accuracy": 0.517,
   "brier": 0.4772,
   "reliability_by_confidence": [
    {
     "conf_range": [
      0.5,
      0.6
     ],
     "n": 3,
     "mean_conf": 0.541,
     "accuracy": 0.0
    },
    {
     "conf_range": [
      0.6,
      0.7
     ],
     "n": 5,
     "mean_conf": 0.666,
     "accuracy": 0.6
    },
    {
     "conf_range": [
      0.7,
      0.8
     ],
     "n": 5,
     "mean_conf": 0.745,
     "accuracy": 0.6
    },
    {
     "conf_range": [
      0.8,
      0.9
     ],
     "n": 3,
     "mean_conf": 0.87,
     "accuracy": 0.0
    },
    {
     "conf_range": [
      0.9,
      0.99
     ],
     "n": 15,
     "mean_conf": 0.967,
     "accuracy": 0.467
    },
    {
     "conf_range": [
      0.99,
      1.0
     ],
     "n": 868,
     "mean_conf": 1.0,
     "accuracy": 0.521
    }
   ],
   "said_yes_at_0.9_plus": {
    "n": 507,
    "actually_8": 85
   },
   "confident_answers_0.9_plus": {
    "n": 883,
    "wrong": 424
   },
   "near_coin_flip_0.4_0.6": 3
  },
  "naive_bayes_calibrated": {
   "accuracy": 0.903,
   "brier": 0.0761,
   "reliability_by_confidence": [
    {
     "conf_range": [
      0.5,
      0.6
     ],
     "n": 0,
     "mean_conf": null,
     "accuracy": null
    },
    {
     "conf_range": [
      0.6,
      0.7
     ],
     "n": 0,
     "mean_conf": null,
     "accuracy": null
    },
    {
     "conf_range": [
      0.7,
      0.8
     ],
     "n": 323,
     "mean_conf": 0.777,
     "accuracy": 0.746
    },
    {
     "conf_range": [
      0.8,
      0.9
     ],
     "n": 101,
     "mean_conf": 0.831,
     "accuracy": 0.97
    },
    {
     "conf_range": [
      0.9,
      0.99
     ],
     "n": 25,
     "mean_conf": 0.947,
     "accuracy": 1.0
    },
    {
     "conf_range": [
      0.99,
      1.0
     ],
     "n": 450,
     "mean_conf": 1.0,
     "accuracy": 0.996
    }
   ],
   "said_yes_at_0.9_plus": {
    "n": 0,
    "actually_8": 0
   },
   "confident_answers_0.9_plus": {
    "n": 475,
    "wrong": 2
   },
   "near_coin_flip_0.4_0.6": 0
  },
  "logistic": {
   "accuracy": 0.95,
   "brier": 0.0375,
   "reliability_by_confidence": [
    {
     "conf_range": [
      0.5,
      0.6
     ],
     "n": 14,
     "mean_conf": 0.542,
     "accuracy": 0.643
    },
    {
     "conf_range": [
      0.6,
      0.7
     ],
     "n": 12,
     "mean_conf": 0.651,
     "accuracy": 0.333
    },
    {
     "conf_range": [
      0.7,
      0.8
     ],
     "n": 18,
     "mean_conf": 0.756,
     "accuracy": 0.444
    },
    {
     "conf_range": [
      0.8,
      0.9
     ],
     "n": 32,
     "mean_conf": 0.853,
     "accuracy": 0.875
    },
    {
     "conf_range": [
      0.9,
      0.99
     ],
     "n": 101,
     "mean_conf": 0.958,
     "accuracy": 0.861
    },
    {
     "conf_range": [
      0.99,
      1.0
     ],
     "n": 722,
     "mean_conf": 1.0,
     "accuracy": 0.994
    }
   ],
   "said_yes_at_0.9_plus": {
    "n": 61,
    "actually_8": 54
   },
   "confident_answers_0.9_plus": {
    "n": 823,
    "wrong": 18
   },
   "near_coin_flip_0.4_0.6": 14
  }
 }
}
```

## 重現

```bash
python3 -m venv venv && ./venv/bin/pip install scikit-learn==1.9.1
./venv/bin/python demo_calibration.py
```
