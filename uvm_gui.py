import sys
import tempfile
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from assembler import assemble_file
from interpreter import UVM

class UVMGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Учебная Виртуальная Машина (УВМ)")
        self.resize(800, 600)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Редактор программы (ассемблер):"))
        self.editor = QTextEdit()
        layout.addWidget(self.editor)
        
        self.run_button = QPushButton("Ассемблировать и Запустить")
        self.run_button.clicked.connect(self.run_program)
        layout.addWidget(self.run_button)
        
        layout.addWidget(QLabel("Дамп памяти:"))
        self.memory_output = QTextEdit()
        self.memory_output.setReadOnly(True)
        layout.addWidget(self.memory_output)
        
        self.setLayout(layout)

    def run_program(self):
        # Создаём временные файлы
        with tempfile.NamedTemporaryFile(suffix=".asm", delete=False) as asm_file:
            asm_file.write(self.editor.toPlainText().encode('utf-8'))
            asm_path = asm_file.name
            
        with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as bin_file:
            bin_path = bin_file.name
        
        # Ассемблируем
        try:
            assemble_file(asm_path, bin_path, test_mode=False)
        except Exception as e:
            self.memory_output.setPlainText(f"Ошибка ассемблера:\n{e}")
            return
        
        # Запускаем интерпретатор
        uvm = UVM()
        try:
            uvm.load_program(bin_path)
            uvm.run()
        except Exception as e:
            self.memory_output.setPlainText(f"Ошибка интерпретатора:\n{e}")
            return
        
        # Выводим дамп памяти (весь диапазон или 0-15)
        output_text = ""
        for addr in range(16):
            output_text += f"[{addr}]: {uvm.memory[addr]}\n"
        self.memory_output.setPlainText(output_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UVMGUI()
    window.show()
    sys.exit(app.exec())
