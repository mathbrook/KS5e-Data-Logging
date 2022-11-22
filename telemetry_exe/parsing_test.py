hex_msg = '00050C5B084B1278'
def hex_to_decimal(hex, bits, is_signed):
    """
    @brief: Helper function to convert a hexadecimal to a decimal. First swaps endianness and then performs twos-complement if needed.
            Referenced partially from: https://stackoverflow.com/questions/6727875/hex-string-to-signed-int-in-python-3-2
    @input: A string representing the hexadecimal number, how many bits it has, and whether if it is signed or unsigned (True --> signed)
    @return: The corresponding decimal value as an integer.
    """

    value = ""
    for i in range(bits//4,-1,-1):
        if i % 2 == 0:
            value = hex[i:i+2] + value
    value = int(value, 16)

    # Checks if needed to perform twos-complement or not; if yes, then performs twos-complement
    if is_signed and value & (1 << (bits - 1)):
        value -= 1 << bits

    return value
def parse_ID_MEGASQUIRT_GP0(raw_message):
    message= "MS3_GP0"
    labels=["Seconds","PW1", "PW2","RPM"]
    values=[
        round(hex_to_decimal(raw_message[0:4],16,False)),
        round(hex_to_decimal(raw_message[4:8],16,False))*0.001,
        round(hex_to_decimal(raw_message[8:12],16,False))*0.001,
        round(hex_to_decimal(raw_message[12:16],16,False))
    ]
    units=["s","ms","ms","rpm"]
    return [message,labels,values,units]
parse_ID_MEGASQUIRT_GP0(hex_msg)