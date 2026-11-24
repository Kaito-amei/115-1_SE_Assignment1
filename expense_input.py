import csv
import os
from datetime import datetime 

FILENAME = "expenses.csv"
FIELDS = ["date", "amount", "category", "notes"]

def init_file():
    # 如果expenses.csv不存在，建立一個新的csv檔案，並寫入標題列
    if not os.path.exists(FILENAME): #os.path.exists(FILENAME)檢查這個檔案在不在，回傳1/0
        with open(FILENAME, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(FIELDS)

def parse_amount(text):
    try:
        amount = int(text.strip())
    except ValueError:
        raise ValueError("請輸入整數金額。")
    if amount <= 0:
        raise ValueError("金額不能為零或負數。")
    return amount
    
def parse_date(text):
    text = text.strip()
    #檢查日期格式是否正確
    if text == "":
        return datetime.now().strftime("%Y-%m-%d")  # 如果沒有輸入日期，使用今天的日期
    try:
        datetime.strptime(text, "%Y-%m-%d")  # 嘗試解析日期格式
    except ValueError:
        raise ValueError("日期格式錯誤，請輸入 YYYY-MM-DD。")
    return text

def parse_category(text):
    category = text.strip()
    if category == "":
        raise ValueError("類別不能為空。")
    return category

def ask(prompt, parse_func):
    while True:
        text = input(prompt) #每圈重新要求input一次
        try:
            return parse_func(text)
        except ValueError as e:
            print(e) # 印出parse_func丟回來的錯誤訊息

def save_expense(date, amount, category, notes):
    with open(FILENAME, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, notes])

def main():
    init_file()
    print("---開始記帳---")

    while True:
        t=input("請輸入日期 (YYYY-MM-DD) 或輸入 'q' 退出: ").strip()
        if t.lower() == 'q':
            break
        try:
            date = parse_date(t)
        except ValueError as e:
            print(e)
            continue
        amount = ask("請輸入金額: ", parse_amount)
        category = ask("請輸入類別: ", parse_category)
        notes = input("請輸入備註: ").strip()

        save_expense(date, amount, category, notes)

        again = input("是否要繼續輸入? (y/n): ")
        if again.lower() != 'y':
            break
    print("---記帳結束，資料已存在", FILENAME, "---")

if __name__ == "__main__":
    main()
