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
        options:a dictionary including the params of the command
        (eg.options={"quiet":None, "exclude":"util/src", "workspace":None})
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
    except Exception:
        logging.debug("Cargo check failed due to the wrong command.")

def cargo_clippy(options, path=TEST_PATH):
    """
    Check the code specification and give the optimization scheme
    Precondition:Third party packages 'cargo clippy' need to be installed
    Args:
        options:a dictionary including the params of the command
        (eg.options={"quiet":None, "exclude":"util/src", "workspace":None})
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
        # To allow or deny a lint 
        elif option in lint_list:
            _cmd += " -- --%s" % (option)
    
    try:
        run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo clippy failed!")
    except Exception:
        logging.debug("Cargo clippy failed due to the wrong command.")

def cargo_fmt(flags, options, path=TEST_PATH):
    """
    Formatting code Automatically
    Precondition:Third party packages 'cargo fmt' need to be installed
    Args:
        flags:a list including the FLAGS of the command
        (eg.flags=["all", "quiet"])
        options:a dictonary including the OPTIONS of the command
        (eg.options={"manifest-path":"/home/stratovirt"})
        path:execute the command under the path
    """
    flag_list = ["all", "quiet", "verbose"]
    option_list = ["manifest-path", "message-format", "package"]
    _cmd = "cd %s && cargo fmt" % (path)
    for flag in flags.keys():
        if flag in flag_list:
            _cmd += " --%s" % (flag)
    for option in options.keys():
        if option in option_list:
            _cmd += " --%s" % (option)
            if options[option] is not None:
                _cmd += " %s" % str(options[option])
    
    try:
        run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo fmt failed!")
    except Exception:
        logging.debug("Cargo fmt failed due to the wrong command.")

def cargo_test(options, testname, path=TEST_PATH):
    """
    Execute all unit and integration tests and build examples of a local package
    Args:
        options:a dictonary including the params of the command
        (eg.options={"quiet":None, "exclude":"util/src", "workspace":None})
        testname:if specified, only run tests containing this string in their names
        (eg.testname="balloon")
        path:execute the command under the path
    """
    option_list = ["quiet", "lib", "bin", "bins", "example", "examples", "test",
                    "tests", "bench", "benches", "all-targets", "doc", "no-run",
                    "no-fail-fast", "package", "all", "workspace", "exclude", "jobs",
                    "release", "profile", "features", "all-features", "no-default-features",
                    "target", "target-dir", "manifest-path", "ignore-rust-version",
                    "message-format", "unit-gragh", "future-incompat-report",
                    "verbose", "color", "frozen", "locked", "offline", "config"]
    _cmd = "cd %s && cargo test" % (path)
    for option in options.keys():
        if option in option_list:
            _cmd += " --%s" % (option)
            if options[option] is not None:
                _cmd += " %s" % str(options[option])
    _cmd += " %s" % str(testname)

    try:
        run(_cmd, shell=True, check=False)
    except CallProcessError:
        logging.debug("Found CallProcessError, cargo test failed!")
    except Exception:
        logging.debug("Cargo test failed due to the wrong command.")
