#!/usr/bin/env python3

#Matthew Wander
#networkFileRW.py
#GPA 8: Working With Files
#8/6/2023


#Try/except clause to import JSON module
try:
    import json
except:
    print('Error! Could not find JSON module!')

#Constraints
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111)? "
SORRY = "Sorry, that is not a valid IP address\n"
FILEROUTERS = 'equip_r.txt'
FILESWITCHES = 'equip_s.txt'
FILEUPDATED = 'updated.txt'
FILEINVALID = 'invalid.txt'

#Funct. to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")
#funct. to get valid IP addr.
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        #Prompt for new IP addr.
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets) ##Debug
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    
    #dictonaries
    ##Read the routers and addresses into the router dict.
    routers = {}
    try:
        with open(FILEROUTERS, 'r') as file:
            routers = json.load(file)
    except FileNotFoundError:
        print(f'{FILEROUTERS} not found!')
        
    #Read the switches and addresses into the switches dict.
    switches = {}
    try:
        with open(FILESWITCHES, 'r') as file:
            switches = json.load(file)
    except FileNotFoundError:
        print(f'{FILESWITCHES} not found!')

    #The updated dictionary holds the device name and new IP addr.
    updated = {}

    #List of bad IP addresses entered by user
    invalidIPAddresses = []

    #Accum. variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #Flags/Sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items():
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)


    while not quitNow:

        #funct. call to get valid device
        device = getValidDevice(routers, switches)

        if device == 'x':
            quitNow = True
            break

        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        if 'r' in device:
            routers[device] = ipAddress
            #print("routers", routers) ##Debug
        else:
            switches[device] = ipAddress
            #print("switches", switches) ##Debug

        devicesUpdatedCount += 1
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    #Summary upon completion of updates
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)
    #Write the updated devices and IP addresses to 'updated.txt'
    with open(FILEUPDATED, 'w') as file:
        json.dump(updated, file)
    print("Number of invalid addresses attempted:", invalidIPCount)
    #Write the invalid IP addresses to 'invalid.txt'
    with open(FILEINVALID, 'w') as file:
        json.dump(invalidIPAddresses, file)
#Top-level scope check
if __name__ == "__main__":
    main()




