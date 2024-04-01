from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QComboBox, QGridLayout, QToolTip, QMenu
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QCursor
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import textwrap
import os
import imghdr
import webbrowser

class PDFCreatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = self.tr("Criador de PDF Personalizado")
        self.logo_path = ""
        self.color = 'grey'
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # Adicionando o botão quadrado no canto superior esquerdo '</>'
        b_button = QPushButton("</>")
        b_button.setFixedSize(30, 30)  # Tamanho do botão
        b_button.setStyleSheet("background-color: lightblue")  # Cor do botão
        b_button.setToolTip(self.tr('Clique para abrir o link'))  # Adicionando tooltip

        # Adicionando a função para abrir o link
        def open_link():
            webbrowser.open('https://portfolio-pjxsantos.vercel.app/')  # Substitua com o seu link

        b_button.clicked.connect(open_link)  # Conectando o botão à função

        layout.addWidget(b_button, 0, 0)

        # Adicionando o título do aplicativo
        app_title = QLabel(self.title)
        app_title.setStyleSheet("font-size: 20px; font-weight: bold;")
        app_title.setAlignment(Qt.AlignCenter)  # Centralizar o título
        layout.addWidget(app_title, 0, 1)

        # Adicionando uma descrição do aplicativo
        app_description = QLabel(self.tr("Este aplicativo permite que você crie PDFs\n personalizados com um título,\n texto e logotipo de sua escolha. \nAlém disso, você pode personalizar a \ncor do seu PDF usando os botões coloridos."))
        app_description.setAlignment(Qt.AlignCenter)  # Centralizar a descrição
        layout.addWidget(app_description, 1, 0, 1, 2)

        # Adicionando o botão de cores
        color_button = QPushButton(self.tr("Escolha a cor"))
        color_button.setStyleSheet("background-color: blue")  # Cor do botão
        color_button.setToolTip(self.tr('Clique para escolher a cor'))  # Adicionando tooltip
        color_menu = QMenu()
        colors = ['black', 'blue', 'red', 'green', 'brown', 'orange', 'purple', 'pink', 'yellow', 'cyan', 'gray', 'magenta', 'lime', 'teal', 'gold', 'indigo', 'salmon', 'orchid', 'lightcoral', 'skyblue']
        for color in colors:
            color_action = color_menu.addAction(color)
            color_action.triggered.connect((lambda color=color: lambda: self.change_color(color))())
        color_button.setMenu(color_menu)
        layout.addWidget(color_button, 2, 0, 1, 2)

        self.logo_label = QLabel(self.tr("Nenhum logotipo selecionado"))
        self.logo_label.setStyleSheet("color: red;")  # Mudar a cor do texto para vermelho
        layout.addWidget(self.logo_label, 3, 0, 1, 2)

        # Restante do código permanece o mesmo...


        layout.addWidget(QLabel(self.tr("Título:")), 4, 0)
        self.title_input = QLineEdit()
        self.title_input.setStyleSheet("background-color: white;")
        layout.addWidget(self.title_input, 4, 1)

        layout.addWidget(QLabel(self.tr("Texto:")), 5, 0)
        self.text_input = QTextEdit()

        self.text_input.setStyleSheet("background-color: white;")
        self.text_input.textChanged.connect(self.update_char_count)
        layout.addWidget(self.text_input, 5, 1)

        self.char_count = QLabel(self.tr("Caracteres digitados: 0"))
        layout.addWidget(self.char_count, 6, 0, 1, 2)

        layout.addWidget(QLabel(self.tr("Modelo:")), 7, 0)
        self.model_input = QComboBox()
        self.model_input.addItems([self.tr("Modelo 1"), self.tr("Modelo 2"), self.tr("Modelo 3")])
        layout.addWidget(self.model_input, 7, 1)

        logo_button = QPushButton(self.tr("Selecionar Logotipo"))
        logo_button.setStyleSheet("background-color: green;")
        logo_button.setToolTip(self.tr('Clique para selecionar o logotipo'))  # Adicionando tooltip
        logo_button.clicked.connect(self.select_logo)
        layout.addWidget(logo_button, 8, 0, 1, 2)

        create_button = QPushButton(self.tr("Criar PDF"))
        create_button.setStyleSheet("background-color: purple;")
        create_button.setToolTip(self.tr('Clique para criar o PDF'))  # Adicionando tooltip
        create_button.clicked.connect(self.create_pdf)
        layout.addWidget(create_button, 9, 0, 1, 2)

        self.setStyleSheet("background-color: lightgray;")

    def update_char_count(self):
        self.char_count.setText(self.tr(f"Caracteres digitados: {len(self.text_input.toPlainText())}"))

    def change_color(self, color):
        self.color = color

    def create_pdf(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))  # Alterar o cursor para "espera"
        # Verificar se o logotipo foi selecionado e se o texto foi escrito
        if not self.logo_path or not self.text_input.toPlainText() or not self.title_input.text():
            QMessageBox.warning(self, self.tr('Erro'), self.tr('Por favor, selecione um logotipo, escreva um título e algum texto antes de criar o PDF.'))
            QApplication.restoreOverrideCursor()  # Restaurar o cursor
            return

        # Verificar se o arquivo de logotipo é uma imagem válida
        if imghdr.what(self.logo_path) is None:
            QMessageBox.warning(self, self.tr('Erro'), self.tr('O arquivo de logotipo selecionado não é uma imagem válida.'))
            QApplication.restoreOverrideCursor()  # Restaurar o cursor
            return

        # Verificar se o modelo selecionado é válido
        model = self.model_input.currentText()
        if model not in [self.tr("Modelo 1"), self.tr("Modelo 2"), self.tr("Modelo 3")]:
            QMessageBox.warning(self, self.tr('Erro'), self.tr('O modelo selecionado não é válido.'))
            QApplication.restoreOverrideCursor()  # Restaurar o cursor
            return

        # Obter o título e o texto do input
        title = self.title_input.text()
        text_lines = self.text_input.toPlainText().split('\n')

        # Limitar cada linha a  caracteres
        text_lines = [textwrap.fill(line, 64) for line in text_lines]
        text_lines = '\n'.join(text_lines).split('\n')

        # Solicitar ao usuário para escolher o diretório e o nome do arquivo para salvar o PDF
        save_path, _ = QFileDialog.getSaveFileName(self, self.tr('Salvar PDF'), '/home', 'PDF Files (*.pdf)')
        if not save_path:
            QApplication.restoreOverrideCursor()  # Restaurar o cursor
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
        c.drawImage(self.logo_path, 10, page_height - 100 - 10,         width=100, height=100)

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
