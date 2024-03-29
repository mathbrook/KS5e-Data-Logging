########################################################################
########################################################################
# Raw Data CSV to Parsed Data CSV Code Section
########################################################################
########################################################################


"""
@Author: Bo Han Zhu
@Date: 1/15/2022
@Description: HyTech custom python parser functions.
@TODO: Dashboard_status is not correct. Need more data to validate bit ordering.

parse_folder --> parse_file --> parse_time
                            --> parse_message --> parse_ID_XXXXXXXXX
"""

# Imports
import os
import sys
from multipliers import Multipliers
from datetime import datetime
import cantools
import pandas as pd
import csv

DEBUG = False # Set True for option error print statements

def hex_to_decimal(hex, bits, is_signed):
    """
    @brief: Helper function to convert a hexadecimal to a decimal. First swaps endianness and then performs twos-complement if needed.
            Referenced partially from: https://stackoverflow.com/questions/6727875/hex-string-to-signed-int-in-python-3-2
    @input: A string representing the hexadecimal number, how many bits it has, and whether if it is signed or unsigned (True --> signed)
    @return: The corresponding decimal value as an integer.
    """

    # Swaps to small-endian
    value = ""
    for i in range(bits // 4):
        if i % 2 == 0:
            value = hex[i:i+2] + value
    value = int(value, 16)

    # Checks if needed to perform twos-complement or not; if yes, then performs twos-complement
    if is_signed and value & (1 << (bits - 1)):
        value -= 1 << bits

    return value

def bin_to_bool(bin):
    """
    @brief: Helper function to convert a single-digit binary to the string "true" or "false".
    @input: 0, 1, "0", or "1"
    @return: true if input is 1 or "1", false if 0 or "0", UNRECOGNIZED_BIN if neither
    """
    try:
        bin = int(bin)
    except:
        if DEBUG: print("UNFATAL ERROR: Binary conversion to boolean failed, received " + str(bin))
        return "UNRECOGNIZED_BIN"

    if bin == 0:
        return "false"
    elif bin == 1:
        return "true"
    else:
        if DEBUG: print("UNFATAL ERROR: Binary conversion to boolean failed, received " + str(bin))
        return "UNRECOGNIZED_BIN"


########################################################################
# Custom Parsing Functions Begin
########################################################################
'''
@brief: Each one of these functions parses the message depending on the corresponding header file in code-2022/Libraries/HyTech_CAN.
        Must be updated consistently when changes occur in the HyTech Library.
@input: A string of a hexadecimal raw message
@return: A four-element list [message, label[], value[], unit[]] 
'''
def parse_ID_FBHNODE1(raw_message):
    message="Fbhnode1"
    labels=["roll","heading"]
    values=[
        hex_to_decimal(raw_message[0:8],32,True) / 100,hex_to_decimal(raw_message[8:16],32,True)/100
    ]
    units = ["deg","deg"]
    return [message, labels, values, units]
def parse_ID_FBHNODE2(raw_message):
    message="Fbhnode2"
    labels=["pitch"]
    values=[
        hex_to_decimal(raw_message[0:8],32,True) / 100
    ]
    units = ["deg"]
    return [message, labels, values, units]

def parse_ID_MC_TEMPERATURES1(raw_message):
    message = "MC_temperatures_1"
    labels = ["module_a_temperature", "module_b_temperature", "module_c_temperature", "gate_driver_board_temperature"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_TEMPERATURES1_MODULE_A_TEMPERATURE.value, 
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.MC_TEMPERATURES1_MODULE_B_TEMPERATURE.value, 
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MC_TEMPERATURES1_MODULE_C_TEMPERATURE.value, 
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.MC_TEMPERATURES1_GATE_DRIVER_BOARD_TEMPERATURE.value
    ]
    units = ["C", "C", "C", "C"]
    return [message, labels, values, units]

def parse_ID_MC_TEMPERATURES2(raw_message):
    message = "MC_temperatures_2"
    labels = ["control_board_temperature", "rtd_1_temperature", "rtd_2_temperature", "rtd_3_temperature"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_TEMPERATURES2_CONTROL_BOARD_TEMPERATURES.value, 
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.MC_TEMPERATURES2_RTD_1_TEMPERATURES.value, 
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MC_TEMPERATURES2_RTD_2_TEMPERATURES.value, 
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.MC_TEMPERATURES2_RTD_3_TEMPERATURES.value
    ]
    units = ["C", "C", "C", "C"]
    return [message, labels, values, units]

def parse_ID_MC_TEMPERATURES3(raw_message):
    message = "MC_temperatures_3"
    labels = ["rtd_4_temperatures", "rtd_5_temperature", "motor_temperature", "torque_shudder"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_TEMPERATURES3_RTD_4_TEMPERATURES.value,
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.MC_TEMPERATURES3_RTD_5_TEMPERATURES.value,
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MC_TEMPERATURES3_MOTOR_TEMPERATURE.value, 
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.MC_TEMPERATURES3_TORQUE_SHUDDER.value
    ]
    units = ["C", "C", "C", "Nm"]
    return [message, labels, values, units]

def parse_ID_MC_ANALOG_INPUTS_VOLTAGES(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xA8.")
    return "UNPARSEABLE"
    # message = "MC_analog_input_voltages"
    # labels = ["MC_analog_input_1", "MC_analog_input_2", "MC_analog_input_3", "MC_analog_input_4"]
    # values = [
    #     hex_to_decimal(raw_message[0:4], 16, True),
    #     hex_to_decimal(raw_message[4:8], 16, True),
    #     hex_to_decimal(raw_message[8:12], 16, True),
    #     hex_to_decimal(raw_message[12:16], 16, True)
    # ]
    # units = ["", "", "", ""]
    # return [message, labels, values, units]

def parse_ID_MC_DIGITAL_INPUTS_STATUS(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xA4.")
    return "UNPARSEABLE"
    # message = "MC_digital_input_status"
    # labels = [
    #     "MC_digital_input_1", 
    #     "MC_digital_input_2", 
    #     "MC_digital_input_3", 
    #     "MC_digital_input_4", 
    #     "MC_digital_input_5", 
    #     "MC_digital_input_6", 
    #     "MC_digital_input_7", 
    #     "MC_digital_input_8"
    # ]
    # values = [
    #     raw_message[1], 
    #     raw_message[3], 
    #     raw_message[5], 
    #     raw_message[7], 
    #     raw_message[9], 
    #     raw_message[11], 
    #     raw_message[13], 
    #     raw_message[15]
    # ]
    # units = ["", "", "", "", "", "", "", ""]
    # return [message, labels, values, units]

def parse_ID_MC_MOTOR_POSITION_INFORMATION(raw_message):
    message = "MC_motor_position_information"
    labels = ["motor_angle", "motor_speed", "elec_output_freq", "delta_resolver_filtered"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_MOTOR_POSITION_INFORMATION_MOTOR_ANGLE.value,
        hex_to_decimal(raw_message[4:8], 16, True), 
        hex_to_decimal(raw_message[8:12], 16, False) / Multipliers.MC_MOTOR_POSITION_INFORMATION_ELEC_OUTPUT_FREQ.value, 
        hex_to_decimal(raw_message[12:16], 16, True)
    ]
    units = ["deg", "RPM", "Hz", ""]
    return [message, labels, values, units]

def parse_ID_MC_CURRENT_INFORMATION(raw_message):
    message = "MC_current_information"
    labels = ["phase_a_current", "phase_b_current", "phase_c_current", "dc_bus_current"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_CURRENT_INFORMATION_PHASE_A_CURRENT.value, 
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.MC_CURRENT_INFORMATION_PHASE_B_CURRENT.value, 
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MC_CURRENT_INFORMATION_PHASE_C_CURRENT.value, 
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.MC_CURRENT_INFORMATION_DC_BUS_CURRENT.value
    ]
    units = ["A", "A", "A", "A"]
    return [message, labels, values, units]

def parse_ID_MC_VOLTAGE_INFORMATION(raw_message):
    message = "MC_voltage_information"
    labels = ["dc_bus_voltage", "output_voltage", "Vd_voltage", "Vq_voltage"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_VOLTAGE_INFORMATION_DC_BUS_VOLTAGE.value,
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.MC_VOLTAGE_INFORMATION_OUTPUT_VOLTAGE.value,
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MC_VOLTAGE_INFORMATION_PHASE_AB_VOLTAGE.value,
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.MC_VOLTAGE_INFORMATION_PHASE_BC_VOLTAGE.value
    ]
    units = ["V", "V", "V", "V"]
    return [message, labels, values, units]

def parse_ID_MC_FLUX_INFORMATION(raw_message):
    message = "MC_flux_information"
    labels = ["Flux_Command", "Flux_Feedback", "Id_Feedback", "Iq_Feedback"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / 10,
        hex_to_decimal(raw_message[4:8], 16, True) / 10,
        hex_to_decimal(raw_message[8:12], 16, True) / 10,
        hex_to_decimal(raw_message[12:16], 16, True) / 10
    ]
    units = ["W", "W", "A", "A"]
    return [message, labels, values, units]
    
def parse_ID_MC_INTERNAL_VOLTAGES(raw_message):
    message = "MC_INTERNAL_VOLTAGES"
    labels = ["12V_Voltage"]
    values = [
        hex_to_decimal(raw_message[12:16], 16, True)/100
    ]
    units = ["V"]
    return [message, labels, values, units]

def parse_ID_MC_INTERNAL_STATES(raw_message):
    message = "MC_internal_states"
    labels = [
        "vsm_state",
        "inverter_state", 
        # "relay_active_1", 
        # "relay_active_2", 
        # "relay_active_3", 
        # "relay_active_4", 
        # "relay_active_5", 
        # "relay_active_6", 
        "inverter_run_mode", 
        "inverter_active_discharge_state", 
        "inverter_command_mode", 
        "inverter_enable_state", 
        "inverter_enable_lockout", 
        "direction_command"
    ]
    
    ##relay_state = hex_to_decimal(raw_message[6:8], 8, False)
    # relay_state_1 = bin_to_bool(str(relay_state & 0x01))
    # relay_state_2 = bin_to_bool(str((relay_state & 0x02) >> 1))
    # relay_state_3 = bin_to_bool(str((relay_state & 0x04) >> 2))
    # relay_state_4 = bin_to_bool(str((relay_state & 0x08) >> 3))
    # relay_state_5 = bin_to_bool(str((relay_state & 0x10) >> 4))
    # relay_state_6 = bin_to_bool(str((relay_state & 0x20) >> 5))
    inverter_run_mode_discharge_state = hex_to_decimal(raw_message[8:10], 8, False)
    inverter_run_mode = bin_to_bool(str(inverter_run_mode_discharge_state & 1))
    inverter_active_discharge_status = bin_to_bool(str(inverter_run_mode_discharge_state >> 5))
    inverter_enable = hex_to_decimal(raw_message[12:14], 8, False)
    inverter_enable_state = bin_to_bool(str(inverter_enable & 1))
    inverter_enable_lockout = bin_to_bool(str((inverter_enable & 0x80) >> 7))

    values = [
        hex(hex_to_decimal(raw_message[0:4], 16, False)),
        hex(int(raw_message[4:6], 16)), 
        # relay_state_1, 
        # relay_state_2,
        # relay_state_3, 
        # relay_state_4, 
        # relay_state_5, 
        # relay_state_6, 
        inverter_run_mode, 
        inverter_active_discharge_status, 
        hex(int(raw_message[10:12], 16)), 
        inverter_enable_state, 
        inverter_enable_lockout, 
        hex(hex_to_decimal(raw_message[14:16], 16, False))
    ]
    units = ["", "", "", "", "", "", "",""]
    return [message, labels, values, units]

def parse_ID_MC_FAULT_CODES(raw_message):
    post_fault_lo = hex_to_decimal(raw_message[0:4], 16, False)
    post_fault_hi = hex_to_decimal(raw_message[4:8], 16, False)
    run_fault_lo = hex_to_decimal(raw_message[8:12], 16, False)
    run_fault_hi = hex_to_decimal(raw_message[12:16], 16, False)
    if((run_fault_hi>0) or (run_fault_lo>0)):
        message = "MC_fault_codes"
        values=[]
        labels=[]
        labels = [
            "run_fault_lo",
            "run_lo_motor_overspeed_fault",
            "run_lo_overcurrent_fault",
            "run_lo_overvoltage_fault", 
            "run_lo_inverter_overtemperature_fault",
            "run_lo_direction_command_fault",
            "run_lo_inverter_response_timeout_fault",
            "run_lo_hardware_gate_desaturation_fault",
            "run_lo_hardware_overcurrent_fault",
            "run_lo_undervoltage_fault",
            "run_lo_can_command_message_lost_fault",
            "run_lo_motor_overtemperature_fault",
            "run_lo_reserved1",
            "run_lo_reserved2",
            "run_lo_reserved3",
            "run_fault_hi",
            "run_hi_module_a_overtemperature_fault",
            "run_hi_module_b_overtemperature_fault", 
            "run_hi_module_c_overtemperature_fault",
            "run_hi_pcb_overtemperature_fault",
            "run_hi_gate_drive_board_1_overtemperature_fault",
            "run_hi_gate_drive_board_2_overtemperature_fault",
            "run_hi_gate_drive_board_3_overtemperature_fault",
            "run_hi_current_sensor_fault",
            "run_hi_resolver_not_connected", 
            "run_hi_inverter_discharge_active"
        ]

        

        values = [
            hex(hex_to_decimal(raw_message[8:12], 16, False)),
            str(run_fault_lo & 0x0001),
            bin_to_bool(str((run_fault_lo & 0x0002) >> 1)),
            bin_to_bool(str((run_fault_lo & 0x0004) >> 2)),
            bin_to_bool(str((run_fault_lo & 0x0008) >> 3)),
            bin_to_bool(str((run_fault_lo & 0x0040) >> 6)),
            bin_to_bool(str((run_fault_lo & 0x0080) >> 7)),
            bin_to_bool(str((run_fault_lo & 0x0100) >> 8)),
            bin_to_bool(str((run_fault_lo & 0x0200) >> 9)),
            bin_to_bool(str((run_fault_lo & 0x0400) >> 10)),
            bin_to_bool(str((run_fault_lo & 0x0800) >> 11)),
            bin_to_bool(str((run_fault_lo & 0x1000) >> 12)),
            bin_to_bool(str((run_fault_lo & 0x2000) >> 13)),
            bin_to_bool(str((run_fault_lo & 0x4000) >> 14)),
            bin_to_bool(str((run_fault_lo & 0x8000) >> 15)),
            hex(hex_to_decimal(raw_message[12:16], 16, False)),
            bin_to_bool(str((run_fault_hi & 0x0004) >> 2)),
            bin_to_bool(str((run_fault_hi & 0x0008) >> 3)),
            bin_to_bool(str((run_fault_hi & 0x0010) >> 4)),
            bin_to_bool(str((run_fault_hi & 0x0020) >> 5)),
            bin_to_bool(str((run_fault_hi & 0x0040) >> 6)),
            bin_to_bool(str((run_fault_hi & 0x0080) >> 7)),
            bin_to_bool(str((run_fault_hi & 0x0100) >> 8)),
            bin_to_bool(str((run_fault_hi & 0x0200) >> 9)),
            bin_to_bool(str((run_fault_hi & 0x4000) >> 14)),
            bin_to_bool(str((run_fault_hi & 0x8000) >> 15))
        ]

        units = []
        for i in range(len(labels)):
            units.append("")
    
        return [message, labels, values, units]
    else:
        return "UNPARSEABLE"

def parse_ID_MC_TORQUE_TIMER_INFORMATION(raw_message):
    message = "MC_torque_timer_information"
    labels = ["commanded_torque", "torque_feedback", "rms_uptime"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_TORQUE_TIMER_INFORMATION_COMMANDED_TORQUE.value,
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.MC_TORQUE_TIMER_INFORMATION_TORQUE_FEEDBACK.value, 
        hex_to_decimal(raw_message[8:16], 32, False) / Multipliers.MC_TORQUE_TIMER_INFORMATION_RMS_UPTIME.value
    ]
    units = ["Nm", "Nm", "s"]
    return [message, labels, values, units]

def parse_ID_MC_FLUX_WEAKENING_OUTPUT(raw_message):
    message = "MC_flux_weakening_output"
    labels = ["modulation_index", "flux_weakening_output", "id_command", "iq_command"]
    values = [
        hex(hex_to_decimal(raw_message[0:4], 16, False)),
        hex(hex_to_decimal(raw_message[4:8], 16, False)),
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MC_FLUX_WEAKENING_OUTPUT_ID_COMMAND.value, 
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.MC_FLUX_WEAKENING_OUTPUT_IQ_COMMAND.value
    ]
    units = ["", "", "", ""]
    return [message, labels, values, units]

def parse_ID_MC_FIRMWARE_INFORMATION(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xA8.")
    return "UNPARSEABLE"
    # message = "MC_firmware_information"
    # labels = ["eeprom_version_project_code", "software_version", "date_code_mmdd", "date_code_yyyy"]
    # values = [
    #     hex_to_decimal(raw_message[0:4], 16, False),
    #     hex_to_decimal(raw_message[4:8], 16, False),
    #     hex_to_decimal(raw_message[8:12], 16, False),
    #     hex_to_decimal(raw_message[12:16], 16, False)
    # ]
    # units = ["", "", "", ""]
    # return [message, labels, values, units]

def parse_ID_MC_DIAGNOSTIC_DATA(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xAF.")
    return "UNPARSEABLE"

def parse_ID_MC_COMMAND_MESSAGE(raw_message):
    message = "MC_command_message"
    labels = ["requested_torque","inverter_enable"]
    ##labels = ["requested_torque", "angular_velocity", "direction", "inverter_enable", "discharge_enable", "command_torque_limit"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, True) / Multipliers.MC_COMMAND_MESSAGE_REQUESTED_TORQUE.value,
        ##hex_to_decimal(raw_message[4:8], 16, True), 
        ##hex(int(raw_message[9], 16)),
        hex_to_decimal(raw_message[10], 4, False), 
        ##hex_to_decimal(raw_message[11], 4, False), 
        ##hex_to_decimal(raw_message[12:16], 16, True)
    ]
    units = ["Nm", ""]
    return [message, labels, values, units]

def parse_ID_MC_READ_WRITE_PARAMETER_COMMAND(raw_message):
    message = "MC_read_write_parameter_command"
    labels = ["parameter_address", "rw_command", "reserved1", "data"]
    values = [
        hex(int(hex_to_decimal(raw_message[0:4], 16, False))),
        hex(int(raw_message[5])),
        hex_to_decimal(raw_message[6:8], 8, False),
        hex(int(hex_to_decimal(raw_message[8:16], 32, False)))
    ]
    units = ["", "", "", ""]
    return [message, labels, values, units]

def parse_ID_MC_READ_WRITE_PARAMETER_RESPONSE(raw_message):
    message = "MC_read_write_parameter_response"
    labels = ["parameter_address", "write_success", "reserved1", "data"]
    values = [
        hex(int(hex_to_decimal(raw_message[0:4], 16, False))),
        hex(int(raw_message[5])),
        hex_to_decimal(raw_message[6:8], 8, False),
        hex(int(hex_to_decimal(raw_message[8:16], 32, False)))
    ]
    units = ["", "", "", ""]
    return [message, labels, values, units]

def parse_ID_MCU_STATUS(raw_message):
    message = "MCU_status"
    labels = [
        "imd_ok_high",
        "shutdown_b_above_threshold",
        "bms_ok_high",
        "shutdown_c_above_threshold",
        "bspd_ok_high",
        "shutdown_d_above_threshold",
        "software_ok_high",
        "shutdown_e_above_threshold",
        "no_accel_implausibility",
        "no_brake_implausibility",
        "brake_pedal_active",
        "bspd_current_high",
        "bspd_brake_high",
        "no_accel_brake_implausibility",
        "mcu_state",
        "inverter_powered",
        "energy_meter_present",
        "activate_buzzer",
        "software_is_ok",
        "launch_ctrl_active",
        "max_torque",
        "torque_mode",
        "distance_travelled"
    ]

    temp_bin_rep = bin(hex_to_decimal(raw_message[2:4], 8, False))[2:].zfill(8) + bin(hex_to_decimal(raw_message[4:6], 8, False))[2:].zfill(8) + bin(hex_to_decimal(raw_message[6:8], 8, False))[2:].zfill(8)
    
    # Change bin rep to small endian
    bin_rep = ""
    for i in range(len(temp_bin_rep)):
        if i % 8 == 0:
            bin_rep = bin_rep + temp_bin_rep[i+7] + temp_bin_rep[i+6] + temp_bin_rep[i+5] + temp_bin_rep[4] + temp_bin_rep[i+3] + temp_bin_rep[i+2] + temp_bin_rep[i+1] + temp_bin_rep[i]

    def binary_to_MCU_STATE(bin_rep):
        # Back to Big Endian
        bin_rep = bin_rep[2] + bin_rep[1] + bin_rep[0]

        if bin_rep == "000": return "STARTUP"
        if bin_rep == "001": return "TRACTIVE_SYSTEM_NOT_ACTIVE"
        if bin_rep == "010": return "TRACTIVE_SYSTEM_ACTIVE"
        if bin_rep == "011": return "ENABLING_INVERTER"
        if bin_rep == "100": return "WAITING_READY_TO_DRIVE_SOUND"
        if bin_rep == "101": return "READY_TO_DRIVE"
        # Should never get here
        if DEBUG: print("UNFATAL ERROR: Unrecognized MCU state: " + bin_rep)
        return "UNRECOGNIZED_STATE"

    values = []
    for i in range(24):
        if i == 8 or i == 9: # torque_mode 2-bits are never used
            continue
        elif i == 16: # convert binary to MCU state
            values.append(binary_to_MCU_STATE(bin_rep[16:19]))
        elif i == 17 or i == 18: # no need to do anything here because i == 16 takes care of them
            continue
        else:
            values.append(bin_to_bool(bin_rep[i]))
    values.append(hex_to_decimal(raw_message[8:10], 8, False))
    values.append(hex_to_decimal(raw_message[10:12], 8, False))
    values.append(hex_to_decimal(raw_message[12:16], 16, False) / Multipliers.MCU_STATUS_DISTANCE_TRAVELLED.value)

    units = []
    for i in range(len(labels) - 3):
        units.append("")
    units.append("Nm")
    units.append("")
    units.append("m")

    return [message, labels, values, units]

def parse_ID_MCU_PEDAL_READINGS(raw_message):
    message = "MCU_pedal_readings"
    labels = ["accelerator_pedal_1", "accelerator_pedal_2", "brake_transducer_1", "steering_sensor"]

    accelerator_1 = round(hex_to_decimal(raw_message[0:4], 16, False))
    accelerator_2 = round(hex_to_decimal(raw_message[4:8], 16, False))
    brake_1 = round(hex_to_decimal(raw_message[8:12], 16, False))
    brake_2 = round(hex_to_decimal(raw_message[12:16], 16, False))
    # If the linear regression occasionally results in a negative value, set it to 0.0
    if accelerator_1 < 0.0:
        accelerator_1 = 0.0
    if accelerator_2 < 0.0:
        accelerator_2 = 0.0

    values = [
        accelerator_1, 
        accelerator_2, 
        brake_1, 
        brake_2
    ]
    units = ["%", "%", "%", "%"]
    return [message, labels, values, units]

def parse_ID_MCU_ANALOG_READINGS(raw_message):
    message = "MCU_analog_readings"
    labels = ["ecu_current", "cooling_current", "temperature", "glv_battery_voltage"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, False) / Multipliers.MCU_ANALOG_READINGS_ECU_CURRENT.value, 
        hex_to_decimal(raw_message[4:8], 16, False) / Multipliers.MCU_ANALOG_READINGS_COOLING_CURRENT.value,
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.MCU_ANALOG_READINGS_TEMPERATURE.value, 
        hex_to_decimal(raw_message[12:16], 16, False) / Multipliers.MCU_ANALOG_READINGS_GLV_BATTERY_VOLTAGE.value
    ]
    units = ["A", "A", "C", "V"]
    return [message, labels, values, units]

def parse_ID_BMS_ONBOARD_TEMPERATURES(raw_message):
    message = "BMS_onboard_temperatures"
    labels = ["average_temperature", "low_temperature", "high_temperature"]
    values = [
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.BMS_ONBOARD_TEMPERATURES_AVERAGE_TEMPERATURE.value,
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.BMS_ONBOARD_TEMPERATURES_LOW_TEMPERATURE.value,
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.BMS_ONBOARD_TEMPERATURES_HIGH_TEMPERATURE.value
    ]
    units = ["C", "C", "C"]
    return [message, labels, values, units]

def parse_ID_BMS_ONBOARD_DETAILED_TEMPERATURES(raw_message):
    message = "BMS_onboard_detailed_temperatures"
    ic_id = str(hex_to_decimal(raw_message[0:2], 8, False))
    labels = ["IC_" + ic_id + "_temperature_0", "IC_" + ic_id + "_temperature_1"]
    values = [
        hex_to_decimal(raw_message[2:6], 16, True) / Multipliers.BMS_ONBOARD_DETAILED_TEMPERATURES_TEMPERATURE_0.value,
        hex_to_decimal(raw_message[6:10], 16, True) / Multipliers.BMS_ONBOARD_DETAILED_TEMPERATURES_TEMPERATURE_1.value
    ]
    units = ["C", "C"]
    return [message, labels, values, units]

def parse_ID_BMS_VOLTAGES(raw_message):
    message = "BMS_voltages"
    labels = ["BMS_voltage_average", "BMS_voltage_low", "BMS_voltage_high", "BMS_voltage_total"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, False) / Multipliers.BMS_VOLTAGES_BMS_VOLTAGE_AVERAGE.value,
        hex_to_decimal(raw_message[4:8], 16, False) / Multipliers.BMS_VOLTAGES_BMS_VOLTAGE_LOW.value,
        hex_to_decimal(raw_message[8:12], 16, False) / Multipliers.BMS_VOLTAGES_BMS_VOLTAGE_HIGH.value,
        hex_to_decimal(raw_message[12:16], 16, False) / Multipliers.BMS_VOLTAGES_BMS_VOLTAGE_TOTAL.value
    ]
    units = ["V", "V", "V", "V"]
    return [message, labels, values, units]

def parse_ID_BMS_DETAILED_VOLTAGES(raw_message):
    message = "BMS_detailed_voltages"
    ic_id = raw_message[3]
    group_id = int(raw_message[2], 16)
    labels = ""
    if group_id == 0:
        labels = ["IC_" + ic_id + "_CELL_0", "IC_" + ic_id + "_CELL_1", "IC_" + ic_id + "_CELL_2"]
    elif group_id == 1:
        labels = ["IC_" + ic_id + "_CELL_3", "IC_" + ic_id + "_CELL_4", "IC_" + ic_id + "_CELL_5"]
    elif group_id == 2:
        labels = ["IC_" + ic_id + "_CELL_6", "IC_" + ic_id + "_CELL_7", "IC_" + ic_id + "_CELL_8"]
    elif group_id == 3 and int(ic_id, 16) % 2 == 0:
        labels = ["IC_" + ic_id + "_CELL_9", "IC_" + ic_id + "_CELL_10", "IC_" + ic_id + "_CELL_11"]
    else:
        if DEBUG: print("UNFATAL ERROR: BMS detailed voltage group " + str(group_id) + " is invalid.")
        return "UNPARSEABLE"
    values = [
        hex_to_decimal(raw_message[4:8], 16, False) / Multipliers.BMS_DETAILED_VOLTAGES_VOLTAGE_0.value,
        hex_to_decimal(raw_message[8:12], 16, False) / Multipliers.BMS_DETAILED_VOLTAGES_VOLTAGE_1.value,
        hex_to_decimal(raw_message[12:16], 16, False) / Multipliers.BMS_DETAILED_VOLTAGES_VOLTAGE_2.value
    ]
    units = ["V", "V", "V"]
    return [message, labels, values, units]

def parse_ID_BMS_TEMPERATURES(raw_message):
    message = "BMS_temperatures"
    labels = ["BMS_average_temperature", "BMS_low_temperature", "BMS_high_temperature"]
    values = [
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.BMS_TEMPERATURES_BMS_AVERAGE_TEMPERATURE.value,
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.BMS_TEMPERATURES_BMS_LOW_TEMPERATURE.value,
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.BMS_TEMPERATURES_BMS_HIGH_TEMPERATURE.value
    ]
    units = ["C", "C", "C"]
    return [message, labels, values, units]

def parse_ID_BMS_DETAILED_TEMPERATURES(raw_message):
    message = "BMS_detailed_temperatures"
    ic_id = raw_message[3]
    group_id = int(raw_message[2], 16)

    # Different parsing if IC_ID is even or old
    # If IC_ID is even, GPIO 5 is humidity; if IC_ID is odd, GPIO 5 is temperature
    isEven = False
    if int(ic_id, 16) % 2 == 0: isEven = True

    labels = ""
    if isEven:
        if group_id == 0:
            labels = ["IC_" + ic_id + "_therm_0", "IC_" + ic_id + "_therm_1", "IC_" + ic_id + "_therm_2"]
        elif group_id == 1:
            labels = ["IC_" + ic_id + "_therm_3", "IC_" + ic_id + "_humidity", "IC_" + ic_id + "_Vref"]
        else:
            if DEBUG: print("UNFATAL ERROR: BMS detailed temperature group " + str(group_id) + " is invalid.")
            return "UNPARSEABLE"
    else:
        if group_id == 0:
            labels = ["IC_" + ic_id + "_therm_0", "IC_" + ic_id + "_therm_1", "IC_" + ic_id + "_therm_2"]
        elif group_id == 1:
            labels = ["IC_" + ic_id + "_therm_3", "IC_" + ic_id + "_temperature", "IC_" + ic_id + "_Vref"]
        else:
            if DEBUG: print("UNFATAL ERROR: BMS detailed temperature group " + str(group_id) + " is invalid.")
            return "UNPARSEABLE"

    values = [
        hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.BMS_DETAILED_TEMPERATURES_THERM_0.value,
        hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.BMS_DETAILED_TEMPERATURES_THERM_1.value,
        hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.BMS_DETAILED_TEMPERATURES_THERM_2.value
    ]

    units = []
    if group_id == 0: units = ["C", "C", "C"]
    else:
        if isEven: units = ["C", "%", "V"]
        else: units = ["C", "C", "V"]

    return [message, labels, values, units]
    
def parse_ID_BMS_STATUS(raw_message):
    message = "BMS_status"
    labels = [
        "BMS_state",
        "BMS_error_flags",
        "BMS_overvoltage",
        "BMS_undervoltage",
        "BMS_total_voltage_high",
        "BMS_discharge_overcurrent",
        "BMS_charge_overcurrent",
        "BMS_discharge_overtemp",
        "BMS_charge_overtemp",
        "BMS_undertemp",
        "BMS_onboard_overtemp",
        "BMS_current",
        "BMS_flags",
        "BMS_shutdown_g_above_threshold",
        "BMS_shutdown_h_above_threshold"
    ]


    error_flags = hex_to_decimal(raw_message[6:10], 16, False)
    flags = hex_to_decimal(raw_message[14:16], 8, False)
    values = [
        hex(int(raw_message[4:6], 16)),
        hex(error_flags),
        bin_to_bool(error_flags & 0x1),
        bin_to_bool((error_flags & 0x2) >> 1),
        bin_to_bool((error_flags & 0x4) >> 2),
        bin_to_bool((error_flags & 0x8) >> 3),
        bin_to_bool((error_flags & 0x10) >> 4),
        bin_to_bool((error_flags & 0x20) >> 5),
        bin_to_bool((error_flags & 0x40) >> 6),
        bin_to_bool((error_flags & 0x80) >> 7),
        bin_to_bool((error_flags & 0x100) >> 8),
        hex_to_decimal(raw_message[10:14], 16, True) / Multipliers.BMS_STATUS_BMS_CURRENT.value,
        hex(int(raw_message[14:16], 16)),
        bin_to_bool(flags & 0x1),
        bin_to_bool((flags & 0x2) >> 1)
    ]

    units = []
    for i in range(len(labels)):
        if i == len(labels) - 4:
            units.append("A")
        else:
            units.append("")

    return [message, labels, values, units]

def parse_ID_FH_WATCHDOG_TEST(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xDC.")
    return "UNPARSEABLE"

def parse_ID_CCU_STATUS(raw_message):
    message = "CCU_status"
    labels = ["charger_enabled"]
    values = [int(raw_message[14:16], 16)]
    units = [""]
    return [message, labels, values, units]

def parse_ID_BMS_BALANCING_STATUS(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xDE.")
    return "UNPARSEABLE"

def parse_ID_BMS_READ_WRITE_PARAMETER_COMMAND(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xE0.")
    return "UNPARSEABLE"

def parse_ID_BMS_PARAMETER_RESPONSE(raw_message):
    if DEBUG: print("UNFATAL ERROR: Do not know how to parse CAN ID 0xE1.")
    return "UNPARSEABLE"

def parse_ID_BMS_COULOMB_COUNTS(raw_message):
    message = "BMS_coulomb_counts"
    labels = ["BMS_total_charge", "BMS_total_discharge"]
    values = [
        hex_to_decimal(raw_message[0:8], 32, False) / Multipliers.BMS_COULOMB_COUNTS_BMS_TOTAL_CHARGE.value,
        hex_to_decimal(raw_message[8:16], 32, False) / Multipliers.BMS_COULOMB_COUNTS_BMS_TOTAL_DISCHARGE.value
    ]
    units = ["Ah", "Ah"]
    return [message, labels, values, units]

def parse_ID_MCU_GPS_READINGS(raw_message):
    message = "MCU_GPS_readings"
    labels = ["latitude", "longitude"]
    values = [
        hex_to_decimal(raw_message[0:8], 32, True) / Multipliers.MCU_GPS_READINGS_LATITUDE.value,
        hex_to_decimal(raw_message[8:16], 32, True) / Multipliers.MCU_GPS_READINGS_LONGITUDE.value
    ]
    units = ["deg", "deg"]
    return [message, labels, values, units]

def parse_ID_MCU_WHEEL_SPEED(raw_message):
    message = "MCU_wheel_speed"
    labels = ["rpm_front_left", "rpm_front_right"]
    values = [
        hex_to_decimal(raw_message[0:8], 32, False)/100,
        hex_to_decimal(raw_message[8:16], 32, False)/100
    ]
    units = ["rpm", "rpm"]
    return [message, labels, values, units]

# @TODO: FIX THIS with more data
def parse_ID_DASHBOARD_STATUS(raw_message):
    message = "Dashboard_status"
    labels = [
        "start_btn",
        "buzzer_active",
        "ssok_above_threshold",
        "shutdown_h_above_threshold",
        "mark_btn",
        "mode_btn",
        "mc_cycle_btn",
        "launch_ctrl_btn",
        "ams_led",
        "imd_led",
        "mode_led",
        "mc_error_led",
        "start_led",
        "launch_control_led"
    ]
    
    raw_message = raw_message[8:] # Strip first 8 padded zeros
    bin_rep = bin(int(raw_message, 16))[2:].zfill(32)
    def blink_modes(bin_rep):
        bin_rep = int(bin(bin_rep)[2:].zfill(2)[1] + bin(bin_rep)[2:].zfill(2)[0], 2) # Back to big-endian
        if bin_rep == 0: return "off"
        elif bin_rep == 1: return "on"
        elif bin_rep == 2: return "fast"
        elif bin_rep == 3: return "slow"
        else:
            if DEBUG: print("UNFATAL ERROR: Unrecognizable blink mode " + str(bin_rep))
            return "UNRECOGNIZED_BLINK"

    led_flags = (bin_rep[30:32] + bin_rep[28:30] + bin_rep[26:28] + bin_rep[24:26])[::-1] + (bin_rep[22:24] + bin_rep[20:22] + bin_rep[18:20] + bin_rep[16:18])[::-1]
    values = [
        bin_to_bool(bin_rep[7]), # Endianness changed
        bin_to_bool(bin_rep[6]),
        bin_to_bool(bin_rep[5]),
        bin_to_bool(bin_rep[4]),
        bin_to_bool(bin_rep[15]),
        bin_to_bool(bin_rep[14]),
        bin_to_bool(bin_rep[13]),
        bin_to_bool(bin_rep[12]),
        blink_modes(int(led_flags, 2) & 0x0003),
        blink_modes((int(led_flags, 2) & 0x000C) >> 2),
        blink_modes((int(led_flags, 2) & 0x0030) >> 4),
        blink_modes((int(led_flags, 2) & 0x00C0) >> 6),
        blink_modes((int(led_flags, 2) & 0x0300) >> 8),
        blink_modes((int(led_flags, 2) & 0x0C00) >> 10)
    ]

    units = []
    for i in range(len(labels)):
        units.append("")
    return [message, labels, values, units]

def parse_ID_SAB_READINGS_FRONT(raw_message):
    message = "SAB_readings_front"
    labels = ["fl_susp_lin_pot", "fr_susp_lin_pot"]
    values = [
        hex_to_decimal(raw_message[8:12], 16, False) / Multipliers.SAB_READINGS_NON_GPS.value,
        hex_to_decimal(raw_message[12:16], 16, False) / Multipliers.SAB_READINGS_NON_GPS.value
    ]
    units = ["mm", "mm"]
    return [message, labels, values, units]

def parse_ID_SAB_READINGS_REAR(raw_message):
    message = "SAB_readings_rear"
    labels = ["cooling_loop_fluid_temp", "amb_air_temp", "bl_susp_lin_pot", "br_susp_lin_pot"]
    values = [
        hex_to_decimal(raw_message[0:4], 16, False) / Multipliers.SAB_READINGS_NON_GPS.value,
        hex_to_decimal(raw_message[4:8], 16, False) / Multipliers.SAB_READINGS_NON_GPS.value,
        hex_to_decimal(raw_message[8:12], 16, False) / Multipliers.SAB_READINGS_NON_GPS.value,
        hex_to_decimal(raw_message[12:16], 16, False) / Multipliers.SAB_READINGS_NON_GPS.value
    ]
    units = ["C", "C", "mm", "mm"]
    return [message, labels, values, units]

def parse_ID_SAB_READINGS_GPS(raw_message):
    message = "SAB_readings_gps"
    labels = ["gps_latitude", "gps_longitude"]
    values = [
        hex_to_decimal(raw_message[0:8], 32, True) / Multipliers.SAB_READINGS_GPS.value,
        hex_to_decimal(raw_message[8:16], 32, True) / Multipliers.SAB_READINGS_GPS.value
    ]
    units = ["deg", "deg"]
    return [message, labels, values, units]


def parse_ID_EM_MEASUREMENT(raw_message):
    message = "EM_measurement"
    labels = ["current", "voltage"]

    def twos_comp(value):
        bits = 32
        if value & (1 << (bits - 1)):
            value -= 1 << bits
        return value
    bin_rep = bin(int(raw_message, 16))
    bin_rep = bin_rep[2:].zfill(64)
    current = round(twos_comp(int(bin_rep[7:39], 2)) / Multipliers.EM_MEASUREMENTS_CURRENT.value, 2)
    voltage = round(twos_comp(int(bin_rep[39:71], 2)) / Multipliers.EM_MEASUREMENTS_VOLTAGE.value, 2)
    values = [current, voltage]

    units = ["A", "V"]
    return [message, labels, values, units]

def parse_ID_EM_STATUS(raw_message):
    message = "EM_status"
    labels = ["voltage_gain", "current_gain", "overvoltage", "overpower", "logging"]

    raw_message = raw_message[8:]
    bin_rep = bin(int(raw_message, 16))
    bin_rep = bin_rep[2:].zfill(32)
    voltage_gain = int(bin_rep[0:4], 2)
    current_gain = int(bin_rep[4:8], 2)
    if voltage_gain == 0:
        voltage_gain = "x1"
    elif voltage_gain == 1:
        voltage_gain = "x2"
    elif voltage_gain == 2:
        voltage_gain = "x4"
    elif voltage_gain == 3:
        voltage_gain = "x8"
    elif voltage_gain == 4:
        voltage_gain = "x16"
    elif voltage_gain == 5:
        voltage_gain = "x32"
    else:
        if DEBUG: print("UNFATAL ERROR: Unknown Energy Meter voltage gain: " + str(voltage_gain))
        voltage_gain = "N/A"
    
    if current_gain == 0:
        current_gain = "x1"
    elif current_gain == 1:
        current_gain = "x2"
    elif current_gain == 2:
        current_gain = "x4"
    elif current_gain == 3:
        current_gain = "x8"
    elif current_gain == 4:
        current_gain = "x16"
    elif current_gain == 5:
        current_gain = "x32"
    else:
        if DEBUG: print("UNFATAL ERROR: Unknown Energy Meter current gain: " + str(current_gain))
        current_gain = "N/A"

    values = [
        voltage_gain,
        current_gain,
        bin_to_bool(bin_rep[8]),
        bin_to_bool(bin_rep[9]),
        bin_to_bool(bin_rep[10])
    ]

    units = ["gain", "gain", "", "", ""]
    return [message, labels, values, units]

def parse_ID_IMU_ACCELEROMETER(raw_message):
    message = "IMU_accelerometer"
    labels = ["lat_accel", "long_accel", "vert_accel"]
    values = [
        round(hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.IMU_ACCELEROMETER_ALL.value, 4),
        round(hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.IMU_ACCELEROMETER_ALL.value, 4),
        round(hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.IMU_ACCELEROMETER_ALL.value, 4)
    ]
    units = ["m/s/s", "m/s/s", "m/s/s"]
    return [message, labels, values, units]

def parse_ID_IMU_GYROSCOPE(raw_message):
    message = "IMU_gyroscope"
    labels = ["yaw", "pitch", "roll"]
    values = [
        round(hex_to_decimal(raw_message[4:8], 16, True) / Multipliers.IMU_GYROSCOPE_ALL.value, 4),
        round(hex_to_decimal(raw_message[8:12], 16, True) / Multipliers.IMU_GYROSCOPE_ALL.value, 4),
        round(hex_to_decimal(raw_message[12:16], 16, True) / Multipliers.IMU_GYROSCOPE_ALL.value, 4)
    ]
    units = ["deg/s", "deg/s", "deg/s"]
    return [message, labels, values, units]
#orion BMS shit i added
def parse_ID_ORIONBMS_MESSAGE1(raw_message):
    message= "Orion BMS1"
    labels=["DCL","hightemp", "lowtemp"]
    values=[
        round(hex_to_decimal(raw_message[0:4],16,False)),
        round(hex_to_decimal(raw_message[8:10],8,True)),
        round(hex_to_decimal(raw_message[10:12],8,True)),
    ]
    units=["A","C","C"]
    return [message,labels,values,units]
def parse_ID_ORIONBMS_MESSAGE2(raw_message):
    message= "Orion BMS2"
    labels=["PackCurrent","PackInstVolt", "PackOpenVolt", "PackSummedVolt"]
    values=[
        round(hex_to_decimal(raw_message[0:4],16,True)),
        round(hex_to_decimal(raw_message[4:8],16,True))/10,
        round(hex_to_decimal(raw_message[8:12],16,True))/10,
        round(hex_to_decimal(raw_message[12:16],16,True))/100
    ]
    units=["Amps","Volts","Volts","Volts"]
    return [message,labels,values,units]
def parse_ID_PRECHARGE(raw_message):
    message= "Precharge"
    labels=["State","AccVoltage", "TSVoltage"]
    state = hex_to_decimal(raw_message[0:2],8,False)
    accV = hex_to_decimal(raw_message[2:4],8,False) + hex_to_decimal(raw_message[4:6],8,False)*100
    tsV = hex_to_decimal(raw_message[6:8],8,False) + hex_to_decimal(raw_message[8:10],8,False)*100

    values=[
        state,
        accV,
        tsV
    ]
    units=["State","V","V"]
    return [message,labels,values,units]
def parse_ID_SHONK_POTS(raw_message):
    message= "Shock_Pots"
    labels=["Shonk_FL","Shonk_FR", "Shonk_RL","Shonk_RR"]
    values=[
        round(hex_to_decimal(raw_message[0:4],16,False)),
        round(hex_to_decimal(raw_message[4:8],16,False)),
        round(hex_to_decimal(raw_message[8:12],16,False)),
        round(hex_to_decimal(raw_message[12:16],16,False))
    ]
    units=["","","",""]

    return [message,labels,values,units]
def parse_ID_ACU_TEMP_SENSORS(raw_message):
    message= "Energus_Voltages"
    board_id = round(hex_to_decimal(raw_message[0:2],8,False))
    if(board_id == 0):
        labels=["Cell_0","Cell_12", "Cell_24","Cell_36","Cell_48"]
    elif(board_id == 1):
        labels=["Cell_1","Cell_13", "Cell_25","Cell_37","Cell_49"]
    elif(board_id == 2):
        labels=["Cell_2","Cell_14", "Cell_26","Cell_38","Cell_50"]       
    elif(board_id == 3):
        labels=["Cell_3","Cell_15", "Cell_27","Cell_39","Cell_51"]
    elif(board_id == 4):
        labels=["Cell_4","Cell_16", "Cell_28","Cell_40","Cell_52"]
    elif(board_id == 5):
        labels=["Cell_5","Cell_17", "Cell_29","Cell_41","Cell_53"]
    elif(board_id == 6):
        labels=["Cell_6","Cell_18", "Cell_30","Cell_42","Cell_54"]
    elif(board_id == 7):
        labels=["Cell_7","Cell_19", "Cell_31","Cell_43","Cell_55"]
    elif(board_id == 8):
        labels=["Cell_8","Cell_20", "Cell_32","Cell_44","Cell_56"]
    elif(board_id == 9):
        labels=["Cell_9","Cell_21", "Cell_33","Cell_45","Cell_57"]
    elif(board_id == 10):
        labels=["Cell_10","Cell_22", "Cell_34","Cell_46","Cell_58"]
    elif(board_id == 11):
        labels=["Cell_11","Cell_23", "Cell_35","Cell_47","Cell_59"]
    else:
        labels=["Cell_69","Cell_23", "Cell_35","Cell_47","Cell_59"]
    values=[
        round(hex_to_decimal(raw_message[2:4],8,False))/100,
        round(hex_to_decimal(raw_message[4:6],8,False))/100,
        round(hex_to_decimal(raw_message[6:8],8,False))/100,
        round(hex_to_decimal(raw_message[8:10],8,False))/100,
        round(hex_to_decimal(raw_message[10:12],8,False))/100
    ]
    units=["V","V","V","V","V"]

    return [message,labels,values,units]
########################################################################
# Custom Parsing Functions End
########################################################################
def get_dbc_files():
    # Get all the DBC files for parsing and add them together
    try:
        path_name = 'DBC_Files'
        file_path = []
        file_count = 0
        for root, dirs, files in os.walk(path_name, topdown=False):
            for name in files:
                if ".dbc" in name or ".DBC" in name:
                    fp = os.path.join(root, name)
                    file_path.append(fp)
                    file_count += 1
    except:
        print('FATAL ERROR: Process failed at step 1.')
        sys.exit(0)
    mega_dbc=cantools.database.Database()
    for filename in file_path:
        with open (filename, 'r') as newdbc:
            mega_dbc.add_dbc(newdbc)

    print('Step 1: found ' + str(file_count) + ' files in the DBC files folder')
    return mega_dbc

def print_all_the_shit_in_dbc_file(db):
    dbc_ids=[]
    for message in db.messages:
        # print(str(vars(message)) + "\n")
        dbc_ids.append(message.frame_id)
        # print(str(message.name)+" ID: "+str(message.frame_id)+" Note: "+str(message.comment))
        # print("\tsignals: ")
        # for signal in message.signals:
            # print("\t\t"+ signal.name)
    return dbc_ids

def parse_message(id, data, db,dbc_ids,unknown_ids):
    labels=[]
    values=[]
    units=[]
    if int(id,16) in dbc_ids:
        actual_message = db.get_message_by_frame_id(int(id,16))
        for signal in actual_message.signals:
            units.append(str(signal.unit))
        parsed_message = db.decode_message(int(id,16),bytearray.fromhex(data))
        for i in parsed_message:
            message_label = str(i)
            labels.append(message_label)
            values.append(str(parsed_message[i]))
        message_name = actual_message.name
        return [message_name,labels,values,units]
    if (id not in unknown_ids) & (int(id,16) not in dbc_ids):
        unknown_ids.append(id)
    return "INVALID_ID"

def parse_message_better(id, data, db,dbc_ids,unknown_ids):
    if int(id,16) in dbc_ids:
        parsed_message = db.decode_message(int(id,16),bytearray.fromhex(data))
        return parsed_message
    if (id not in unknown_ids) & (int(id,16) not in dbc_ids):
        unknown_ids.append(id)
    return "INVALID_ID"

def parse_time(raw_time):
    '''
    @brief: Converts raw time into human-readable time.
    @input: The raw time given by the raw data CSV.
    @return: A string representing the human-readable time.
    '''
    ms = int(raw_time) % 1000
    raw_time = int(raw_time) / 1000
    time = str(datetime.utcfromtimestamp(raw_time).strftime('%Y-%m-%dT%H:%M:%S'))
    time = time + "." + str(ms).zfill(3) + "Z"
    return time
def parse_used_ids(filename,dbc_for_parsing,dbc_ids,unknown_ids):
    header_list = ["Time"]
    infile = open("Raw_Data/" + filename, "r")
    flag_first_line=True
    for line in infile.readlines():
        if flag_first_line:
            flag_first_line = False
        else:
            raw_id = line.split(",")[1]
            length = line.split(",")[2]
            raw_message = line.split(",")[3]
            if length == 0 or raw_message == "\n":
                continue
            raw_message = raw_message[:(int(length) * 2)] # Strip trailing end of line/file characters that may cause bad parsing
            raw_message = raw_message.zfill(16) # Sometimes messages come truncated if 0s on the left. Append 0s so field-width is 16.
            current_message = parse_message_better(raw_id,raw_message,dbc_for_parsing,dbc_ids,unknown_ids)
            if current_message != "INVALID_ID":
                for i in current_message:
                    if i not in header_list:
                        header_list.append(i)
    return header_list

def parse_file(filename,dbc):
    '''
    @brief: Reads raw data file and creates parsed data CSV.
            Loops through lines to write to parsed datafile.
            Calls the parse_message and parse_time functions as helpers.
    @input: The filename of the raw and parsed CSV.
    @return: N/A
    '''

    # Array to keep track of IDs we can't parse

    unknown_ids = []
    # Array to keep track of IDs we CAN parse
    dbc_ids = print_all_the_shit_in_dbc_file(dbc)
    header_list = parse_used_ids(filename,dbc,dbc_ids,unknown_ids)
    # Miscellaneous shit lol
    nextline = [""] * len(header_list)
    header_string=",".join(header_list)


    infile = open("Raw_Data/" + filename, "r")
    outfile = open("Parsed_Data/" + filename, "w")
    outfile2 = open("Better_Parsed_Data/Better" + filename, "w")

    flag_second_line = True
    flag_first_line = True
    last_time=''
    for line in infile.readlines():
        # On the first line, do not try to parse. Instead, set up the CSV headers.
        if flag_first_line:
            flag_first_line = False
            outfile.write("time,id,message,label,value,unit\n")
            outfile2.write(header_string+"\n")
        # Otherwise attempt to parse the line.
        else:
            raw_time = line.split(",")[0]
            raw_id = line.split(",")[1]
            length = line.split(",")[2]
            raw_message = line.split(",")[3]

            # Do not parse if the length of the message is 0, otherwise bugs will occur later.
            if length == 0 or raw_message == "\n":
                continue
            
            # Call helper functions
            time = parse_time(raw_time)
            raw_message = raw_message[:(int(length) * 2)] # Strip trailing end of line/file characters that may cause bad parsing
            raw_message = raw_message.zfill(16) # Sometimes messages come truncated if 0s on the left. Append 0s so field-width is 16.
            # Get actual message, referencing our DBC file and ID lists
            table = parse_message(raw_id, raw_message,dbc,dbc_ids,unknown_ids)

            if table == "INVALID_ID" or table == "UNPARSEABLE":
                continue

            # Assertions that check for parser failure. Notifies user on where parser broke.
            assert len(table) == 4, "FATAL ERROR: Parser expected 4 arguments from parse_message at ID: 0x" + table[0] + ", got: " + str(len(table))
            assert len(table[1]) == len (table[2]) and len(table[1]) == len(table[3]), "FATAL ERROR: Label, Data, or Unit numbers mismatch for ID: 0x" + raw_id
            
            # Harvest parsed datafields and write to outfile.
            message = table[0].strip()
            for i in range(len(table[1])):
                label = table[1][i].strip()
                value = str(table[2][i]).strip()
                unit = table[3][i].strip()

                outfile.write(time + ",0x" + raw_id + "," + message + "," + label + "," + value + "," + unit + "\n")
            current_message = parse_message_better(raw_id,raw_message,dbc,dbc_ids,unknown_ids)
            if current_message != "INVALID_ID":
                for i in current_message:
                    nextline[header_list.index(str(i))]=str(current_message[i])
            if time == last_time:
                continue
            elif flag_second_line==True:
                flag_second_line = False
                print("Second Line")
                continue
            elif time != last_time:
                # write our line to file
                # clear it out and begin putting new values in it
                last_time = time
                nextline[header_list.index("Time")]=raw_time
                outfile2.write(",".join(nextline) + "\n")
                nextline = [""] * len(header_list)
    print("These IDs not found in DBC: " +str(unknown_ids))
    infile.close()
    outfile.close()
    outfile2.close()
    return

def parse_folder():
    '''
    @brief: Locates Raw_Data directory or else throws errors. Created Parsed_Data directory if not created.
            Calls the parse_file() function on each raw CSV and alerts the user of parsing progress.
    @input: N/A
    @return: N/A
    '''

    # Stop attempting to parse if Raw_Data is not there.
    if not os.path.exists("Raw_Data"):
        print("FATAL ERROR: Raw_Data folder does not exist. Please move parser.py or create Raw_Data folder.")
        sys.exit(0)

    # Stop attempting to parse if DBC folder is not there.
    if not os.path.exists("DBC_Files"):
        print("FATAL ERROR: DBC Files folder does not exist. Please move parser.py or create Raw_Data folder.")
        sys.exit(0)

    # Creates Parsed_Data folder if not there.
    if not os.path.exists("Parsed_Data"):
        os.makedirs("Parsed_Data")
        # Creates Parsed_Data folder if not there.
    if not os.path.exists("Better_Parsed_Data"):
        os.makedirs("Better_Parsed_Data")
    # Generate the main DBC file object for parsing
    dbc_file = get_dbc_files()
    # Loops through files and call parse_file on each raw CSV.
    for file in os.listdir("Raw_Data"):
        filename = os.fsdecode(file)
        if filename.endswith(".CSV") or filename.endswith(".csv"):
            parse_file(filename,dbc_file)
            print("Successfully parsed: " + filename)
        else:
            continue

    return 

########################################################################
########################################################################
# Parsed Data CSV to MAT struct Code Section
########################################################################
########################################################################

"""
@Author: Sophia Smith + Bo Han Zhu
@Date: 2/11/2022
@Description: Takes a Parse_Data folder of CSVs and outputs a .mat struct for plotting.

create_mat():
    read_files() --> create_dataframe(csv_files) --> get_time_elapsed(frames_list) --> create_struct(frames_list1) --> transpose_all(struct1)

"""

import os
import re
import pandas as pd
import scipy.io
import numpy as np
import dateutil.parser as dp
from os import listdir
from os.path import isfile, join
from datetime import datetime
from scipy.io import savemat


def read_files():
    '''
    @brief: Reads parsed data files from Parsed_Data folder and returns a 
            list of file paths (as strings)
    @input: None
    @return: None
    '''
    try:
        path_name = 'Parsed_Data'

        file_path = []
        file_count = 0
        for root, dirs, files in os.walk(path_name, topdown=False):
            for name in files:
                if ".CSV" in name or ".csv" in name:
                    fp = os.path.join(root, name)
                    file_path.append(fp)
                    file_count += 1
    except:
        print('FATAL ERROR: Process failed at step 1.')
        sys.exit(0)

    print('Step 1: found ' + str(file_count) + ' files in the Parsed_Data folder')
    return file_path

def create_dataframe(files = []):
    '''
    @brief: Reads parsed data file and creates a pandas dataframe.
            Each row is formatted to work with the Matlab parser. 
    @input: A list of files
    @return: A dataframe list
    '''
    try:
        df_list = []
        for f in files:
            df = pd.read_csv(f)
            df_list.append(df)
    except:
        print('FATAL ERROR: Process failed at step 2.')
        sys.exit(0)

    print('Step 2: created dataframes')

    return df_list

def get_time_elapsed(frames = []):
    '''
    @brief: Calculated the elapsed time for each label based on a baseline
    @input: A dataframe list
    @ouput: An updated dataframe list with elapsed times
    '''
    skip = 0
    df_list = []
    start_time = 0
    set_start_time = True # boolean flag: we only want to set the start time once, during the first (i.e. earliest) CSV
    try:
        for df in frames:
            skip += 1
            timestamps = [dp.isoparse(x) for x in df['time']]
            if(len(timestamps) != 0):
                
                if set_start_time:
                    start_time = min(timestamps)
                    set_start_time = False # don't set start time again this run

                last_time = -1 # sometimes the Teensy has a slight ms miscue where it jumps back 1 sec on a second change, we must address it here
                time_delta = []
                for x in timestamps:
                    current_time = (x - start_time).total_seconds() * 1000
                    if current_time < last_time:
                        current_time += 1000 # add one second on a second switch miscue
                    time_delta.append(current_time)
                    last_time = current_time

                df['time_elapsed'] = pd.Series(time_delta)
                df_list.append(df)
            else:
                if DEBUG: print("Frame " + skip + "was skipped in elapsed time calculation.")
                continue
    except:
        print('FATAL ERROR: Process failed at step 3.')
        sys.exit(0)

    print('Step 3: calculated elapsed time')
    return df_list

def create_struct(frames = []):
    '''
    @brief: Formats dataframe data to work with the Matlab parser. 
    @input: A dataframe of the original CSV with elapsed times
    @return: A dictionary of times and values for each label
    '''
    
    struct = {}
    all_labels = []

    # Need to average out all values under one timestamp
    last_time = {}
    same_time_sum = {}
    same_time_count = {}

    try:
        for df in frames:
            labels = df['label'].unique()
            df = df[pd.to_numeric(df['value'], errors='coerce').notnull()]

            for label in labels:
                df_label = df[df['label'] == label]
                df_new = df_label[['time_elapsed', 'value']].copy()
                rows = df_new.values.tolist()

                for i in range(len(rows)):
                    if label in all_labels:
                        # Do not add to struct if the time is the same, instead add to tracking dictionaries
                        if last_time[label] == float(rows[i][0]):
                            # Update tracking dictionaries
                            same_time_sum[label] = same_time_sum[label] + float(rows[i][1])
                            same_time_count[label] = same_time_count[label] + 1
                        else:
                            # Add tracking dictionaries' values to struct
                            struct[label][0].append(last_time[label])
                            struct[label][1].append(same_time_sum[label] / same_time_count[label])

                            # Reset all tracking dictionaries
                            last_time[label] = float(rows[i][0])
                            same_time_sum[label] = float(rows[i][1])
                            same_time_count[label] = 1
                    else:
                        struct[label] = [[float(rows[i][0])], [float(rows[i][1])]]
                        all_labels.append(label)
                        last_time[label] = float(rows[i][0])
                        same_time_sum[label] = float(rows[i][1])
                        same_time_count[label] = 1

    except:
        print('FATAL ERROR: Process failed at step 4.')
        sys.exit(0)

    print('Step 4: created struct')
    return struct

def transpose_all(struct):
    '''
    @brief: Helper function to transfer 2xN array into Nx2 array for dataPlots
    @input: A dictionary of multiple 2xN arrays
    @return: A dictionary of those 2xN arrays transposed as Nx2 arrays
    '''
    for label in struct:
        struct[label] = np.array(struct[label]).T
    return struct

def create_mat():
    '''
    @brief: Entry point to the parser to create the .mat file
    @input: N/A
    @return: N/A
    '''
    print("Step 0: starting...")
    csv_files = read_files()
    frames_list = create_dataframe(csv_files)
    frames_list1 = get_time_elapsed(frames_list)
    struct1 = create_struct(frames_list1)
    struct2 = transpose_all(struct1)

    try:
        savemat('output.mat', {'S': struct2}, long_field_names=True)
        print('Saved struct in output.mat file.')
    except:
        print('FATAL ERROR: Failed to create .mat file')


