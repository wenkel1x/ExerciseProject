import tkinter as tk
from tkinter import ttk, messagebox,scrolledtext
import calendar
import datetime
import collect as cl
import os
import threading
import io
import sys
import traceback

def clear_output_text():
    output_text.config(state="normal")
    output_text.delete(1.0,tk.END)
    output_text.config(state='disabled')

def startmain():
    path=file_path_entry.get()
    startmonth=month_menu.get()
    monthnum=monthNum_entry.get()
    clear_output_text()
    captured_output = io.StringIO()

    original_stdout=sys.stdout
    original_stderr=sys.stderr
    sys.stdout=captured_output
    sys.stderr=captured_output
    def run():
        try:
            cl.main(path,startmonth,monthnum)
        except Exception as e:
            traceback.print_exc(file=captured_output)
        finally:
            sys.stdout=original_stdout
            sys.stderr=original_stderr
            output_text.config(state='normal')
            output_text.insert(tk.END,captured_output.getvalue())
            output_text.config(state="disabled")
            output_text.yview(tk.END)

            captured_output.close()
    threading.Thread(target=run).start()

root=tk.Tk()
root.geometry("500x400")
root.title("Oversea Loading by model summary")
subtitle_lable = tk.Label(root,text="create by RosieWang",font=("Arial",12),fg="gray")
subtitle_lable.pack(pady=10)

file_frame=tk.Frame(root)
file_frame.pack(pady=10,padx=10,anchor='w')
file_path_lable=tk.Label(file_frame, text="统计Excel文件路径: ")
file_path_lable.pack(side="left",padx=5)
file_path_entry=tk.Entry(file_frame,width=40)
file_path_entry.pack(side="left",padx=5)
file_path_entry.insert(0,os.getcwd())

#开始月份
month_frame=tk.Frame(root)
month_frame.pack(pady=10,padx=10,anchor='w')

month_lable =tk.Label(month_frame, text="开始月份: ")
month_lable.pack(side="left",padx=5)
current_month = datetime.datetime.now().month

months =[calendar.month_abbr[month].capitalize() for month in range(1,13)]
month_var =tk.StringVar(root)
month_var.set(months[current_month -1])
month_menu=ttk.Combobox(month_frame,textvariable=month_var,values=months)
month_menu.pack(side="left",padx=5)

#获取几个月的结果
monthNum_entry =tk.Frame(root)
monthNum_entry.pack(pady=10,padx=10,anchor='w')
monthNum_lable =tk.Label(monthNum_entry, text="统计月份个数: ")
monthNum_lable.pack(side="left",padx=5)
monthNum_entry=tk.Entry(monthNum_entry,width=20)
monthNum_entry.pack(side="left",padx=5)
monthNum_entry.insert(0,"4")

#编辑json文本
edit_frame=tk.Frame(root)
edit_frame.pack(pady=10,padx=10,anchor='w')
edit_button_1 = tk.Button(edit_frame,text="编辑配置文件",command=lambda: cl.edit_json_fle("Json"))
edit_button_1.pack(side="left",padx=10)
edit_button_2 = tk.Button(edit_frame,text="README.txt",command=lambda: cl.edit_json_fle("Readme"))
edit_button_2.pack(side="left",padx=10)
run_button =tk.Button(edit_frame, text="运行主程序", command=startmain)
run_button.pack(side="left",padx=10)
clear_button=tk.Button(edit_frame,text="Clear Button",command=clear_output_text)
clear_button.pack(side="left",padx=10)

output_text=scrolledtext.ScrolledText(root,state='disabled')
output_text.pack(side="left",padx=10,pady=10,fill=tk.BOTH,expand=True)


root.mainloop()