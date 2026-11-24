import csv

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

if __name__ == "__main__":
    print(load_totals())