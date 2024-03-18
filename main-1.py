import os
import textwrap
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

class PDFCreatorApp(App):
    def build(self):
        self.title = "Criador de PDF Personalizado"
        self.logo_path = ""
        self.char_count = Label(text="Caracteres digitados: 0", size_hint_y=None, height=30)
        
        layout = BoxLayout(orientation='vertical')
        
        self.logo_label = Label(text="", size_hint_y=None, height=30)
        layout.add_widget(self.logo_label)
        
        layout.add_widget(Label(text="Título:", size_hint_y=None, height=30))
        
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        layout.add_widget(title_layout)
        
        self.title_input = TextInput(size_hint_x=0.5)
        title_layout.add_widget(self.title_input)
        
        layout.add_widget(Label(text="Texto:", size_hint_y=None, height=30))
        
        self.text_input = TextInput()
        self.text_input.bind(text=self.update_char_count)
        layout.add_widget(self.text_input)
        
        layout.add_widget(self.char_count)
        
        self.confirmation_label = Label(text="", size_hint_y=None, height=30)
        layout.add_widget(self.confirmation_label)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        layout.add_widget(button_layout)
        
        logo_button = Button(text="Selecionar Logotipo", size_hint_x=0.5, size_hint_y=None, height=30)
        logo_button.bind(on_release=self.select_logo)
        button_layout.add_widget(logo_button)
        
        create_button = Button(text="Criar PDF", size_hint_x=0.5, size_hint_y=None, height=30)
        create_button.bind(on_release=self.create_pdf)
        button_layout.add_widget(create_button)
        
        return layout

    def update_char_count(self, instance, value):
        self.char_count.text = f"Caracteres digitados: {len(value)}"

    def create_pdf(self, instance):
        # Verificar se o logotipo foi selecionado e se o texto foi escrito
        if not self.logo_path or not self.text_input.text:
            self.confirmation_label.text = "Por favor, selecione um logotipo e escreva algum texto antes de criar o PDF."
            self.confirmation_label.color = (1, 0, 0, 1)  # Cor do texto alterada para vermelho
            return

        # Obter o título e o texto do input
        title = self.title_input.text
        text_lines = self.text_input.text.split('\n')
        
        # Limitar cada linha a  caracteres
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
                c.drawImage(self.logo_path, 10, page_height - 100 - 10, width=100, height=100)
                y_position = 720
                page_num += 1
                lines_count = 0
                add_header_footer(c, page_num, frame_width, page_width, page_height)  # Adicionar cabeçalho e rodapé na nova página
            c.drawString(logo_area_width + 10, y_position, line)
            y_position -= 20
            lines_count += 1
        
        # Salvar o PDF
        c.save()
        
        # Verificar se o PDF foi criado com sucesso
        if os.path.exists("seu_pdf_personalizado.pdf"):
            self.confirmation_label.text = "PDF criado com sucesso!"
            self.confirmation_label.color = (0, 1, 0, 1)  # Cor do texto alterada para verde
        else:
            self.confirmation_label.text = "Erro ao criar o PDF. Por favor, tente novamente."
            self.confirmation_label.color = (1, 0, 0, 1)  # Cor do texto alterada para vermelho

    def select_logo(self, instance):
        filechooser = FileChooserIconView()
        select_button = Button(text="Selecionar", size_hint_y=None, height=30)
        select_button.bind(on_release=lambda x: self.update_logo_path(filechooser.selection, x))
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(filechooser)
        popup_content.add_widget(select_button)
        self.popup = Popup(title="Selecione um arquivo", content=popup_content, size_hint=(0.9, 0.9))
        self.popup.open()

    def update_logo_path(self, selection, instance):
        if selection:
            self.logo_path = selection[0]
            self.logo_label.text = f"Logotipo selecionado: {self.logo_path}"
        else:
            self.logo_label.text = "Nenhum logotipo selecionado"
        self.popup.dismiss()  # Fechar o popup

        


if __name__ == "__main__":
    PDFCreatorApp().run()
