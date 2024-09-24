import argparse
from collections import defaultdict

# creates a dictionary to identify port-protocol corresponding to a tag
tag_dict = defaultdict(list)
tag_count = dict()
def read_tag_lookup(lookup_file):
    with open(lookup_file, 'rt') as lkp:
        for line in lkp:
            line = line.strip()
            # check for empty lines
            if line:
                lkp_list = line.split(",")
                if(lkp_list[0].isdigit()):
                    lkp_list[0] = lkp_list[0].strip()
                    lkp_list[1] = lkp_list[1].strip()
                    lkp_list[2] = lkp_list[2].strip()
                    tag_dict[lkp_list[2]].append(lkp_list[0]+'-'+lkp_list[1])
                    tag_count[lkp_list[2]] = 0


# A dictionary, mapping protocol numbers to names, it is not exhaustive
protocol_dict = dict()
def create_protocol_dict():
    protocol_dict[0] = "hopopt"
    protocol_dict[1] = "icmp"
    protocol_dict[2] = "igmp"
    protocol_dict[3] = "ggp"
    protocol_dict[4] = "ipv4"
    protocol_dict[5] = "st"
    protocol_dict[6] = "tcp"
    protocol_dict[7] = "cbt"
    protocol_dict[8] = "egp"
    protocol_dict[17] = "udp"


def read_log(input_file):
    port_protocol_count = dict()
    with open(input_file, 'rt') as inp:
        # The for loop reads line by line and ensures that the program does not crash when reading a large log file
        for line in inp:
            line = line.strip()
            # check for empty lines
            if line:
                line = line.split(' ')
                # Check for version 2
                if line[0] != "2":
                    continue
                # Do not consider if dstport or protocol does not exist in log
                if(line[6] != "-" and line[7] != "-"):
                    key = line[6]+"-"+protocol_dict[int(line[7])]
                    num = 0
                    if key in port_protocol_count.keys():
                        num = port_protocol_count[key]
                    port_protocol_count[key] = num+1

    untagged = 0
    tag_found = False
    for key in port_protocol_count.keys():
        for tag in tag_dict.keys():
            if key in tag_dict[tag]:
                tag_count[tag] += port_protocol_count[key]
                tag_found = True
                break
        if not tag_found:
            untagged += 1

    '''
    print(port_protocol_count)
    print("-----------------------------")
    print(tag_count)
    print("-----------------------------")
    print(untagged)
    '''

    # Write data to output file - output.txt
    with open("./output.txt", 'wt') as out:
        out.write("Tag Counts: \n")
        out.write("Tag,Count\n")
        for tag in tag_count.keys():
            if tag_count[tag] > 0:
                data = tag + "," + str(tag_count[tag]) + "\n"
                out.write(data)
        data = "Untagged" + "," + str(untagged) + "\n"
        out.write(data)
        
        out.write("\n")
        out.write("Port/Protocol Combination Counts: \n")
        out.write("Port,Protocol,Count\n")
        for key in port_protocol_count.keys():
            port = key.split('-')[0]
            protocol = key.split('-')[1]
            data = port + "," + protocol + "," + str(port_protocol_count[key]) + "\n"
            out.write(data)
                

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="./log.txt", nargs="?",
        help="Full path of input log file.")
    parser.add_argument("--lookup", type=str, default="./lookup.txt", nargs="?",
        help="Full path of lookup file.")
    
    args = parser.parse_args()
    input_file = args.input
    lookup_file = args.lookup

    read_tag_lookup(lookup_file)
    create_protocol_dict()
    read_log(input_file)
