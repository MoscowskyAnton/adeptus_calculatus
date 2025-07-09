import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QMainWindow, QAction, QFileDialog, QTextEdit, QSizePolicy, QSplitter, QGridLayout, QScrollArea
)
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class EmittingStream(QObject):
    text_written = pyqtSignal(str)
    def write(self, text):
        if text.strip():
            self.text_written.emit(str(text))
    def flush(self):
        pass

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

        # Dropdown enabled and populated on init
        self.dropdown.clear()
        self.dropdown.addItems(self.original_options)
        self.dropdown.setDisabled(False)

    def handle_stop_start(self):
        self.is_start = not self.is_start
        new_label = "Start" if self.is_start else "Stop"
        self.stop_start_btn.setText(new_label)

        if not self.is_start:
            # "Start" pressed: disable dropdown
            self.dropdown.setDisabled(True)
            print(f"[Step {self.step_number}] Started - dropdown disabled.")
        else:
            # "Stop" pressed: enable dropdown
            self.dropdown.setDisabled(False)
            print(f"[Step {self.step_number}] Stopped - dropdown enabled.")

    def handle_apply(self):
        selected_value = self.dropdown.currentText()
        print(f"[Step {self.step_number}] Apply clicked. Selected value: {selected_value}")
        self.setDisabled(True)
        print(f"[Step {self.step_number}] Block locked after apply.")
        if self.on_apply_callback:
            self.on_apply_callback(self.step_number)

class RightBlock(QWidget):
    def __init__(self, block_number, text, image_path):
        super().__init__()
        self.block_number = block_number
        self.text = text
        self.image_path = image_path

        self.layout = QVBoxLayout()
        self.label = QLabel(f"#{block_number} {self.text}")
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.setLayout(self.layout)
        self.load_image(image_path)

    def load_image(self, path):
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.image_label.setText("Image not found")
        else:
            scaled_pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def update_text(self, new_text):
        self.text = new_text
        self.label.setText(f"#{self.block_number} {self.text}")

    def update_image(self, new_path):
        self.image_path = new_path
        self.load_image(new_path)

class MainWindow(QMainWindow):
    def __init__(self, dropdown_options_list, extra_texts_list, right_texts, right_images, right_columns=2):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main vertical splitter: top (left+right), bottom (console)
        self.vertical_splitter = QSplitter(Qt.Vertical)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.vertical_splitter)
        self.central_widget.setLayout(main_layout)

        # Top horizontal splitter: left and right parts
        self.horizontal_splitter = QSplitter(Qt.Horizontal)

        # Left side: scroll area with StepBlocks
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        # Container widget for step blocks (to put inside scroll area)
        step_blocks_container = QWidget()
        step_blocks_layout = QVBoxLayout()
        step_blocks_container.setLayout(step_blocks_layout)

        self.blocks = []
        for i, (options, extra_text) in enumerate(zip(dropdown_options_list, extra_texts_list), start=1):
            block = StepBlock(i, options, extra_text=extra_text, on_apply_callback=self.enable_next_block)
            self.blocks.append(block)
            step_blocks_layout.addWidget(block)
        step_blocks_layout.addStretch()

        # Scroll area for step blocks
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(step_blocks_container)
        left_layout.addWidget(scroll_area)

        # Disable all blocks except first
        for block in self.blocks[1:]:
            block.setDisabled(True)

        self.horizontal_splitter.addWidget(left_widget)
        self.horizontal_splitter.setCollapsible(0, False)

        # Right side: grid layout for RightBlocks
        right_widget = QWidget()
        right_layout = QGridLayout()
        right_widget.setLayout(right_layout)

        self.right_blocks = []
        for m, (text, img_path) in enumerate(zip(right_texts, right_images), start=1):
            rblock = RightBlock(m, text, img_path)
            self.right_blocks.append(rblock)
            row = (m - 1) // right_columns
            col = (m - 1) % right_columns
            right_layout.addWidget(rblock, row, col)

        # Add stretch to last row and column for spacing
        right_layout.setRowStretch(row + 1, 1)
        right_layout.setColumnStretch(right_columns, 1)

        self.horizontal_splitter.addWidget(right_widget)
        self.horizontal_splitter.setCollapsible(1, False)

        # Add horizontal splitter to top part of vertical splitter
        self.vertical_splitter.addWidget(self.horizontal_splitter)

        # Console QTextEdit at bottom part of vertical splitter
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setMinimumHeight(150)
        self.console.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.vertical_splitter.addWidget(self.console)
        self.vertical_splitter.setCollapsible(1, False)

        # Set initial splitter sizes (top bigger, console smaller)
        self.vertical_splitter.setSizes([700, 150])
        self.horizontal_splitter.setSizes([400, 300])

        self.init_menu()

        # Redirect stdout and stderr to console
        sys.stdout = EmittingStream(text_written=self.write_to_console)
        sys.stderr = EmittingStream(text_written=self.write_to_console)

        # Start maximized (full screen)
        self.showMaximized()

    def write_to_console(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.console.setTextCursor(cursor)

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
            # Implement your data loading logic here

    def enable_next_block(self, current_step):
        next_index = current_step  # zero-based index = current_step - 1, next block = current_step
        if next_index < len(self.blocks):
            next_block = self.blocks[next_index]
            if next_block.isEnabled() is False:
                next_block.setDisabled(False)
                print(f"[MainWindow] Enabled Step #{next_block.step_number}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Example with 25 step blocks to test scrolling
    dropdown_options = [["Option 1", "Option 2", "Option 3"]] * 25
    extra_texts = [f"(Step {i})" for i in range(1, 26)]

    # Example right side data (3 blocks)
    right_texts = [
        "Right block text 1",
        "Right block text 2",
        "Right block text 3"
    ]

    right_images = [
        "path/to/image1.png",  # Replace with actual image paths
        "path/to/image2.png",
        "path/to/image3.png"
    ]

    window = MainWindow(dropdown_options, extra_texts, right_texts, right_images, right_columns=3)
    window.setWindowTitle("Step Blocks with Scrollable Left, Grid Right, and Console")
    window.show()
    sys.exit(app.exec_())
