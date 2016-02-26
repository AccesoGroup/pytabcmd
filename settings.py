from configparser import ConfigParser

SECRET_CFG_FILE = '/etc/pytabcmd.cfg'
SECRET_CFG_SECTION = 'secret_variables'


def get_cfg_setting(setting):
    """ Get the secret setting or return exception. """
    try:
        config = ConfigParser()
        config.read(SECRET_CFG_FILE)
        return config.get(SECRET_CFG_SECTION, setting)
    except KeyError as e:
        print("Set the %s cfg variable in %s" % (setting, SECRET_CFG_FILE,))
        raise e

TABLEAU_ONLINE_URL = 'https://10ay.online.tableau.com'
