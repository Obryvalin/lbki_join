# cli.py
import argparse
from lbki_join import read_csv, join_data, write_csv

def main():
    parser = argparse.ArgumentParser(description="LBKI_JOIN: SQL-style JOIN для CSV файлов")

    parser.add_argument('left_file', help='Путь к левому CSV')
    parser.add_argument('right_file', help='Путь к правому CSV')
    parser.add_argument('-k1', '--left-key', required=True, help='Колонка в левом файле для JOIN')
    parser.add_argument('-k2', '--right-key', required=True, help='Колонка в правом файле для JOIN')
    parser.add_argument('-t', '--join-type', choices=['inner', 'left', 'right', 'outer'],
                        default='inner', help='Тип JOIN (по умолчанию: inner)')
    parser.add_argument('-d1', '--left-delimiter', choices=[',', ';', '\t'], help='Разделитель левого файла (если не указан — автоопределение)')
    parser.add_argument('-d2', '--right-delimiter', choices=[',', ';', '\t'], help='Разделитель правого файла (если не указан — автоо��ределение)')
    parser.add_argument('-o', '--output', required=True, help='Выходной CSV файл')

    args = parser.parse_args()

    left_delim = args.left_delimiter
    right_delim = args.right_delimiter
    if left_delim == '\t':
        left_delim = '\t'
    if right_delim == '\t':
        right_delim = '\t'

    try:
        left_headers, left_data = read_csv(args.left_file, left_delim)
        right_headers, right_data = read_csv(args.right_file, right_delim)

        # Проверка наличия ключей
        if args.left_key not in left_headers:
            raise ValueError(f"Ключ '{args.left_key}' не найден в левом файле. Доступные: {left_headers}")
        if args.right_key not in right_headers:
            raise ValueError(f"Ключ '{args.right_key}' не найден в правом файле. Доступные: {right_headers}")

        result = join_data(left_data, right_data, args.left_key, args.right_key, args.join_type)
        write_csv(result, args.output, left_delim or ',')

        print(f"\n[✓] JOIN выполнен успешно!")
        print(f"{'─' * 50}")
        print(f"Статистика:")
        print(f"  Левый файл (LEFT):     {len(left_data)} строк")
        print(f"  Правый файл (RIGHT):   {len(right_data)} строк")
        print(f"{'─' * 50}")
        print(f"  Результат ({args.join_type.upper()}):      {len(result)} строк")
        print(f"{'─' * 50}")
        print(f"Сохранено в: {args.output}\n")

    except Exception as e:
        print(f"[✕] Ошибка: {e}")

if __name__ == '__main__':
    main()