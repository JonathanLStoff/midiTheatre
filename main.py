import json
import sys

from PySide6.QtCore import QAbstractListModel, QSortFilterProxyModel, Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget
)


class Action:
    def __init__(self, name, channel, key, value):
        self.name = name
        self.channel = channel
        self.key = key
        self.value = value

class ActionModel(QAbstractListModel):
    def __init__(self, actions=None):
        super().__init__()
        self.actions = actions or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.actions[index.row()].name
        return None

    def rowCount(self, index):
        return len(self.actions)

class ActionManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Action Manager")
        self.setGeometry(100, 100, 800, 600)
        
        self.actions = []
        self.current_order = []
        self.load_data()
        
        self.init_ui()
        
    def init_ui(self):
        main_splitter = QSplitter()
        
        # Sidebar
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout()
        
        self.sidebar_list = QListView()
        self.action_model = ActionModel(self.actions)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.action_model)
        self.proxy_model.sort(0, Qt.AscendingOrder)
        self.sidebar_list.setModel(self.proxy_model)
        
        new_btn = QPushButton("New Action")
        new_btn.clicked.connect(self.create_action)
        
        sidebar_layout.addWidget(self.sidebar_list)
        sidebar_layout.addWidget(new_btn)
        sidebar_widget.setLayout(sidebar_layout)
        
        # Main content
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        
        self.order_list = QListWidget()
        
        btn_layout = QHBoxLayout()
        up_btn = QPushButton("↑")
        up_btn.clicked.connect(lambda: self.move_item(-1))
        down_btn = QPushButton("↓")
        down_btn.clicked.connect(lambda: self.move_item(1))
        btn_layout.addWidget(up_btn)
        btn_layout.addWidget(down_btn)
        
        content_layout.addWidget(self.order_list)
        content_layout.addLayout(btn_layout)
        content_widget.setLayout(content_layout)
        
        main_splitter.addWidget(sidebar_widget)
        main_splitter.addWidget(content_widget)
        
        self.setCentralWidget(main_splitter)
        self.refresh_lists()
        
    def refresh_lists(self):
        self.action_model.layoutChanged.emit()
        self.order_list.clear()
        self.order_list.addItems([action.name for action in self.current_order])

    def load_data(self):
        try:
            with open('actions.json', 'r') as f:
                data = json.load(f)
                self.actions = [Action(a['name'], a['channel'], a['key'], a['value']) 
                               for a in data.get('actions', [])]
                ordered_names = data.get('order', [])
                self.current_order = [next(act for act in self.actions if act.name == name) 
                                     for name in ordered_names]
        except FileNotFoundError:
            self.actions = []
            self.current_order = []

    def save_data(self):
        data = {
            'actions': [{'name': a.name, 'channel': a.channel, 
                        'key': a.key, 'value': a.value} for a in self.actions],
            'order': [a.name for a in self.current_order]
        }
        with open('actions.json', 'w') as f:
            json.dump(data, f)

    def create_action(self):
        dialog = ActionDialog(self)
        if dialog.exec():
            new_action = dialog.get_action()
            if any(a.name == new_action.name for a in self.actions):
                QMessageBox.warning(self, "Error", "Action name must be unique")
                return
                
            self.actions.append(new_action)
            self.current_order.append(new_action)
            self.save_data()
            self.refresh_lists()

    def move_item(self, direction):
        current_row = self.order_list.currentRow()
        if current_row == -1:
            return
            
        new_row = current_row + direction
        if 0 <= new_row < len(self.current_order):
            self.current_order.insert(new_row, self.current_order.pop(current_row))
            self.save_data()
            self.refresh_lists()
            self.order_list.setCurrentRow(new_row)

class ActionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Action")
        
        layout = QVBoxLayout()
        
        self.name_edit = QLineEdit()
        self.channel_edit = QLineEdit()
        self.channel_edit.setValidator(QIntValidator(0, 127))
        self.key_edit = QLineEdit()
        self.key_edit.setValidator(QIntValidator(0, 127))
        self.value_edit = QLineEdit()
        self.value_edit.setValidator(QIntValidator(0, 127))
        
        fields = [
            ("Name:", self.name_edit),
            ("Channel (0-127):", self.channel_edit),
            ("Key (0-127):", self.key_edit),
            ("Value (0-127):", self.value_edit)
        ]
        
        for label, widget in fields:
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(label))
            hbox.addWidget(widget)
            layout.addLayout(hbox)
            
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        
    def get_action(self):
        return Action(
            self.name_edit.text(),
            int(self.channel_edit.text()),
            int(self.key_edit.text()),
            int(self.value_edit.text())
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ActionManager()
    window.show()
    sys.exit(app.exec())