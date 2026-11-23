import csv
import os

filename = "expenses.csv"

if not os.path.exists(filename): #os.path.exists(filename)檢查這個檔案在不在，回傳True或False
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "amount", "category", "notes"])

while True:
    date = input("輸入日期 (YYYY-MM-DD) 或輸入 'q' 退出: ")
    if date.lower() == 'q':
        break
    amount = input("輸入金額: ")
    category = input("輸入類別: ")
    notes = input("輸入備註: ")

    with open(filename, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, notes])

    again = input("是否要繼續輸入? (y/n): ")
    if again.lower() != 'y':
        break