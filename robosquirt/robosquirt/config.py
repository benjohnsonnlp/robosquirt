"""
Module for fetching configuration information from a file.
"""
from configparser import NoSectionError, NoOptionError, ConfigParser
from functools import partial
import os
from os import path
from pathlib import Path


class ExpandedConfigParser(ConfigParser):

    def getlist(self, section, option):
        value = self.get(section, option)
        values = value.split(",")
        return list(filter(None, (x.strip() for x in values)))


class ConfigurationError(Exception):
    """
    Raise this for any configuration problems.
    """


def _get_conf(fn, section, option):
    try:
        return fn(section, option)
    except (NoSectionError, NoOptionError):
        return None


def get_project_root():
    here = Path(path.dirname(path.realpath(__file__)))
    return here.parents[1]


def get_configuration(name="robosquirt"):
    """
    Handle fetching configuration data. Returns a dictionary of configuration values. If any problems are encountered
    (missing required values or sections, numeric values that aren't actually numbers, etc.) then ``ConfigurationError``
    will be raised.

    1. Start by looking in the local directory for the ``{{name}}.conf`` file.
    2. Look for the same file in the user's home directory.
    3. Look for system-wide configuration in ``/etc/{{name}}.conf``
    4. Look for an environmental variable {{NAME}}_CONF_DIR which would contain the file path.

    """
    env_var_name = "{}_CONF_DIR".format(name.upper())
    conf_file_name = "{}.conf".format(name)
    locations = (
        os.curdir,
        os.path.expanduser("~"),
        "/etc",
        os.environ.get(env_var_name)
    )
    conf = ExpandedConfigParser({
        "debug": "false",
        "hostname": "localhost",
        "routing_key": None
    })
    candidate_locations = [os.path.join(loc, conf_file_name) for loc in locations if loc]
    conf.read(candidate_locations)
    get_conf = partial(_get_conf, conf.get)
    getint_conf = partial(_get_conf, conf.getint)
    getlist_conf = partial(_get_conf, conf.getlist)
    getbool_conf = partial(_get_conf, conf.getboolean)

    if not conf.sections():
        raise FileNotFoundError("Couldn't find a valid {name}.conf configuration file in: {paths}.".format(
            name=name,
            paths=", ".join(candidate_locations)))

    return {
        "sqlite_db_path": get_conf("Database", "path") or str(get_project_root()),
        "log_debug": getbool_conf("Logging", "debug") or True,
    }


config = get_configuration()
