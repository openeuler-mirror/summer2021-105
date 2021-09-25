# Copyright (c) 2021 Huawei Technologies Co.,Ltd. All rights reserved.
#
# StratoVirt is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan
# PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http:#license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
"""global resources"""

import threading
import random
from subprocess import run
from subprocess import CalledProcessError
from utils.config import CONFIG
from utils.utils_network import generate_random_name, generate_random_mac
from utils.decorators import Singleton


class NetworkResource(Singleton):
    """Network resource"""
    tap_cmd = "ip"

    def __init__(self, bridge=CONFIG.bridge_name, nets_num=CONFIG.nets_num,
                 ip_3rd=CONFIG.ip_3rd, ip_prefix=CONFIG.ip_prefix,
                 dhcp_lower_limit=CONFIG.dhcp_lower_limit, dhcp_top_limit=CONFIG.dhcp_top_limit,
                 static_ip_lower_limit=CONFIG.static_ip_lower_limit, netmasklen=CONFIG.netmasklen,
                 static_ip_top_limit=CONFIG.static_ip_top_limit, netmask=CONFIG.netmask):
        self.bridge = bridge
        self.ip_3rd = ip_3rd
        self.ip_prefix = ip_prefix
        self.dhcp_lower_limit = dhcp_lower_limit
        self.dhcp_top_limit = dhcp_top_limit
        self.ipaddr = "%s.%s.1" % (self.ip_prefix, str(self.ip_3rd))
        self.static_ip_range = list(range(static_ip_lower_limit, static_ip_top_limit))
        self.netmasklen = netmasklen
        self.netmask = netmask
        self.lock = threading.Lock()
        self.ip_resources = dict()
        self.nets_num = nets_num
        self.cmd_dict = {
            "create_dnsmasq": "ps -ef | grep dnsmasq | grep -w %s",
            "alloc_ipaddr":  "dnsmasq --no-hosts --no-resolv --strict-order --bind-interfaces" \
                              "--interface=%s --except-interface=lo --leasefile-ro " \
                              "--dhcp-range=%s,%s",
            "link_tap": "brctl addif %s %s && ip link set %s up",
            "unlink_tap": "ip link set %s down 2>/dev/null; brctl delif %s %s 2>/dev/null;"
        }

    def check_env(self):
        """Check dnsmasq process is running normal"""
        # create bridge if it does not exist
        run("brctl show %s || brctl addbr %s" % (self.bridge, self.bridge), shell=True, check=True)

        run("ifconfig %s up" % self.bridge, shell=True, check=True)

        for index in range(self.nets_num):
            ipaddr = "%s.%s.1" % (self.ip_prefix, str(self.ip_3rd + index))
            run("ip addr add %s/%s dev %s" % (ipaddr, self.netmasklen, self.bridge),
                shell=True, check=False)

        # create dnsmasq to alloc ipaddr if it's not running
        _cmd = self.cmd_dict["create_dnsmasq"] % self.bridge
        _result = run(_cmd, shell=True, check=True)
        iprange_low = "%s.%s.%s" % (self.ip_prefix, str(self.ip_3rd), str(self.dhcp_lower_limit))
        iprange_high = "%s.%s.%s" % (self.ip_prefix, str(self.ip_3rd), str(self.dhcp_top_limit))
        if _result.returncode != 0:
            _cmd = self.cmd_dict["alloc_ipaddr"] % (self.bridge, iprange_low, iprange_high)
            _result = run(_cmd, shell=True, check=True)
            return not bool(_result.returncode)

        return True

    def create_tap(self, tapname):
        """create a tap device to vm, and link tap to bridge"""
        try:
            _cmd = "ip tuntap add %s mode tap && " % (tapname) + \
                    self.cmd_dict["link_tap"] % (self.bridge, tapname, tapname)
            run(_cmd, shell=True, check=True)
        except CalledProcessError:
            _cmd = "tunctl -t %s && " % (tapname) + \
                    self.cmd_dict["link_tap"] % (self.bridge, tapname, tapname)
            run(_cmd, shell=True, check=True)
            NetworkResource.tap_cmd = "tunctl"

    def generator_tap(self, generate_tap=True):
        """
        Generator a tap and a mac device

        Returns:
            {"name": tapname, "mac": mac}
        """
        self.check_env()
        tapname = generate_random_name()

        if generate_tap:
            self.create_tap(tapname)

        mac = generate_random_mac()
        return {"name": tapname, "mac": mac}

    def add_to_bridge(self, tapname):
        """Add tap device to bridge"""
        _cmd = "ip link show %s && " % (tapname) + \
                self.cmd_dict["link_tap"] % (self.bridge, tapname, tapname)
        run(_cmd, shell=True, check=True)

    def clean_tap(self, tapname): 
        """Clean tap device from host"""
        if NetworkResource.tap_cmd == "tunctl":
            _cmd = self.cmd_dict["unlink_tap"] % (tapname, self.bridge, tapname) + \
                    "tunctl -d %s 2>/dev/null" % (tapname)
        else:
            _cmd = self.cmd_dict["unlink_tap"] % (tapname, self.bridge, tapname) + \
                    "ip tuntap del %s mode tap 2>/dev/null" % (tapname)
        run(_cmd, shell=True, check=False)
        with self.lock:
            if tapname in self.ip_resources:
                static_index = int(str(self.ip_resources[tapname]["ipaddr"]).split(".")[-1])
                self.static_ip_range.append(static_index)
                del self.ip_resources[tapname]

    def alloc_ipaddr(self, tapname, index=0):
        """
        Alloc an static ip address

        Returns:
            {"ipaddr": xxx, "netmask": xxx, "netmasklen": xxx, "gateway": xxx}
        """
        with self.lock:
            if tapname in self.ip_resources:
                return self.ip_resources[tapname]

            if not self.static_ip_range:
                return None
            static_index = random.choice(self.static_ip_range)
            self.static_ip_range.remove(static_index)
            _temp = {"ipaddr": "%s.%s.%s" % (self.ip_prefix, str(self.ip_3rd + index), str(static_index)),
                     "netmask": self.netmask,
                     "netmasklen": self.netmasklen,
                     "gateway": self.ipaddr}
            self.ip_resources[tapname] = _temp
            return self.ip_resources[tapname]


class VsockResource(Singleton):
    """Vsock resource"""
    def __init__(self):
        self.lock = threading.Lock()
        self.used_cids = set()

    @staticmethod
    def init_vsock():
        """Init vsock"""
        if run("lsmod | grep vhost_vsock", shell=True, check=False).returncode != 0:
            if run("modprobe vhost_vsock", shell=True, check=False).returncode != 0:
                return False

        return True

    @staticmethod
    def find_contextid():
        """Find uniq context ID"""
        first_cid = 3
        max_cid = 10000
        rand_cid = random.choice(range(first_cid, max_cid))
        return rand_cid


NETWORKS = NetworkResource()
VSOCKS = VsockResource()
