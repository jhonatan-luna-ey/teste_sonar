```python
import easyocr
from PyQt6.QtWidgets import QApplication, QPushButton, QProgressBar, QLineEdit, QWidget, QFileDialog, QMessageBox
from PyQt6 import uic, QtWidgets
from PIL import Image, ImageDraw
import os
import leitor_cnh_versao2 as func_cnh

###### QFileDialog em https://www.tutorialspoint.com/pyqt/pyqt_qfiledialog_widget.htm

import sys

class UI(QWidget):
    def __init__(self):
        super().__init__()

        self.path_foto = ""

        # Carregando a interface
        uic.loadUi("interface.ui", self)

        self.pathPhoto = self.findChild(QLineEdit, "pathPhoto")
        self.buttonCarregarPhoto = self.findChild(QPushButton, "pushButton")
        self.nome = self.findChild(QLineEdit, "lineEdit_nome")
        self.identidade = self.findChild(QLineEdit, "lineEdit_identidade")
        self.cpf = self.findChild(QLineEdit, "lineEdit_cpf")
        self.dtNascimento = self.findChild(QLineEdit, "lineEdit_dtNascimento")
        self.filiacao = self.findChild(QLineEdit, "lineEdit_filiacao")
        self.categoria = self.findChild(QLineEdit, "lineEdit_categoria")
        self.registo = self.findChild(QLineEdit, "lineEdit_numeroRegistro")
        self.validade = self.findChild(QLineEdit, "lineEdit_validade")
        self.primeiraHabilitacao = self.findChild(QLineEdit, "lineEdit_1ahabilitacao")
        self.barraProgresso = self.findChild(QProgressBar, "progressBar")

        self.interfaceInicial()

        # Conectando aos botões:
        self.buttonCarregarPhoto.clicked.connect(self.carregarFoto)
        self.pathPhoto.returnPressed.connect(self.carregarFotoLineEdit)

    def interfaceInicial(self):
        self.nome.setEnabled(False)
        self.identidade.setEnabled(False)
        self.cpf.setEnabled(False)
        self.dtNascimento.setEnabled(False)
        self.filiacao.setEnabled(False)
        self.categoria.setEnabled(False)
        self.registo.setEnabled(False)
        self.validade.setEnabled(False)
        self.primeiraHabilitacao.setEnabled(False)
        self.barraProgresso.setVisible(False)

    def carregarFoto(self):
        self.path_foto = QFileDialog.getOpenFileName(self, 'Abrir arquivo',
                                    os.getcwd(),"Image files (*.jpg *.gif *.png)")
        self.pathPhoto.setText(self.path_foto[0])
        self.barraProgresso.setVisible(True)
        self.lerCarteira(self.path_foto[0])

    def carregarFotoLineEdit(self):
        if os.path.exists(self.pathPhoto.text()):
            self.path_foto = self.pathPhoto.text()
            self.barraProgresso.setVisible(True)
            self.lerCarteira(self.path_foto)
        else:
            QMessageBox.warning(self, "Atenção", "Diretório inválido")
            self.path_foto = ""
            self.pathPhoto.setText("")

    def lerCarteira(self, path):
        # Zerar algum campo previamente preenchido
        self.nome.setText("")
        self.identidade.setText("")
        self.cpf.setText("")
        self.dtNascimento.setText("")
        self.filiacao.setText("")
        self.categoria.setText("")
        self.registo.setText("")
        self.validade.setText("")
        self.primeiraHabilitacao.setText("")
        self.barraProgresso.setValue(20)

        # Tratando a imagem
        img_tratada = func_cnh.tratamento_carteira(path)
        self.barraProgresso.setValue(25)

        # Desenha a bord