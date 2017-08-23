from channels.models import Categories
from collections import defaultdict
import csv


def csv_to_list(csv_file):
    categories = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                if k == "Category":
                    categories.append(v.split("/"))
    return categories


def fill_database(categories_list, channel_obj):
    for item in categories_list:
        if len(item) == 1:
            category = Categories.objects.create(name=item[-1].strip(),
                                                 channel=channel_obj)
            ancestors_list = [category]
        elif len(item) >= 2:
            if len(ancestors_list) >= len(item):
                non_ancestors_total = len(ancestors_list) - len(item) + 1
                for remove in range(non_ancestors_total):
                    ancestors_list.pop()
            category = Categories.objects.create(name=item[-1].strip(),
                                                 channel=channel_obj,
                                                 parent=ancestors_list[-1])
            ancestors_list.append(category)
    return True
