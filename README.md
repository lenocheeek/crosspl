# Учебная Виртуальная Машина (УВМ)

Проект реализует учебную виртуальную машину (УВМ) с ассемблером, интерпретатором и GUI для работы с памятью и стековыми операциями.  
Поддерживаются команды загрузки констант, чтения и записи памяти, а также унарная операция `BITREVERSE`.

---

## **Содержание репозитория**
assembler_itog/
├─ assembler.py # Ассемблер для УВМ
├─ interpreter.py # Интерпретатор УВМ
├─ uvm_gui.py # Кроссплатформенный GUI для Mac/Windows/Linux
├─ examples/ # Тестовые программы на ассемблере
│ ├─ vector_bitreverse.asm
│ ├─ vector_bitreverse_2.asm
│ └─ vector_bitreverse_3.asm
├─ README.md

## **Этапы работы**

### Этап 1 — Ассемблер
- Создан CLI-ассемблер (`assembler.py`), который переводит текстовую программу на ассемблере в промежуточное представление.
- Поддерживаются команды:
  - `LOAD_CONST <значение>` — загрузка константы на стек
  - `READ_MEM <адрес>` — чтение значения из памяти на стек
  - `WRITE_MEM` — запись элемента со стека в память
  - `BITREVERSE` — переворот битов верхнего элемента стека
- Режим тестирования `--test` выводит промежуточное представление и машинный код в hex.

**Пример запуска:**

```bash
python3 assembler.py examples/vector_bitreverse.asm vector_bitreverse.bin --test
```
### Этап 2 - Формирование машинного кода
- Ассемблер преобразует промежуточное представление в 4-байтовые команды.
- Результат сохраняется в бинарный файл для интерпретатора.
### Этап 3 - Интерпретатор и операции с памятью
- Интерпретатор (interpreter.py) выполняет команды УВМ.
- Память моделируется как массив размером 1024 ячейки.
- Возможности:
  -  Загрузка констант
  -  Чтение и запись в память
  -  Унарная операция BITREVERSE
-  Вывод дампа памяти в XML-файл.
**Пример запуска:**
```bash
python3 interpreter.py vector_bitreverse_2.bin memory_vector_2.xml --start 0 --end 9
```
### Этап 4 - Арифметико-логическое устройство (АЛУ)
- Реализована операция BITREVERSE.
- Тестовые программы демонстрируют корректность выполнения с записью результатов в память.
### Этап 5 - Тестовые задачи
- Примеры:
  - Вектор [1..10] → применение BITREVERSE.
  - Вектор [10..19] → применение BITREVERSE.
  - Произвольный вектор [5,123,255,1024,512,7,31,63,128,256] → BITREVERSE.
- Дамп памяти для каждого примера создается в XML и соответствует ожиданиям.
### Этап 6 - Кроссплатформенный GUI
- uvm_gui.py — графический интерфейс для работы с УВМ:
  - Редактор программы на ассемблере
  - Кнопка "Ассемблировать и Запустить"
  - Вывод дампа памяти
- Сборка нативного приложения на Mac:
```bash
pyinstaller --name UVM_GUI --onefile --windowed uvm_gui.py
```
- Поддержка Windows и Linux через PyInstaller.
## Примеры тестов
### Тест 1 — Инициализация и копирование массива
```asm
; Инициализация исходного вектора: 1,2,3,4,5 в ячейки 0..4
LOAD_CONST 1
LOAD_CONST 0
WRITE_MEM

LOAD_CONST 2
LOAD_CONST 1
WRITE_MEM

LOAD_CONST 3
LOAD_CONST 2
WRITE_MEM

LOAD_CONST 4
LOAD_CONST 3
WRITE_MEM

LOAD_CONST 5
LOAD_CONST 4
WRITE_MEM

; Копирование элементов в обратном порядке: в ячейки 10..14
READ_MEM 4
LOAD_CONST 10
WRITE_MEM

READ_MEM 3
LOAD_CONST 11
WRITE_MEM

READ_MEM 2
LOAD_CONST 12
WRITE_MEM

READ_MEM 1
LOAD_CONST 13
WRITE_MEM

READ_MEM 0
LOAD_CONST 14
WRITE_MEM
```
### Ожидаемый дамп:
```markdown
[0]: 1
[1]: 2
[2]: 3
[3]: 4
[4]: 5
[10]: 5
[11]: 4
[12]: 3
[13]: 2
[14]: 1
```
### Тест 2 — BITREVERSE для вектора [10..19]
```asm
; Инициализация вектора 10..19 в ячейки 0..9
LOAD_CONST 10
LOAD_CONST 0
WRITE_MEM

LOAD_CONST 11
LOAD_CONST 1
WRITE_MEM

LOAD_CONST 12
LOAD_CONST 2
WRITE_MEM

LOAD_CONST 13
LOAD_CONST 3
WRITE_MEM

LOAD_CONST 14
LOAD_CONST 4
WRITE_MEM

LOAD_CONST 15
LOAD_CONST 5
WRITE_MEM

LOAD_CONST 16
LOAD_CONST 6
WRITE_MEM

LOAD_CONST 17
LOAD_CONST 7
WRITE_MEM

LOAD_CONST 18
LOAD_CONST 8
WRITE_MEM

LOAD_CONST 19
LOAD_CONST 9
WRITE_MEM

; Применяем BITREVERSE ко всем элементам
READ_MEM 0
BITREVERSE
LOAD_CONST 0
WRITE_MEM

READ_MEM 1
BITREVERSE
LOAD_CONST 1
WRITE_MEM

READ_MEM 2
BITREVERSE
LOAD_CONST 2
WRITE_MEM

READ_MEM 3
BITREVERSE
LOAD_CONST 3
WRITE_MEM

READ_MEM 4
BITREVERSE
LOAD_CONST 4
WRITE_MEM

READ_MEM 5
BITREVERSE
LOAD_CONST 5
WRITE_MEM

READ_MEM 6
BITREVERSE
LOAD_CONST 6
WRITE_MEM

READ_MEM 7
BITREVERSE
LOAD_CONST 7
WRITE_MEM

READ_MEM 8
BITREVERSE
LOAD_CONST 8
WRITE_MEM

READ_MEM 9
BITREVERSE
LOAD_CONST 9
WRITE_MEM
```
### Ожидаемый дамп:
```markdown
[0]: 1342177280
[1]: 3724541952
...
[9]: 3355443200
```
### Тест 3 — Произвольный вектор [5,123,255,1024,...]
```asm
; Инициализация произвольного вектора в ячейки 0..7
LOAD_CONST 5
LOAD_CONST 0
WRITE_MEM

LOAD_CONST 123
LOAD_CONST 1
WRITE_MEM

LOAD_CONST 255
LOAD_CONST 2
WRITE_MEM

LOAD_CONST 1024
LOAD_CONST 3
WRITE_MEM

LOAD_CONST 7
LOAD_CONST 4
WRITE_MEM

LOAD_CONST 31
LOAD_CONST 5
WRITE_MEM

LOAD_CONST 64
LOAD_CONST 6
WRITE_MEM

LOAD_CONST 511
LOAD_CONST 7
WRITE_MEM

; Применяем BITREVERSE ко всем элементам
READ_MEM 0
BITREVERSE
LOAD_CONST 0
WRITE_MEM

READ_MEM 1
BITREVERSE
LOAD_CONST 1
WRITE_MEM

READ_MEM 2
BITREVERSE
LOAD_CONST 2
WRITE_MEM

READ_MEM 3
BITREVERSE
LOAD_CONST 3
WRITE_MEM

READ_MEM 4
BITREVERSE
LOAD_CONST 4
WRITE_MEM

READ_MEM 5
BITREVERSE
LOAD_CONST 5
WRITE_MEM

READ_MEM 6
BITREVERSE
LOAD_CONST 6
WRITE_MEM

READ_MEM 7
BITREVERSE
LOAD_CONST 7
WRITE_MEM
```
### Ожидаемый дамп:
```markdown
[0]: 2684354560
[1]: 3724541952
...
[7]: 4286578688
```

## Инструкция по использованию
1. Написать программу на ассемблере в examples/.
2. Ассемблировать:
```bash
python3 assembler.py examples/my_program.asm my_program.bin
```
3. Выполнить программу через интерпретатор:
```bash
python3 interpreter.py my_program.bin memory_dump.xml --start 0 --end 15
```
4. Для GUI:
```bash
python3 uvm_gui.py
```


## Примечания
- Интерпретатор использует стековую модель, память инициализируется нулями.
- BITREVERSE работает на 32-битных значениях.
- GUI кроссплатформенный и может быть собран на Mac, Windows и Linux.
