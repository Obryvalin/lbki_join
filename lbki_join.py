# core.py
import csv
from typing import List, Dict, Any, Tuple, Optional

def detect_delimiter(file_path: str) -> str:
    """Автоматическое определение разделителя."""
    with open(file_path, 'r', encoding='utf-8') as f:
        sample = f.read(1024)
        f.seek(0)
        sniffer = csv.Sniffer()
        return sniffer.sniff(sample).delimiter

def read_csv(file_path: str, delimiter: Optional[str] = None) -> Tuple[List[str], List[Dict[str, str]]]:
    """Читаем CSV, возвращаем заголовки и данные (список словарей)."""
    if delimiter is None:
        delimiter = detect_delimiter(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        headers = reader.fieldnames or []
        data = [row for row in reader]
    return headers, data

def join_data(
    left_data: List[Dict[str, str]],
    right_data: List[Dict[str, str]],
    left_key: str,
    right_key: str,
    join_type: str = 'inner'
) -> List[Dict[str, str]]:
    """
    Выполняет JOIN операции.
    Поддерживает: inner, left, right, outer.
    Ключи могут отличаться по названию.
    """
    result = []

    # Индекс правой таблицы по ключу
    right_index = {}
    for row in right_data:
        key = row.get(right_key, '')
        if key not in right_index:
            right_index[key] = []
        right_index[key].append(row)

    all_left_keys = set(row.get(left_key, '') for row in left_data)
    all_right_keys = set(right_index.keys())
    common_keys = all_left_keys & all_right_keys

    for left_row in left_data:
        lkey = left_row.get(left_key, '')

        if join_type == 'inner':
            if lkey in common_keys:
                for rrow in right_index.get(lkey, []):
                    result.append({**left_row, **rrow})

        elif join_type == 'left':
            if lkey in right_index:
                for rrow in right_index[lkey]:
                    result.append({**left_row, **rrow})
            else:
                merged = {**left_row}
                merged.update({k: '' for k in right_data[0].keys()})  # Пустые поля справа
                result.append(merged)

        elif join_type == 'right':
            if lkey in right_index:
                for rrow in right_index[lkey]:
                    result.append({**left_row, **rrow})
            else:
                # Обработка случая, когда нет совпадений слева — добавляем только правые строки позже
                pass

    # Для RIGHT и OUTER отдельно обрабатываем правые строки без совпадений
    if join_type in ('right', 'outer'):
        for rrow in right_data:
            rkey = rrow.get(right_key, '')
            if rkey not in all_left_keys or join_type == 'outer':
                matched = False
                for lrow in left_data:
                    if lrow.get(left_key, '') == rkey:
                        result.append({**lrow, **rrow})
                        matched = True
                if not matched:
                    merged = {k: '' for k in left_data[0].keys()} if left_data else {}
                    merged.update(rrow)
                    result.append(merged)

    if join_type == 'outer':
        # Уже обработано выше
        pass

    return result

def write_csv(data: List[Dict[str, str]], output_path: str, delimiter: str = ','):
    """Запись результата в CSV."""
    if not data:
        print("Нет данных для записи.")
        return

    fieldnames = list(data[0].keys())
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)