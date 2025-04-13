#Rahman ve Rahim olan Allah'ın adıyla.
import os
import sys
import openai
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon

openai.api_key = ""

class ChatGPTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Malus App")
        self.setGeometry(100, 100, 400, 350)

        def get_resource_path(relative_path):
                if getattr(sys, 'frozen', False):  # PyInstaller ile paketlenmiş mi?
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.abspath(".")
                return os.path.join(base_path, relative_path)

        self.setWindowIcon(QIcon(get_resource_path("app.ico")))
    
        self.logoLabel = QLabel(self)
        pixmap = QPixmap(get_resource_path("maluslogo.png")) 
        self.logoLabel.setPixmap(pixmap)
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setFixedSize(400, 200)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.creatorLabel = QLabel("made by marthia © 2025")
        self.creatorLabel.setStyleSheet("font-size: 12pt; color: gray; text-align: center;")
        self.creatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel("Bir dosya seçin:")
        self.uploadButton = QPushButton("Dosya Seç")
        self.uploadButton.clicked.connect(self.uploadFile)
        
        self.prompt1Button = QPushButton("Stok Sınır Güncelle")
        self.prompt1Button.clicked.connect(lambda: self.sendToChatGPT("Bu birinci prompt." + self.extraInput, self.filePath))
        
        self.prompt2Button = QPushButton("Satış Şartı Güncelle")
        self.prompt2Button.clicked.connect(lambda: self.sendToChatGPT("Bu ikinci prompt." + self.extraInput, self.filePath))
        
        self.prompt3Button = QPushButton("Diğer (İsteğinizi detaylı bir şekilde açıklayınız.)")
        self.prompt3Button.clicked.connect(lambda: self.sendToChatGPT(self.extraInput ,self.filePath))

        self.extraInput = QLineEdit()
        self.extraInput.setPlaceholderText("Varsa ekstra uyarı veya düzenlemeleri buraya girin...")

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        
        self.saveButton = QPushButton("Çıktıyı Kaydet")
        self.saveButton.setVisible(False)
        self.saveButton.clicked.connect(self.saveOutput)
        
        layout = QVBoxLayout()
        layout.addWidget(self.logoLabel)
        layout.addWidget(self.label)
        layout.addWidget(self.uploadButton)
        layout.addWidget(self.prompt1Button)
        layout.addWidget(self.prompt2Button)
        layout.addWidget(self.prompt3Button)
        layout.addWidget(self.extraInput)
        layout.addWidget(self.outputText)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.creatorLabel)
        
        self.setLayout(layout)
        self.filePath = None
    
    def uploadFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", "", "Excel Dosyaları (*.xlsx *.xls)")
        if filePath:
            self.filePath = filePath
            self.label.setText(f"Seçilen Dosya: {filePath}")
    
    def sendToChatGPT(self, prompt, filePath):
        if not filePath:
            self.outputText.setText("Lütfen önce bir dosya seçin.")
            return
        
        extraText = self.extraInput.text()
        fullPrompt = f"{prompt} {extraText}"
        
        try:
            # Excel dosyasını oku
            if filePath.endswith(".xlsx") or filePath.endswith(".xls"):
                df = pd.read_excel(filePath)
                fileContent = df.to_string()
            else:
                self.outputText.setText("Lütfen bir Excel dosyası seçin.")
                return
        
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "system", "content": fullPrompt},
                          {"role": "user", "content": fileContent}]
            )
        
            outputText = response["choices"][0]["message"]["content"]
            self.outputText.setText(outputText)
            self.processedData = outputText
            self.saveButton.setVisible(True)
        
        except Exception as e:
            self.outputText.setText(f"Hata oluştu: {str(e)}")
    
    def saveOutput(self):
        savePath, _ = QFileDialog.getSaveFileName(self, "Çıktıyı Kaydet", "output.xlsx", "Excel Dosyaları (*.xlsx)")
        if savePath:
            df = pd.DataFrame([self.processedData.split('\n')])  # Çıktıyı satır satır DataFrame'e çevir
            df.to_excel(savePath, index=False, header=False)  # Excel dosyasına kaydet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatGPTApp()
    window.show()
    sys.exit(app.exec())
