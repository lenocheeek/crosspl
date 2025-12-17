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
    parts = line.strip().split()
    if not parts or parts[0].startswith(";"):
        return None
    mnemonic = parts[0].upper()
    if mnemonic not in INSTRUCTIONS:
        raise ValueError(f"Неизвестная команда: {mnemonic}")
    instr = INSTRUCTIONS[mnemonic]
    operand = None
    if instr["B_bits"]:
        if len(parts) < 2:
            raise ValueError(f"Команда {mnemonic} требует операнд")
        operand = int(parts[1])
    return {"A": instr["A"], "B": operand}

# ==============================
# Преобразование в машинный код
# ==============================
def intermediate_to_binary(intermediate):
    binary_code = bytearray()
    for instr in intermediate:
        A = instr["A"]
        B = instr["B"] or 0
        word = (B << 6) | A
        binary_code += struct.pack("<I", word)
    return binary_code

# ==============================
# Ассемблирование файла
# ==============================
def assemble_file(input_path, output_path, test_mode=False):
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

    binary_code = intermediate_to_binary(intermediate)

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
    parser = argparse.ArgumentParser(description="Ассемблер для УВМ (Этап 2)")
    parser.add_argument("input", help="Путь к исходному файлу asm")
    parser.add_argument("output", help="Путь к бинарному файлу")
    parser.add_argument("--test", action="store_true", help="Режим тестирования")
    args = parser.parse_args()

    assemble_file(args.input, args.output, test_mode=args.test)
