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
"""Test microvm memory check"""

import logging
import pytest
import time

@pytest.mark.acceptance
def test_memory_check(microvm):
    """
    Test a normal microvm's function of checking memory:

    1) Launch to test_vm.
    2) run the function of checking memory for some time.
    3) print the memory usage exceeded message.
    """
    test_vm = microvm
    test_vm.launch()
    time.sleep(30)
    exceeded_mes = test_vm.memory_check.get_exceeded_event()
    assert exceeded_mes is not None
    test_vm.shutdown()
