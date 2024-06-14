# WhatsApp Sender

## Descrição

Este é um projeto de envio automatizado de mensagens pelo WhatsApp utilizando Python e Django. O sistema permite adicionar e gerenciar contatos, bem como enviar mensagens para números de telefone ou contatos previamente cadastrados. O envio das mensagens é feito de forma automatizada através do WhatsApp Web.

## Funcionalidades

- **Gerenciamento de Contatos**:

  - Adicionar, editar e excluir contatos.
  - Visualizar a lista de contatos cadastrados.

- **Envio de Mensagens**:
  - Enviar mensagens para números de telefone inseridos manualmente.
  - Enviar mensagens para contatos selecionados a partir da lista de contatos cadastrados.
  - Envio automatizado utilizando `pywhatkit`.

## Requisitos

- Python 3.6 ou superior
- Django 3.0 ou superior
- `pywhatkit` para o envio das mensagens pelo WhatsApp Web

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/AllanCardosoDev/envio_zap.git
   cd envio_zap
   ```

2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv myenv
   source myenv/bin/activate # No Windows: myenv\Scripts\activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicialize o banco de dados:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser # Para criar um usuário admin
   ```

5. Inicie o servidor Django:

   ```bash
   python manage.py runserver
   ```

6. Acesse o sistema em `http://127.0.0.1:8000`.

## Uso

1. **Gerenciar Contatos**:

   - Acesse a seção "Gerenciar Contatos" no menu de navegação.
   - Adicione novos contatos utilizando o formulário disponível.
   - Edite ou exclua contatos existentes.

2. **Enviar Mensagens**:
   - Acesse a seção "Enviar Mensagem" no menu de navegação.
   - Insira números de telefone manualmente ou selecione contatos já cadastrados.
   - Digite a mensagem desejada e clique em "Enviar".
   - As mensagens serão enviadas automaticamente utilizando o WhatsApp Web.

## Observações

- Certifique-se de que o WhatsApp Web esteja ativo e logado no navegador durante o envio das mensagens.
- O sistema utiliza `pywhatkit` para envio das mensagens, que interage diretamente com o WhatsApp Web.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma nova branch: `git checkout -b minha-branch`.
3. Faça suas alterações e commite-as: `git commit -m 'Minhas alterações'`.
4. Envie suas alterações: `git push origin minha-branch`.
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
