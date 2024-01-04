import cantools
from cantools.database import conversion
import json
import sys
from parser_api import get_dbc_files
import time

def cantools_json_to_dbc(input_json: str,outfilename: str):
    with open(input_json) as file:
        can_json_input = json.load(file)

    new_signal_dict = {}

    for signal in can_json_input["signals"]:

        new_signal = cantools.db.Signal(name=signal["name"],start=signal["start"],length=signal["length"])
        new_signal.byte_order=signal["byte_order"]
        new_signal.is_signed=signal["is_signed"]
        new_signal.initial=signal["initial"]
        new_signal.minimum=(signal["min"])
        new_signal.maximum=signal["max"]
        if "conversion" in signal:
            if "is_float" in signal:
                new_signal.is_float=signal["conversion"]["is_float"]
            if "scale" in signal["conversion"]:
                new_signal.scale = signal["conversion"]["scale"]
            if "offset" in signal["conversion"]:
                new_signal.offset = signal["conversion"]["offset"]
            if "choices" in signal["conversion"]:
                new_signal.choices = signal["conversion"]["choices"]
        # new_signal.is_multiplexer=signal["is_multipexer"]
        # new_signal.comment=signal["comment"]
        # new_signal.unit=signal["units"]
        new_signal_dict[new_signal.name]=new_signal

    list_of_cantools_msgs = []

    for message in can_json_input["messages"]:
        message_info = can_json_input["messages"][message]
        signals = []

        for signal in message_info["signals"]:
            signals.append(new_signal_dict[signal])

        new_message = cantools.db.Message(frame_id=message_info["id"],
                                        name=message,length=message_info["length"],
                                        signals=signals,
                                        senders=message_info["senders"])
        
        new_message.comment=message_info["comment"]
        new_message.is_extended_frame=message_info["is_extended_frame"]
        new_message.bus_name=message_info["bus_name"]
        list_of_cantools_msgs.append(new_message)

    nodes = [cantools.db.Node('vcu',"the vehicle control unit"),
             cantools.db.Node('bms'),
             cantools.db.Node('inverter'),
             cantools.db.Node('dash')]
    
    buses = [cantools.db.Bus('ks8', None, 500000)]
    
    new_db = cantools.db.Database(list_of_cantools_msgs,nodes=nodes,buses=buses)
    cantools.db.dump_file(new_db,outfilename+'.dbc')
    cantools.db.dump_file(new_db,outfilename+'.sym',database_format='sym')

def cantools_dbc_to_json(db: cantools.db.Database,outfilename: str):

    signals_list = []
    messages_list = {"messages":{}}
    for message in db.messages:

        message_dict= {
            "id": "",
            "length": "",
            "signals":[],
            "comment":"",
            "is_extended_frame":"",
            "bus_name":""
        }
        message_dict["id"] = message.frame_id
        message_dict["length"]=message.length
        for signal in message.signals:

            signal_dict = {}
            message_dict["signals"].append(signal.name)
            signal_dict["name"]=signal.name
            signal_dict["start"]=signal.start
            signal_dict["length"]=signal.length
            signal_dict["byte_order"]=signal.byte_order
            signal_dict["is_signed"]=signal.is_signed
            signal_dict["initial"]=signal.initial
            signal_dict["comment"]=signal.comment
            signal_dict["units"]=signal.unit
            signal_conv_type = (type(signal.conversion))

            if signal_conv_type == conversion.IdentityConversion:
                signal_dict["conversion"]={"is_float":"false"}
            elif signal_conv_type == conversion.LinearConversion:
                signal_dict["conversion"]={"scale":signal.scale,"offset":signal.offset,"is_float":signal.is_float}
            elif signal_conv_type == conversion.NamedSignalConversion:
                signal_dict["conversion"]={"scale":signal.scale,"offset":signal.offset,"choices":{}}

                for i in signal.choices:
                    signal_dict["conversion"]["choices"][str(i)]=str(signal.choices[i])

            signal_dict["min"]=signal.minimum
            signal_dict["max"]=signal.maximum
            signal_dict["is_multiplexer"]=signal.is_multiplexer
            signals_list.append(signal_dict)
        message_dict["comment"]=message.comment
        message_dict["bus_name"]=message.bus_name
        message_dict["is_extended_frame"]=message.is_extended_frame
        message_dict["senders"]=message.senders
        messages_list["messages"][message.name]=message_dict
        messages_list["signals"]=signals_list
    
    with open(outfilename+".json","w") as outfile:
        json.dump(messages_list,outfile,indent=4)

# Method to test the generation code that it isnt messing things up
def test_json_gen():
    # Make a json file with the existing DBCs
    cantools_dbc_to_json(db = get_dbc_files(),outfilename="test")

    # Parse the json file and generate a new singular DBC
    cantools_json_to_dbc(input_json="test.json",outfilename="ksu_dbc")

    # Turn the DBC file we made into another json and compare with the first
    mega_dbc=cantools.db.Database()
    with open ('ksu_dbc.dbc', 'r') as newdbc:
        mega_dbc.add_dbc(newdbc)
    cantools_dbc_to_json(db=mega_dbc,outfilename="can_descriptor")

    # Compare their differences
    import difflib
    with open('can_descriptor.json') as file_1:
        file_1_text = file_1.readlines()
    
    with open('test.json') as file_2:
        file_2_text = file_2.readlines()
    
    # Find and print the diff:
    for line in difflib.unified_diff(
            file_1_text, file_2_text, fromfile='file1.txt', tofile='file2.txt', lineterm=''):
                print(line)
import subprocess
def json_gen():
    args=sys.argv[1]
    filename=args
    cantools_json_to_dbc(input_json="can_descriptor.json",outfilename=filename)
    # subprocess.run(["make -C .\dbcc"])
    subprocess.run(["make","-C",".\dbcc"])
    subprocess.run([".\dbcc\dbcc",filename+".dbc"])

if __name__ == "__main__":
    json_gen()