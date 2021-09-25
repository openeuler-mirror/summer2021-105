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
"""monitor vm memory usage"""

import time
import logging
from subprocess import run
from subprocess import CalledProcessError
from subprocess import PIPE
from monitor import monitor_info
from monitor import MEMORY_USAGE_EXCEEDED


class MemorySupervisor(monitor_info.MonitorInfo):
    """Checks vm memory usage, and logs or reports error"""

    def __init__(self, pid, isDotter=True, max_memory=4096):
        """Max memory default value is 4096Kib"""
        _monitor_type = MEMORY_USAGE_EXCEEDED
        _monitor_cycle = 10
        super(MemorySupervisor, self).__init__(_monitor_type,
                                                _monitor_cycle,
                                                "vm")
        self._pid = pid
        self.isDotter = isDotter
        self.max_memory = max_memory
        # guest memory top limit is 131072(128M)
        self.guest_memory_limit = 131072
        self.exceeded_event_list = []

    def update_pid(self, pid):
        """Update vm pid"""
        self._pid = pid

    def update_max_memory(self, max_memory):
        """Update vm max_memory"""
        self.max_memory = max_memory

    def get_exceeded_event(self):
        """Output memory usage exceeded event info"""
        return self.exceeded_event_list 

    def run(self):
        """Run monitor"""
        self.set_state('running')
        while self._enable and self._state != 'stop':
            self.supervise()
            time.sleep(self.monitor_cycle)

    def supervise(self):
        """
        Check memory usage exceeded or not(overwrite to the monitorinfo)
        """
        pmap_cmd = "pmap -xq {}".format(self._pid)
        mem_total = 0
        try:
            pmap_out = run(
                pmap_cmd, 
                shell=True, 
                check=True,
                stdout=PIPE
            ).stdout.decode('utf-8').split("\n")
        except CalledProcessError:
            return False
        # delte useless lines which doesn't contain memory related information
        pmap_out = pmap_out[1:-1]
        pmap_out_delta = []
        for line in range(len(pmap_out)):
            pmap_out_i = pmap_out[line].split()
            if int(pmap_out_i[1]) > self.guest_memory_limit:
                # this is the guest's memory region
                continue
            pmap_out_delta.append(pmap_out_i)
        mem_total = sum(int(pmap_out_delta[i][2]) for i in range(len(pmap_out_delta)))

        if self.isDotter:
            logging.debug("mem_total:%s" % mem_total)
            self.exceeded_event_list.append("mem_total:%s" % mem_total)

        if mem_total >= self.max_memory:
            logging.warning("memory usage is %s, it's greater than %s" % (mem_total, self.max_memory))
            exceeded = True
            level = "error"
            err_msg = "memory usage is %s, it's greater than %s" % (mem_total, self.max_memory)
            self.exceeded_event_list.append(err_msg)
            self.enqueue(level, err_msg)
            return exceeded, level, err_msg