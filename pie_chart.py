import csv
import matplotlib.pyplot as plt

# 設定中文字型（Windows 內建的微軟正黑體），避免中文變成方框
plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

def load_totals(filename="expenses.csv", month=None):
    """讀取 csv，回傳每個類別的總金額，例如 {"餐飲": 120, "交通": 50}"""
    totals = {}
    with open(filename, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:          # 空行或壞掉的行，跳過
                continue
            if row[0] == "date":      # 標題列，跳過
                continue
            if month and not row[0].startswith(month):   # 不是指定月份，跳過
                continue
            try:
                amount = int(row[1])
            except ValueError:        # 金額不是數字，跳過
                continue
            category = row[2]
            totals[category] = totals.get(category, 0) + amount
    return totals

def draw_pie_chart(filename="expenses.csv", show=True, save_path=None, month=None):
    """依類別畫出支出圓餅圖，回傳圖片物件 (fig)，方便之後 GUI 使用"""
    totals = load_totals(filename, month)
    if not totals:
        print("沒有資料可以畫圖。")
        return None

    total = sum(totals.values())

    def make_label(pct):
        amount = round(pct * total / 100)
        return f"{pct:.1f}%\n${amount}"

    fig, ax = plt.subplots()
    ax.pie(totals.values(), labels=totals.keys(), autopct=make_label, startangle=90)
    title = f"{month} 各類別支出比例" if month else "各類別支出比例"
    ax.set_title(f"{title}（總計 ${total}）")
    ax.axis("equal")

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"圓餅圖已存成 {save_path}")
    if show:
        plt.show()
    return fig

if __name__ == "__main__":
    draw_pie_chart(save_path="pie_chart.png")