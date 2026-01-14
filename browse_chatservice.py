from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class AllServicesListener(ServiceListener):
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"[+] Service type found: {name} ({type_})")

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"[*] Service updated: {name} ({type_})")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"[-] Service removed: {name} ({type_})")


def main() -> None:
    zc = Zeroconf()
    listener = AllServicesListener()

    # change if necessary
    service_type = "_chatservice._tcp.local."

    browser = ServiceBrowser(zc, service_type, listener)

    try:
        input("Browsing for ALL mDNS service types\nEnter to exit.\n")
    finally:
        zc.close()


if __name__ == "__main__":
    main()
