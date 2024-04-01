from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import textwrap
import os
import imghdr  # Para validar imagens

class PDFCreatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Criador de PDF Personalizado"
        self.logo_path = ""
        self.color = 'grey'
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Adicionando o botão quadrado no canto superior esquerdo '</>'
        b_button = QPushButton("</>")
        b_button.setFixedSize(30, 30)  # Tamanho do botão
        b_button.setStyleSheet("background-color: lightblue")  # Cor do botão
        layout.addWidget(b_button)

        # Adicionando o título do aplicativo
        app_title = QLabel("Criador de PDF Personalizado")
        app_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        app_title.setAlignment(Qt.AlignCenter)  # Centralizar o título
        layout.addWidget(app_title)

        # Adicionando uma descrição do aplicativo
        app_description = QLabel("Este aplicativo permite que você crie PDFs\n personalizados com um título,\n texto e logotipo de sua escolha. \nAlém disso, você pode personalizar a \ncor do seu PDF usando os botões coloridos.")
        app_description.setAlignment(Qt.AlignCenter)  # Centralizar a descrição
        layout.addWidget(app_description)

        # Adicionando os botões de cores
        color_layout = QHBoxLayout()
        colors = ['black', 'blue', 'red', 'green', 'brown', 'orange', 'purple', 'pink', 'yellow', 'cyan']
        for color in colors:
            color_button = QPushButton()
            color_button.setFixedSize(30, 30)  # Tamanho do botão
            color_button.setStyleSheet(f"background-color: {color};")  # Cor do botão
            color_button.clicked.connect((lambda color=color: lambda: self.change_color(color))())
            color_layout.addWidget(color_button)
        layout.addLayout(color_layout)

        self.logo_label = QLabel("Nenhum logotipo selecionado")
        self.logo_label.setStyleSheet("color: red;")  # Mudar a cor do texto para vermelho
        layout.addWidget(self.logo_label)

        layout.addWidget(QLabel("Título:"))
        self.title_input = QLineEdit()
        self.title_input.setStyleSheet("background-color: white;")
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Texto:"))
        self.text_input = QTextEdit()
        self.text_input.setStyleSheet("background-color: white;")
        self.text_input.textChanged.connect(self.update_char_count)
        layout.addWidget(self.text_input)

        self.char_count = QLabel("Caracteres digitados: 0")
        layout.addWidget(self.char_count)

        layout.addWidget(QLabel("Modelo:"))
        self.model_input = QComboBox()
        self.model_input.addItems(["Modelo 1", "Modelo 2", "Modelo 3"])
        layout.addWidget(self.model_input)

        logo_button = QPushButton("Selecionar Logotipo")
        logo_button.setStyleSheet("background-color: green;")
        logo_button.clicked.connect(self.select_logo)
        layout.addWidget(logo_button)

        create_button = QPushButton("Criar PDF")
        create_button.setStyleSheet("background-color: purple;")
        create_button.clicked.connect(self.create_pdf)
        layout.addWidget(create_button)

        self.setStyleSheet("background-color: lightgray;")

    def update_char_count(self):
        self.char_count.setText(f"Caracteres digitados: {len(self.text_input.toPlainText())}")

    def change_color(self, color):
        self.color = color

    def create_pdf(self):
        # Verificar se o logotipo foi selecionado e se o texto foi escrito
        if not self.logo_path or not self.text_input.toPlainText() or not self.title_input.text():
            QMessageBox.warning(self, 'Erro', 'Por favor, selecione um logotipo, escreva um título e algum texto antes de criar o PDF.')
            return

        # Verificar se o arquivo de logotipo é uma imagem válida
        if imghdr.what(self.logo_path) is None:
            QMessageBox.warning(self, 'Erro', 'O arquivo de logotipo selecionado não é uma imagem válida.')
            return

        # Obter o título e o texto do input
        title = self.title_input.text()
        text_lines = self.text_input.toPlainText().split('\n')

        # Limitar cada linha a  caracteres
        text_lines = [textwrap.fill(line, 64) for line in text_lines]
        text_lines = '\n'.join(text_lines).split('\n')

        # Solicitar ao usuário para escolher o diretório e o nome do arquivo para salvar o PDF
        save_path, _ = QFileDialog.getSaveFileName(self, 'Salvar PDF', '/home', 'PDF Files (*.pdf)')
        if not save_path:
            return

        # Criar um objeto canvas para desenhar no PDF
        c = canvas.Canvas(save_path, pagesize=letter)

        # Definir as dimensões da página
        page_width, page_height = letter

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
        c.setFillColor(self.color)
        c.rect(0, 0, logo_area_width, page_height, fill=1)
        c.drawImage(self.logo_path, 10, page_height - 100 - 10, width=100, height=100)

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
        for line in text_lines:
            if lines_count >= lines_per_page:  # Verificar se é necessário criar uma nova página
                add_header_footer(c, page_num, frame_width, page_width, page_height)
                c.showPage()
                c.setStrokeColor('black')
                c.setFillColor('white')
                c.rect(logo_area_width, 0, frame_width, frame_height, fill=1)
                c.setFillColor(self.color)
                c.rect(0, 0, logo_area_width, page_height, fill=1)
                c.drawImage(self.logo_path, 10, page_height - 100 - 10, width=100, height=100)
                y_position = 720
                page_num += 1
                lines_count = 0
                add_header_footer(c, page_num, frame_width, page_width, page_height)  # Adicionar cabeçalho e rodapé na nova página
            c.setFillColor('black')  # Definir a cor do texto para preto
            c.drawString(logo_area_width + 10, y_position, line)
            y_position -= 20
            lines_count += 1

        # Salvar o PDF
        c.save()

        # Verificar se o PDF foi criado com sucesso
        if os.path.exists(save_path):
            QMessageBox.information(self, 'Sucesso', 'PDF criado com sucesso!')
        else:
            QMessageBox.warning(self, 'Erro', 'Erro ao criar o PDF. Por favor, tente novamente.')

    def select_logo(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            self.logo_path = fname[0]
            self.logo_label.setText("Logotipo selecionado")
            self.logo_label.setStyleSheet("color: green;")  # Mudar a cor do texto para verde quando um logotipo for selecionado

if __name__ == '__main__':
    app = QApplication([])
    ex = PDFCreatorApp()
    ex.show()
    app.exec_()
