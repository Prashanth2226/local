import json
import os
import sys
import string
    

def generate_kconfig(json_data, depth,node_prefix=None, offset_tobeadded=None, maplayer=None, nodelayer=None, connection_type=None, menu_name=None):
    indent = "  "
    kconfig_lines = []
    print(f'menu_name   :   {menu_name}')

    for item in json_data.get(maplayer, []):
        print(f'maplayer   :   {maplayer}')
        print(f'nodelayer   :   {nodelayer}')
        print(f'connection_type   :   {connection_type}')
        print(f'item test "{depth}": {item}')
        if nodelayer in item:
            if (menu_name=="map"):
                node_name = item.get("Node name","")
                print(f"test node name:   {node_name} and depth :  {depth}")
                node_prefix = node_name.split(":")[0]
                connection = node_name.split(":")[1]
                print(f"node_prefix:   {node_prefix} and depth :  {depth}")
                print(f' connection  : {connection}')
            if(menu_name=="interrupt"):
                node_prefix = "MIV"
                connection = None
        print(f'offset_tobeadded : {offset_tobeadded}')
        print(f' node_prefix  : {node_prefix}')
        
        
        if not node_prefix.startswith(str(connection_type)) and (offset_tobeadded==connection_type):        
            for var_name, var_value in item.items():
                if var_name not in [nodelayer]:
                    if (menu_name=="interrupt"):
                        processor_instance = item.get("Processor instance","")
                    print(f'checking var_value : {var_value}')
                    print(f'check var_name in loop:{var_name}')
                    register_name = item.get("Node name","").split(":")[0]
                    if register_name.islower():
                        register_name=register_name.upper()
                    print(f'inside not matching string loop register_name: {register_name}')
                    register_offset = item.get("Offset Address","")
                    if register_offset.find("_"):
                        register_offset = register_offset.replace('_','')
                    print(f'inside not mathcing string loop register_offset: {register_offset}')
                    if (menu_name=="interrupt"):
                        processor_instance = item.get("Processor instance","")
                        driver_component = item.get("Driver component","")
                        driver_pin = (item.get("Driver pin","").rsplit("/",1)[-1].replace(':','_')).upper()
                        interrupt_pin = item.get("Interrupt pin","")
                        if PLIC_number is not None:
                            kconfig_lines.append(f'{indent*(depth)} config {processor_instance} {driver_pin} ')
                            kconfig_lines.append(f'{indent*(depth)} default {PLIC_number}  ')
                    if register_offset is not "":#and (var_name == "Type"):
                        print(f'register_name: {register_name}')
                        print(f'register_offset: {register_offset}')
                        kconfig_lines.append(f'{indent*(depth-1)} config {register_name}  ')
                        if ((depth==1) and (connection != None)):
                            kconfig_lines.append(f'{indent*(depth)} default {connection}  ')
                        else:
                            kconfig_lines.append(f'{indent*(depth)} default {register_offset}  ')
                    break
            if nodelayer in item:
               inner_data = generate_kconfig(item,depth=depth+1,node_prefix=node_prefix,offset_tobeadded=connection_type,maplayer=nodelayer, nodelayer=nodelayer, connection_type=connection_type, menu_name=menu_name)
               kconfig_lines.append(inner_data)
        
        
        
        
        if  node_prefix.startswith(str(connection_type)):
            for var_name, var_value in item.items():
                if var_name not in [nodelayer]:
                    if (menu_name=="interrupt"):
                        processor_instance = item.get("Processor instance","")
                    print(f'checking var_value : {var_value}')
                    print(f'check var_name in loop:{var_name}')
                    register_name = item.get("Node name","").split(":")[0]
                    if register_name.islower():
                        register_name=register_name.upper()
                    print(f'inside matching string loop register_name: {register_name}')
                    register_offset = item.get("Offset Address","")
                    if register_offset.find("_"):
                        register_offset = register_offset.replace('_','')
                    print(f'inside matching string loop register_offset: {register_offset}')
                    if var_value.startswith(str(connection_type)):
                        generate_kconfig(item,depth=depth+1,node_prefix=node_prefix, offset_tobeadded=connection_type,maplayer=nodelayer, nodelayer=nodelayer, connection_type=connection_type, menu_name=menu_name)                        
                    if (var_name == "Type"):
                        print(f'register_name: {register_name}')
                        print(f'register_offset: {register_offset}')
                        kconfig_lines.append(f'{indent*(depth-1)} config {register_name}  ')
                        if ((depth==1) and (connection != None)):
                            kconfig_lines.append(f'{indent*(depth)} default {connection}  ')
                        else:
                            kconfig_lines.append(f'{indent*(depth)} default {register_offset}')
                        
                    if (menu_name=="interrupt"):
                        processor_instance = item.get("Processor instance","")
                        component_type = item.get("Component type","")
                        driver_component = item.get("Driver component","")
                        driver_pin = (item.get("Driver pin","").rsplit("/",1)[-1].replace(':','_')).upper()
                        interrupt_pin = item.get("Interrupt pin","")
                        print(f'driver_component: {driver_component}')
                        print(f'driver_pin: {driver_pin.upper()}')
                        print(f'interrupt_pin: {interrupt_pin}')
                        if driver_component is not None:
                            if (depth==1):
                                kconfig_lines.append(f'{indent*(depth)} config {processor_instance} ')
                                kconfig_lines.append(f'{indent*(depth)} component_type {component_type}')
                            kconfig_lines.append(f'{indent*(depth)} config {driver_pin} ')
                            kconfig_lines.append(f'{indent*(depth)} default {interrupt_pin}')
                            kconfig_lines.append(f'{indent*(depth)} driver component {driver_component}')
                            break
                            
            if nodelayer in item:
               inner_data = generate_kconfig(item,depth=depth+1,node_prefix=node_prefix, offset_tobeadded=connection_type,maplayer=nodelayer, nodelayer=nodelayer, connection_type=connection_type, menu_name=menu_name)
               kconfig_lines.append(inner_data)
    
    return '\n'.join(kconfig_lines)
    
    
if __name__== "__main__":
    pwd = "C:\\my_branches\\miv_examples\\test_json_files\\existing"
    output_kconfig_file = pwd+"\\Kconfig"
    #output_kconfig_file = "prashanth@10.61.32.82:~/auto_h/Kconfig"
    keyword_in_file = ["memory_map"]#, "interrupt_map"]#, "ip" ]
    
    file_key_mapping = {
        "memory_map" : {"menu_name":"map","maplayer":"Initiator/Bus/Bridge/Target OffsetAddress Range HighAddress", "nodelayer":"Connected Node", "categorise":True, "connection_type":"MIV"},
        "interrupt_map" :{"menu_name":"interrupt","maplayer":"Processor interrupt map", "nodelayer":"Interrupt connection map (Hierarchical driver pin name - Interrupt pin name)","categorise":False, "connection_type":"MIV"},
        "ip" : {"menu_name":"ip", "maplayer":"components", "nodelayer":None,"categorise":False}
    }
    all_kconfig_sections = {}
    
    for root, dirs, files in os.walk(pwd):
        for filename in files:
            for keyword in keyword_in_file:
                if keyword in filename.lower():
                    input_json_file = os.path.join(root, filename)
                    print(f'input file is :{input_json_file}')
                    with open(input_json_file, "r") as json_file:
                        json_data = json.load(json_file)
                    
                    keys_Data = file_key_mapping.get(keyword,  {"maplayer": None, "nodelayer": None})
                    maplayer = keys_Data.get("maplayer")
                    nodelayer = keys_Data.get("nodelayer")
                    menu_name = keys_Data.get("menu_name")
                    categorise = keys_Data.get("categorise")
                    connection_type = keys_Data.get("connection_type")
                  
                    connected_node = json_data.get("Connected Node",{})
                    node_name = json_data.get("Node name", "")
                    node_prefix = node_name.split("/")[0] if categorise else None
                    if categorise:                  
                        if node_prefix not in all_kconfig_sections:
                            all_kconfig_sections[node_prefix]=[]
                    kconfig_section = generate_kconfig(json_data, depth=1, maplayer=maplayer, nodelayer=nodelayer, connection_type=connection_type, menu_name=menu_name)
                    
                    if categorise:
                        #all_kconfig_sections[node_prefix].append(f'menu{"    "*2}:      {menu_name}')
                        all_kconfig_sections[node_prefix].append('')
                        all_kconfig_sections[node_prefix].append('')
                        all_kconfig_sections[node_prefix].append(f'{kconfig_section}')
                        all_kconfig_sections[node_prefix].append('')
                        all_kconfig_sections[node_prefix].append('')
                    else:
                        if None not in all_kconfig_sections:
                            all_kconfig_sections[None]=[]
                        all_kconfig_sections[None].append(f'menu{"    "*2}:      {menu_name}')    
                        all_kconfig_sections[node_prefix].append('')
                        all_kconfig_sections[node_prefix].append('')
                        all_kconfig_sections[None].append(f'{kconfig_section}')
                        all_kconfig_sections[node_prefix].append('')
                        all_kconfig_sections[node_prefix].append('')
                    
    with open(output_kconfig_file, "w") as kconfig_file:
        for node_prefix, sections in all_kconfig_sections.items():
            kconfig_file.write('\n'.join(sections))
            kconfig_file.write('\n')
    print(f'kconfig file generated: {output_kconfig_file}')