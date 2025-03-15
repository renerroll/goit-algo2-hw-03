import csv
import timeit
from BTrees.OOBTree import OOBTree 

def load_data(filename):
    items = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = {
                'ID': int(row['ID']),
                'Name': row['Name'],
                'Category': row['Category'],
                'Price': float(row['Price'])
            }
            items.append(item)
    return items

def add_item_to_tree(tree, item):
    tree.insert(item['ID'], item)

def add_item_to_dict(dictionary, item):
    dictionary[item['ID']] = item

def range_query_tree(tree, min_price, max_price):
    return [
        value for key, value in tree.items()
        if min_price <= value['Price'] <= max_price
    ]

def range_query_dict(dictionary, min_price, max_price):
    return [
        value for value in dictionary.values()
        if min_price <= value['Price'] <= max_price
    ]

def measure_time(query_function, data_structure, min_price, max_price):
    setup_code = f"""
from __main__ import {query_function.__name__}, {data_structure.__name__}, min_price, max_price, tree, dictionary
"""
    test_code = f"{query_function.__name__}(tree if data_structure == 'tree' else dictionary, min_price, max_price)"
    return timeit.timeit(test_code, setup=setup_code, number=100)

if __name__ == '__main__':
    items = load_data('generated_items_data.csv')
    
    tree = OOBTree()
    dictionary = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    min_price = 50.0
    max_price = 150.0

    tree_time = timeit.timeit(
        stmt=lambda: range_query_tree(tree, min_price, max_price), number=100
    )

    dict_time = timeit.timeit(
        stmt=lambda: range_query_dict(dictionary, min_price, max_price), number=100
    )

    print(f"Total range_query time for OOBTree: {tree_time:.4f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.4f} seconds")
