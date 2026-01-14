import socket
from zeroconf import Zeroconf, ServiceInfo

def main() -> None:
    zc = Zeroconf()

    # change if necessary
    service_type = "_chatservice._tcp.local."
    service_name = "TestService._chatservice._tcp.local."

    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)

    info = ServiceInfo(
        type_=service_type,
        name=service_name,
        addresses=[socket.inet_aton(host_ip)],
        port=12345,
        properties={b"path": b"/"},
        server=f"{hostname}.local.",
    )

    print(f"Registering service {service_name} on {host_ip}:12345")
    zc.register_service(info)

    try:
        input("Service registered. Enter to unregister and exit\n")
    finally:
        print("Unregistering service")
        zc.unregister_service(info)
        zc.close()

if __name__ == "__main__":
    main()
