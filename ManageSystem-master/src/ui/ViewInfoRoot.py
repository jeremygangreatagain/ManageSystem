from tkinter import *
from tkinter import messagebox
import pandas as pd

# 定义 readR 函数，用于从 Excel 文件读取数据
def readR():
    ioR = r'../lib/Students.xlsx'
    dataR = pd.read_excel(ioR, sheet_name=0, names=['ID', 'Name', 'Sex', 'Age', 'Math', 'C', 'Java'])
    return dataR

# 删除学生记录
def delete_student(student_id):
    global dataR, showInfoRoot
    try:
        dataR = dataR[dataR['ID'] != student_id]  # 从dataR中移除对应ID的学生记录
        dataR.to_excel('../lib/Students.xlsx', index=False)  # 更新Excel文件
        refresh_display(dataR)  # 刷新界面显示
        messagebox.showinfo('提示', '删除成功！')
    except KeyError:
        messagebox.showerror('错误', '学号不存在！')

# 添加学生信息显示
def add_student_info(parent, index, row):
    # 创建一个新的 Frame 作为每条记录的容器
    record_frame = Frame(parent, bg='lightblue', borderwidth=2, relief='groove')
    record_frame.grid(row=index, column=0, sticky="ew", padx=5, pady=2)

    # 为每个字段创建 Label 并添加到 record_frame
    for i, (key, value) in enumerate(row.items(), start=1):
        Label(record_frame, text=f"{key}: {value}", bg='lightblue', anchor=W).grid(row=0, column=i, sticky="ew")

    # 为每行添加一个删除按钮
    delete_button = Button(record_frame, text="删除", command=lambda row_id=row['ID']: delete_student(row_id))
    delete_button.grid(row=0, column=len(row)+1, sticky="ew")

    # 确保每行都有足够的空间
    record_frame.columnconfigure(0, weight=1)
    record_frame.rowconfigure(0, weight=1)

# 刷新显示
def refresh_display(data):
    global showInfoRoot  # 声明全局变量以便访问
    for widget in showInfoRoot.winfo_children():
        widget.destroy()  # 销毁 showInfoRoot 里的 widgets
    for index, row in data.iterrows():  # 获取行的索引和数据
        add_student_info(showInfoRoot, index, row)  # 传递 index 和 row 给 add_student_info

# 添加学生信息窗口
def add_student_window():
    global add_student_root
    add_student_root = Toplevel(viewInfoRoot)  # 创建一个新窗口
    add_student_root.title('添加学生信息')
    add_student_root.geometry('300x300+500+300')

    student_data = {}
    entry_frames = []

    labels = ['ID', 'Name', 'Sex', 'Age', 'Math', 'C', 'Java']
    for i, label in enumerate(labels):
        frame = Frame(add_student_root)
        frame.pack(fill=X)
        Label(frame, text=label, width=10, anchor=E).pack(side=LEFT, padx=5)
        entry = Entry(frame, width=20)
        entry.pack(side=RIGHT, padx=5, expand=True, fill=X)
        student_data[label] = entry
        entry_frames.append(frame)

    def submit_student():
        global dataR
        new_student = {key: entry.get() for key, entry in student_data.items()}
        new_dataR = pd.DataFrame([new_student])
        dataR = pd.concat([dataR, new_dataR], ignore_index=True)
        dataR.to_excel('../lib/Students.xlsx', index=False)
        refresh_display(dataR)
        add_student_root.destroy()

    Button(add_student_root, text="添加", command=submit_student).pack(pady=10)

# 点击"导出"按钮的操作
def clickExportR():
    global dataR
    with open('../lib/export.txt', 'a') as file:
        import datetime
        ntime = datetime.datetime.now()
        stime = ntime.strftime("%Y-%m-%d %H:%M:%S")
        file.write(str(dataR))
        file.write('\n')
        file.write(str(ntime))
        file.write('\n')
    messagebox.showinfo('提示', '导出成功！')

def ViewInfoRoot():
    global viewInfoRoot, showInfoRoot, dataR
    viewInfoRoot = Tk()
    viewInfoRoot.title('欢迎来到学生管理系统！')
    viewInfoRoot.geometry('600x600+300+300')
    viewInfoRoot['bg'] = 'lightblue'

    dataR = readR()  # 读取数据

    showInfoRoot = Frame(viewInfoRoot, bg='lightblue')
    showInfoRoot.pack(expand=True, fill=BOTH)

    refresh_display(dataR)  # 刷新显示

    btnFrame = Frame(viewInfoRoot, bg='lightblue')
    btnFrame.pack(fill=X)

    # 添加 “添加学生” 按钮
    Button(btnFrame, text='添加学生', command=add_student_window, width=10, height=1, relief=GROOVE).grid(row=0, column=2, padx=5)

    # 添加 “返回” 和 “导出” 按钮
    Button(btnFrame, text='返回', width=10, height=1, relief=GROOVE, command=viewInfoRoot.destroy).grid(row=0, column=0, padx=5)
    Button(btnFrame, text='导出', width=10, height=1, relief=GROOVE, command=lambda: clickExportR(showInfoRoot)).grid(row=0, column=1, padx=5)

    viewInfoRoot.mainloop()

if __name__ == '__main__':
    ViewInfoRoot()
