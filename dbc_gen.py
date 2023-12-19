import cantools

# Your JSON data
json_data = {
    "messages": {
        "message1": {
            "id": "0x01",
            "length": "8",
            "signals": [
                "signal1", "signal2"
            ],
            "comment": "this is a test message",
            "is_extended_frame": "False",
            "bus_name": "None"
        }
    },
    "signals": [
        {
            "name": "signal1",
            "start": "0",
            "length": "32",
            "byte_order": "little_endian",
            "is_signed": "False",
            "initial": "0",
            "scale": "1",
            "offset": "0",
            "min": "0",
            "max": 100,
            "unit": "volts",
            "comment": "this is a test signal",
            "is_multiplexer": "False",
            "is_float": "False",
            "decimal": "None"
        },
        {
            "name": "signal2",
            "start": "32",
            "length": "32",
            "byte_order": "little_endian",
            "is_signed": "False",
            "initial": "0",
            "scale": "1",
            "offset": "0",
            "min": "0",
            "max": 100,
            "unit": "volts",
            "comment": "this is a test signal",
            "is_multiplexer": "False",
            "is_float": "False",
            "decimal": "None"
        }
    ]
}

# Create a new database
db = cantools.db.Database()

# Add messages and signals to the database
for msg_name, msg_data in json_data['messages'].items():
    frame_id = int(msg_data['id'], 16)
    length = int(msg_data['length'])
    is_extended_frame = bool(msg_data['is_extended_frame'])
    signals=[]
    print("Frame id: " + str(frame_id))
    print("length: " + str(length))
    print(is_extended_frame)
    message = cantools.db.Message(signals=signals,frame_id=frame_id, name=msg_name, length=length, is_extended_frame=is_extended_frame)
    
    for signal in msg_data['signals']:
        for sig in json_data['signals']:
            if sig['name'] == signal:
                signal = cantools.db.Signal(
                    sig['name'],
                    start=int(sig['start']),
                    length=int(sig['length']),
                    byte_order=sig['byte_order'],
                    is_signed=bool(sig['is_signed']),
                    raw_initial=int(sig['initial']),
                    minimum=int(sig['min']),
                    maximum=int(sig['max']),
                    unit=sig['unit'],
                    comment=sig['comment'],
                    is_multiplexer=bool(sig['is_multiplexer'])
                )
                message.add_signal(signal)
    
    db.add_message(message)

# Save the database as a DBC file
db_filename = 'generated_dbc.dbc'  # Replace with your desired filename
db.save_file(db_filename)

print(f"DBC file '{db_filename}' generated successfully.")
