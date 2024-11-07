import tkinter as tk;
import sqlite3 as sql;
from tkinter import messagebox;

root = tk.Tk()
root.title("Sistema de Notas - Alunos")
root_width = 800
root_height = 800

root.configure(background="gray")

form_frame = tk.Frame(root, background="light gray", width=root_width-20, height=root_height / 5)
form_frame.place(x=10, y=10)

form_title = tk.Label(form_frame, text="Fomulário do Aluno", background="light gray");
form_title.place(x=0, y=5)

form_frame.update()
form_title.place(x=(form_frame.winfo_width() / 2) - (form_title.winfo_width() / 2), y=5)

nomeAluno_label = tk.Label(form_frame, text="Nome do Aluno:", background="light gray")
nomeAluno_entry = tk.Entry(form_frame)
matriculaAluno_label = tk.Label(form_frame, text="Matricula:", background="light gray")
matriculaAluno_entry = tk.Entry(form_frame)

form_title_height = form_title.winfo_height() + 15

nomeAluno_label.place(x=10, y=form_title_height)
form_frame.update()
nomeAluno_entry.place(x=10 + nomeAluno_label.winfo_width() + 5, y=form_title_height, width=400)
matriculaAluno_label.place(x= 10 + nomeAluno_label.winfo_width() + 405 + 10, y=form_title_height)

form_frame.update()
matriculaAluno_entry.place(x= 10 + nomeAluno_label.winfo_width() + 405 + 15 + matriculaAluno_label.winfo_width(), y=form_title_height, width=150)

notas_frame_heigth = form_title.winfo_height() + nomeAluno_label.winfo_height()
notas_frame = tk.Frame(form_frame, background="dark gray", width=610, height=50)
notas_frame.place(x=(root_width / 2) - (610 / 2), y=notas_frame_heigth + 30)

nota1Aluno_label    = tk.Label(notas_frame, text="Insira a Nota da A.V. 1", background="light gray")
nota2Aluno_label    = tk.Label(notas_frame, text="Insira a Nota da A.V. 2", background="light gray")
mediaAluno_label    = tk.Label(notas_frame, text="Média",                   background="light gray")
situacaoAluno_label = tk.Label(notas_frame, text="Resultado",               background="light gray")

notas_frame.update()
nota1Aluno_label    .place(x=5,              y=5,   width=150)
nota2Aluno_label    .place(x=5 + 150,        y=5,   width=150)
mediaAluno_label    .place(x=5 + (150*2),    y=5,   width=150)
situacaoAluno_label .place(x=5 + (150*3),    y=5,   width=150)

nota1Aluno_entry    = tk.Entry(notas_frame, justify="center")
nota2Aluno_entry    = tk.Entry(notas_frame, justify="center")
mediaAluno_entry    = tk.Entry(notas_frame, justify="center")
situacaoAluno_entry = tk.Entry(notas_frame, justify="center")

mediaAluno_entry    .config(state="readonly")
situacaoAluno_entry .config(state="readonly")

notas_frame.update()
notas_frame_labels_height = nota1Aluno_label.winfo_height() + 5
nota1Aluno_entry    .place(x=5,             y=notas_frame_labels_height, width=150)
nota2Aluno_entry    .place(x=5 + (150),     y=notas_frame_labels_height, width=150)
mediaAluno_entry    .place(x=5 +  (150*2),  y=notas_frame_labels_height, width=150)
situacaoAluno_entry .place(x=5 +  (150*3),  y=notas_frame_labels_height, width=150)

def limparCampos():
        nomeAluno_entry.delete(0, tk.END)
        matriculaAluno_entry.delete(0, tk.END)
        nota1Aluno_entry.delete(0, tk.END)
        nota2Aluno_entry.delete(0, tk.END)
        mediaAluno_entry.config(state="normal")
        mediaAluno_entry.delete(0, tk.END) 
        mediaAluno_entry.config(state="readonly")
        situacaoAluno_entry.config(state="normal")
        situacaoAluno_entry.delete(0, tk.END)
        situacaoAluno_entry.config(state="readonly")

def calcular_media_das_notas():
    n1 = nota1Aluno_entry.get().strip().replace('.', '').replace(',', '.')
    n2 = nota2Aluno_entry.get().strip().replace('.', '').replace(',', '.')

    if n1 == "" or n2 == "":
        return

    try:
        n1 = float(n1)
        n2 = float(n2)

        if 0 <= n1 <= 10 and 0 <= n2 <= 10:
            media = (n1 + n2) / 2
            mediaAluno_entry.config(state="normal")
            mediaAluno_entry.delete(0, tk.END)
            media_formatada = f"{media:.2f}"
            mediaAluno_entry.insert(0, str(media_formatada).replace('.', ','))
            mediaAluno_entry.config(state="readonly")

            situacaoAluno_entry.config(state="normal")
            if media >= 7:
                situacaoAluno_entry.delete(0, tk.END)
                situacaoAluno_entry.insert(0, "Aprovado")
            else:
                situacaoAluno_entry.delete(0, tk.END)
                situacaoAluno_entry.insert(0, "Reprovado")
            situacaoAluno_entry.config(state="readonly")
        else:
            limparCampos()

    except ValueError as e:
        limparCampos()     

def number(value):
    mask = "##.###.##0,00"
    only_numbers = ''.join(filter(str.isdigit, str(value)))
    if not only_numbers:
        only_numbers = "0"
    
    only_numbers = str(int(only_numbers))
    value_length = len(only_numbers)
    masked_value = ""
    
    for i in range(len(mask) - 1, -1, -1):
        if mask[i] == "#" and value_length == 0:
            break
        elif mask[i] == "#" and value_length != 0:
            masked_value = only_numbers[value_length - 1] + masked_value
            value_length -= 1
        elif mask[i] == "0" and value_length != 0:
            masked_value = only_numbers[value_length - 1] + masked_value
            value_length -= 1
        else:
            masked_value = mask[i] + masked_value
    
    if not masked_value[0].isdigit():
        masked_value = masked_value[1:]
    
    return masked_value

def aplicar_mascara(entry_widget):
    valor = entry_widget.get()
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, number(valor))
    calcular_media_das_notas()

nota1Aluno_entry.bind("<KeyRelease>", lambda event: aplicar_mascara(nota1Aluno_entry))
nota2Aluno_entry.bind("<KeyRelease>", lambda event: aplicar_mascara(nota2Aluno_entry))

root.update()
alunos_panel = tk.Frame(root, background="light gray", width=root_width-20, height=(root_height / 5) * 4 - 30)
alunos_panel.place(x="10", y=form_frame.winfo_height() + 20)

canvas = tk.Canvas(alunos_panel, background="light gray", width=root_width-40, height=(root_height / 5) * 4 - 50)
scrollbar = tk.Scrollbar(alunos_panel, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

content_frame = tk.Frame(canvas, background="light gray")
canvas.create_window((0, 0), window=content_frame, anchor="nw")

header_matricula = tk.Label(content_frame, text="MATRICULA", background="dark gray", font=("Arial", 9, "bold"), width=15)
header_nomeAluno = tk.Label(content_frame, text="ALUNO",     background="dark gray", font=("Arial", 9, "bold"), width=50)
header_nota1     = tk.Label(content_frame, text="NOTA 1",    background="dark gray", font=("Arial", 9, "bold"), width=10)
header_nota2     = tk.Label(content_frame, text="NOTA 2",    background="dark gray", font=("Arial", 9, "bold"), width=10)
header_situacao  = tk.Label(content_frame, text="SITUAÇÃO",  background="dark gray", font=("Arial", 9, "bold"), width=15)

header_matricula    .grid(row=0, column=0, padx=(10, 1), pady=1) 
header_nomeAluno    .grid(row=0, column=1, padx=1,       pady=1)
header_nota1        .grid(row=0, column=2, padx=1,       pady=1)
header_nota2        .grid(row=0, column=3, padx=1,       pady=1)
header_situacao     .grid(row=0, column=4, padx=1,       pady=1)

content_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

banco = sql.connect('alunos.db')
banco.row_factory = sql.Row

cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS alunos (matricula TEXT, nome TEXT, nota_1 TEXT, nota_2 TEXT, situacao TEXT)")
    
def buscar_todos():
    cursor.execute("SELECT * FROM alunos")
    result = [dict(row) for row in cursor.fetchall()]

    for index, aluno in enumerate(result):
        tk.Label(content_frame, text=aluno['matricula'],background="#E9E9E9", width=15)             .grid(row=index + 1, column=0, padx=(10, 1), pady=1, sticky="w")
        tk.Label(content_frame, text=aluno['nome'],     background="#E9E9E9", width=50, anchor="w") .grid(row=index + 1, column=1, padx=1,       pady=1, sticky="w")
        tk.Label(content_frame, text=aluno['nota_1'],   background="#E9E9E9", width=10)             .grid(row=index + 1, column=2, padx=1,       pady=1, sticky="w")
        tk.Label(content_frame, text=aluno['nota_2'],   background="#E9E9E9", width=10)             .grid(row=index + 1, column=3, padx=1,       pady=1, sticky="w")
        tk.Label(content_frame, text=aluno['situacao'], background="#E9E9E9", width=15)             .grid(row=index + 1, column=4, padx=1,       pady=1, sticky="w")

    for widget in content_frame.grid_slaves(row=len(result) + 1):
        widget.destroy()

def salvar_aluno():
    matricula   = matriculaAluno_entry  .get()
    nome_aluno  = nomeAluno_entry       .get()
    nota_1      = nota1Aluno_entry      .get()
    nota_2      = nota2Aluno_entry      .get()
    situacao    = situacaoAluno_entry   .get()

    entrys = [matricula, nome_aluno, nota_1, nota_2, situacao]

    for entry in entrys:
        if entry == "":
            messagebox.showinfo("Atenção", "É necessário o preenchimento de todos os campos")
            return

    cursor.execute(f"SELECT * FROM alunos WHERE matricula = '{matricula}'")
    result = cursor.fetchone()

    if result:
        messagebox.showerror("Erro", "Aluno já existe no banco de dados")
    else:
        cursor.execute(f"INSERT INTO alunos VALUES ('{matricula}', '{nome_aluno}', '{nota_1}', '{nota_2}', '{situacao}')")
        banco.commit()

        buscar_todos()
        limparCampos()

def buscar_matricula():
    matricula = matriculaAluno_entry.get()

    cursor.execute(f"SELECT * FROM alunos WHERE matricula = '{matricula}'")
    result = cursor.fetchone()

    def set_value(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    if result:
        set_value(nomeAluno_entry,  result[1])
        set_value(nota1Aluno_entry, result[2])
        set_value(nota2Aluno_entry, result[3])
        calcular_media_das_notas()
        return True
    else:
        messagebox.showwarning("Aviso", "Matricula não encontrada.")
        return False

def deletar_matricula():
    matricula = matriculaAluno_entry.get()

    if buscar_matricula():
            cursor.execute(f"DELETE FROM alunos WHERE matricula = '{matricula}'")
            banco.commit()

            buscar_todos()
            limparCampos()

def editar_matricula():
    matricula   = matriculaAluno_entry  .get()
    nome_aluno  = nomeAluno_entry       .get()
    nota_1      = nota1Aluno_entry      .get()
    nota_2      = nota2Aluno_entry      .get()
    situacao    = situacaoAluno_entry   .get()

    if buscar_matricula():
        cursor.execute(f"UPDATE alunos SET nome='{nome_aluno}', nota_1='{nota_1}', nota_2='{nota_2}', situacao='{situacao}' WHERE matricula='{matricula}'")
        banco.commit()

        messagebox.showinfo("OK", "Dados do Aluno atualizados")
        buscar_todos()
        limparCampos()

form_frame.update()
btn_salvar   = tk.Button(form_frame, text="Salvar",     command=salvar_aluno)
btn_consulta = tk.Button(form_frame, text="Consultar",  command=buscar_matricula)
btn_editar   = tk.Button(form_frame, text="Editar",     command=editar_matricula)
btn_deletar  = tk.Button(form_frame, text="Deletar",    command=deletar_matricula)

botoes_height = notas_frame_heigth + notas_frame.winfo_height() + 37.5
btn_salvar  .place(x=187.5,  y=botoes_height, width=100)
btn_consulta.place(x=292.5,  y=botoes_height, width=100)
btn_editar  .place(x=397.5,  y=botoes_height, width=100)
btn_deletar .place(x=502.5,  y=botoes_height, width=100)

def centralizar_janela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

centralizar_janela(root, root_width, root_height)

buscar_todos()

root.mainloop()