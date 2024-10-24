import shodan
import sys
import prettytable as pt

# Configuration
API_KEY = "***" #вместо *** укажите ключ API, полученный после регистрации на shodan.io

if __name__ == "__main__":
    api = shodan.Shodan(API_KEY)
    with open("adrs.txt", "r") as adrs:
        table = pt.PrettyTable()
        table.field_names = ["IP", "Organization", "Port", "Product", "Version"]
        f = adrs.readlines()
        g = [i.strip() for i in f]
        ips = set(g)
        for ip in ips:
            try:
                a = api.host(ip)
                print("Organization:", a['isp'], "\n")

                for i in range(len(a['ports'])):
                    print("Port ", a['ports'][i])
                    for service in a['data']:
                        if service['port'] == a['ports'][i]:
                            new_row: list = [ip, a['isp'], a['ports'][i]]
                            if 'product' in service:
                                print("Product: ", service['product'])
                                new_row.append(service['product'])
                            else:
                                print("Product neizvesten")
                                new_row.append("Unknown")
                            if 'version' in service:
                                print("Version:", service['version'], "\n")
                                new_row.append(service['version'])
                            else:
                                print("Versiya neizvestna\n")
                                new_row.append("Unknown")
                            print("Data:", service['data'])
                            table.add_row(new_row)
            except Exception as e:
                if e.args[0] == 'No information available for that IP.':
                    continue
                else:
                    print('Error: %s' % e)
                    sys.exit(1)
        with open("shodan_out.txt", 'w') as sh:
            row = table.get_string()
            sh.write(row)
            sh.write('\n')