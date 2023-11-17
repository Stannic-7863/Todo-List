from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMenu, QToolButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create a vertical layout for the main window
        layout = QVBoxLayout(self)

        # Create a label
        self.label = QLabel("Selected Item:")

        # Create a tool button with three-dot icon
        menu_button = QToolButton(self)
        menu_button.setText("Menu")
        menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        menu_button.setMenu(self.create_menu())

        # Add the label and tool button to the layout
        layout.addWidget(self.label)
        layout.addWidget(menu_button)

    def create_menu(self):
        menu = QMenu(self)

        # Add actions to the menu
        action1 = menu.addAction("Action 1")
        action1.triggered.connect(lambda: self.menu_action_triggered("Action 1"))

        action2 = menu.addAction("Action 2")
        action2.triggered.connect(lambda: self.menu_action_triggered("Action 2"))

        action3 = menu.addAction("Action 3")
        action3.triggered.connect(lambda: self.menu_action_triggered("Action 3"))

        return menu

    def menu_action_triggered(self, action_text):
        self.label.setText(f"Selected Action: {action_text}")

if __name__ == "__main__":
    app = QApplication([])

    # Create an instance of the main window
    main_window = MainWindow()

    # Set up the main window properties
    main_window.setWindowTitle("PyQt6 QToolButton with Menu Example")
    main_window.show()

    # Start the application event loop
    app.exec()
