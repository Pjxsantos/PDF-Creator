import tkinter as tk
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

def create_pdf():
    # Obter o título e o texto do input
    title = title_input.get()
    text_lines = text_input.get("1.0", "end-1c").split('\n')
    
    # Criar um objeto canvas para desenhar no PDF
    c = canvas.Canvas("seu_pdf_personalizado.pdf", pagesize=letter)
    
    # Definir as dimensões da página
    page_width, page_height = c._pagesize
    
    # Variável para controlar a numeração das páginas
    page_num = 1
    
    # Função para converter número da página para hexadecimal
    def to_hex(num):
        return hex(num)[2:].upper()
    
    # Função para adicionar cabeçalho, rodapé e numeração de página
    def add_header_footer(canvas, page_num, frame_width, page_width, page_height):
        # Adicionar data e hora no rodapé do quadro
        now = datetime.now()
        date_time_string = now.strftime("%d/%m/%Y %H:%M:%S")
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
        if y_position < 40:  # Verificar se é necessário criar uma nova página
            add_header_footer(c, page_num, frame_width, page_width, page_height)
            c.showPage()
            c.setStrokeColor('black')
            c.setFillColor('white')
            c.rect(logo_area_width, 0, frame_width, frame_height, fill=1)
            y_position = 720
            page_num += 1
        c.drawString(logo_area_width + 10, y_position, line)
        y_position -= 20
    
    # Adicionar cabeçalho e rodapé na última página
    add_header_footer(c, page_num, frame_width, page_width, page_height)
    
    # Salvar o PDF
    c.save()
    
    # Mensagem de confirmação
    confirmation_label.config(bg='#808080', text="PDF criado com sucesso!\n")


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
logo_button.pack(pady=10)

logo_label = tk.Label(root, text="", bg='#808080', fg='black')
logo_label.pack()

title_label = tk.Label(root, text="Título:", bg='#808080', fg='black')
title_label.pack()

title_input = tk.Entry(root, bd=0, highlightthickness=2, highlightbackground='#808080',
                       highlightcolor='#4b6da7', relief='flat')
title_input.pack(pady=5)

text_label = tk.Label(root, text="Texto:", bg='#808080', fg='black')
text_label.pack()

text_input = tk.Text(root, bd=0, highlightthickness=2, highlightbackground='#808080',
                     highlightcolor='#4b6da7', relief='flat')
text_input.pack(pady=5)

create_button = tk.Button(root, text="Criar PDF", command=create_pdf,
                          bg='#4b6da7', fg='white', borderwidth=0, highlightthickness=0,
                          activebackground='#87CEEB', activeforeground='white')
create_button.pack(pady=10)

confirmation_label = tk.Label(root, text="", bg='#808080', fg='black')
confirmation_label.pack()

# Executar a aplicação
root.mainloop()