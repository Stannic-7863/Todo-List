from PyQt5.QtWidgets import QRadioButton, QWidget, QVBoxLayout, QApplication, QSizePolicy
from PyQt5.QtCore import QSize, Qt

class LineWrappedRadioButton(QRadioButton):
    def __init__(self, text='', parent=None):
        super(LineWrappedRadioButton, self).__init__(text, parent)
        policy = self.sizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Preferred)
        self.setSizePolicy(policy)
        self.updateGeometry()

    def wrap_lines(self, width):
        words = self.text().split()
        lines = []
        current_line = ""

        for word in words:
            if self.fontMetrics().width(current_line + " " + word) <= width:
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line.strip())
                current_line = word

        lines.append(current_line.strip())
        wrapped_text = "\n".join(lines).strip()
        self.setText(wrapped_text)

    def resizeEvent(self, event):
        control_element_width = self.sizeHint().width() - self.style().itemTextRect(
            self.fontMetrics(), self.rect(), Qt.TextShowMnemonic, False, self.text()
        ).width()
        self.wrap_lines(event.size().width() - control_element_width)
        super(LineWrappedRadioButton, self).resizeEvent(event)

    def minimumSizeHint(self):
        return QSize(super(QRadioButton, self).minimumSizeHint().width(), self.sizeHint().height())


def main():
    import sys

    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    button = LineWrappedRadioButton(
        "Lorem ipsum dolor sit amet, consectetur fghhhhhhhhhhhhh gfh fhf ggfh adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua."
    )
    layout.addWidget(button)
    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
