import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt, QEvent

class OTETBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Widgets erstellen
        self.web_view = QWebEngineView()
        self.address_bar = QLineEdit()
        self.search_button = QPushButton('Suchen')
        self.back_button = QPushButton('◄')
        self.forward_button = QPushButton('►')

        # Layout erstellen
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.forward_button)
        button_layout.addWidget(self.address_bar)
        button_layout.addWidget(self.search_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.web_view)

        # Widget für das Hauptfenster erstellen
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Statusleiste hinzufügen
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Signal-Slot-Verbindungen
        self.search_button.clicked.connect(self.search_duckduckgo)
        self.back_button.clicked.connect(self.web_view.back)
        self.forward_button.clicked.connect(self.web_view.forward)
        self.web_view.urlChanged.connect(self.update_address_bar)

        # Mausereignisse überwachen
        self.web_view.installEventFilter(self)

        # Fenster konfigurieren
        self.setWindowTitle('OTET Browser')
        self.setGeometry(100, 100, 800, 600)

        # Stylesheet anpassen (Opera-ähnliches Design)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #1C1C1C;
                color: #FFFFFF;
            }
            QLineEdit {
                background-color: #2E2E2E;
                color: #FFFFFF;
                border: 1px solid #5C5C5C;
                padding: 5px;
                border-radius: 10px;  /* Abgerundete Ecken */
            }
            QPushButton {
                background-color: #3F3F3F;
                color: #FFFFFF;
                border: 1px solid #5C5C5C;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4F4F4F;
            }
            QPushButton:pressed {
                background-color: #2F2F2F;
            }
            QWebEngineView {
                border: 1px solid #5C5C5C;
            }
        ''')

        # DuckDuckGo direkt laden
        self.load_duckduckgo()

    def search_duckduckgo(self):
        search_query = self.address_bar.text()
        duckduckgo_url = "https://duckduckgo.com/?q=" + search_query
        self.web_view.setUrl(QUrl(duckduckgo_url))

    def load_duckduckgo(self):
        duckduckgo_url = "https://duckduckgo.com/"
        self.web_view.setUrl(QUrl(duckduckgo_url))

    def update_address_bar(self, q):
        self.address_bar.setText(q.toString())
        self.status_bar.showMessage(f'Geladen: {q.toString()}')

    def eventFilter(self, obj, event):
        if obj is self.web_view and event.type() == QEvent.Wheel:
            # Überwachen Sie das Mausradereignis und navigieren Sie vorwärts oder rückwärts
            if event.angleDelta().y() > 0:
                self.web_view.forward()
            else:
                self.web_view.back()
            return True
        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = OTETBrowser()
    browser.show()
    sys.exit(app.exec_())
