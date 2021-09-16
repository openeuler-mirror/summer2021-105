# StratoVirt is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan
# PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http:#license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
"""Some cargo functions"""

import os
import logging
from subprocess import run
from subprocess import CalledProcessError

TEST_PATH = os.path.join(os.path.dirname(__file__), "../../..")

def cargo_check(options, path=TEST_PATH):
    """
    It can be helpful for running a faster compile if you only need correctness checks.
    Precondition:Third party packages 'cargo check' need to be installed
    Args:
        options:a dictionary including the params of command
        path:execute the command under the path
    """
    option_list = ["quiet", "package", "all", "workspace", "exclude", "jobs",
                    "lib", "bin", "bins", "example", "examples", "test",
                    "tests", "bench", "benches", "all-targets", "release",
                    "profile", "features", "all-features", "no-default-features",
                    "target", "target-dir", "manifest-path", "ignore-rust-version",
                    "message-format", "unit-gragh", "future-incompat-report",
                    "verbose", "color", "frozen", "locked", "offline", "config"]
    _cmd = "cd %s && cargo check" % (path)
    for option in options.keys():
        if option in option_list:
            _cmd += " --%s" % (option)
        if options[option] is not None:
            _cmd += " %s" % str(options[option]) 
    
    try:
        res = run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo check failed!")

def cargo_clippy(options, path=TEST_PATH):
    """
    Check the code specification and give the optimization scheme
    Precondition:Third party packages 'cargo clippy' need to be installed
    Args:
        options:a dictionary including the params of command
        path:execute the command under the path
    """
    lint_list = ["warn", "allow", "deny", "forbid"]
    option_list = ["quiet", "package", "all", "workspace", "exclude", "jobs",
                    "lib", "bin", "bins", "example", "examples", "test",
                    "tests", "bench", "benches", "all-targets", "release",
                    "profile", "features", "all-features", "no-default-features",
                    "target", "target-dir", "manifest-path", "ignore-rust-version",
                    "message-format", "unit-gragh", "future-incompat-report",
                    "verbose", "color", "frozen", "locked", "offline", "config"]
    _cmd = "cd %s && cargo clippy" % (path)
    for option in options.keys():
        if option in option_list:
            _cmd += " --%s" % (option)
            if options[option] is not None:
                _cmd += " %s" % str(options[option])
                continue
        # To allow or deny a lint 
        elif option in lint_list:
            _cmd += " -- --%s" % (option)
    
    try:
        run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo clippy failed!")

def cargo_fmt(all=False, quiet=False, verbose=False, path=TEST_PATH):
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

def cargo_test():
    """
    Execute all unit and integration tests and build examples of a local package
    """
    

def cargo_all():
    """run all of cargo functions by default"""
    try:
        cargo_check()
        cargo_clippy()
        cargo_fmt()
        cargo_test()
    except Exception:
        logging.warning("Found Exception during running cargo_all()!")