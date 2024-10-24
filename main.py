import requests
import json
import sys

API = ["***"] #вместо *** укажите свой ключ API, полученный после регистрации на securitytrails.com


def get_subdomains(domain):
    headers = {"apikey": API[-1], #fix 0
               "children_only": "false",
               "include_inactive": "false"}
    response = requests.get(str("https://api.securitytrails.com/v1/domain/" + str(domain) + "/subdomains"), headers=headers)

    with open("m.txt", "w") as f:
        f.write(response.text)


if __name__ == '__main__':
    domain = sys.argv[1]
    get_subdomains(domain)
    subdomains = ''
    with open("m.txt", "r") as rf:
        subdomains = json.load(rf)
    ips = open("ips.txt", "w")
    adrs = open("adrs.txt", "w")
    for i, sd in enumerate(subdomains["subdomains"]):
        # sd = json.loads(response.text)["subdomains"][0]
        apikey = {"apikey": API[i%len(API)]}
        rsp = requests.get(str("https://api.securitytrails.com/v1/domain/" + sd + "." + domain), headers=apikey)
        data = json.loads(rsp.text)
        # print(data)
        if data["current_dns"]["a"]:
            a = []
            for j in range(len(data["current_dns"]["a"]["values"])):
                a.append(data["current_dns"]["a"]["values"][j]["ip"])
            b = data["hostname"]
            ip = str(str(b) + ":" )
            for i in a:
                ip = ip + i +" "
                adrs.write(str(i + '\n'))
            ips.write(ip + '\n')
        else:
            ips.write(str(data["hostname"] + '\n'))
