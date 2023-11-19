from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QScrollBar, QStyle

class CustomScrollBar(QScrollBar):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(12)
        self.setMaximumWidth(12)
        self.setStyleSheet("""
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
            }

            QScrollBar::handle:vertical {
                background-color: #888;
                min-height: 20px;
            }
        """)

    def enterEvent(self, event):
   
        print("Scrollbar handle hovered in")
        super().enterEvent(event)

    def leaveEvent(self, event):
        
        print("Scrollbar handle hovered out")
        super().leaveEvent(event)

    

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        scroll_area = QScrollArea(self)
        content_widget = QWidget(self)
        content_layout = QVBoxLayout(content_widget)

        for i in range(20):
            label = QLabel(f"Label {i + 1}")
            content_layout.addWidget(label)

        scroll_area.setWidget(content_widget)

        custom_scrollbar = CustomScrollBar()
        scroll_area.setVerticalScrollBar(custom_scrollbar)

        layout.addWidget(scroll_area)

        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Custom Scrollbar Example')

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
