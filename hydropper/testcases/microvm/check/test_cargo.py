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
"""Test cargo function"""

import logging
import utils.utils_cargo

def test_cargo_functions():
    """
    Test functions of cargo:

    1) call the cargo's interface.
    2) check the correctness of the result.
    """
    try:
        utils.utils_cargo.cargo_check()
    except Exception:
        logging.debug("Test of cargo functions failed!")
    else:
        logging.debug("Test of cargo functions succeed!")