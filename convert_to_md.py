import json

def convert_gcon(gcon):
    md = ""
    tags = ""

    if 'text' in gcon:
        md += f"{gcon['text']}\n"

    if 'description' in gcon:
        md += "### Description\n"
        md += f"> *{gcon['description']}*\n"

    tags = "#GCON" + f" #{''.join(gcon['title'].split(' '))}"

    if 'category' in gcon:
        tags += f" #{gcon['category']}"
    if 'subcategory' in gcon:
        tags += f" #{gcon['subcategory']}"

    md += f"\n{tags}\n"

    return md


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

def convert_building(bldg):
    if not 'id' in bldg:
        return

    md = ""
    tags = ""

    if 'text' in bldg:
        md += f"{bldg['text']}\n"

    md += "### Statistics\n"
    md += f"**Cost:** {bldg['cost']}\n"
    md += f"**Maintenance:** {bldg['maintenance_cost']}\n"
    md += f"**Culture:** {bldg['culture_gain']}\n"
    md += f"**Pollution:** {bldg['pollution']}\n"
    md += f"**Production:** {bldg['production']}\n"

    if bldg['bombardment_defense'] or bldg['naval_bombardment_defense'] or bldg['defense_bonus'] or bldg['naval_defense_bonus']:
        md += "#### Defense Statistics\n"
        md += f"**Bombardment Defense:** {bldg['bombardment_defense']}\n"
        md += f"**Naval Bombardment Defense:** {bldg['naval_bombardment_defense']}\n"
        md += f"**Defense Bonus:** {bldg['defense_bonus']}\n"
        md += f"**Naval Defense Bonus:** {bldg['naval_defense_bonus']}\n"

    if bldg['air_power'] or bldg['naval_power']:
        md += "#### Power Statistics\n"
        if bldg['air_power']:
            md += f"**Air Power:** {bldg['air_power']}\n"
        if bldg['naval_power']:
            md += f"**Naval Power:** {bldg['naval_power']}\n"
        if bldg['unit_frequency'] and bldg['produced_unit']:
            md += f"**Produces {bldg['produced_unit']} every {bldg['unit_frequency']} turns**\n"

    if bldg['happy'] or bldg['happy_all_cities'] or bldg['unhappy'] or bldg['unhappy_all_cities']:
        md += "#### Happiness Statistics\n"
        if bldg['happy']:
            md += f"**Happy Citizens:** +{bldg['happy']}\n"
        if bldg['happy_all_cities']:
            md += f"**Happy Citizens (All Cities):** +{bldg['happy_all_cities']}\n"
        if bldg['unhappy']:
            md += f"**Unhappy Citizens:** {bldg['unhappy']}\n"
        if bldg['unhappy_all_cities']:
            md += f"**Unhappy Citizens (All Cities):** {bldg['unhappy_all_cities']}\n"

    if 'description' in bldg:
        md += "### Description\n"
        md += f"> *{bldg['description']}*\n"

    
    requirements = []
    resources = [bldg['required_resource_1'], bldg['required_resource_2']]
    resources = [r for r in resources if r]
    if resources:
        requirements.append(f"**Required Resources:** {', '.join(resources)}")
    if bldg['required_advance']:
        requirements.append(f"**Required Technology:** {bldg['required_advance']}")
    if bldg['required_building']:
        requirements.append(f"**Required Building:** {bldg['required_building']}")
    if bldg['required_government']:
        requirements.append(f"**Required Government:** {bldg['required_government']}")

    if requirements:
        md += "### Requirements\n"
        md += "\n".join(requirements) + "\n"

    if bldg['no_required_armies']:
        md += f"**Number of Required Armies:** {bldg['no_required_armies']}\n"

    if bldg['obsoleted_by_advance']:
        md += f"**Obsoleted by:** {bldg['obsoleted_by_advance']}\n"

    tags = "#BLDG" + f" #{''.join(bldg['name'].split(' '))}"
    if bldg['category']:
        tags += f" #{bldg['category']}"
    if bldg['subcategory']:
        tags += f" #{bldg['subcategory']}"
    md += f"\n{tags}\n"

    return md



with open('Civilopedia2.json', 'r') as file:
    civilopedia = json.load(file)

for k, v in civilopedia.items():
    if k.startswith('prto_'):
        if not 'name' in v:
            continue

        name = v['name']
        print(name)
        with open(f'output/{name}.md', 'w') as unit_file:
            unit_file.write(convert_unit(v))
    if k.startswith('bldg_'):
        if not 'name' in v:
            continue

        name = v['name'].replace('/', '_')
        with open(f'output/{name}.md', 'w') as bldg_file:
            bldg_file.write(convert_building(v))
    if k.startswith('gcon_'):
        if not 'title' in v:
            continue

        title = v['title']
        print(f'output/{title}.md')
        with open(f'output/{title}.md', 'w') as gcon_file:
            gcon_file.write(convert_gcon(v))
