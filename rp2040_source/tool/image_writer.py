import serial.tools.list_ports
import time
from image_converter import *
dos_com = ""
vid = "2E8A"
pid = "0003"
def list_serial_ports():
    global dos_com
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
    else:
        print("Available serial ports:")
        for port, desc, hwid in sorted(ports):
            vid_pid_info = parse_hwid(hwid)
            print(f"{port}: (VID: {vid_pid_info['vid']}, PID: {vid_pid_info['pid']})")
            if vid == vid_pid_info['vid'] and pid == vid_pid_info['pid']:
                dos_com = port
                print(f"found dos device {dos_com}")
                sendImage()

def parse_hwid(hwid):
    # Example of a hardware ID: 'USB VID:PID=2341:0043 SER=12345 LOCATION=1-1.2:1.0'
    vid_pid_str = hwid.split('VID:PID=')[1].split(' ')[0]
    vid, pid = vid_pid_str.split(':')
    return {'vid': vid, 'pid': pid}
def send_byte_array(ser, byte_array):
    try:
        # Open the serial port
        # Ensure that the port is open
        if ser.is_open:
            ser.write(byte_array)
            ser.flush()
            print("Byte array sent successfully.")
        else:
            print(f"Error: Could not open.")
    
    except serial.SerialException as e:
        print(f"Error: {e}")
def sendImage():
    input_image_path = 'qr.png'
    data = resize_and_convert_to_binary_grayscale(input_image_path,new_size=(296,128))
    print(f"open device {dos_com}")
    ser = serial.Serial(dos_com, baudrate=4000000, timeout=0.01)
    data = bytearray(data)
    lenOfData = len(data)
    header = [0x00,0x01,lenOfData>>8,lenOfData & 0x00ff]
    header = bytearray(header)
    payload = header + data
    send_byte_array(ser, payload)
    run_command = [0x00,0x02,0x00]
    send_byte_array(ser,run_command)
    # Close the serial port
    ser.close()
if __name__ == "__main__":
    list_serial_ports()
