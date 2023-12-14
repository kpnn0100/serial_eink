import usb.core

# Find all USB devices
devices = usb.core.find(find_all=True)

# Iterate through the list of devices
for device in devices:
    print("Device ID:", device.idVendor, ":", device.idProduct)
    print("Device Class:", device.bDeviceClass)
    print("Device Subclass:", device.bDeviceSubClass)
    print("Device Protocol:", device.bDeviceProtocol)
    print("Max Packet Size for Endpoint 0:", device.bMaxPacketSize0)
    print("Number of Configurations:", device.bNumConfigurations)
    print("\n---------------------------\n")
