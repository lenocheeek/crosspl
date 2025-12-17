import sys
import struct
import argparse

# ==============================
# Спецификация команд УВМ
# ==============================
INSTRUCTIONS = {
    "LOAD_CONST": {"A": 42, "B_bits": (6, 21)},  # Загрузка константы в стек
    "READ_MEM":   {"A": 23, "B_bits": (6, 29)},  # Чтение из памяти
    "WRITE_MEM":  {"A": 1,  "B_bits": None},     # Запись в память (операнд с вершины стека)
    "BITREVERSE": {"A": 60, "B_bits": None},     # Унарная операция
}

# ==============================
# Разбор строки ассемблера
# ==============================
def assemble_line(line):
    """
    Преобразует строку ассемблера в промежуточное представление.
    Формат промежуточного представления: {"A": int, "B": int or None}
    """
    # Игнорируем пустые строки и комментарии
    parts = line.strip().split()
    if not parts or parts[0].startswith(";"):
        return None

    mnemonic = parts[0].upper()
    if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Неизвестная команда: {mnemonic}")

    instr = INSTRUCTIONS[mnemonic]
    
    # Проверяем наличие операнда
    operand = None
    if instr["B_bits"]:  # Если команда требует операнд
        if len(parts) < 2:
            raise ValueError(f"Команда {mnemonic} требует операнд")
        operand = int(parts[1])
    return {"A": instr["A"], "B": operand}

# ==============================
# Преобразование в машинный код
# ==============================
def intermediate_to_binary(intermediate):
    """
    Преобразует промежуточное представление в машинный код (4 байта на команду)
    """
    binary_code = bytearray()
    for instr in intermediate:
        A = instr["A"]
        B = instr["B"] or 0
        # Составляем 32-битное слово: A в младших 6 битах, B в старших битах
        word = (B << 6) | A
        binary_code += struct.pack("<I", word)  # little-endian
    return binary_code

# ==============================
# Основная сборка файла
# ==============================
def assemble_file(input_path, output_path, test_mode=False):
    """
    Ассемблирует текстовый файл в бинарный.
    В режиме test_mode выводит промежуточное представление и hex-код.
    """
    # Чтение исходного файла и формирование промежуточного представления
    intermediate = []
    with open(input_path, "r") as f:
        for line in f:
            instr = assemble_line(line)
            if instr:
                intermediate.append(instr)

    if test_mode:
        print("\n=== Промежуточное представление ===")
        for i, instr in enumerate(intermediate):
            print(f"{i}: {instr}")

    # Преобразование в машинный код
    binary_code = intermediate_to_binary(intermediate)

    # Сохранение в бинарный файл
    with open(output_path, "wb") as f:
        f.write(binary_code)

    print(f"\nКоличество ассемблированных команд: {len(intermediate)}")

    if test_mode:
        print("\n=== Байтовый формат (hex) ===")
        for i in range(0, len(binary_code), 4):
            chunk = binary_code[i:i+4]
            print(" ".join(f"0x{b:02X}" for b in chunk))

# ==============================
# CLI
# ==============================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ассемблер для УВМ (Этап 1)")
    parser.add_argument("input", help="Путь к исходному файлу asm")
    parser.add_argument("output", help="Путь к бинарному файлу")
    parser.add_argument("--test", action="store_true", help="Режим тестирования")
    args = parser.parse_args()

    assemble_file(args.input, args.output, test_mode=args.test)
