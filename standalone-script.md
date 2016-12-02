---
layout: page
title: Standalone-скрипт
permalink: /standalone-script/
---


## Парсинг

XML-ки на вход приходят небольшие, поэтому чем париться с SAX- или DOM-парсингом — проще сразу сконвертировать в python dictionary, тем более что благодаря [xmltodict](https://github.com/martinblech/xmltodict) с этим проблем не возникает; и уже этот словарь дальше анализировать. Доступа ко всей РосРеестровской машинерии для XML-преобразований всё равно нет.

Python dictionary — это почти то же самое, что и JSON. Поэтому анализировать удобнее всего через Developer Tools какого-нибудь браузера. Скрипт умеет не просто выплёвывать JSON, но заворачивать его в html-файл с доступом к данным через `window.data` в консоли:

```bash
cd standalone-script
./parse.py -i instectable-data.html your_input_data.xml
# на выходе будет файлик instectable-data.html, который можно
# открыть в браузере и в консоли пристально рассмотреть переменную `data` 
```

Эта возможность полезна для отладки при добавлении нового функционала. Форматов-то у РосРеестра, как оказалось, больше одного =)


## Экспорт JSON

Если хочется сохранить JSON-дамп документа целиком, используйте параметр `-j`:

```bash
./parse.py ./data-samples/doc14350111.xml -j ./output.json
```

На выходе будет JSON-представление оригинального XML-документа целиком. 


## Экспорт CSV

Собственно полезной нагрузкой является вытаскивание из XML-файлов информации об участках и её экспорт в CSV:

```bash
./parse.py ./data-samples/doc14350111.xml -c ./output.csv -v
```

Здесь мы уже получаем только нужную информацию.


## Многословный режим

Флаг `--verbose` (или сокращённо `-v`) включает отображение подробной информации о ходе работы скрипта:

```bash
➜  ./parse.py ./data-samples/doc14350111.xml -j ./test.json -c ./test.csv -H test.html -v
Parsing original document...
Parsing original document DONE
Storing JSON file...
Storing JSON file DONE
Storing HTML file...
Storing HTML file DONE
Extracting Parcels...
Extracting Parcels DONE
Storing CSV file...
Storing CSV file DONE
```

## Внутреннее устройство

Архитектурой внутреннее устройства скрипта назвать было бы слишком уж громко, так что обойдёмся словами попроще.

В файле `parse.py` расположен целый ряд функций с вполне говорящими названиями:

- `parse_to_dict(file_path)` - превращает xml-файл в python dictionary
- `dump_dict_to_json(data)` — сохраняет словарь в красиво отформатированный JSON-файл
- `get_root_node_name(file_dict)` — выясняет, с какого рода файлом мы имеем дело (по имени корневого узла)
- `find_parcel_node(data)` — локализует узел с данными по участкам
- `get_raw_parcels(file_dict)` — вытаскивает сырые данные об участках
- `clean_parcels(raw_parcels)` — очищает сырые данные, оставляя только нужные в понятном формате
- `store_as_csv(parcels, output_file_path)` — сохраняет CSV-файл

Кроме того там содержится код для анализа параметров, с которыми вызывается скрипт, он тоже вполне говорящий.

```python
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path", help="input xml file to parse", type=str)
    parser.add_argument("-c", "--csv_output_file_path", help="output csv file to export data", type=str)
    parser.add_argument("-j", "--json_output_file_path", help="output csv file to export data", type=str)
    parser.add_argument("-H", "--html_output_file_path", help="create an html file with navigateable JSON representation", type=str)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")    
    args = parser.parse_args()
```