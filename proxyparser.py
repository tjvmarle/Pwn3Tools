# These headers are in Big Endian!
packetTypes = {"heartbeat": 0x0000,
               "pos": 0x6d76,
               "jump": 0x6a70,
               "fireball": 0x2a69}

headerTypes = {v: k for k, v in packetTypes.items()}

# Formatting for printing the packets

formatter = {"pos": (4, 8, 8, 8, 8, 4, 4),
             # header #posxy #posxy #faceAnglexy #faceAnglexz # #movedirection

             "jump": (4, 2, 10, 10, 8, 8, 4, 4),
             # header up/down(?) posxy posxy facexy facexy facez(?) jumpdirection

             "fireball": (4, 8, 8, 8, 8, 4, 10, 10, 8, 8),  # ...4:
             }

# Don't print these packets
ignorePrint = ("heartbeat",)
printFilter = list(packetTypes[x] for x in ignorePrint)
printOnly = ("pos",)

# Create additional packets for the server
injector_queue = []


def mod_packet(data):
    header = int.from_bytes(data[:2], "big")
    headerType = headerTypes[header] if header in headerTypes else "unknown"

    if headerType != "pos":
        return data

    x_pos = int.from_bytes(data[2:6][::-1], 'big')
    x_new = (x_pos + 256).to_bytes(4, 'big')

    new_data = data[0:2] + x_new[::-1] + data[6:]
    # print_packet("[g2s:2000]: ", new_data)

    return new_data


def big_to_little(bigEndian):
    littleEndian = ""
    while len(bigEndian) > 0:
        littleEndian += bigEndian[-2:]
        bigEndian = bigEndian[:-2]

    return littleEndian


def format_packet(data, printRanges):
    packet_string = data.hex()
    msg = ""

    while len(packet_string) > 0:
        for rangeVal in printRanges:
            bigEndString = packet_string[:rangeVal]
            msg += big_to_little(bigEndString) + " "

            packet_string = packet_string[rangeVal:]
        msg += "..." + packet_string
        break
    return msg


def print_packet(prefix, data):
    # TCP uses big endian, printing is done in little Endian
    header = int.from_bytes(data[:2], "big")

    if header in printFilter:
        return

    headerType = headerTypes[header] if header in headerTypes else "unknown"

    if printOnly and headerType not in printOnly:
        return

    if headerType in formatter:
        print(prefix + format_packet(data, formatter[headerType]))
    else:
        print(prefix + data.hex())

    return


def parse(data, port, origin):

    # Ignore server-side packets for now
    if port != 3333 and origin != "server":
        print_packet("[g2s:{}]: ".format(port), data)
        data = mod_packet(data)
        print_packet("[g2s:2000]: ", data)

    return data


def inject(proxies):
    print("pls inject")
    for proxy in proxies:
        print("Inject on port:", proxy.port)
        if proxy.g2p.connected:
            pass
            # for packet in injector_queue:
            #     proxy.g2p.server.sendall(packet)


def execute(cmd):
    print("cmd: [{}]".format(cmd))
