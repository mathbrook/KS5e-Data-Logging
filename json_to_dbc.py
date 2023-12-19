import cantools
from cantools.database import conversion
import json
from parser_api import get_dbc_files
# with open("can_descriptor.json") as file:
#     test = json.load(file)


# print(test["messages"])
# print(test["signals"])

db = get_dbc_files()

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
        print(signal)
        signal_dict = {}
        message_dict["signals"].append(signal.name)
        signal_dict["name"]=signal.name
        signal_dict["start"]=signal.start
        signal_dict["length"]=signal.length
        signal_dict["byte_order"]=signal.byte_order
        signal_dict["is_signed"]=signal.is_signed
        signal_dict["initial"]=signal.initial
        signal_conv_type = (type(signal.conversion))
        if signal_conv_type == conversion.IdentityConversion:
            signal_dict["conversion"]={"is_float":"false"}
        elif signal_conv_type == conversion.LinearConversion:
            signal_dict["conversion"]={"scale":signal.scale,"offset":signal.offset,"is_float":signal.is_float}
        elif signal_conv_type == conversion.NamedSignalConversion:
            signal_dict["conversion"]={"scale":signal.scale,"offset":signal.offset,"choices":{}}
            for i in signal.choices:
                print(i)
                print(signal.choices[i])
            for i in signal.choices:
                signal_dict["conversion"]["choices"][str(i)]=str(signal.choices[i])
        # signal_dict["choices"]=str(signal.conversion.choices)
        signal_dict["min"]=signal.minimum
        signal_dict["max"]=signal.maximum
        signal_dict["is_multiplexer"]=signal.is_multiplexer
        # signal_dict[""]
        signals_list.append(signal_dict)
    message_dict["comment"]=message.comment
    message_dict["bus_name"]=message.bus_name
    message_dict["is_extended_frame"]=message.is_extended_frame
    messages_list["messages"][message.name]=message_dict
    messages_list["signals"]=signals_list
 
with open("test.json","w") as outfile:
    json.dump(messages_list,outfile,indent=4)
