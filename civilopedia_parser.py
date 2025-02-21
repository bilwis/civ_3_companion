import re
import json

#Read Civilopedia (directly copied from game folder)
def read_civilopedia(filename):
    rx = re.compile(r"#(?P<key>[\w\t '-]+)\n(?P<title>[^\^][\w\ ]+)?\n*?(?P<body>[\s\S]*?)(?=^\n*$|#)", flags=re.MULTILINE)
    rx_key_only = re.compile(r"#(?P<key>[\w\t '-]+)")
    rx_category = re.compile(r"; (?P<category>[a-zA-Z]+[ a-zA-Z]+)_{10}")
    rx_subcategory = re.compile(r";[ ]{1,10}_+ ?(?P<subcategory>[a-zA-Z-]+[ a-zA-Z]+)_+")

    with open(filename, 'r', encoding='cp1252') as file:
        raw_data = file.read()

    #Remove comment lines for regex search
    lines = raw_data.split('\n')
    filtered_lines = [line for line in lines if not line.startswith(';')]
    data = '\n'.join(filtered_lines)

    #Get each match and create dict entry for it
    dict = {}
    for entry in rx.finditer(data):
        key = entry.group("key").lower().strip()
        #print(key)

        division = key.split('_')

        if division[0] == "desc":
            key2 = key.split('_')[1:]
            key = '_'.join(key2)

            sub_key = 'description'

            if not key in dict:
                #Some entries have only a description, no main text
                #print("WARNING: {} description without main entry encountered!".format(key))
                dict[key] = {}
                #sub_key = 'text'

            dict[key]['division'] = division[1].upper()
            dict[key][sub_key] = entry.group("body")
            
        else:
            dict[key] = {}
            dict[key]['division'] = division[0].upper()
            if entry.group("title"):
                dict[key]['title'] = entry.group("title")
            dict[key]['text'] = entry.group("body")
            

    #Sanitize
    del dict['game_concepts_keys']
    del dict['game_concepts']
    del dict['eof']

    #Go over raw data and category, subcategory
    current_category = 'GameConcepts'
    current_subcategory = ''
    for line in raw_data.split('\n'):
        
        if cat_match := rx_category.match(line):
            line_text = cat_match.group(1)

            if line_text.lower().startswith("end"):
                current_category = ''
                current_subcategory = ''
                print(f"End of Category: '{line_text}'\n\n")
                continue

            current_category = ''.join(word.capitalize() for word in line_text.split())
            print(f"Switched to Category '{current_category}'")
        elif subcat_match := rx_subcategory.match(line):
            line_text = subcat_match.group(1)

            current_subcategory = ' '.join(line_text.split('-'))
            current_subcategory = ''.join(word.capitalize() for word in current_subcategory.split())
            
            print(f"\tSwitched to Subcategory '{current_subcategory}'")
        elif key_match := rx_key_only.match(line):
            line_text = key_match.group(1).lower()

            if line_text.startswith('desc'):
                line_text = '_'.join(line_text.split('_')[1:])

            if line_text in dict:
                dict[line_text.lower()]['category'] = current_category
                dict[line_text.lower()]['subcategory'] = current_subcategory

            print(f"\t\tKey: {line_text}")

    return dict

dict = read_civilopedia('Civilopedia.txt')

#Write to file
with open('Civilopedia.json', 'w') as file:
    file.write(json.dumps(dict, indent=2))
    file.close()

#print(json.dumps(dict, indent=2))