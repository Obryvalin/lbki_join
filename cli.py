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
    parser.add_argument('-d', '--delimiter', choices=[',', ';', '\t'], help='Разделитель (если не указан — автоопределение)')
    parser.add_argument('-o', '--output', required=True, help='Выходной CSV файл')

    args = parser.parse_args()

    delim = args.delimiter
    if delim == '\t':
        delim = '\t'  # корректная передача табуляции

    try:
        left_headers, left_data = read_csv(args.left_file, delim)
        right_headers, right_data = read_csv(args.right_file, delim)

        # Проверка наличия ключей
        if args.left_key not in left_headers:
            raise ValueError(f"Ключ '{args.left_key}' не найден в левом файле. Доступные: {left_headers}")
        if args.right_key not in right_headers:
            raise ValueError(f"Ключ '{args.right_key}' не найден в правом файле. Доступные: {right_headers}")

        result = join_data(left_data, right_data, args.left_key, args.right_key, args.join_type)
        write_csv(result, args.output, delim or ',')

        print(f"[✓] JOIN выполнен. Результат сохранён в: {args.output}")
        print(f"    Строк в результате: {len(result)}")

    except Exception as e:
        print(f"[✕] Ошибка: {e}")

if __name__ == '__main__':
    main()