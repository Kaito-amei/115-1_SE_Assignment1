import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# 讓 matplotlib 只負責「畫圖」，不要自己開視窗，視窗交給 tkinter 管
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 月曆選日期（需要先 pip install tkcalendar）
from tkcalendar import Calendar

from expense_input import (FILENAME, init_file, save_expense,
                           parse_date, parse_amount, parse_category)
from pie_chart import draw_pie_chart

CATEGORIES = ["餐飲", "交通", "娛樂", "購物", "生活用品", "其他"]


# ---------- 讀取資料 ----------

def load_records():
    """讀取 CSV 的所有紀錄，回傳 [(行號, 資料), ...]，依日期由新到舊排序。
    行號是這筆資料在 CSV 裡的位置，刪除時靠它找到正確的那一行。"""
    records = []
    try:
        with open(FILENAME, newline="", encoding="utf-8-sig") as f:
            for line_no, row in enumerate(csv.reader(f)):
                if line_no == 0 or len(row) < 3:   # 跳過標題列、空行或壞掉的行
                    continue
                records.append((line_no, row))
    except FileNotFoundError:
        pass
    records.reverse()                   # 同一天的紀錄，後輸入的排前面
    records.sort(key=lambda record: record[1][0], reverse=True)
    return records


def delete_records(line_numbers):
    """刪除 CSV 裡指定行號的資料：全部讀出來，刪掉那幾行，再整個寫回去"""
    with open(FILENAME, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    for line_no in sorted(line_numbers, reverse=True):   # 從後面刪，前面的行號才不會跑掉
        del rows[line_no]
    with open(FILENAME, "w", newline="", encoding="utf-8-sig") as f:
        csv.writer(f).writerows(rows)


def get_months():
    """從 CSV 找出有資料的月份，例如 ["全部", "2026-11", "2026-10"]"""
    months = {row[0][:7] for line_no, row in load_records()}
    return ["全部"] + sorted(months, reverse=True)


# ---------- 列表排序 ----------

sort_column = "date"   # 目前依哪一欄排序
sort_reverse = True    # True = 由大到小（日期就是由新到舊）


def sort_value(row, column):
    """取出這一列要拿來比大小的值"""
    if column == "amount":
        return int(row[1]) if row[1].isdigit() else 0   # 金額要用數字比，不然 "80" 會比 "120" 大
    index = {"date": 0, "category": 2, "note": 3}[column]
    return row[index] if len(row) > index else ""


def on_heading_click(column):
    """點欄位標題：點同一欄就反過來排，點別欄就改用那一欄排"""
    global sort_column, sort_reverse
    if column == sort_column:
        sort_reverse = not sort_reverse
    else:
        sort_column = column
        sort_reverse = column in ("date", "amount")   # 日期、金額預設由大到小
    refresh_table()


# ---------- 更新畫面 ----------

def refresh_table():
    """清空表格，依目前的排序方式重新把所有紀錄放進去"""
    # 在目前排序的欄位標題後面加上箭頭
    for key, title, width, anchor in columns:
        arrow = ""
        if key == sort_column:
            arrow = " ▼" if sort_reverse else " ▲"
        table.heading(key, text=title + arrow)

    table.delete(*table.get_children())
    total = 0
    records = load_records()
    records.sort(key=lambda record: sort_value(record[1], sort_column),
                 reverse=sort_reverse)
    for line_no, row in records:
        date, amount, category = row[0], row[1], row[2]
        note = row[3] if len(row) > 3 else ""
        # iid 是這一列在表格裡的編號，這裡直接用 CSV 的行號
        table.insert("", tk.END, iid=str(line_no),
                     values=(date, amount, category, note))
        if amount.isdigit():
            total += int(amount)
    summary_label.config(text=f"共 {len(records)} 筆，總計 ${total}")


def refresh_months():
    """打開月份下拉選單前，重新讀一次有哪些月份"""
    month_box["values"] = get_months()


# ---------- 按鈕要做的事 ----------

def on_save(event=None):
    """按下「儲存」：檢查輸入 → 存檔 → 更新列表 → 清空金額和備註"""
    try:
        date = parse_date(date_entry.get())
        amount = parse_amount(amount_entry.get())
        category = parse_category(category_box.get())
    except ValueError as e:
        messagebox.showerror("輸入錯誤", str(e))
        return

    note = note_entry.get().strip()
    save_expense(date, amount, category, note)
    status_label.config(text=f"已儲存：{date} {category} {amount} 元")
    refresh_table()

    # 日期和類別保留，方便連續輸入同一天的支出
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)
    amount_entry.focus()


def on_delete(event=None):
    """按下「刪除」：確認後刪掉列表中選取的紀錄（可以一次選多筆）"""
    selected = table.selection()
    if not selected:
        messagebox.showinfo("尚未選取", "請先在列表中點選要刪除的紀錄")
        return

    if len(selected) == 1:
        values = table.item(selected[0], "values")
        message = f"確定要刪除這筆紀錄嗎？\n\n{values[0]}　{values[2]}　{values[1]} 元"
    else:
        message = f"確定要刪除選取的 {len(selected)} 筆紀錄嗎？"
    if not messagebox.askyesno("確認刪除", message):
        return

    delete_records([int(iid) for iid in selected])
    status_label.config(text=f"已刪除 {len(selected)} 筆紀錄")
    refresh_table()


def open_calendar():
    """按下「月曆」：開一個小視窗，點選日期後填回日期欄位"""
    # 月曆一打開就顯示目前日期欄位的那一天，欄位格式不對就顯示今天
    try:
        current = datetime.strptime(date_entry.get().strip(), "%Y-%m-%d")
    except ValueError:
        current = datetime.today()

    popup = tk.Toplevel(root)
    popup.title("選擇日期")
    popup.resizable(False, False)
    popup.transient(root)   # 視窗跟著主視窗，不會跑到後面
    popup.grab_set()        # 選完日期前不能操作主視窗

    cal = Calendar(popup, selectmode="day", date_pattern="yyyy-mm-dd",
                   locale="zh_TW", year=current.year, month=current.month,
                   day=current.day)
    cal.pack(padx=10, pady=10)

    def on_pick(event):
        date_entry.delete(0, tk.END)
        date_entry.insert(0, cal.get_date())
        popup.destroy()

    cal.bind("<<CalendarSelected>>", on_pick)   # 點了某一天就填回去並關閉


def on_show_chart():
    """按下「顯示圓餅圖」：呼叫組員的 draw_pie_chart，畫在新視窗裡"""
    month = month_box.get()
    if month == "全部":
        month = None

    fig = draw_pie_chart(FILENAME, show=False, month=month)
    if fig is None:
        messagebox.showinfo("沒有資料", "目前沒有可以畫圖的資料")
        return
    plt.close(fig)  # 交給 tkinter 顯示，pyplot 這邊就不用再管它

    chart_window = tk.Toplevel(root)
    chart_window.title("支出圓餅圖")
    canvas = FigureCanvasTkAgg(fig, master=chart_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


# ---------- 建立視窗 ----------

init_file()

root = tk.Tk()
root.title("記帳小幫手")
root.resizable(False, False)

# ===== 左邊：輸入表單 =====
form = ttk.Frame(root, padding=16)
form.grid(row=0, column=0, sticky="n")

ttk.Label(form, text="日期").grid(row=0, column=0, sticky="w", pady=4)
# 日期：可以直接打字，也可以按旁邊的「月曆」按鈕用月曆選
date_frame = ttk.Frame(form)
date_frame.grid(row=0, column=1, pady=4, sticky="ew")
date_entry = ttk.Entry(date_frame, width=16)
date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
date_entry.pack(side="left")
ttk.Button(date_frame, text="月曆", width=5,
           command=open_calendar).pack(side="right")

ttk.Label(form, text="金額").grid(row=1, column=0, sticky="w", pady=4)
amount_entry = ttk.Entry(form, width=24)
amount_entry.grid(row=1, column=1, pady=4)

ttk.Label(form, text="類別").grid(row=2, column=0, sticky="w", pady=4)
category_box = ttk.Combobox(form, values=CATEGORIES, width=22)
category_box.set(CATEGORIES[0])
category_box.grid(row=2, column=1, pady=4)

ttk.Label(form, text="備註").grid(row=3, column=0, sticky="w", pady=4)
note_entry = ttk.Entry(form, width=24)
note_entry.grid(row=3, column=1, pady=4)

ttk.Button(form, text="儲存", command=on_save).grid(
    row=4, column=0, columnspan=2, sticky="ew", pady=(12, 4))

status_label = ttk.Label(form, text="", foreground="green")
status_label.grid(row=5, column=0, columnspan=2)

ttk.Separator(form).grid(row=6, column=0, columnspan=2, sticky="ew", pady=12)

ttk.Label(form, text="月份").grid(row=7, column=0, sticky="w", pady=4)
month_box = ttk.Combobox(form, state="readonly", width=22,
                         postcommand=refresh_months)
month_box.grid(row=7, column=1, pady=4)
refresh_months()
month_box.set("全部")

ttk.Button(form, text="顯示圓餅圖", command=on_show_chart).grid(
    row=8, column=0, columnspan=2, sticky="ew", pady=(8, 0))

# ===== 右邊：紀錄列表 =====
list_frame = ttk.Frame(root, padding=(0, 16, 16, 16))
list_frame.grid(row=0, column=1, sticky="n")

ttk.Label(list_frame, text="支出紀錄").grid(row=0, column=0, sticky="w",
                                            pady=(0, 4))

columns = [  # (欄位代號, 標題, 寬度, 對齊)
    ("date", "日期", 100, "center"),
    ("amount", "金額", 70, "e"),
    ("category", "類別", 80, "center"),
    ("note", "備註", 150, "w"),
]
table = ttk.Treeview(list_frame, columns=[c[0] for c in columns],
                     show="headings", height=12)
for key, title, width, anchor in columns:
    table.heading(key, text=title,
                  command=lambda k=key: on_heading_click(k))
    table.column(key, width=width, anchor=anchor)
table.grid(row=1, column=0)

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=1, column=1, sticky="ns")

# 列表下方：左邊刪除按鈕，右邊筆數和總計
bottom_frame = ttk.Frame(list_frame)
bottom_frame.grid(row=2, column=0, sticky="ew", pady=(6, 0))
ttk.Button(bottom_frame, text="刪除選取的紀錄", command=on_delete).pack(side="left")
summary_label = ttk.Label(bottom_frame, text="")
summary_label.pack(side="right")

# 選取紀錄後按鍵盤的 Delete 鍵也能刪除
table.bind("<Delete>", on_delete)

refresh_table()

# 在任何欄位按 Enter 也能儲存
root.bind("<Return>", on_save)
amount_entry.focus()

root.mainloop()
