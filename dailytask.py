from datetime import date
import tkinter as tk
import tkinter.font as font
import csv

# Daily tasks tracker
# Shows the tasks that i wanna do as a checklist, there is a text input area
# to add more tasks. Resets task progress when its a new day.

"""Change Font and size"""
family = "Helvetica"
size = 16

today = date.today()
def main():
    loadDarkmode()
    if not already_opened():
        daily_reset()
    
    global entry
    global label
    global root
    global my_font
    global toggle_button
    root = tk.Tk()
    root.title("Daily Tasks")
    root.bind("<Return>", lambda event: get_input())
      
    my_font = font.Font(family=family, size=size)
    
    load_buttons()
    
    entry_frame = tk.Frame(root)
    entry_frame.pack(side=tk.BOTTOM, fill=tk.X)

    entry = tk.Entry(entry_frame, width=33)
    entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    button = tk.Button(entry_frame, text="Enter", command=get_input)
    button.pack(side=tk.LEFT)
    
    toggle_button = tk.Button(entry_frame, text="Dark Mode", command=toggle_dark_mode)
    toggle_button.pack(side=tk.RIGHT)
    
    if dark_mode:
        try:
            toggle_button.config(text="Light Mode")
            setup_dark_theme()
        except:
            pass
    
    root.mainloop()
    
def backup():
    with open('tasks.csv') as tasks_file:
        with open('date.txt') as date_file:
            tasks_reader = csv.reader(tasks_file)
            date_reader = csv.reader(date_file)
            with open('backup.txt', 'a') as backup_file:
                for row in date_reader:
                    backup_file.write(','.join(row) + '\n')
                for row in tasks_reader:
                    backup_file.write(','.join(row) + '\n')
              
def daily_reset():
    try:
        backup()
        with open("date.txt", "w") as f:
                f.write(str(today))
        with open('tasks.csv') as f:
            reader = csv.reader(f)
            lines = list(reader)
            for line in lines:
                line[1] = "1"
                
        lines = [i for i in lines if i]
    
        f = open("tasks.csv", "w")
        f.truncate()
        f.close()
    
        writer = csv.writer(open('tasks.csv', 'w', newline=''))
        writer.writerows(lines)
    
    except:
        pass
      
def load_buttons():
    try:
        with open('tasks.csv') as f:
            reader = csv.reader(f)
            lines = list(reader)
            for line in lines:
                create_button(line[0])
                if line[1] == "0":
                    task_frame = root.nametowidget(f"task_frame{line[0]}")
                    button = task_frame.nametowidget(f"new_button{line[0]}")
                    button.configure(bg = "gray")
    except:
        return False
                                    
def create_button(text):
    # check if a button with the same name already exists
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame) and widget.winfo_name() == f"task_frame{text}":
            return False
    
    task_frame = tk.Frame(root, name=f"task_frame{text}")
    task_frame.pack(side="top", anchor="w")
    
    new_button = tk.Button(task_frame,font=my_font, text=text,command=lambda: button_on(text), name=f"new_button{text}")
    new_button.pack(side=tk.LEFT)
       
    delete = tk.Button(task_frame, fg="red", text="X", command=lambda: delete_button(text))
    delete.pack(side=tk.RIGHT)
    return True
    
def button_on(text):
    task_frame = root.nametowidget(f"task_frame{text}")
    button = task_frame.nametowidget(f"new_button{text}")   
    with open('tasks.csv') as f:
        reader = csv.reader(f)
        lines = list(reader)
        for line in lines:
            if line[0] == text:
                if line[1] == "0":
                    line[1] = "1"
                    if dark_mode == True:
                        button.configure(bg = "#1E1E1E")
                    else:
                        button.configure(bg = "white")
                    break                    
                if line[1] == "1":
                    line[1] = "0"
                    button.configure(bg = "gray")
                    break   
    f = open("tasks.csv", "w")
    f.truncate()
    f.close()
    
    writer = csv.writer(open('tasks.csv', 'w', newline=''))
    writer.writerows(lines)               

def delete_button(text):
    button = root.nametowidget(f"task_frame{text}")
    with open('tasks.csv') as f:
        reader = csv.reader(f)
        lines = list(reader)
        for line in lines:
            if line[0] == text:
                line.clear()
                
    lines = [i for i in lines if i]
    
    f = open("tasks.csv", "w")
    f.truncate()
    f.close()
    
    writer = csv.writer(open('tasks.csv', 'w', newline=''))
    writer.writerows(lines)
                   
    button.destroy()

def get_input():
    text = entry.get()
    if text == "":
        return False
    if create_button(text):
        print("Task added")
        add_task(text)
    entry.delete(0, tk.END)

def add_task(task):
    with open("tasks.csv", "a") as f:
        f.write(f"{task},1\n")
        
def already_opened():
    try:
        with open("date.txt") as f:
            return f.readline() == str(today)
    except FileNotFoundError:
        with open("date.txt", "w") as f:
            f.write(str(today))
        return False
    
def loadDarkmode():
    global dark_mode
    try:
        with open("darkmode.txt") as f:
            if f.read() == "on":
                dark_mode = True
            else:
                dark_mode = False
    except:
        dark_mode = True
    
def apply_dark_theme(widget):
    #apply dark theme to a widget and its childs
    widget.configure(bg='#1E1E1E', fg='#FFFFFF')   
    if isinstance(widget, tk.Frame):
        for child in widget.winfo_children():
            apply_dark_theme(child)
            
def apply_light_theme(widget):
    #apply light theme to a widget and its childs
    widget.configure(bg='#FFFFFF', fg='#1E1E1E')

    if isinstance(widget, tk.Frame):
        for child in widget.winfo_children():
            apply_light_theme(child)
            
            
def setup_dark_theme():
    # apply the dark theme to all widgets
    root.tk_setPalette(background='#1E1E1E', foreground='#FFFFFF')   
    
    for child in root.winfo_children():
        apply_dark_theme(child)
        
def setup_light_theme():
    # apply the light theme to all widgets
    root.tk_setPalette(background='#FFFFFF', foreground='#1E1E1E')
    
    for child in root.winfo_children():
        apply_light_theme(child)
        
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        toggle_button.config(text="Light Mode")
        with open("darkmode.txt", "w") as f:
            f.write("on")
        try:
            setup_dark_theme()
        except:
            print("Dark mode!")
    else:
        toggle_button.config(text="Dark Mode")
        with open("darkmode.txt", "w") as f:
            f.write("off")
        try:
            setup_light_theme()
        except:
            print("Light mode!")

if __name__ == "__main__":
    main()
