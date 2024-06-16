import pywhatkit as kit
import time
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import threading
import sqlite3

# Inicialização do banco de dados
def init_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT PRIMARY KEY,
            phone_number TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Dicionários para armazenar o mapeamento de nomes para números
contact_mapping = {}

# Função para enviar mensagem pelo WhatsApp
def send_whatsapp_message(phone_number, message, wait_time=10):
    try:
        # Envia a mensagem instantaneamente e fecha a aba após o envio
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=wait_time, tab_close=True, close_time=5)
        print(f"Mensagem enviada para {phone_number}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {phone_number}: {e}")
        messagebox.showerror("Erro", f"Erro ao enviar mensagem para {phone_number}: {e}")
    # Aguarde um tempo curto antes de enviar a próxima mensagem
    time.sleep(10)

# Função para iniciar o envio de mensagens em uma thread separada
def start_sending():
    def send_messages():
        print("Botão de envio pressionado")  # Linha de depuração para confirmar a chamada da função
        entries = text_entries.get("1.0", tk.END).strip().split("\n")
        message = text_message.get("1.0", tk.END).strip()
        
        if not entries or not message:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return
        
        all_numbers = []
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        
        for entry in entries:
            entry = entry.strip()
            cursor.execute('SELECT phone_number FROM contacts WHERE name=?', (entry,))
            result = cursor.fetchone()
            if result:
                phone_number = result[0]
            else:
                phone_number = entry
            
            if not phone_number.startswith("+"):
                messagebox.showwarning("Atenção", f"Número de telefone inválido ou nome não encontrado: {entry}. Deve começar com '+'.")
                continue
            all_numbers.append(phone_number)
        
        progress['maximum'] = len(all_numbers)
        for i, phone_number in enumerate(all_numbers):
            send_whatsapp_message(phone_number, message, wait_time=int(wait_time_var.get()))
            progress['value'] = i + 1
            window.update_idletasks()
        
        conn.close()
        messagebox.showinfo("Concluído", "Envio de mensagens concluído.")
    
    threading.Thread(target=send_messages).start()

# Função para adicionar um novo contato
def add_contact():
    name = simpledialog.askstring("Nome do Contato", "Digite o nome do contato:")
    phone_number = simpledialog.askstring("Número de Telefone", "Digite o número de telefone no formato internacional (ex: +5511999999999):")
    if name and phone_number:
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR REPLACE INTO contacts (name, phone_number) VALUES (?, ?)', (name, phone_number))
        conn.commit()
        conn.close()
        contact_mapping[name] = phone_number
        messagebox.showinfo("Sucesso", f"Contato {name} adicionado com sucesso.")
    else:
        messagebox.showwarning("Atenção", "Nome e número de telefone são obrigatórios.")

# Função para visualizar contatos
def view_contacts():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone_number FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    
    view_window = tk.Toplevel()
    view_window.title("Contatos")
    view_window.geometry("400x300")
    
    text_view = tk.Text(view_window, height=15, width=50)
    text_view.pack(pady=10)
    
    for name, phone_number in contacts:
        text_view.insert(tk.END, f"Nome: {name}, Número: {phone_number}\n")

# Função para editar um contato
def edit_contact():
    name = simpledialog.askstring("Editar Contato", "Digite o nome do contato a ser editado:")
    if name:
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute('SELECT phone_number FROM contacts WHERE name=?', (name,))
        result = cursor.fetchone()
        if result:
            new_phone_number = simpledialog.askstring("Novo Número", "Digite o novo número de telefone no formato internacional (ex: +5511999999999):")
            if new_phone_number:
                cursor.execute('UPDATE contacts SET phone_number=? WHERE name=?', (new_phone_number, name))
                conn.commit()
                conn.close()
                contact_mapping[name] = new_phone_number
                messagebox.showinfo("Sucesso", f"Contato {name} atualizado com sucesso.")
            else:
                messagebox.showwarning("Atenção", "Número de telefone é obrigatório.")
        else:
            conn.close()
            messagebox.showwarning("Erro", "Contato não encontrado.")
    else:
        messagebox.showwarning("Atenção", "Nome é obrigatório.")

# Função para remover um contato
def remove_contact():
    name = simpledialog.askstring("Remover Contato", "Digite o nome do contato a ser removido:")
    if name:
        conn = sqlite3.connect('contacts.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE name=?', (name,))
        conn.commit()
        conn.close()
        if name in contact_mapping:
            del contact_mapping[name]
        messagebox.showinfo("Sucesso", f"Contato {name} removido com sucesso.")
    else:
        messagebox.showwarning("Atenção", "Nome é obrigatório.")

# Função para carregar contatos do banco de dados
def load_data_from_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, phone_number FROM contacts')
    contacts = cursor.fetchall()
    conn.close()
    
    contact_mapping.clear()
    for name, phone_number in contacts:
        contact_mapping[name] = phone_number

# Inicializar banco de dados
init_db()

# Configuração da janela principal
window = tk.Tk()
window.title("Enviar Mensagens WhatsApp")
window.geometry("600x800")

# Configuração do notebook (abas)
notebook = ttk.Notebook(window)
notebook.pack(pady=10, expand=True)

# Frame para a aba de envio de mensagens
frame_send_messages = tk.Frame(notebook, width=600, height=700)
frame_send_messages.pack(fill="both", expand=True)

# Frame para a aba de gerenciamento de contatos
frame_manage_contacts = tk.Frame(notebook, width=600, height=700)
frame_manage_contacts.pack(fill="both", expand=True)

# Adicionar abas ao notebook
notebook.add(frame_send_messages, text="Enviar Mensagens")
notebook.add(frame_manage_contacts, text="Gerenciar Contatos")

# Configuração da aba de envio de mensagens
tk.Label(frame_send_messages, text="Números de Telefone, Nomes (um por linha):").pack(pady=5)
text_entries = tk.Text(frame_send_messages, height=10)
text_entries.pack(pady=5)
tk.Label(frame_send_messages, text="Mensagem:").pack(pady=5)
text_message = tk.Text(frame_send_messages, height=5)
text_message.pack(pady=5)
tk.Label(frame_send_messages, text="Tempo de espera (segundos):").pack(pady=5)
wait_time_var = tk.StringVar(value="10")
wait_time_entry = tk.Entry(frame_send_messages, textvariable=wait_time_var)
wait_time_entry.pack(pady=5)
progress = ttk.Progressbar(frame_send_messages, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=20)
btn_send = tk.Button(frame_send_messages, text="Enviar Mensagens", command=start_sending)
btn_send.pack(pady=10)

# Configuração da aba de gerenciamento de contatos
btn_add_contact = tk.Button(frame_manage_contacts, text="Adicionar Contato", command=add_contact)
btn_add_contact.pack(pady=5)
btn_view_contacts = tk.Button(frame_manage_contacts, text="Visualizar Contatos", command=view_contacts)
btn_view_contacts.pack(pady=5)
btn_edit_contact = tk.Button(frame_manage_contacts, text="Editar Contato", command=edit_contact)
btn_edit_contact.pack(pady=5)
btn_remove_contact = tk.Button(frame_manage_contacts, text="Remover Contato", command=remove_contact)
btn_remove_contact.pack(pady=5)

# Carregar dados do banco de dados ao iniciar
load_data_from_db()

window.mainloop()
