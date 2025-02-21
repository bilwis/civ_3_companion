import json

def convert_unit(unit):
    if not 'id' in unit:
        return
    
    md = ""
    tags = ""

    if 'text' in unit:
        md += f"{unit['text']}\n" # Text ("small" description)

    md += "### Statistics\n"
    md += f"**Cost:** {unit['cost']}\n"
    md += f"**Attack:** {unit['attack']}\n"
    md += f"**Defense:** {unit['defense']}\n"
    md += f"**Movement:** {unit['movement']}\n"

    md += "#### Additional Statistics\n"
    md += f"**Population Cost:** {unit['population_cost']}\n"
    md += f"**Rate of Fire**: {unit['rate_of_fire']}\n"
    md += f"**Bombard Strength:** {unit['bombard_strength']}\n"
    md += f"**Bombard Range:** {unit['bombard_range']}\n"
    md += f"**Operational Range:** {unit['operational_range']}\n"
    md += f"**Capacity:** {unit['capacity']}\n"

    if 'description' in unit:
        md += "### Description\n"
        md += f"> *{unit['description']}*\n"

    md += "### Requirements/Upgrades\n"
    resources = [unit['required_resource_1'], unit['required_resource_2'], unit['required_resource_3']]
    resources = [r for r in resources if r]
    md += f"**Required Resources:** {', '.join(resources)}\n"
    md += f"**Required Technology:** {unit['required_advancement']}\n"
    md += f"**Required Civ:** {unit['availability']}\n"
    if unit['upgrade_to']:
        md += f"**Upgrades to:** {unit['upgrade_to']}\n"
        tags += "#Upgradeable "

    tags += unit['flag_string'] + " #PTRO" + " #Unit" + f" #{''.join(unit['name'].split(' '))}"
    md += f"\n{tags}\n"

    return md




with open('Civilopedia2.json', 'r') as file:
    civilopedia = json.load(file)

for k, v in civilopedia.items():
    if k.startswith('prto_'):
        print(convert_unit(v))
