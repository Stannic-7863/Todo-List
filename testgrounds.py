from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QSequentialAnimationGroup

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.addButton = QPushButton("Add Widget")
        self.addButton.clicked.connect(self.addAnimatedWidget)

        self.layout.addWidget(self.addButton)

    def addAnimatedWidget(self):
        newWidget = QWidget(self)
        newWidget.setStyleSheet("background-color: red;")
        newWidget.setFixedSize(100, 100)

        # Set up opacity effect
        opacity_effect = QGraphicsOpacityEffect(self)
        newWidget.setGraphicsEffect(opacity_effect)

        self.layout.addWidget(newWidget)

        # Set the initial position outside the view
        newWidget.setGeometry(QRect(0, self.height(), newWidget.width(), newWidget.height()))

        # Add animation to slide into view and change opacity
        opacity_animation = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_animation.setDuration(500)  # Set the duration of the opacity animation in milliseconds
        opacity_animation.setStartValue(0.0)
        opacity_animation.setEndValue(1.0)

        
        # Group animations in sequence
        sequential_group = QSequentialAnimationGroup(self)
        sequential_group.addAnimation(opacity_animation)
        sequential_group.start(QSequentialAnimationGroup.DeletionPolicy.DeleteWhenStopped)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
