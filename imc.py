from imcsdk.imchandle import ImcHandle
import regex


# filename = '/Users/your_user_name/Desktop/test.csv'
filename = 'cimc.txt'

file = open(filename, "r")

o = file.read()

ip1 = regex.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", o)
hosts = ip1
for host in hosts:
    print("host: ", host)

    try:
        handle = ImcHandle(host, "admin", "ciscopsdt")
        handle.login()

        handle.set_dump_xml()

        print(handle.imc)


        # print("firmware: ", handle.query_dn("sys/rack-unit-1/mgmt/fw-system"))

        firmware_query = handle.query_dn("sys/rack-unit-1/mgmt/fw-system")
        name_query = handle.query_dn("sys/rack-unit-1")
        hostname_query = handle.query_dn("sys")
        # hostname_query = handle.query_classid(class_id="topSystem",need_response=True) #can get the same output through handle.imc()

        print(hostname_query)

        toCSV = [["HostIP", host], ["Product Name", name_query.name], ["Hostname", handle.imc], ["fw_version", firmware_query.version, "\n"]]

        with open('firmware.csv', 'a') as csvFile:
            for row in toCSV:
                for column in row:
                    csvFile.write('%s;' % column)
                csvFile.write('\n')

        print("Writing complete")


        handle.set_dump_xml()
        handle.logout()

    except Exception as err:
        print("Exception:", str(err))
        import traceback, sys
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

file.close()
