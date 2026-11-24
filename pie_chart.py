import csv
import matplotlib.pyplot as plt

def load_totals(filename="expenses.csv"):
    """讀取 csv，回傳每個類別的總金額，例如 {"餐飲": 120, "交通": 50}"""
    totals = {}
    with open(filename, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3:          # 空行或壞掉的行，跳過
                continue
            if row[0] == "date":      # 標題列，跳過
                continue
            try:
                amount = int(row[1])
            except ValueError:        # 金額不是數字，跳過
                continue
            category = row[2]
            totals[category] = totals.get(category, 0) + amount
    return totals

def draw_pie_chart(filename="expenses.csv", show=True):
    """依類別畫出支出圓餅圖，回傳圖片物件 (fig)，方便之後 GUI 使用"""
    totals = load_totals(filename)
    if not totals:
        print("沒有資料可以畫圖。")
        return None

    fig, ax = plt.subplots()
    ax.pie(totals.values(), labels=totals.keys(),
           autopct="%1.1f%%", startangle=90)
    ax.set_title("各類別支出比例")
    ax.axis("equal")

    if show:
        plt.show()
    return fig

if __name__ == "__main__":
    draw_pie_chart()