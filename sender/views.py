from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Contact
from .forms import ContactForm
import pywhatkit as kit
import time
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

# Função para enviar mensagem pelo WhatsApp
def send_whatsapp_message(phone_number, message, wait_time=10):
    try:
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=wait_time, tab_close=True, close_time=5)
    except Exception as e:
        print(f"Erro ao enviar mensagem para {phone_number}: {e}")

def send_message(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        entries = request.POST.get('entries').strip().split('\n')
        selected_contacts = request.POST.getlist('selected_contacts')
        message = request.POST.get('message').strip()

        all_numbers = []

        for contact_id in selected_contacts:
            contact = Contact.objects.get(pk=contact_id)
            all_numbers.append(contact.phone_number)

        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue

            if not entry.startswith("+"):
                return render(request, 'sender/send_message.html', {
                    'error': f'O número de telefone "{entry}" não foi encontrado ou está inválido. Verifique se o nome está correto ou insira um número de telefone começando com "+".',
                    'entries': request.POST.get('entries'),
                    'message': message,
                    'contacts': contacts,
                })

            all_numbers.append(entry)

        def send_messages():
            for phone_number in all_numbers:
                send_whatsapp_message(phone_number, message, wait_time=10)
                time.sleep(10)

        threading.Thread(target=send_messages).start()
        return render(request, 'sender/send_message.html', {
            'success': 'Mensagens enviadas com sucesso!',
            'contacts': contacts,
        })

    return render(request, 'sender/send_message.html', {'contacts': contacts})

def home(request):
    return render(request, 'sender/home.html')

def manage_contacts(request):
    contacts = Contact.objects.all()
    return render(request, 'sender/manage_contacts.html', {'contacts': contacts})

def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_contacts')
    else:
        form = ContactForm()
    return render(request, 'sender/add_contact.html', {'form': form})

def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('manage_contacts')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'sender/edit_contact.html', {'form': form})

def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('manage_contacts')
    return render(request, 'sender/delete_contact.html', {'contact': contact})
