"""
  python mdns_cli.py --all-types
  python mdns_cli.py --type _chatservice._tcp
  python mdns_cli.py --type _http._tcp --resolve
  python mdns_cli.py --all-types --follow-types --resolve

"""

import argparse
import socket
import sys
import time
from typing import Dict, Optional, Set

from zeroconf import ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf


def normalize_type(t: str) -> str:
    t = t.strip()
    if not t:
        raise ValueError("Empty service type")
    if not t.endswith("."):
        t += "."
    if ".local." not in t:
        #_http._tcp. or _http._tcp
        t = t.rstrip(".") + ".local."
    return t


def decode_properties(props: Dict[bytes, bytes]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for k, v in (props or {}).items():
        try:
            ks = k.decode("utf-8", errors="replace")
        except Exception:
            ks = repr(k)
        try:
            vs = v.decode("utf-8", errors="replace")
        except Exception:
            vs = repr(v)
        out[ks] = vs
    return out


def format_info(info: ServiceInfo) -> str:
    addrs = []
    try:
        addrs = list(info.parsed_scoped_addresses())
    except Exception:
        for a in info.addresses:
            addrs.append(socket.inet_ntoa(a))
    props = decode_properties(info.properties)
    return (
        f"    server:    {info.server}\n"
        f"    addresses: {addrs}\n"
        f"    port:      {info.port}\n"
        f"    weight/prio: {info.weight}/{info.priority}\n"
        f"    txt:       {props}"
    )


class TypeListener(ServiceListener):
    # _services._dns-sd._udp.local. 
    def __init__(
        self,
        zc: Zeroconf,
        follow_types: bool,
        resolve_instances: bool,
        started_browsers: Set[str],
        type_browsers: Dict[str, ServiceBrowser],
        verbose: bool,
    ):
        self.zc = zc
        self.follow_types = follow_types
        self.resolve_instances = resolve_instances
        self.started_browsers = started_browsers
        self.type_browsers = type_browsers
        self.verbose = verbose

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        # _http._tcp.local.
        print(f"[TYPE +] {name}")
        if self.follow_types:
            stype = name 
            if stype not in self.started_browsers:
                self.started_browsers.add(stype)
                listener = InstanceListener(self.zc, stype, self.resolve_instances, self.verbose)
                self.type_browsers[stype] = ServiceBrowser(self.zc, stype, listener)
                if self.verbose:
                    print(f"    -> now browsing instances of {stype}")

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        if self.verbose:
            print(f"[TYPE *] {name}")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"[TYPE -] {name}")


class InstanceListener(ServiceListener):
    # _http._tcp.local.

    def __init__(self, zc: Zeroconf, service_type: str, resolve: bool, verbose: bool):
        self.zc = zc
        self.service_type = service_type
        self.resolve = resolve
        self.verbose = verbose

    def _resolve_and_print(self, name: str) -> None:
        info = self.zc.get_service_info(self.service_type, name, timeout=2000)
        if info:
            print(format_info(info))
        else:
            print("    (resolve failed / no info yet)")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"[INST +] {name} ({type_})")
        if self.resolve:
            self._resolve_and_print(name)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        if self.verbose:
            print(f"[INST *] {name} ({type_})")
        if self.resolve:
            self._resolve_and_print(name)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"[INST -] {name} ({type_})")


def main() -> int:
    p = argparse.ArgumentParser(description="Avahi-like mDNS/DNS-SD browser using python-zeroconf")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--all-types", action="store_true", help="List service types (like avahi-browse -a)")
    g.add_argument("--type", dest="service_type", help="Browse a specific service type, e.g. _http._tcp or _chatservice._tcp")

    p.add_argument("--follow-types", action="store_true",
                   help="When using --all-types, also browse instances of each discovered type")
    p.add_argument("--resolve", action="store_true",
                   help="Resolve instances to IP/port/TXT (like avahi-browse -r)")
    p.add_argument("--verbose", action="store_true", help="Print update events too")
    p.add_argument("--seconds", type=int, default=0,
                   help="Run for N seconds then exit (0 = wait for Enter)")

    args = p.parse_args()

    zc = Zeroconf()
    started_browsers: Set[str] = set()
    type_browsers: Dict[str, ServiceBrowser] = {}

    try:
        if args.all_types:
            # browse all service types
            meta_type = "_services._dns-sd._udp.local."
            tlistener = TypeListener(
                zc=zc,
                follow_types=args.follow_types,
                resolve_instances=args.resolve,
                started_browsers=started_browsers,
                type_browsers=type_browsers,
                verbose=args.verbose,
            )
            ServiceBrowser(zc, meta_type, tlistener)
            print("Browsing ALL service types (_services._dns-sd._udp.local.)")
            if args.follow_types:
                print("Following discovered types and browsing their instances")
        else:
            stype = normalize_type(args.service_type)
            ilistener = InstanceListener(zc, stype, args.resolve, args.verbose)
            ServiceBrowser(zc, stype, ilistener)
            print(f"Browsing instances of: {stype}")

        if args.seconds and args.seconds > 0:
            end = time.time() + args.seconds
            while time.time() < end:
                time.sleep(0.2)
        else:
            input("Press Enter to exit\n")

    finally:
        zc.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
