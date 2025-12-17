import struct
import argparse
import xml.etree.ElementTree as ET

MEM_SIZE = 1024  # Размер памяти УВМ

class UVM:
    def __init__(self):
        self.memory = [0] * MEM_SIZE  # Объединенная память команд и данных
        self.stack = []               # Стек
        self.ip = 0                   # Instruction pointer
        self.program = []             # Список инструкций в промежуточном представлении

    # ==============================
    # Загрузка бинарной программы
    # ==============================
    def load_program(self, path):
        with open(path, "rb") as f:
            data = f.read()
        for i in range(0, len(data), 4):
            word = struct.unpack("<I", data[i:i+4])[0]
            A = word & 0b111111          # младшие 6 бит
            B = word >> 6                 # старшие биты
            self.program.append({"A": A, "B": B})

    # ==============================
    # Основной цикл выполнения программы
    # ==============================
    def run(self):
        while self.ip < len(self.program):
            instr = self.program[self.ip]
            self.execute(instr)
            self.ip += 1

    # ==============================
    # Исполнение одной команды
    # ==============================
    def execute(self, instr):
        A = instr["A"]
        B = instr["B"]

        if A == 42:  # LOAD_CONST
            self.stack.append(B)

        elif A == 23:  # READ_MEM
            if not (0 <= B < MEM_SIZE):
                raise ValueError(f"Адрес {B} вне диапазона памяти")
            self.stack.append(self.memory[B])

        elif A == 1:  # WRITE_MEM
            if len(self.stack) < 2:
                raise ValueError("Недостаточно элементов на стеке для WRITE_MEM")
            addr = self.stack.pop()
            value = self.stack.pop()
            if not (0 <= addr < MEM_SIZE):
                raise ValueError(f"Адрес {addr} вне диапазона памяти")
            self.memory[addr] = value

        elif A == 60:  # BITREVERSE
            if not self.stack:
                raise ValueError("Стек пуст для BITREVERSE")
            value = self.stack.pop()
            rev = int('{:032b}'.format(value)[::-1], 2)
            self.stack.append(rev)

        else:
            raise ValueError(f"Неизвестная команда A={A}")

    # ==============================
    # Дамп памяти в XML
    # ==============================
    def dump_memory(self, start, end, path):
        if not (0 <= start <= end < MEM_SIZE):
            raise ValueError("Диапазон дампа вне границ памяти")
        root = ET.Element("memory")
        for addr in range(start, end + 1):
            cell = ET.SubElement(root, "cell")
            cell.set("address", str(addr))
            cell.text = str(self.memory[addr])
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

# ==============================
# CLI
# ==============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Интерпретатор УВМ — Этап 3")
    parser.add_argument("binary", help="Путь к бинарному файлу программы")
    parser.add_argument("output", help="Путь к файлу XML дампа памяти")
    parser.add_argument("--start", type=int, required=True, help="Начальный адрес дампа")
    parser.add_argument("--end", type=int, required=True, help="Конечный адрес дампа")
    args = parser.parse_args()

    uvm = UVM()
    uvm.load_program(args.binary)
    uvm.run()
    uvm.dump_memory(args.start, args.end, args.output)
    print(f"Дамп памяти сохранён в {args.output}")
