import csv
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

# 讓 matplotlib 只負責「畫圖」，不要自己開視窗，視窗交給 tkinter 管
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from expense_input import (FILENAME, init_file, save_expense,
                           parse_date, parse_amount, parse_category)
from pie_chart import draw_pie_chart

CATEGORIES = ["餐飲", "交通", "娛樂", "購物", "生活用品", "其他"]


# ---------- 按鈕要做的事 ----------

def on_save(event=None):
    """按下「儲存」：檢查輸入 → 存檔 → 清空金額和備註"""
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

    # 日期和類別保留，方便連續輸入同一天的支出
    amount_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)
    amount_entry.focus()


def get_months():
    """從 CSV 找出有資料的月份，例如 ["全部", "2026-11", "2026-10"]"""
    months = set()
    try:
        with open(FILENAME, newline="", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                if row and row[0] != "date":
                    months.add(row[0][:7])
    except FileNotFoundError:
        pass
    return ["全部"] + sorted(months, reverse=True)


def refresh_months():
    """打開月份下拉選單前，重新讀一次有哪些月份"""
    month_box["values"] = get_months()


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

form = ttk.Frame(root, padding=16)
form.grid()

# 輸入欄位
ttk.Label(form, text="日期").grid(row=0, column=0, sticky="w", pady=4)
date_entry = DateEntry(form, width=21, date_pattern="yyyy-mm-dd", locale="zh_TW")
date_entry.grid(row=0, column=1, pady=4)

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

# 分隔線
ttk.Separator(form).grid(row=6, column=0, columnspan=2, sticky="ew", pady=12)

# 圓餅圖區
ttk.Label(form, text="月份").grid(row=7, column=0, sticky="w", pady=4)
month_box = ttk.Combobox(form, state="readonly", width=22,
                         postcommand=refresh_months)
month_box.grid(row=7, column=1, pady=4)
refresh_months()
month_box.set("全部")

ttk.Button(form, text="顯示圓餅圖", command=on_show_chart).grid(
    row=8, column=0, columnspan=2, sticky="ew", pady=(8, 0))

# 在任何欄位按 Enter 也能儲存
root.bind("<Return>", on_save)
amount_entry.focus()

root.mainloop()
