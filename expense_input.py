import csv
import os

filename = "expenses.csv"

if not os.path.exists(filename): #os.path.exists(filename)檢查這個檔案在不在，回傳True或False
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "amount", "category", "notes"])

def ask_amount():
    while True:
        text = input("請輸入金額: ").strip()
        #先嘗試把文字轉成整數，轉失敗(abc之類的)就會跳到except，顯示錯誤訊息
        try:
            amount = int(text)
        except ValueError:
            print("請輸入整數金額。")
            continue
        if amount < 0:
            print("金額不能為負數。")
            continue
        return amount
def ask_date():
    while True:
        date = input("請輸入日期 (YYYY-MM-DD) 或輸入 'q' 退出: ").strip()
        #檢查日期格式是否正確
        if date == "q":
            exit()
        try:
            year, month, day = map(int, date.split('-'))
            if not (1 <= month <= 12 and 1 <= day <= 31 and len(str(year)) == 4):
                raise ValueError
        except ValueError:
            print("日期格式錯誤，請輸入 YYYY-MM-DD。")
            continue
        return date

def ask_category():
    while True:
        category = input("請輸入類別: ").strip()
        if category == "":
            print("類別不能為空。")
            continue
        return category

def ask_notes():
    notes = input("請輸入備註: ").strip()
    return notes

while True:
    date = ask_date()
    amount = ask_amount()
    category = ask_category()
    notes = ask_notes()

    with open(filename, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, notes])

    again = input("是否要繼續輸入? (y/n): ")
    if again.lower() != 'y':
        break

