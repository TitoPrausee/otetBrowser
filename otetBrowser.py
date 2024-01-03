import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QEvent, QRect, QPropertyAnimation, Qt

class OTETBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # ...

        # Widgets erstellen
        self.web_view = QWebEngineView()
        self.address_bar = QLineEdit()
        self.search_button = QPushButton('Suchen')
        self.back_button = QPushButton('◄')
        self.forward_button = QPushButton('►')
        self.overlay_label = QLabel(self)

        # Setzen Sie den Stil für den Suchen-Button
        self.search_button.setObjectName('searchButton')
        self.search_button.setCursor(Qt.PointingHandCursor)

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

        # DuckDuckGo direkt laden
        self.load_duckduckgo()

        # Animation für den Suchen-Button
        self.button_animation = QPropertyAnimation(self.overlay_label, b'geometry')
        self.button_animation.setDuration(200)
        self.button_animation.setStartValue(QRect(0, 0, 0, 0))
        self.button_animation.setEndValue(self.overlay_label.geometry())

        # Startposition für die Overlay-Grafik festlegen
        self.overlay_label.setGeometry(self.search_button.geometry())
        self.overlay_label.setStyleSheet('''
            background-color: #111;
            border-radius: 8px;
        ''')

    def search_duckduckgo(self):
        search_query = self.address_bar.text()
        duckduckgo_url = "https://duckduckgo.com/?q=" + search_query
        self.web_view.setUrl(QUrl(duckduckgo_url))
        self.start_button_animation()

    def start_button_animation(self):
        self.button_animation.start()

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
