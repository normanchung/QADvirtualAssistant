import json

def parse_menu_data():
    """
    Description: Maps the meta_uri for a specific menu item
    Return: new JSON object @ 'qad-metadata/menu-data-new.json'
    """

    dict = {}
    # read menu data and extract relevant info
    with open('qad-metadata/menu-data.json', 'r') as file:
        data = json.load(file)
        for role in data:
            for items in role['subMenuItems']:
                if items['subMenuItems']:
                    for subitems in items['subMenuItems']:
                        # 1-to-1 mapping of name and meta_uri
                        dict[subitems['label']] = subitems['target']
                        
    # create new JSON object
    with open('qad-metadata/menu-data-new.json', 'w') as file:
        json.dump(dict, file)

def get_menu_data():
    """
    Usage: dict[menu_item] = meta_uri
    Return: dictionary from JSON object @ 'qad-metadata/menu-data-new.json'
    """

    with open('qad-metadata/menu-data-new.json', 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    parse_menu_data()