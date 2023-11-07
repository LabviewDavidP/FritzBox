from time import sleep as sleep
from itertools import count
from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzServiceError

from fritzconnection.lib.fritzstatus import FritzStatus


def get_wlan_status():
    status = []
    action = "GetInfo"
    for n in count(1):
        service = f"WLANConfiguration{n}"
        try:
            result = fc.call_action(service, action)
        except FritzServiceError:
            break
        status.append((service, result))
    return status


def get_compact_wlan_status():
    keys = ("NewSSID", "NewChannel", "NewStatus")
    return [(service, {key[3:]: status[key] for key in keys})
            for service, status in get_wlan_status()
            ]


def wlan_status():
    for service, status in get_compact_wlan_status():
        print(f"{service}: {status}")


def tester():
    print(f"Version:   {fc.system_version}\n"
          f"Model-Name: {fc.modelname}\n"
          f"Address:   {fc.address}\n"
          f"Port:      {fc.port}\n")
    # fc.reconnect()


if __name__ == "__main__":
    # define variables
    address: str
    user: str
    address, user = "192.168.178.1", "fritz"
    fc = FritzConnection(use_cache=True,
                         address=address,
                         # user=user,
                         cache_format="json",
                         cache_directory="D:\\")

    DSLInterfaceConfig = fc.call_action("WANDSLInterfaceConfig", "GetStatisticsTotal")
    print(DSLInterfaceConfig)

    DSLInterfaceConfig_GetInfo = fc.call_action("WANDSLInterfaceConfig", "GetInfo")
    print(DSLInterfaceConfig_GetInfo)
    print(DSLInterfaceConfig_GetInfo["NewDownstreamPower"])
    print(DSLInterfaceConfig_GetInfo.get("NewATURCountry"))

    fs = FritzStatus(use_cache=True,
                     address=address,
                     # user=user,
                     cache_format="json", cache_directory="D:\\")
    i: int = 0
    i_max: int = 3
    while i < i_max:
        print(fs.str_transmission_rate)
        i = i + 1
        sleep(0.1)

    link = fs.is_linked
    print(link)

    tester()
    wlan_status()

    #DSL_Link_C1 = fc.call_action("WANDSLLinkC1", "GetInfo")
    #print(DSL_Link_C1)



# fc.reconnect()  # get a new external ip from the provider
