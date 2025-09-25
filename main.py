import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os, json

# Arquivo de dados
DATA_FILE = "usuarios.json"

def carregar_dados():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_dados(dados):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# -------------------- Classe principal --------------------
class CaloriasApp:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title(f"Calcule Calorias - Usuário: {usuario}")
        self.root.geometry("900x600")

        # Criar abas notebook
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Aba 1 - Calculadora
        frame_calc = tk.Frame(notebook, bg="white")
        notebook.add(frame_calc, text="Calculadora")

        # Aba 2 - Alimentos Saudáveis
        frame_alimentos = tk.Frame(notebook, bg="white")
        notebook.add(frame_alimentos, text="Alimentos Saudáveis")

        # Aba 3 - Meus Pacientes
        frame_pacientes = tk.Frame(notebook, bg="white")
        notebook.add(frame_pacientes, text="Meus Pacientes")

        # ---- Calculadora ----
        tk.Label(frame_calc, text="Nome do Paciente:", bg="white").pack()
        self.entry_nome_paciente = tk.Entry(frame_calc)
        self.entry_nome_paciente.pack(pady=5)

        tk.Label(frame_calc, text="Peso (kg):", bg="white").pack()
        self.entry_peso = tk.Entry(frame_calc)
        self.entry_peso.pack()

        tk.Label(frame_calc, text="Altura (cm):", bg="white").pack()
        self.entry_altura = tk.Entry(frame_calc)
        self.entry_altura.pack()

        tk.Label(frame_calc, text="Idade:", bg="white").pack()
        self.entry_idade = tk.Entry(frame_calc)
        self.entry_idade.pack()

        tk.Label(frame_calc, text="Sexo (M/F):", bg="white").pack()
        self.entry_sexo = tk.Entry(frame_calc)
        self.entry_sexo.pack()

        tk.Label(frame_calc, text="Nível de atividade:", bg="white").pack()
        self.combo_atividade = ttk.Combobox(frame_calc, values=[
            "Sedentário",
            "Leve (1-3 dias/semana)",
            "Moderado (3-5 dias/semana)",
            "Ativo (6-7 dias/semana)",
            "Muito Ativo (treino 2x/dia)"
        ])
        self.combo_atividade.pack()
        self.combo_atividade.current(0)

        tk.Button(frame_calc, text="Adicionar Paciente / Calcular", command=self.adicionar_calcular_paciente, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

        # ---- Alimentos Saudáveis ----
        tk.Label(frame_alimentos, text="Selecione o paciente:", bg="white").pack(pady=5)
        self.combo_pacientes_alimentos = ttk.Combobox(frame_alimentos, state="readonly")
        self.combo_pacientes_alimentos.pack(pady=5)

        # lista padrão por 100g
        self.alimentos = [
            ("Peito de frango grelhado", 165, 31),
            ("Ovo cozido", 155, 13),
            ("Salmão grelhado", 206, 22),
            ("Atum em lata (água)", 116, 26),
            ("Feijão carioca cozido", 127, 8.7),
            ("Lentilha cozida", 116, 9),
            ("Quinoa cozida", 120, 4.1),
            ("Arroz integral cozido", 111, 2.6),
            ("Batata-doce cozida", 86, 1.4),
            ("Brócolis cozido", 55, 3.7),
            ("Espinafre cozido", 23, 2.9),
            ("Abacate", 160, 2),
            ("Maçã", 52, 0.3),
            ("Banana", 89, 1.1),
            ("Iogurte natural", 61, 3.5),
            ("Queijo cottage", 98, 11),
        ]

        colunas = ("Selecionar", "Alimento", "Calorias (kcal)", "Proteína (g)")
        self.tree_alimentos = ttk.Treeview(frame_alimentos, columns=colunas, show="headings", height=15)
        for col in colunas:
            self.tree_alimentos.heading(col, text=col)
            if col == "Selecionar":
                self.tree_alimentos.column(col, width=70, anchor="center")
            else:
                self.tree_alimentos.column(col, width=200, anchor="center")
        self.tree_alimentos.pack(fill="both", expand=True, padx=10, pady=10)

        self.check_vars = []
        for alimento in self.alimentos:
            var = tk.BooleanVar(value=False)
            self.check_vars.append(var)
            self.tree_alimentos.insert("", "end", values=("", *alimento))

        # clique em qualquer lugar da linha marca/desmarca
        def toggle_checkbox(event):
            item = self.tree_alimentos.identify_row(event.y)
            if not item:
                return
            index = self.tree_alimentos.index(item)
            var = self.check_vars[index]
            var.set(not var.get())
            self.tree_alimentos.set(item, "Selecionar", "✔" if var.get() else "")

        self.tree_alimentos.bind("<Button-1>", toggle_checkbox)

        # Campo para escolher a porção em gramas
        tk.Label(frame_alimentos, text="Informe a porção (g):", bg="white").pack()
        self.entry_porcao = tk.Entry(frame_alimentos)
        self.entry_porcao.insert(0, "100")  # valor padrão
        self.entry_porcao.pack(pady=5)

        tk.Button(frame_alimentos, text="Adicionar Selecionados ao Paciente", command=self.adicionar_selecionado, bg="#FF9800", fg="white").pack(pady=5)
        tk.Button(frame_alimentos, text="Ver dieta do paciente", command=self.ver_dieta_paciente, bg="#4CAF50", fg="white").pack(pady=5)

        # ---- Meus Pacientes ----
        self.tree_pacientes = ttk.Treeview(frame_pacientes, columns=("Nome",), show="headings", height=20)
        self.tree_pacientes.heading("Nome", text="Nome do Paciente")
        self.tree_pacientes.column("Nome", anchor="center", width=300)
        self.tree_pacientes.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(frame_pacientes, bg="white")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Remover Paciente", command=self.remover_paciente, bg="#F44336", fg="white").pack(side="left", padx=5)

        # Carregar dados
        self.dados = carregar_dados()
        if usuario not in self.dados:
            self.dados[usuario] = {"pacientes": {}}
        self.atualizar_pacientes()

    # ---------------- Funções ----------------
    def adicionar_calcular_paciente(self):
        nome = self.entry_nome_paciente.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Digite o nome do paciente!")
            return
        try:
            peso = float(self.entry_peso.get())
            altura = float(self.entry_altura.get())
            idade = int(self.entry_idade.get())
            sexo = self.entry_sexo.get().upper()
            atividade = self.combo_atividade.get()
        except ValueError:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return

        if sexo == "M":
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
        elif sexo == "F":
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)
        else:
            messagebox.showerror("Erro", "Sexo inválido! Use M ou F.")
            return

        fatores = {
            "Sedentário": 1.2,
            "Leve (1-3 dias/semana)": 1.375,
            "Moderado (3-5 dias/semana)": 1.55,
            "Ativo (6-7 dias/semana)": 1.725,
            "Muito Ativo (treino 2x/dia)": 1.9
        }
        get = tmb * fatores.get(atividade, 1.2)

        if nome not in self.dados[self.usuario]["pacientes"]:
            self.dados[self.usuario]["pacientes"][nome] = {"alimentos": [], "dados_calc": {}}
        self.dados[self.usuario]["pacientes"][nome]["dados_calc"] = {
            "peso": peso,
            "altura": altura,
            "idade": idade,
            "sexo": sexo,
            "atividade": atividade,
            "tmb": tmb,
            "get": get
        }
        salvar_dados(self.dados)
        self.atualizar_pacientes()
        messagebox.showinfo("Sucesso", f"Paciente {nome} adicionado com TMB {tmb:.2f} kcal e GET {get:.2f} kcal.")

    def adicionar_selecionado(self):
        nome_paciente = self.combo_pacientes_alimentos.get().strip()
        if not nome_paciente or nome_paciente not in self.dados[self.usuario]["pacientes"]:
            messagebox.showerror("Erro", "Selecione um paciente válido!")
            return

        try:
            porcao = float(self.entry_porcao.get())
            if porcao <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Digite uma porção válida em gramas!")
            return

        adicionados = []
        for idx, var in enumerate(self.check_vars):
            if var.get():
                nome, cal_100g, prot_100g = self.alimentos[idx]

                # regra de 3 proporcional
                cal_total = cal_100g * (porcao / 100)
                prot_total = prot_100g * (porcao / 100)

                # salvar no paciente
                self.dados[self.usuario]["pacientes"][nome_paciente]["alimentos"].append(
                    (f"{nome} ({porcao:.0f}g)", round(cal_total, 2), round(prot_total, 2))
                )
                adicionados.append(f"{nome} ({porcao:.0f}g)")

                # desmarca
                var.set(False)
                self.tree_alimentos.set(self.tree_alimentos.get_children()[idx], "Selecionar", "")

        if not adicionados:
            messagebox.showwarning("Aviso", "Nenhum alimento selecionado!")
            return

        salvar_dados(self.dados)
        messagebox.showinfo("Sucesso", f"Adicionados: {', '.join(adicionados)} ao paciente {nome_paciente}.")

    def atualizar_pacientes(self):
        self.tree_pacientes.delete(*self.tree_pacientes.get_children())
        pacientes = self.dados[self.usuario]["pacientes"].keys()
        for paciente in pacientes:
            self.tree_pacientes.insert("", "end", values=(paciente,))
        self.combo_pacientes_alimentos["values"] = list(pacientes)

    def remover_paciente(self):
        selecionado = self.tree_pacientes.selection()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione um paciente!")
            return
        nome = self.tree_pacientes.item(selecionado[0], "values")[0]
        if messagebox.askyesno("Confirmação", f"Remover paciente {nome}?"):
            del self.dados[self.usuario]["pacientes"][nome]
            salvar_dados(self.dados)
            self.atualizar_pacientes()

    def ver_dieta_paciente(self):
        nome_paciente = self.combo_pacientes_alimentos.get().strip()
        if not nome_paciente or nome_paciente not in self.dados[self.usuario]["pacientes"]:
            messagebox.showerror("Erro", "Selecione um paciente válido!")
            return

        janela = tk.Toplevel(self.root)
        janela.title(f"Dieta de {nome_paciente}")
        janela.geometry("600x400")

        tk.Label(janela, text=f"Dieta de {nome_paciente}", font=("Arial", 14, "bold")).pack(pady=10)

        colunas = ("Alimento", "Calorias (kcal)", "Proteína (g)")
        tree = ttk.Treeview(janela, columns=colunas, show="headings", height=10)
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=180)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        total_cal = 0
        total_prot = 0
        for alimento in self.dados[self.usuario]["pacientes"][nome_paciente]["alimentos"]:
            tree.insert("", "end", values=alimento)
            total_cal += float(alimento[1])
            total_prot += float(alimento[2])

        tk.Label(janela, text=f"Total de Calorias: {total_cal:.2f} kcal", font=("Arial", 12)).pack(pady=5)
        tk.Label(janela, text=f"Total de Proteínas: {total_prot:.2f} g", font=("Arial", 12)).pack(pady=5)

# -------------------- Tela de login --------------------
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Calcule Calorias")
        self.root.geometry("300x250")

        tk.Label(root, text="Usuário:").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack(pady=5)

        tk.Label(root, text="Senha:").pack(pady=5)
        self.entry_senha = tk.Entry(root, show="*")
        self.entry_senha.pack(pady=5)

        tk.Button(root, text="Entrar", command=self.login, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(root, text="Cadastrar", command=self.cadastrar, bg="#2196F3", fg="white").pack()

        self.dados = carregar_dados()

    def login(self):
        usuario = self.entry_user.get().strip()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Digite usuário e senha!")
            return

        if usuario not in self.dados:
            messagebox.showerror("Erro", "Usuário não encontrado!")
            return

        if self.dados[usuario].get("senha") != senha:
            messagebox.showerror("Erro", "Senha incorreta!")
            return

        self.root.destroy()
        nova_root = tk.Tk()
        CaloriasApp(nova_root, usuario)
        nova_root.mainloop()

    def cadastrar(self):
        usuario = self.entry_user.get().strip()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Digite usuário e senha para cadastro!")
            return

        if usuario in self.dados:
            messagebox.showerror("Erro", "Usuário já existe!")
            return

        self.dados[usuario] = {"senha": senha, "pacientes": {}}
        salvar_dados(self.dados)
        messagebox.showinfo("Sucesso", f"Usuário {usuario} cadastrado!")

if __name__ == "__main__":
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()
