from flask import Flask, request, render_template_string
from selenium import webdriver
import urllib.parse
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def form():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Orçamentos</title>
        </head>
        <body>
            <section class="contact" id="contact">
                <h2 class="heading">Orçamentos</h2>

                <form action="/send" method="post">
                    <div class="input-box">
                        <input type="text" name="name" placeholder="Nome Completo" required>
                    </div>
                    <div class="input-box">
                        <select name="event_type" required>
                            <option value="" disabled selected>Tipo de evento</option>
                            <option value="Pré-Wedding">Pré-Wedding</option>
                            <option value="Casamento">Casamento</option>
                            <option value="Aniversário">Aniversário</option>
                            <option value="Debutante">Debutante</option>
                            <option value="Retratos Corporativos">Retratos Corporativos</option>
                            <option value="Eventos Corporativos">Eventos Corporativos</option>
                            <option value="Fotografia de Imóveis">Fotografia de Imóveis</option>
                            <option value="Chá Revelação">Chá Revelação</option>
                        </select>
                    </div>
                    <div class="input-box">
                        <input type="datetime-local" name="datetime" required>
                    </div>
                    <div class="input-box">
                        <input type="number" name="phone" placeholder="Seu número" required>
                    </div>
                    <textarea name="message" cols="30" rows="10" placeholder="Sua mensagem" required></textarea>
                    <input type="submit" value="Send Message" class="btn">
                </form>
            </section>
        </body>
        </html>
    ''')

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    event_type = request.form['event_type']
    datetime_str = request.form['datetime']
    phone = request.form['phone']
    message = request.form['message']

    # Formatar a data e hora para o horário de Brasília
    try:
        datetime_obj = datetime.fromisoformat(datetime_str)
        # Definindo o fuso horário de Brasília
        brt = pytz.timezone('America/Sao_Paulo')
        datetime_brasilia = datetime_obj.astimezone(brt)
        formatted_datetime = datetime_brasilia.strftime('%d/%m/%Y às %H:%M')
    except ValueError:
        formatted_datetime = "Data inválida"

    full_message = f"Nome: {name}\nTipo de evento: {event_type}\nData/Hora: {formatted_datetime}\nMensagem: {message}"
    my_phone_number = '5543999948236'  # Substitua com seu número de telefone no formato internacional sem o sinal de "+"

    whatsapp_url = f"https://web.whatsapp.com/send?phone={my_phone_number}&text={urllib.parse.quote(full_message)}"

    # Automatizar o envio usando Selenium
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Atualize o caminho para o ChromeDriver
    driver.get(whatsapp_url)

    # Aguardar a página carregar e enviar a mensagem
    input_box = driver.find_element("xpath", '//div[@contenteditable="true"][@data-tab="6"]')
    input_box.send_keys(full_message)
    input_box.send_keys(Keys.ENTER)

    return "Mensagem enviada!"

if __name__ == '__main__':
    app.run(debug=True)
