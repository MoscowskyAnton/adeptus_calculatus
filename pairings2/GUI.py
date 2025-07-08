from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QMainWindow, QAction, QFileDialog, QTextEdit, QSizePolicy
)
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import sys

class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        if text.strip():  # avoid empty lines
            self.text_written.emit(str(text))

    def flush(self):
        pass  # No need to implement flush for this use case

class StepBlock(QWidget):
    def __init__(self, step_number, options, extra_text="", on_apply_callback=None):
        super().__init__()
        self.step_number = step_number
        self.original_options = options
        self.extra_text = extra_text
        self.on_apply_callback = on_apply_callback

        self.layout = QHBoxLayout()

        self.label = QLabel(f"Step #{step_number} {self.extra_text}")
        self.stop_start_btn = QPushButton("Start")
        self.dropdown = QComboBox()
        self.apply_btn = QPushButton("Apply")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.stop_start_btn)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.apply_btn)

        self.setLayout(self.layout)

        self.stop_start_btn.clicked.connect(self.handle_stop_start)
        self.apply_btn.clicked.connect(self.handle_apply)

        self.is_start = True
        self.dropdown.clear()
        self.dropdown.setDisabled(True)

    def handle_stop_start(self):
        self.is_start = not self.is_start
        new_label = "Start" if self.is_start else "Stop"
        self.stop_start_btn.setText(new_label)

        if self.is_start:
            self.dropdown.clear()
            self.dropdown.addItems(self.original_options)
            self.dropdown.setDisabled(False)
            print(f"[Step {self.step_number}] Started - dropdown populated and enabled.")
        else:
            self.dropdown.clear()
            self.dropdown.setDisabled(True)
            print(f"[Step {self.step_number}] Stopped - dropdown cleared and disabled.")

    def handle_apply(self):
        selected_value = self.dropdown.currentText()
        print(f"[Step {self.step_number}] Apply clicked. Selected value: {selected_value}")

        self.setDisabled(True)
        print(f"[Step {self.step_number}] Block locked after apply.")

        if self.on_apply_callback:
            self.on_apply_callback(self.step_number)

class MainWindow(QMainWindow):
    def __init__(self, dropdown_options_list, extra_texts_list):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.blocks = []

        for i, (options, extra_text) in enumerate(zip(dropdown_options_list, extra_texts_list), start=1):
            block = StepBlock(i, options, extra_text=extra_text, on_apply_callback=self.enable_next_block)
            self.blocks.append(block)
            self.main_layout.addWidget(block)

        for block in self.blocks[1:]:
            block.setDisabled(True)

        # Add console QTextEdit at the bottom
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setMinimumHeight(150)
        self.console.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.console)

        self.central_widget.setLayout(self.main_layout)

        self.init_menu()

        # Redirect stdout and stderr to the console
        sys.stdout = EmittingStream(text_written=self.write_to_console)
        sys.stderr = EmittingStream(text_written=self.write_to_console)

    def write_to_console(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.console.setTextCursor(cursor)
    
        # Add newline if the console doesn't already end with one
        if not self.console.toPlainText().endswith('\n'):
            self.console.insertPlainText('\n')
    
        self.console.insertPlainText(text)
        self.console.moveCursor(QTextCursor.End)

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        load_action = QAction("Load data...", self)
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Data File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(f"Load data from: {file_name}")
            # Add your data loading logic here

    def enable_next_block(self, current_step):
        next_index = current_step
        if next_index < len(self.blocks):
            next_block = self.blocks[next_index]
            if next_block.isEnabled() is False:
                next_block.setDisabled(False)
                print(f"[MainWindow] Enabled Step #{next_block.step_number}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    dropdown_options = [
        ["Apple", "Banana", "Cherry"],
        ["Red", "Green", "Blue", "Yellow"],
        ["Cat", "Dog"],
        ["Python", "C++", "Java", "Rust"],
        ["Option A", "Option B"]
    ]

    extra_texts = [
        "(First step)",
        "(Second step)",
        "(Third step)",
        "(Fourth step)",
        "(Fifth step)"
    ]

    window = MainWindow(dropdown_options, extra_texts)
    window.setWindowTitle("Step Blocks with Console Output")
    window.resize(700, 400)
    window.show()
    sys.exit(app.exec_())
