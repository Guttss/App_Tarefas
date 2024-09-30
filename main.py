import tkinter as tk # usa para criar interfaces graficas, como: janela principal, botões, rótulos, entradas de texto, etc
from tkinter import ttk, font, messagebox, BOTH
from tkinter import PhotoImage


# criando janela
window = tk.Tk()
window.title("Meu app de tarefas")
# definindo cor do fundo
window.configure(background="#F0F0F0")
# definindo dimensões da janela
window.geometry("500x600")

frame_in_edition = None
tasks = []

# função para adicionar tarefa
def add_task():
    global frame_in_edition

    task = task_entry.get().strip()
    if task and task != "Escreva sua tarefa aqui!":
        if frame_in_edition is not None:
            update_task(task)
            frame_in_edition = None
        else:
            add_item_task(task)
            task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, Insira uma tarefa")


def add_item_task(task):
    global tasks

    frame_task = tk.Frame(internal_canvas, background="white", bd=1, relief=tk.SOLID)

    check_var = tk.BooleanVar()
    task_data = {"frame" : frame_task, "task" : task, "status" : "Pendente", "check_var": check_var}
    tasks.append(task_data)

    label_task = tk.Label(frame_task, text=task, font=("Garamond", 16), background="white", width=25, height=2, anchor="w")
    label_task.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    botton_edition = tk.Button(frame_task, image=edit_icon, command=lambda f=frame_task, l = label_task: prepar_edition(f, l), background="white", relief=tk.FLAT,width=20, height=20)
    botton_edition.pack(side=tk.RIGHT, padx=5)

    botton_delete = tk.Button(frame_task, image=delete_icon, command=lambda f=frame_task: delete_task(f), background="white", relief=tk.FLAT, width=20, height=20)
    botton_delete.pack(side=tk.RIGHT, padx=5)
    
    # para posicionar o frame task
    frame_task.pack(fill=tk.X, padx=5, pady=5)

    check_button = ttk.Checkbutton(frame_task, variable=task_data["check_var"], command=lambda : change_status(task_data))
    check_button.pack(side=tk.RIGHT, padx=5)

    internal_canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


# editar as tarefas
def prepar_edition(frame_task, label_task):
    global frame_in_edition
    frame_in_edition = frame_task
    task_entry.delete(0, tk.END)
    task_entry.insert(0, label_task.cget("text"))


def update_task(new_task):
    global frame_in_edition
    for widget in frame_in_edition.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=new_task)


def delete_task(frame_task):
    frame_task.destroy()
    internal_canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# mudar o status da tarefa
def change_status(task_data):
    if task_data["check_var"].get():
        task_data["status"] = "Concluida"
    else:
        task_data["status"] = "Pendente"
    apply_filter() # replicar o filtro sempre que o status mudar 
    

# função para aplicar o filtro
def apply_filter(status_filter = "Todos"):
    for task_data in tasks:
        if status_filter == "Todos":
            # fill = tk.X diz para expandir horizontalmente para preencher todo o espaço disponivel
            task_data["frame"].pack(fill=tk.X, padx=5, pady=5)
        elif status_filter == "Concluidas" and task_data["status"] == "Concluida":
            task_data["frame"].pack(fill=tk.X, padx=5, pady=5)
        elif status_filter== "Pendentes" and task_data["status"] == "Pendente":
            task_data["frame"].pack(fill=tk.X, padx=5, pady=5)
        else:
            task_data["frame"].pack_forget() # esconde a tarefa

# funções para os botões
def show_all_tasks():
    apply_filter("Todos")


def show_complete_tasks():
    apply_filter("Concluidas")


def show_pending_tasks():
    apply_filter("Pendentes")


edit_icon = PhotoImage(file="edit.png").subsample(20, 20)
delete_icon = PhotoImage(file="delete.png").subsample(20, 20)

# fonte do cabeçalho
header_font = font.Font(family="Garamond", size=24, weight="bold")
# criando rótulo
header_label = tk.Label(window, text="Meu App de Tarefas", font = header_font, background="#F0F0F0", fg="#333").pack(pady=20)

frame = tk.Frame(window, background="#F0F0F0")
frame.pack(pady=10)

# campo de entrada
task_entry = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, background="white", fg="gray", width=30)
task_entry.pack(side=tk.LEFT, padx=10)

# botão de adicionar
add_botton = tk.Button(frame, command=add_task, text="Adicionar Tarefa", background="#4CAF50", fg="white", height=1, width=15, font=("Roboto", 11), relief=tk.FLAT)
add_botton.pack(side=tk.LEFT, padx=10)

# Criar um frame para a listar de tarefas com rolagem
task_list_frame = tk.Frame(window, background="white")
task_list_frame.pack(fill=BOTH, expand=True, padx=10, pady=10) 

# tk.Canvas permite desenhar formas geometricas, gráficos, imagens entre outros
canvas = tk.Canvas(task_list_frame, background="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# definindo o scroll bar
scroll_bar = ttk.Scrollbar(task_list_frame, orient="vertical", command=canvas.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

# adicionar os botões
filter_name = tk.Frame(window, background="#F0F0F0")
filter_name.pack(pady=10)

button_all = tk.Button(filter_name, text="Todas", command=show_all_tasks, background="#4CAF50", fg="white", width=10)
button_all.pack(side=tk.LEFT, padx=5)

button_complete = tk.Button(filter_name, text="Concluídas", command=show_complete_tasks, background="#4CAF50", fg="white", width=10)
button_complete.pack(side=tk.LEFT, padx=5)

button_peding = tk.Button(filter_name, text="Pendentes", command=show_pending_tasks, background="#4CAF50", fg="white", width=10)
button_peding.pack(side=tk.LEFT, padx=5)

# para que o scrool bar possa aparecer
canvas.configure(yscrollcommand=scroll_bar.set)
internal_canvas = tk.Frame(canvas, background="white")
canvas.create_window((0, 0), window=internal_canvas, anchor="nw")
internal_canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


# rodar o app
window.mainloop()