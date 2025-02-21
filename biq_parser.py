import struct
import json
from io import BytesIO

def read_building_data(file_path):
    with open(file_path, "rb") as f:
        # Move to the offset where the number of buildings is located
        f.seek(0x2E4)
        # Read the number of buildings (4 bytes, unsigned integer)
        num_buildings = struct.unpack('<i', f.read(4))[0]

        buildings = {}

        # Iterate over each building block
        for i in range(0, num_buildings):
            block_length_bytes = f.read(4)
            if not block_length_bytes:
                break  # End of file or no more buildings
            block_length = struct.unpack('<i', block_length_bytes)[0]

            # Read the entire unit block
            bld_block = f.read(block_length)
            r = BytesIO(bld_block)

            # Read the name (32 bytes string starting 68 bytes into the block)
            r.seek(64, 1)  # move 68 bytes forward from current position
            name = r.read(32).decode('utf-8').strip('\x00')

            # Read the database key (32 bytes string following the name)
            database_key = r.read(32).decode('utf-8').strip('\x00').lower()

            buildings[database_key] = {}
            buildings[database_key]['name'] = name
            buildings[database_key]['id'] = i

            buildings[database_key]['doubles_happiness_of_building_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['gain_in_every_city_building_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['gain_in_every_city_on_continent_building_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['required_building_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['cost'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['culture_gain'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['bombardment_defense'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['naval_bombardment_defense'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['defense_bonus'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['naval_defense_bonus'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['maintenance_cost'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['happy_all_cities'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['happy'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['unhappy_all_cities'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['unhappy'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['no_required_buildings'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['air_power'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['naval_power'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['pollution'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['production'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['required_government_id'] = struct.unpack('<i', r.read(4))[0]
            r.seek(4, 1) # spaceship part
            buildings[database_key]['required_advance_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['obsoleted_by_advance_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['required_resource_id_1'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['required_resource_id_2'] = struct.unpack('<i', r.read(4))[0]
            r.seek(4*4, 1) # binary flags
            buildings[database_key]['no_required_armies'] = struct.unpack('<i', r.read(4))[0]
            r.seek(4*2, 1)
            buildings[database_key]['produced_unit_id'] = struct.unpack('<i', r.read(4))[0]
            buildings[database_key]['unit_frequency'] = struct.unpack('<i', r.read(4))[0]
            r.close()

    f.close()

    return buildings

FLAG_NAMES_UNIT = {
    0: "wheeled",
    1: "foot_soldier",
    2: "blitz",
    3: "cruise_missile",
    4: "all_terrain_as_roads",
    5: "radar",
    6: "amphibious_unit",
    7: "invisible",
    8: "aircraft_carrier",
    9: "draft",
    10: "immobile",
    11: "sink_in_sea",
    12: "sink_in_ocean",
    13: "flag_unit",
    14: "carry_foot_units_only",
    15: "starts_golden_age",
    16: "nuclear_weapon",
    17: "hidden_nationality",
    18: "army",
    19: "leader",
    20: "icbm",
    21: "stealth",
    22: "detect_invisible",
    23: "tactical_missile",
    24: "carry_tactical_missiles",
    25: "ranged_attack_animations",
    26: "turn_to_attack",
    27: "lethal_land_bombardment",
    28: "lethal_sea_bombardment",
    29: "king",
    30: "requires_escort"
}

FLAG_NAMES_RACES = {
    0: "Barbarian",
    1: "Rome", 
    2: "Egypt",
    3: "Greece", 
    4: "Babylon",
    5: "Germany",
    6: "Russia",
    7: "China",
    8: "America",
    9: "Japan",
    10: "France",
    11: "India",
    12: "Persia",
    13: "Aztecs",
    14: "Zululand",
    15: "Iroquois",
    16: "England",
    17: "Mongols",
    18: "Spain",
    19: "Scandinavia",
    21: "Celts",
    23: "Carthage",
    20: "Ottomans",
    22: "Arabia",
    24: "Korea",
    25: "Sumeria",
    26: "Hittites",
    29: "Byzantines",
    30: "Inca",
    31: "Maya",
    28: "Portugal",
    27: "Netherlands"
}

def extract_flags_from_bytes(bytes_data, start_index=0, end_index=31, FLAG_NAMES=FLAG_NAMES_UNIT):
    """Extract 32 boolean flags from 4 bytes with named flags"""
    flags = {}
    value = struct.unpack('<I', bytes_data)[0]
    
    for i in range(end_index):
        flag_index = start_index + i
        if FLAG_NAMES == None:
            flags[flag_index] = bool(value & (1 << i))
            continue
        elif flag_index in FLAG_NAMES:
            flags[FLAG_NAMES[flag_index]] = bool(value & (1 << i))

    
    return flags
    
def read_units_data(file_path):
    with open(file_path, "rb") as f:
        # Move to the offset where the number of buildings is located
        f.seek(0x8FA4)
        # Read the number of units (4 bytes, unsigned integer)
        num_units = struct.unpack('<i', f.read(4))[0]

        #print(num_units)

        units = {}

        for i in range(0,num_units):
            # Read the length of the unit block (4 bytes, unsigned integer)
            block_length_bytes = f.read(4)
            if not block_length_bytes:
                break  # End of file or no more units
            block_length = struct.unpack('<i', block_length_bytes)[0]

            # Read the entire unit block
            unit_block = f.read(block_length)
            r = BytesIO(unit_block)
            
            r.seek(4, 1) 
            name = r.read(32).decode('utf-8').strip('\x00')

            # Read the database key (32 bytes string following the name)
            database_key = r.read(32).decode('utf-8').strip('\x00').lower()

            if database_key in units:
                continue

            units[database_key] = {}
            units[database_key]['name'] = name
            units[database_key]['id'] = i

            units[database_key]['bombard_strength'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['bombard_range'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['capacity'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['cost'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['defense'] = struct.unpack('<i', r.read(4))[0]
            r.seek(4, 1) # icon index
            units[database_key]['attack'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['operational_range'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['population_cost'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['rate_of_fire'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['movement'] = struct.unpack('<i', r.read(4))[0]

            units[database_key]['required_advancement_id'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['upgrade_to_id'] = struct.unpack('<i', r.read(4))[0]

            units[database_key]['required_resource_id_1'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['required_resource_id_2'] = struct.unpack('<i', r.read(4))[0]
            units[database_key]['required_resource_id_3'] = struct.unpack('<i', r.read(4))[0]

            units[database_key]['flags'] = extract_flags_from_bytes(r.read(4))
            r.seek(4, 1) #ai strategy binary
            units[database_key]['available_to_id'] = extract_flags_from_bytes(r.read(4), start_index=0, end_index=32, FLAG_NAMES=None)

            r.close()

    f.close()

    return units
    
def read_advancements_data(file_path):
    with open(file_path, "rb") as f:
        # Move to the offset where the number of techs is located
        f.seek(0x2D15F)
        # Read the number of advancements (4 bytes, unsigned integer)
        num_advs = struct.unpack('<i', f.read(4))[0]

        #print(num_units)

        advs = {}

        for i in range(0,num_advs):
            # Read the length of the unit block (4 bytes, unsigned integer)
            block_length_bytes = f.read(4)
            if not block_length_bytes:
                break  # End of file or no more units
            block_length = struct.unpack('<i', block_length_bytes)[0]

            # Read the entire unit block
            adv_block = f.read(block_length)
            r = BytesIO(adv_block)
            
            name = r.read(32).decode('utf-8').strip('\x00')

            # Read the database key (32 bytes string following the name)
            database_key = r.read(32).decode('utf-8').strip('\x00').lower()

            advs[database_key] = {}
            advs[database_key]['name'] = name
            advs[database_key]['id'] = i

            advs[database_key]['cost'] = struct.unpack('<i', r.read(4))[0]
            r.seek(4*4, 1) 
            advs[database_key]['required_advancement_id_1'] = struct.unpack('<i', r.read(4))[0]
            advs[database_key]['required_advancement_id_2'] = struct.unpack('<i', r.read(4))[0]
            advs[database_key]['required_advancement_id_3'] = struct.unpack('<i', r.read(4))[0]
            advs[database_key]['required_advancement_id_4'] = struct.unpack('<i', r.read(4))[0]

            r.close()

    f.close()

    return advs

def read_race_data(file_path):
    with open(file_path, "rb") as f:
        # Move to the offset where the number of races is located
        f.seek(0x124DF)
        # Read the number of civs/races (4 bytes, unsigned integer)
        num_races = struct.unpack('<i', f.read(4))[0]

        print(num_races)

        races = {}

        for i in range(0,num_races):
            # Read the length of the unit block (4 bytes, unsigned integer)
            block_length_bytes = f.read(4)
            if not block_length_bytes:
                break  # End of file or no more units
            block_length = struct.unpack('<i', block_length_bytes)[0]

            print(block_length)

            # Read the entire race block
            adv_block = f.read(block_length)
            r = BytesIO(adv_block)

            no_city_names = struct.unpack('<i', r.read(4))[0]
            city_names = []
            for j in range(0, no_city_names):
                city_names.append(r.read(24).decode('cp1252').strip('\x00'))

            no_leader_names = struct.unpack('<i', r.read(4))[0]
            leader_names = []
            for j in range(0, no_leader_names):
                print(leader_names)
                leader_names.append(r.read(32).decode('cp1252').strip('\x00'))
            
            leader_name = r.read(32).decode('utf-8').strip('\x00')
            leader_title = r.read(24).decode('utf-8').strip('\x00')

            # Read the database key (32 bytes string following the name)
            database_key = r.read(32).decode('utf-8').strip('\x00').lower()

            adjective = r.read(40).decode('utf-8').strip('\x00')
            name = r.read(40).decode('utf-8').strip('\x00')
            noun = r.read(40).decode('utf-8').strip('\x00')

            races[database_key] = {}
            races[database_key]['name'] = name
            races[database_key]['id'] = i

            races[database_key]['noun'] = noun
            races[database_key]['adjective'] = adjective

            races[database_key]['leader_name'] = leader_name
            races[database_key]['leader_title'] = leader_title

            races[database_key]['leader_names'] = leader_names
            races[database_key]['city_names'] = city_names

            r.close()

    f.close()

    return races

def read_resources_data(file_path):
    with open(file_path, "rb") as f:
        # Move to the offset where the number of techs is located
        f.seek(0x7180)
        # Read the number of resources (4 bytes, unsigned integer)
        num_res = struct.unpack('<i', f.read(4))[0]

        #print(num_units)

        resources = {}

        for i in range(0,num_res):
            # Read the length of the unit block (4 bytes, unsigned integer)
            block_length_bytes = f.read(4)
            if not block_length_bytes:
                break  # End of file or no more units
            block_length = struct.unpack('<i', block_length_bytes)[0]

            # Read the entire unit block
            res_block = f.read(block_length)
            r = BytesIO(res_block)
            
            name = r.read(24).decode('utf-8').strip('\x00')

            # Read the database key (32 bytes string following the name)
            database_key = r.read(32).decode('utf-8').strip('\x00').lower()

            resources[database_key] = {}
            resources[database_key]['name'] = name
            resources[database_key]['id'] = i
            r.seek(4*4, 1) 
            resources[database_key]['required_advancement_id'] = struct.unpack('<i', r.read(4))[0]
            resources[database_key]['food_bonus'] = struct.unpack('<i', r.read(4))[0]
            resources[database_key]['shields_bonus'] = struct.unpack('<i', r.read(4))[0]
            resources[database_key]['commerce_bonus'] = struct.unpack('<i', r.read(4))[0]

            r.close()

    f.close()

    return resources

def read_govt_data(file_path):
    with open(file_path, "rb") as f:
        # Move to the offset where the number of techs is located
        f.seek(0x7ADC)
        # Read the number of governments (4 bytes, unsigned integer)
        num_govts = struct.unpack('<i', f.read(4))[0]

        governments = {}

        for i in range(0,num_govts):
            # Read the length of the govt block (4 bytes, unsigned integer)
            block_length_bytes = f.read(4)
            if not block_length_bytes:
                break  # End of file or no more units
            block_length = struct.unpack('<i', block_length_bytes)[0]

            # Read the entire unit block
            govt_block = f.read(block_length)
            r = BytesIO(govt_block)

            default_type = struct.unpack('<i', r.read(4))[0]
            transition_type = struct.unpack('<i', r.read(4))[0]
            requires_maintenance = struct.unpack('<i', r.read(4))[0]
            r.seek(4, 1) # unknown entry
            standard_tile_penalty = struct.unpack('<i', r.read(4))[0]
            standard_trade_bonus = struct.unpack('<i', r.read(4))[0]
            
            name = r.read(64).decode('utf-8').strip('\x00')

            # Read the database key (32 bytes string following the name)
            database_key = r.read(32).decode('utf-8').strip('\x00').lower()


            governments[database_key] = {}
            governments[database_key]['name'] = name
            governments[database_key]['id'] = i
            governments[database_key]['is_default_type'] = default_type
            governments[database_key]['is_transition_type'] = transition_type
            governments[database_key]['requires_maintenance'] = requires_maintenance
            governments[database_key]['standard_tile_penalty'] = standard_tile_penalty
            governments[database_key]['standard_trade_bonus'] = standard_trade_bonus

            ruler_titles = []
            for j in range(8):
                title = r.read(32).decode('utf-8').strip('\x00')
                ruler_titles.append(title)

            governments[database_key]['male_titles'] = ruler_titles[::2]
            governments[database_key]['female_titles'] = ruler_titles[1::2]


            governments[database_key]['required_advancement_id'] = struct.unpack('<i', r.read(4))[0]
            governments[database_key]['food_bonus'] = struct.unpack('<i', r.read(4))[0]
            governments[database_key]['shields_bonus'] = struct.unpack('<i', r.read(4))[0]
            governments[database_key]['commerce_bonus'] = struct.unpack('<i', r.read(4))[0]

            r.close()

    f.close()

    return governments

def link_buildings(buildings, building_id_list, unit_id_list, advancement_id_list, resource_id_list):
    for k,v in buildings.items():
            
        v['doubles_happiness_of_building'] = building_id_list[v['doubles_happiness_of_building_id']] if v['doubles_happiness_of_building_id'] != -1 else ''
        del v['doubles_happiness_of_building_id']

        v['gain_in_every_city_building'] = building_id_list[v['gain_in_every_city_building_id']] if v['gain_in_every_city_building_id'] != -1 else ''
        del v['gain_in_every_city_building_id']

        v['gain_in_every_city_on_continent_building'] = building_id_list[v['gain_in_every_city_on_continent_building_id']] if v['gain_in_every_city_on_continent_building_id'] != -1 else ''
        del v['gain_in_every_city_on_continent_building_id']

        v['required_building'] = building_id_list[v['required_building_id']] if v['required_building_id'] != -1 else ''
        del v['required_building_id']

        v['required_advance'] = advancement_id_list[v['required_advance_id']] if v['required_advance_id'] != -1 else ''
        del v['required_advance_id']

        v['obsoleted_by_advance'] = advancement_id_list[v['obsoleted_by_advance_id']] if v['obsoleted_by_advance_id'] != -1 else ''
        del v['obsoleted_by_advance_id']

        v['produced_unit'] = unit_id_list[v['produced_unit_id']] if v['produced_unit_id'] != -1 else ''
        del v['produced_unit_id']

        v['required_resource_1'] = resource_id_list[v['required_resource_id_1']] if v['required_resource_id_1'] != -1 else ''
        del v['required_resource_id_1']

        v['required_resource_2'] = resource_id_list[v['required_resource_id_2']] if v['required_resource_id_2'] != -1 else ''
        del v['required_resource_id_2']

    return buildings

def link_units(units, building_id_list, unit_id_list, advancement_id_list, resource_id_list, race_id_list):
    for k,v in units.items():

        v['upgrade_to'] = unit_id_list[v['upgrade_to_id']] if v['upgrade_to_id'] != -1 else ''
        del v['upgrade_to_id']

        v['required_advancement'] = advancement_id_list[v['required_advancement_id']] if v['required_advancement_id'] != -1 else ''
        del v['required_advancement_id']
            
        v['required_resource_1'] = resource_id_list[v['required_resource_id_1']] if v['required_resource_id_1'] != -1 else ''
        del v['required_resource_id_1']

        v['required_resource_2'] = resource_id_list[v['required_resource_id_2']] if v['required_resource_id_2'] != -1 else ''
        del v['required_resource_id_2']
        
        v['required_resource_3'] = resource_id_list[v['required_resource_id_3']] if v['required_resource_id_3'] != -1 else ''
        del v['required_resource_id_3']

        v['available_to'] = {}
        for key, value in v['available_to_id'].items():
            v['available_to'][race_id_list[int(key)]] = value

        del v['available_to_id']


    return units

def link_advancements(advs, advancement_id_list):
    for k,v in advs.items():

        v['required_advancement_1'] = advancement_id_list[v['required_advancement_id_1']] if v['required_advancement_id_1'] != -1 else ''
        del v['required_advancement_id_1']
            
        v['required_advancement_2'] = advancement_id_list[v['required_advancement_id_2']] if v['required_advancement_id_2'] != -1 else ''
        del v['required_advancement_id_2']
        
        v['required_advancement_3'] = advancement_id_list[v['required_advancement_id_3']] if v['required_advancement_id_3'] != -1 else ''
        del v['required_advancement_id_3']

        v['required_advancement_4'] = advancement_id_list[v['required_advancement_id_4']] if v['required_advancement_id_4'] != -1 else ''
        del v['required_advancement_id_4']

    return advs

def link_resources(resources, advancement_id_list):
    for k,v in resources.items():

        v['required_advancement'] = advancement_id_list[v['required_advancement_id']] if v['required_advancement_id'] != -1 else ''
        del v['required_advancement_id']

    return resources

with open('Civilopedia.json', 'r') as file:
    civilopedia = json.load(file)

file_path = 'conquests_uncompressed.biq'
buildings = read_building_data(file_path)
units = read_units_data(file_path)
advs = read_advancements_data(file_path)
resources = read_resources_data(file_path)
races = read_race_data(file_path)

print(len(races))
print(json.dumps(races, indent=2))

building_id_list = {v['id']: k for k, v in buildings.items()}
unit_id_list = {v['id']: k for k, v in units.items()}
advs_id_list = {v['id']: k for k, v in advs.items()}
res_id_list = {v['id']: k for k, v in resources.items()}
race_id_list = {v['id']: k for k, v in races.items()}



print(race_id_list)

buildings = link_buildings(buildings, building_id_list, unit_id_list, advs_id_list, res_id_list)
units = link_units(units, building_id_list, unit_id_list, advs_id_list, res_id_list, race_id_list)
advs = link_advancements(advs, advs_id_list)
resources = link_resources(resources, advs_id_list)

for k,v in civilopedia.items():
    if k in resources:
        civilopedia[k].update(resources[k])
    elif k in buildings:
        civilopedia[k].update(buildings[k])
    elif k in units:
        civilopedia[k].update(units[k])
    elif k in advs:
        civilopedia[k].update(advs[k])
    elif k in races:
        civilopedia[k].update(races[k])

with open('Civilopedia.json', 'w') as file:
    file.write(json.dumps(civilopedia, indent=2))
    file.close()