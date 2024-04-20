def search_json(json_data, search_word):
    results = []

    if isinstance(json_data, dict):
        search_dict(json_data, search_word.lower(), results)

    return results


def search_dict(data, search_word, results, parent_keys=[]):
    for key, value in data.items():
        current_keys = parent_keys + [key]
        if isinstance(value, dict):
            search_dict(value, search_word, results, current_keys)
        elif isinstance(value, list):
            search_list(value, search_word, results, current_keys)
        elif isinstance(value, str) and search_word in value.lower():
            results.append(
                {"keys": current_keys, "value": value, "search_word": search_word}
            )


def search_list(data_list, search_word, results, parent_keys=[]):
    for index, item in enumerate(data_list):
        current_keys = parent_keys + [str(index)]
        if isinstance(item, dict):
            search_dict(item, search_word, results, current_keys)
        elif isinstance(item, list):
            search_list(item, search_word, results, current_keys)
        elif isinstance(item, str) and search_word in item.lower():
            results.append(
                {"keys": current_keys, "value": item, "search_word": search_word}
            )
