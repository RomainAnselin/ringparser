from heapq import nlargest
from heapq import nsmallest
import sys

# Check arguments
# (note 2 includes arg 0 which is this script!)
if len(sys.argv) == 2:
    filename=sys.argv[1]
else:
    print ("\n***",sys.argv[0], "***\n")
    print ('Incorrect number of arguments, please run script as follows:')
    print ('\n\n'+str(sys.argv[0])+' <Extract of one DC nodetool ring>')
    sys.exit(0)

token_dictionary = {}
with open(filename) as f:
    content = f.readlines()
    for line in content:
        if len(line.split()) == 8:
            token = line.split()[7]
            # print(token)
            ipaddress = line.split()[0]
            # print(ipaddress)
            params = {}
            params["ipaddress"]={"ipaddress":ipaddress}
            token_dictionary[token]=params["ipaddress"]

# print(token_dictionary)

token_list = []

for token in token_dictionary:
    token_list.append(token)

for i in range(0, len(token_list)):
    if (i == 0):
        minToken = -9223372036854775808
        maxToken = 9223372036854775808
        mydiff = abs (minToken - int(token_list[0])) + abs (maxToken - int(token_list[i-1]))
        token_dictionary[token_list[i]]["diff_to_next"] = mydiff
        token_dictionary[token_list[i]]["position_in_ring"] = i
    else:
        mydiff = int(token_list[i]) - int(token_list[i-1])
        # print(mydiff)
        diff_to_next = {"diff_to_next": mydiff}
        token_dictionary[token_list[i]]["diff_to_next"]=mydiff
        token_dictionary[token_list[i]]["position_in_ring"] = i

# print(token_dictionary)

ip_dict = {}

for token in token_dictionary:
    # print("the token difference is: ", token_dictionary[token]["diff_to_next"], " and IP is: ", token_dictionary[token]["ipaddress"])
    ip_dict[token_dictionary[token]["ipaddress"]] = {"total_token": 0}
    # print(ip_dict[token_dictionary[token]["ipaddress"]])

# print(ip_dict)

for token in token_dictionary:
    # print("the token difference is: ", token_dictionary[token]["diff_to_next"], " and IP is: ", token_dictionary[token]["ipaddress"])
    ip_dict[token_dictionary[token]["ipaddress"]]["total_token"] = int(ip_dict[token_dictionary[token]["ipaddress"]]["total_token"]) + int(token_dictionary[token]["diff_to_next"])

#print("----- IP dictionary -----\n" , ip_dict)

total_token = 0

for ip in ip_dict:
    # print("ip address", ip, "\thas\t", ip_dict[ip]["total_token"] , " tokens in total")
    total_token = total_token + ip_dict[ip]["total_token"]

position = 0

for ip in ip_dict:
    ip_dict[ip]["ratio"] = ip_dict[ip]["total_token"]/18446744073709551616
    ip_dict[ip]["position"] = position
    position = position + 1
    print("ip address", ip, "\thas\t", ip_dict[ip]["total_token"] , " tokens in total and a ratio of:\t", round(ip_dict[ip]["ratio"]*100,2))

# print("-----\n ip dictionary with position: " , ip_dict)

average_token_number = 18446744073709551616/len(ip_dict)

for ip in ip_dict:
    ip_dict[ip]["deviation"]=(ip_dict[ip]["total_token"]- average_token_number)/average_token_number


# print(ip_dict)

deviations = []

for ip in ip_dict:
    deviations.append(ip_dict[ip]["deviation"])

# print(min(deviations))

deviation_dict = {}

for ip in ip_dict:
    deviation_dict[ip] = ip_dict[ip]["deviation"]

# print(deviation_dict)


positions = []

for ip in ip_dict:
    deviations.append(ip_dict[ip]["position"])

position_dict = {}

for ip in ip_dict:
    position_dict[ip] = ip_dict[ip]["position"]

# print("ips to positions; ", position_dict)

ip_of_positons_dict = {v: k for k, v in position_dict.items()}

# print("positions to ips: ", ip_of_positons_dict)




print("min deviation per node: ", min(deviation_dict, key=deviation_dict.get), ":", deviation_dict[min(deviation_dict, key=deviation_dict.get)])
print("max deviation per node: ", max(deviation_dict, key=deviation_dict.get), ":", deviation_dict[max(deviation_dict, key=deviation_dict.get)])

ThreeHighest = nlargest(3, deviation_dict, key = deviation_dict.get)
ThreeLowest = nsmallest(3, deviation_dict, key = deviation_dict.get)

print("3 highest nodes")
for val in ThreeHighest:
   print(val, " : ", deviation_dict.get(val))

print("3 lowest nodes")
for val in ThreeLowest:
   print(val, " : ", deviation_dict.get(val))


# print(18446744073709551616 - total_token)
#
# print(ratios)
#
# print(int(18446744073709551616/len(ip_dict)))

ratio_dict = {}

for ip in ip_dict:
    ratio_dict[ip] = ip_dict[ip]["ratio"]

# print(ratio_dict)

rep_factor = 3


data_by_ip = {}

#calculate the amount of data held per node

# take the ration per node, add to that the ratio of the previous nodes until replication factor is reached

for ip in ip_dict:
    ip_ratio = 0
    for i in range (0, rep_factor):
        ip_ratio = ip_ratio + ratio_dict[ip_of_positons_dict[(position_dict[ip]-i)%len(ip_dict)]]
    data_by_ip[ip] = round(ip_ratio*100, 1)

'''
print("token ratio by ip: ", ratio_dict)
print("data held by ip with replication factor ", rep_factor, " : ", data_by_ip)

print("min ownership per node with RF factored in: ", min(data_by_ip, key=data_by_ip.get), ":", data_by_ip[min(data_by_ip, key=data_by_ip.get)])
print("max ownership per node with RF factored in: ", max(data_by_ip, key=data_by_ip.get), ":", data_by_ip[max(data_by_ip, key=data_by_ip.get)])
'''
