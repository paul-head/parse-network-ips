import csv
from commonregex import CommonRegex
from socket import inet_ntoa, inet_aton

lst = []

with open('ips.csv', 'r') as csvfile:
    lines = csvfile.readlines()

    for line in lines:
        parsed_text = CommonRegex(line)
        lst.extend(parsed_text.ips)


final_lst = list(map(inet_ntoa, sorted(map(inet_aton, lst))))


for ip in final_lst:
    print(ip)