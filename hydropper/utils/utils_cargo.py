# StratoVirt is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan
# PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http:#license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
"""Some cargo fuctions"""

import logging
from subprocess import run
from subprocess import CalledProcessError

def cargo_check(quiet=False, path="/root/zld/stratovirt"):
    """
    It can be helpful for running a faster compile if you only need correctness checks.
    Precondition:Third party packages 'cargo check' need to be installed
    Args:
        quiet:whether no output printed to stdout
        path:execute the command under the path
    """
    _cmd = "cd %s && cargo check" % (path)
    if quiet:
        _cmd += " -q"
    
    try:
        res = run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo check failed!")

def cargo_clippy(quiet=False, path="/root/zld/stratovirt"):
    """
    Check the code specification and give the optimization scheme
    Precondition:Third party packages 'cargo clippy' need to be installed
    Args:
        quiet:whether no output printed to stdout
        path:execute the command under the path
    """
    _cmd = "cd %s && cargo clippy" % (path)
    if quiet:
        _cmd += " -q"
    
    try:
        run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo clippy failed!")

def cargo_fmt(all=False, quiet=False, verbose=False, path="/root/zld/stratovirt"):
    """
    Formatting code Automatically
    Precondition:Third party packages 'cargo fmt' need to be installed
    Args:
        all:format all packages (only usable in workspaces)
        quiet:whether no output printed to stdout
        verbose:Use verbose output
        path:execute the command under the path
    """
    _cmd = "cd %s && cargo fmt" % (path)
    if all:
        _cmd += " --all"
    if quiet:
        _cmd += " --quiet"
    if verbose:
        _cmd += " --verbose"
    
    try:
        run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo fmt failed!")

def cargo_all():
    """run all of cargo interface by default"""
    try:
        cargo_check()
        cargo_clippy()
        cargo_fmt()
    except Exception:
        logging.warning("Found Exception during running cargo_all()!")