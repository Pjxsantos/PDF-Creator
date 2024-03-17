# Programa assinado por PAULO XAVIER

import textwrap
import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def update_char_count(event=None):
    char_count.set(f"Caracteres digitados: {len(text_input.get('1.0', 'end'))}")

def create_pdf():
    # Obter o título e o texto do input
    title = title_input.get()
    text_lines = text_input.get("1.0", "end-1c").split('\n')
    
    # Limitar cada linha a 64 caracteres
    text_lines = [textwrap.fill(line, 64) for line in text_lines]
    text_lines = '\n'.join(text_lines).split('\n')
    
    # Criar um objeto canvas para desenhar no PDF
    c = canvas.Canvas("seu_pdf_personalizado.pdf", pagesize=letter)
    
    # Definir as dimensões da página
    page_width, page_height = c._pagesize
    
    # Variável para controlar a numeração das páginas
    page_num = 1
    
    # Variável para limitar a quantidade de linhas por página
    lines_per_page = 34  # Altere este valor conforme necessário
    lines_count = 0
    
    # Função para converter número da página para hexadecimal
    def to_hex(num):
        return hex(num)[2:].upper()
    
    # Função para adicionar cabeçalho, rodapé e numeração de página
    def add_header_footer(canvas, page_num, frame_width, page_width, page_height):
        # Adicionar data e hora no rodapé do quadro
        now = datetime.now()
        date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
        canvas.setFont("Helvetica", 10)  # Definir o tamanho da fonte para 10
        canvas.setFillColor('black')  # Definir a cor do texto para preto
        canvas.drawString(frame_width + 10, 20, f"{date_time_string}")
        
        # Numeração de páginas em hexadecimal
        canvas.drawString(page_width - frame_width + 10, 20, f"Página {to_hex(page_num)}")
    
    # Adicionar o logotipo no canto esquerdo com fundo cinza
    logo_area_width = page_width * 0.2
    c.setFillColor('grey')
    c.rect(0, 0, logo_area_width, page_height, fill=1)
    c.drawImage(logo_path, 10, page_height - 100 - 10, width=100, height=100)
    
    # Desenhar um quadro estilizado que ocupa 80% da largura da página
    frame_width = page_width * 0.8
    frame_height = page_height
    c.setStrokeColor('black')  # Definir a cor da linha para preto
    c.setFillColor('white')    # Definir a cor de preenchimento para branco
    c.rect(logo_area_width, 0, frame_width, frame_height, fill=1)
    
    # Adicionar o título em negrito e alinhado com o texto dentro do quadro
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor('black')  # Definir a cor do texto para preto
    c.drawString(logo_area_width + 10, 720, title)
    
    # Iniciar a posição y para o texto abaixo do título
    y_position = 700
    
    # Adicionar o texto linha por linha dentro do quadro
    c.setFont("Helvetica", 10)
    c.setFillColor('black')  # Definir a cor do texto para preto
    for line in text_lines:
        if lines_count >= lines_per_page:  # Verificar se é necessário criar uma nova página
            add_header_footer(c, page_num, frame_width, page_width, page_height)
            c.showPage()
            c.setStrokeColor('black')
            c.setFillColor('white')
            c.rect(logo_area_width, 0, frame_width, frame_height, fill=1)
            c.setFillColor('grey')
            c.rect(0, 0, logo_area_width, page_height, fill=1)
            c.drawImage(logo_path, 10, page_height - 100 - 10, width=100, height=100)
            y_position = 720
            page_num += 1
            lines_count = 0
            add_header_footer(c, page_num, frame_width, page_width, page_height)  # Adicionar cabeçalho e rodapé na nova página
        c.drawString(logo_area_width + 10, y_position, line)
        y_position -= 20
        lines_count += 1
    
    # Salvar o PDF
    c.save()
    
    # Mensagem de confirmação
    confirmation_label.config(bg='#808080', text="PDF criado com sucesso!", fg='green')  # Cor do texto alterada para verde


def select_logo():
    global logo_path
    logo_path = filedialog.askopenfilename()
    logo_label.config(text=f"Logotipo selecionado: {logo_path}")

# Criar a janela principal
root = tk.Tk()
root.title("Criador de PDF Personalizado")
root.configure(bg='#808080')  # Define a cor de fundo para azul claro

# Variável para o caminho do logotipo
logo_path = ""

# Adicionar widgets com estilos personalizados
logo_button = tk.Button(root, text="Selecionar Logotipo", command=select_logo,
                        bg='#4b6da7', fg='white', borderwidth=0, highlightthickness=0,
                        activebackground='#87CEEB', activeforeground='white')
logo_button.grid(row=0, column=0, padx=10, pady=10)

logo_label = tk.Label(root, text="", bg='#808080', fg='black')
logo_label.grid(row=1, column=0, padx=10)

title_label = tk.Label(root, text="Título:", bg='#808080', fg='black')
title_label.grid(row=2, column=0, padx=10)

title_input = tk.Entry(root, bd=0, highlightthickness=2, highlightbackground='#808080',
                       highlightcolor='#4b6da7', relief='flat')
title_input.grid(row=3, column=0, padx=10, pady=5)

text_label = tk.Label(root, text="Texto:", bg='#808080', fg='black')
text_label.grid(row=4, column=0, padx=10)

text_input = tk.Text(root, bd=0, highlightthickness=2, highlightbackground='#808080',
                     highlightcolor='#4b6da7', relief='flat')
text_input.grid(row=5, column=0, padx=10, pady=5)  # Altere o valor de 'height' conforme necessário
text_input.bind("<KeyRelease>", update_char_count)

char_count = tk.StringVar()
char_count_label = tk.Label(root, textvariable=char_count, bg='#808080', fg='black')
char_count_label.grid(row=6, column=0, padx=10, sticky='e')

create_button = tk.Button(root, text="Criar PDF", command=create_pdf,
                          bg='#4b6da7', fg='white', borderwidth=0, highlightthickness=0,
                          activebackground='#87CEEB', activeforeground='white')
create_button.grid(row=7, column=0, padx=10, pady=10)

confirmation_label = tk.Label(root, text="", bg='#808080', fg='black')
confirmation_label.grid(row=8, column=0, padx=10)

# Executar a aplicação
root.mainloop()
