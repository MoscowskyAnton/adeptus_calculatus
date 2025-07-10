import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox,
    QMainWindow, QAction, QFileDialog, QTextEdit, QSizePolicy, QSplitter, QGridLayout, QScrollArea, QLineEdit
)
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
import numpy as np

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class WorkerThread(QThread):
    # Optional: define a signal to communicate with the GUI if needed
    update = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        #self.solver = solver
        self._running = False
        self.node = None

    def run(self):
        if self.node is None:
            raise ValueError("Node not inited for worker")
        self._running = True
        #self.node = node
        print("Worker started")
        cnt = 0
        while self._running:
            # Simulate work
            #print("Working...")
            #self.update.emit("Working...")  # emit signal if needed
            #time.sleep(1)
            v = self.node._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)
            cnt+=1
            if cnt % 1000 == 0:
                print(f"{cnt} simulations passed")
            
            
        print("Worker stopped")

    def stop(self):
        self._running = False



class EmittingStream(QObject):
    text_written = pyqtSignal(str)
    def write(self, text):
        if text.strip():
            self.text_written.emit(str(text))
    def flush(self):
        pass
    
class SheetControlBlock(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        
        self.parent_window = parent_window
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel("Sheet name")
        self.text_input = QLineEdit()
        self.read_btn = QPushButton("Read")
        self.combo = QComboBox()
        self.load_btn = QPushButton("Load")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_input)
        self.layout.addWidget(self.read_btn)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(self.load_btn)
        
        self.read_btn.setDisabled(True)
        self.load_btn.setDisabled(True)

        # Connect buttons
        self.read_btn.clicked.connect(self.on_read)
        self.load_btn.clicked.connect(self.on_load)
        
        self.spreadsheet = None

    def on_read(self):
        # Example: fill combo box with dummy sheet names
        sheet_name = self.text_input.text().strip()
        if not sheet_name:
            print("Please enter a sheet name before reading.")
            return
        
        self.spreadsheet = self.parent_window.client.open(sheet_name)
        # Access the worksheet by its exact sheet name (case-sensitive)
        worksheets = self.spreadsheet.worksheets()
        sheet_names = [ws.title for ws in worksheets if ws.title.startswith("Team")]
        
        if len(sheet_names):
            self.combo.clear()
            self.combo.addItems(sheet_names)
            self.load_btn.setDisabled(False)
            print(f"Read from {sheet_name} appropriate sheets: {sheet_names}")
        else:
            print(f"No appropriate sheet was readed from {sheet_name} - sheet name must start with \"Team\" word, like Team: PlanB")
            
        #print(f"Read sheets for '{sheet_name}': {sheets}")

    def on_load(self):
        print("Loading...")
        selected = self.combo.currentText()
        if self.spreadsheet is None:
            print("Some error with read sheet")
        elif selected:
            
            self.load_btn.setDisabled(True)
            print(f"Load button pressed. Selected sheet: {selected}")
            # Add your load logic here
            worksheet = self.spreadsheet.worksheet(selected)
            
            # READ 8x8 standart Tlen table TODO different table parsers
            
            self.parent_window.teams = [[], []]
            for i in range(8):
                self.parent_window.teams[0].append(worksheet.acell(f'B{7+i*3}').value)
            print(f"Read team 0: {self.parent_window.teams[0]}")
            for i in ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']:
                self.parent_window.teams[1].append(f"{worksheet.acell(f'{i}3').value} - {worksheet.acell(f'{i}4').value}")
            print(f"Read team 1: {self.parent_window.teams[1]}")
            
            scores_raw_data = worksheet.get('D7:K30')
            
            full_len = 8
            def_value = 0
            ch = []
            for d in scores_raw_data:
                dc = [def_value if i == '' else int(i) for i in d]
                for i in range(len(dc), full_len):
                    dc.append(def_value)
                ch.append(dc)
            
            self.parent_window.solver.game.scores = np.array(ch).reshape(8, 3, 8).transpose(0, 2, 1)
            
            print(f"Read scores") #" {self.parent_window.solver.game.scores}")
            
            mapping = worksheet.get('C7:C9')
            mapping = {v[0]:i for i,v in enumerate(mapping)}
            
            raw_tables_data = worksheet.get('D45:K52')
            def_value = "Middle"
            tables_str = []
            for d in raw_tables_data:
                t = [def_value if not i in mapping else i for i in d]
                for i in range(len(t), full_len):
                    t.append(def_value)
                tables_str.append(t)
            
            #print(mapping)
            tables_int = []
            for t in tables_str:
                tables_int.append([mapping[i] for i in t])
            
            self.parent_window.solver.game.tables = np.array(tables_int)
            
            print(f"Read tables")#" {self.parent_window.solver.game.tables}")
            
            self.parent_window.start_solver()
            self.load_btn.setDisabled(False)
            
        else:
            print("No sheet selected to load.")

class StepBlock(QWidget):
    def __init__(self, parent_window, step_number, options, extra_text="", on_apply_callback=None):
        super().__init__()
        self.parent_window = parent_window
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
        
        # game stuff
        self.game_node = None
        
    def update_dropdown_from_node(self):
        self.dropdown.clear()
        items = []
        
        def parse_param(param):
            team = None
            if "team" in param:
                team = param["team"]
            other_key = None
            for key, value in param.items():
                if "table" in key:
                    return f"table {value+1}" # because for norm people count is from 0 not 1
                if key == "team":
                    pass
                else:
                    other_key = key
            if not other_key is None and not team is None:
                if "choosed" in other_key:
                    team = team -1 # DANGER super koslyl
                if isinstance(param[other_key], int):
                    return self.parent_window.teams[team][param[other_key]]
                elif isinstance(param[other_key], tuple):
                    return self.parent_window.teams[team][param[other_key][0]] + ", " + self.parent_window.teams[team][param[other_key][1]]
            return str(param)
        
        if not self.game_node is None:
            if self.game_node.is_fully_expanded():
                for child in self.game_node.children:
                    items.append(f"{parse_param(child.parent_action)} {round(np.mean(child._results) ,2)}")
                self.dropdown.addItems(items)
                best_no = self.game_node.best_child_no(0.0)
                item = self.dropdown.model().item(best_no) 
                if item:
                    font = item.font()
                    font.setBold(True)  # Set font to bold
                    item.setFont(font)
                self.dropdown.show()
            else:
                for param in self.game_node._params:
                    items.append(parse_param(param))
                self.dropdown.addItems(items)
        
        

    def handle_stop_start(self):
        self.is_start = not self.is_start
        new_label = "Start" if self.is_start else "Stop"
        self.stop_start_btn.setText(new_label)

        if not self.is_start:
            # "Start" pressed: disable dropdown
            self.dropdown.setDisabled(True)
            print(f"[Step {self.step_number}] Started - dropdown disabled.")
            
            #self.game_node.best_action(500)
            self.parent_window.worker.node = self.game_node
            self.parent_window.worker.start()
            print(f"[Step {self.step_number}] finished calculation")
        else:
            # "Stop" pressed: enable dropdown
            self.dropdown.setDisabled(False)
            print(f"[Step {self.step_number}] Stopped - dropdown enabled.")
            
            self.parent_window.worker.stop()
            self.parent_window.worker.wait() 
            
            # update dropdown
            self.update_dropdown_from_node()
            
    def handle_apply(self):
        #selected_value = self.dropdown.currentText()
        #print(f"[Step {self.step_number}] Apply clicked. Selected value: {selected_value}")
        self.setDisabled(True)
        print(f"[Step {self.step_number}] Block locked after apply.")
        
            
        if len(self.parent_window.blocks) > self.step_number:
            if self.parent_window.blocks[self.step_number].game_node is None:
                selected_action_no = self.dropdown.currentIndex()
                # has children
                if len(self.game_node.children) < selected_action_no+1:
                    while not self.game_node.is_fully_expanded():
                        self.game_node.expand()
                #print(self.game_node.children)
                self.parent_window.blocks[self.step_number].game_node = self.game_node.children[selected_action_no]
            self.parent_window.blocks[self.step_number].update_dropdown_from_node()
            
        elif len(self.parent_window.blocks) == self.step_number:
            selected_action_no = self.dropdown.currentIndex()
            if len(self.game_node.children) < selected_action_no+1:
                while not self.game_node.is_fully_expanded():
                    self.game_node.expand()
            self.parent_window.final_game_node = self.game_node.children[selected_action_no]
                
        if self.on_apply_callback:
            self.on_apply_callback(self.step_number)

class RightBlock(QWidget):
    def __init__(self, block_number, text, image_path):
        super().__init__()
        self.block_number = block_number
        self.text = text
        self.image_path = image_path

        self.layout = QVBoxLayout()
        self.label = QLabel(f"T#{block_number} {self.text}")
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
        self.label.setText(f"T#{self.block_number} {self.text}")

    def update_image(self, new_path):
        self.image_path = new_path
        self.load_image(new_path)

class MainWindow(QMainWindow):
    #def __init__(self, dropdown_options_list, extra_texts_list, right_texts, right_images, right_columns=2):
    def __init__(self, solver, teams = [], right_columns = 4):
        super().__init__()
        
        self.solver = solver
        self.teams = teams
        
        n_steps = len(self.solver.step_actions)
        #print(n_steps)
        
        dropdown_options_list = [[] for _ in range(n_steps)]
        #defs_ids = self.solver.game.get_available_defenders(state = self.solver.root.state, team = 0)
        
        #extra_texts_list = [""] * n_steps
        extra_texts_list = []
        tmp_state = self.solver.root.state.copy()
        for step in self.solver.step_actions:
            action, params = step(tmp_state)
            text = ""
            #print(params)
            for key in params[0]:
                if key == "team":
                    text += f"T{params[0][key]} "
                else:
                    text += f"{key} "
            extra_texts_list.append(text)
            action(state = tmp_state, **params[0])
    
        
        right_texts = ["______ vs _______" for i in range(8)]

        # TODO: load from somewhere
        right_images = [
            "C:/Users/79165/YandexDisk/Fest/H&A_F1.png",  
            "C:/Users/79165/YandexDisk/Fest/CoB_F2.png",
            "C:/Users/79165/YandexDisk/Fest/S&D_CA1_FEST.png",
            "C:/Users/79165/YandexDisk/Fest/TP_CA8_FEST.png",
            "C:/Users/79165/YandexDisk/Fest/H&A_CA7.png",
            "C:/Users/79165/YandexDisk/Fest/CoB_CA6.png",
            "C:/Users/79165/YandexDisk/Fest/SA_CA3.png",
            "C:/Users/79165/YandexDisk/Fest/DoW_CA5.png",
            ]
        
        self.final_game_node = None
        
        # sheet stuff
        self.creds = None
        self.client = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Add the new SheetControlBlock at the top
        self.sheet_control = SheetControlBlock(self)
        main_layout.addWidget(self.sheet_control)

        # Main vertical splitter: top (left+right), bottom (console)
        self.vertical_splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(self.vertical_splitter)

        # Top horizontal splitter: left and right parts
        self.horizontal_splitter = QSplitter(Qt.Horizontal)

        # Left side: scroll area with StepBlocks
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        step_blocks_container = QWidget()
        step_blocks_layout = QVBoxLayout()
        step_blocks_container.setLayout(step_blocks_layout)

        self.blocks = []
        for i, (options, extra_text) in enumerate(zip(dropdown_options_list, extra_texts_list), start=1):
            block = StepBlock(self, i, options, extra_text=extra_text, on_apply_callback=self.enable_next_block)
            self.blocks.append(block)
            step_blocks_layout.addWidget(block)
        step_blocks_layout.addStretch()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(step_blocks_container)
        left_layout.addWidget(scroll_area)

        for block in self.blocks:
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

        right_layout.setRowStretch(row + 1, 1)
        right_layout.setColumnStretch(right_columns, 1)

        self.horizontal_splitter.addWidget(right_widget)
        self.horizontal_splitter.setCollapsible(1, False)

        self.vertical_splitter.addWidget(self.horizontal_splitter)

        # Console QTextEdit at bottom part of vertical splitter
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.NoWrap)
        self.console.setMinimumHeight(150)
        self.console.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.vertical_splitter.addWidget(self.console)
        self.vertical_splitter.setCollapsible(1, False)

        self.vertical_splitter.setSizes([700, 150])
        self.horizontal_splitter.setSizes([400, 300])

        self.init_menu()

        sys.stdout = EmittingStream(text_written=self.write_to_console)
        sys.stderr = EmittingStream(text_written=self.write_to_console)

        self.showMaximized()
        
        self.worker = WorkerThread()
        
    def start_solver(self):
        self.blocks[0].game_node = self.solver.root
        self.blocks[0].update_dropdown_from_node()
        self.blocks[0].setDisabled(False)

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

        load_action = QAction("Load credentials...", self)
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def load_data(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Сredintails File", "", "JSON Files (*.json);", options=options)
        if file_name:
            print(f"Load credintails from: {file_name}")
            # Implement your data loading logic here
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
                ]
            
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
            self.client = gspread.authorize(self.creds)
            self.sheet_control.read_btn.setDisabled(False)

    def enable_next_block(self, current_step):
        next_index = current_step  # zero-based index = current_step - 1, next block = current_step
        if next_index < len(self.blocks):
            next_block = self.blocks[next_index]
            if next_block.isEnabled() is False:
                next_block.setDisabled(False)
                print(f"[MainWindow] Enabled Step #{next_block.step_number}")
        
        self.update_right_part(current_step)
        
    def update_right_part(self, current_step):
        #print(f"{current_step} \\ {len(self.blocks)}")
        if current_step == len(self.blocks) and not self.final_game_node is None:
            state = self.final_game_node.state
            #print(self.final_game_node.parent_action)
            #print(state)
            #print(state.formed_pairs)
            final_score = self.solver.game.get_score(state)
            print(f"Pairing game is finished with score {final_score} to team 0")
        else:
            state = self.blocks[current_step].game_node.state
        for form_pair in state.formed_pairs:
            
            p0, p1, t = form_pair
            table_type = self.solver.game.tables[p0, t]
            #print(form_pair, table_type)
            score = self.solver.game.scores[p0, p1, table_type]
            self.right_blocks[t].update_text(f"{self.teams[0][p0]} vs {self.teams[1][p1]}: {score}")
            
        

# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     # Example with 25 step blocks to test scrolling
#     dropdown_options = [["Option 1", "Option 2", "Option 3"]] * 25
#     extra_texts = [f"(Step {i})" for i in range(1, 26)]

#     # Example right side data (3 blocks)
#     right_texts = [
#         "Right block text 1",
#         "Right block text 2",
#         "Right block text 3"
#     ]

#     right_images = [
#         "path/to/image1.png",  # Replace with actual image paths
#         "path/to/image2.png",
#         "path/to/image3.png"
#     ]

#     window = MainWindow(dropdown_options, extra_texts, right_texts, right_images, right_columns=3)
#     window.setWindowTitle("Step Blocks with Scrollable Left, Grid Right, and Console")
#     window.show()
#     sys.exit(app.exec_())
