import json
import re

#Clean text from special characters and replace with markdown
def clean_text(text, title_list):
    rx_link = re.compile(r"\$LINK<(?P<display>[^=]+)=(?P<key>[^>]+)>")
    rx_bold = re.compile(r"{([^\}]+)}")
    rx_italic = re.compile(r"\[([^\]]+)\]")

    text = text.replace('^', '') #Clean start of line caret

    text = text.strip('\n')

    #Keep only double newlines
    text = text.replace('\n\n', '\\d')
    text = text.replace('\n', ' ')
    text = text.replace('\\d', '\n\n')
    text = text.replace('  ', ' ')

    text = re.sub(rx_bold, r'**\1**', text)
    text = re.sub(rx_italic, r'*\1*', text)

    def replace_link(match):
        m_key = match.group('key').lower()

        if m_key.startswith('menu'):
            return match.group('display')
        
        if m_key == 'prto_galleys':
            m_key = 'prto_galley'
        
        display = match.group('display')
        key = title_list[m_key]
        return f'[[{key}|{display}]]'
    
    text = re.sub(rx_link, replace_link, text)

    return text

#Scan text for tables and create markdown tables
def create_tables(text):
    rx_table_line = re.compile(r"(?P<key>[\w '-/:<>\[\]|=\{\}]+)\t{1,}[ ]*\t{0,}(?P<values>[\w\ ,.+%-~\t]+)")

    lines = text.split("\n")
    row = 0

    new_lines = []

    for line in lines:
        if match := re.match(rx_table_line, line):
            key = match.group('key')
            values = match.group('values').split('\t')
            values = [v.strip().replace('*','') for v in values if v.strip()]

            #Header
            if row == 0 and key.startswith('**') and len(values) > 0:
                key = key.strip("*")
                cols = '| {} |'.format(' | '.join([f'**{i}**' for i in [key,] + values if i != '']))
                sep_line = '| {} |'.format(' | '.join([f'-----' for i in [key,] + values if i != '']))

                new_lines.append(cols + '\n' + sep_line)
                #print(line)
                row += 2

            #No explicit Header
            elif row == 0 and len(values) > 0:
                col_count = len([key,] + values)

                header_line = '| {} |'.format(' | '.join([f'Column {i}' for i in range(0, col_count)]))
                sep_line = '| {} |'.format(' | '.join([f'-----' for i in range(0, col_count)]))
                content_line = '| {} |'.format(' | '.join([f'{i}' for i in [key,] + values if i != '']))

                new_lines.append(header_line + '\n' + sep_line + '\n' + content_line)
                row += 3

            elif row > 0:
                new_lines.append('| {} |'.format(' | '.join([f'{i}' for i in [key,] + values if i != ''])))
                row += 1

            else: 
                continue 

        else:
            #Special case
            if line.strip().lower().startswith('unit support'):
                new_lines.append("| Unit Support | |")
                row += 1

            else:
                new_lines.append(line)


    text = '\n'.join(new_lines)

    """    
    if (row > 0):
        print(text)
    """

    return text

#Replace references such as "prto_settler" with links to the actual title, e.g. "[[Settler]]"
def inject_links(value, title_list):
    if isinstance(value, str) and value in title_list:
        return f'[[{title_list[value]}]]'
    
    return value


def create_flag_string(flags):
    if not flags:
        return ""
    
    formatted_flags = []
    for flag, value in flags.items():
        if value:  # Only include flag if value is True
            # Convert snake_case to PascalCase
            words = flag.split('_')
            pascal_case = ''.join(word.capitalize() for word in words)
            formatted_flags.append(f"#{pascal_case}")
    
    return ' '.join(formatted_flags)

def create_availability_string(available_to, title_list):
    if not available_to:
        return ""
    
    formatted_availability = []
    barbarians = False
    for key, value in available_to.items():
        if value:  # Only include flag if value is True
            if key == 'race_barbarians':
                barbarians = True
            formatted_availability.append(f"[[{title_list[key]}]]")

    if len(formatted_availability) == 32:
        return "All Civilizations"
    
    if len(formatted_availability) == 31 and not barbarians:
        return "All Civilizations except Barbarians"
    
    return ', '.join(formatted_availability)
    

with open('Civilopedia.json', 'r') as file:
    civilopedia = json.load(file)

title_list = {}
title_list['race_barbarians'] = 'Barbarians'

for k, v in civilopedia.items():
    if 'name' in v:
        title_list[k] = v['name']
    elif 'title' in v:
        title_list[k] = v['title']
    else:
        title_list[k] = k

print(title_list)

for k, v in civilopedia.items():
    if 'text' in v:
        v['text'] = create_tables(clean_text(v['text'], title_list))

    if 'description' in v:
        v['description'] = create_tables(clean_text(v['description'], title_list))

    for k2, v2 in v.items():
        #print(v2)
        v[k2] = inject_links(v2, title_list)

    if 'flags' in v:
        v['flag_string'] = create_flag_string(v['flags'])

    if 'available_to' in v:
        v['availability'] = create_availability_string(v['available_to'], title_list)


with open('Civilopedia2.json', 'w') as file:
    file.write(json.dumps(civilopedia, indent=2))
    file.close()

