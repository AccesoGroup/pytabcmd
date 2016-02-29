import subprocess

from . import settings


class PyTabCmd(object):
    def __init__(self, *args, **kwargs):
        self.tabcmd = kwargs.get('tabcmd',
                                 settings.get_cfg_setting('TABCMD_EXE_PATH'))
        self.username = kwargs.get(
            'username', settings.get_cfg_setting('TABLEAU_ONLINE_USERNAME'))

        # Default value: Tableau Online
        self.server = kwargs.get('server', settings.TABLEAU_ONLINE_URL)

        self.linux = kwargs.get('linux', False) is True

    def _execute_command(self, command):
        # In Tableau 9.2 we have to append --no-certcheck for linux connections
        # More info here: https://community.tableau.com/message/450517#450517
        command = command + ["--no-certcheck"] if self.linux else command
        subprocess.call(command)

    def login(self, site, password=None):
        pwd = password or settings.get_cfg_setting('TABLEAU_ONLINE_PASSWORD'),
        command = [
            self.tabcmd,
            'login',
            "-u", "%s" % self.username,
            "-p", "%s" % pwd,
            "-s", "%s" % self.server,
            "-t", "%s" % site,
        ]
        self._execute_command(command)

    def create_project(self, name, description=None):
        command = [
            self.tabcmd,
            'createproject',
            "-n", "%s" % name,
        ]
        if description is not None:
            command += ["-d", description]
        self._execute_command(command)

    def delete_project(self, name):
        command = [
            self.tabcmd,
            'deleteproject',
            name
        ]
        self._execute_command(command)
