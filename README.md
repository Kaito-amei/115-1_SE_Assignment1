# 記帳工具（Expense Tracker）

軟體工程導論 作業一：兩人協作的 Python 記帳工具。
可以輸入每筆支出，並依類別畫出圓餅圖。

## 分工
| 模組 | 檔案 | 負責人 | 分支 |
|---|---|---|---|
| 輸入模組 | `expense_input.py` | 1132951莊雅筑 | `input_module` |
| 圓餅圖模組 | `pie_chart.py` | 1132959張芸芸 | `visualization_module`、`feature_pie_enhance` |

## 安裝
需要 Python 3 和 matplotlib：
```
pip install matplotlib
```

## 使用方式

### 1. 輸入支出
```
python expense_input.py
```
依照提示輸入日期 (YYYY-MM-DD)、金額（正整數）、類別、備註（可空白），可以連續輸入多筆。
資料會存到 `expenses.csv`。輸入 `q` 可離開。

### 2. 畫圓餅圖
```
python pie_chart.py
```
讀取 `expenses.csv`，依類別加總金額並顯示圓餅圖，同時存成 `pie_chart.png`。

圓餅圖功能：
- 每一塊顯示百分比和金額，標題顯示總支出
- 藍色漸層配色，依金額由大到小排序（越深代表金額越大）
- 可以只看某個月份的支出

### 3. 進階用法（在其他程式中使用）
```python
import pie_chart

pie_chart.draw_pie_chart("expenses.csv")                          # 畫全部
pie_chart.draw_pie_chart("expenses.csv", month="2026-11")         # 只畫 2026 年 11 月
pie_chart.draw_pie_chart("expenses.csv", save_path="out.png")     # 存成圖片
fig = pie_chart.draw_pie_chart("expenses.csv", show=False)        # 不跳視窗，回傳 fig（給 GUI 用）
```

用範例資料試跑：
```
python -c "import pie_chart; pie_chart.draw_pie_chart('sample_expenses.csv')"
```

## 資料格式
`expenses.csv`（編碼 utf-8-sig）：

| 欄位 | 說明 |
|---|---|
| date | 日期，YYYY-MM-DD |
| amount | 金額，正整數 |
| category | 類別，例如 餐飲、交通 |
| note | 備註，可空白 |

## 範例圓餅圖
使用 `sample_expenses.csv` 產生：

![範例圓餅圖](sample_pie.png)
