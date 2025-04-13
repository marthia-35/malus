#Rahman ve Rahim olan Allah'ın adıyla.
#CHECK LINE 41
import os
import sys
import openai
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QLabel, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QIcon
import traceback
openai.api_key = "ENTERAPIHERE1"

class ChatGPTApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Malus App v1.1")
        self.setGeometry(100, 100, 400, 350)

        def get_resource_path(relative_path):
                if getattr(sys, 'frozen', False):
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
        
        # Made by Marthia, a member of Demirciler TechGuild # enkazlardan çıkıp sevdiysek seni, hangi deprem yıkar bizi #

        self.creatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel("Bir dosya seçin:")
        self.uploadButton = QPushButton("Dosya Seç")
        self.uploadButton.clicked.connect(self.uploadFile)
        
        self.prompt1Button = QPushButton("Stok Sınır Güncelle")
        self.prompt1Button.clicked.connect(lambda: self.sendToChatGPT("Bu birinci prompt.", self.filePath))
        
        self.prompt2Button = QPushButton("Satış Şartı Güncelle")
        self.prompt2Button.clicked.connect(lambda: self.sendToChatGPT("Bu ikinci prompt.", self.filePath))

        self.outputText = QTextEdit()
        self.outputText.setReadOnly(True)
        
        self.saveButton = QPushButton("Çıktıyı Kaydet")
        self.saveButton.setVisible(False)
        self.saveButton.clicked.connect(self.saveOutput)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.logoLabel)
        layout.addWidget(self.uploadButton)
        layout.addWidget(self.prompt1Button)
        layout.addWidget(self.prompt2Button)
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
        try:
            print("Fonksiyon başladı!")

            if not filePath:
                print("HATA: Dosya seçilmemiş!")
                return

            print(f"Dosya yükleniyor: {filePath}")
            with open(filePath, "rb") as file:
                fileContent = file.read()

            client = openai.OpenAI(api_key="ENTERAPIHERE2")

            print("API çağrısı yapılıyor...")
            messages = [
                {"role": "user", "content": prompt}
            ]

            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=500
            )

            print("API yanıtı alındı!")
            chat_response = response.choices[0].message.content
            print("Yanıt:", chat_response)

        except openai.OpenAIError as e:
            print("OpenAI API Hatası:", str(e))
            traceback.print_exc()

        except Exception as e:
            print("Bilinmeyen bir hata oluştu:", str(e))
            traceback.print_exc()


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
