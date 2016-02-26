import os
import subprocess
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest

import settings
from pytabcmd import PyTabCmd


@pytest.fixture(autouse=True)
def mock_get_cfg_setting(monkeypatch):
    monkeypatch.setattr(settings, 'get_cfg_setting', lambda x: x)


class TestConstructor(object):

    def test_constructor_uses_settings_tabmc_by_default(self):
        assert PyTabCmd().tabcmd == \
            settings.get_cfg_setting('TABCMD_EXE_PATH')

    def test_constructor_uses_custom_tabcmd_when_provided(self):
        assert PyTabCmd(tabcmd='/foo/bar/tabcmd').tabcmd == '/foo/bar/tabcmd'

    def test_constructor_uses_settings_user_by_default(self):
        instance = PyTabCmd()
        assert instance.username == \
            settings.get_cfg_setting('TABLEAU_ONLINE_USERNAME')

    def test_constructor_uses_custom_user_when_provided(self):
        instance = PyTabCmd(username='John Doe')
        assert instance.username == 'John Doe'

    def test_constructor_uses_tableau_online_server_by_default(self):
        assert PyTabCmd().server == settings.TABLEAU_ONLINE_URL

    def test_constructor_uses_custom_server_when_provided(self):
        assert PyTabCmd(server='server').server == 'server'

    def test_constructor_sets_linux_false_by_default(self):
        assert PyTabCmd().linux is False

    def test_constructor_sets_linux_when_provided(self):
        assert PyTabCmd(linux=True).linux is True


class TestLogin(object):

    @pytest.fixture(autouse=True)
    def init_variables(self):
        self.instance = PyTabCmd()

    @pytest.fixture(scope="function")
    def mock_exec_command(self, mocker):
        return mocker.patch.object(PyTabCmd, '_execute_command')

    def test_login_uses_settings_password_by_default(self, mock_exec_command):
        self.instance.login(site='foo')
        assert "%s %s" % \
            ('-p', settings.get_cfg_setting('TABLEAU_ONLINE_PASSWORD')) in \
            " ".join(mock_exec_command.call_args[0][0])

    def test_login_uses_password_when_provided(self, mock_exec_command):
        self.instance.login(site='foo', password='foobar')
        assert "%s %s" % ('-p', 'foobar') in \
            " ".join(mock_exec_command.call_args[0][0])


class TestCreateProject(object):

    @pytest.fixture(autouse=True)
    def init_variables(self):
        self.instance = PyTabCmd()

    @pytest.fixture(scope="function")
    def mock_exec_command(self, mocker):
        return mocker.patch.object(PyTabCmd, '_execute_command')

    def test_create_project_needs_project_name(self, mock_exec_command):
        with pytest.raises(TypeError):
            self.instance.create_project()

    def test_create_project_sets_project_name(self, mock_exec_command):
        self.instance.create_project('foo')
        assert "-n foo" in \
            " ".join(mock_exec_command.call_args[0][0])

    def test_create_project_appends_description(self, mock_exec_command):
        self.instance.create_project('foo', 'bar')
        assert "-d bar" in \
            " ".join(mock_exec_command.call_args[0][0])


class TestDeleteProject(object):

    @pytest.fixture(autouse=True)
    def init_variables(self):
        self.instance = PyTabCmd()

    @pytest.fixture(scope="function")
    def mock_exec_command(self, mocker):
        return mocker.patch.object(PyTabCmd, '_execute_command')

    def test_delete_project_needs_project_name(self, mock_exec_command):
        with pytest.raises(TypeError):
            self.instance.delete_project()

    def test_delete_project_sets_project_name(self, mock_exec_command):
        self.instance.delete_project('foo')
        assert "deleteproject foo" in \
            " ".join(mock_exec_command.call_args[0][0])


class TestExecuteCommand(object):

    @pytest.fixture(autouse=True)
    def init_variables(self):
        self.instance = PyTabCmd()

    @pytest.fixture(scope="function")
    def mock_subprocess(self, mocker):
        return mocker.patch.object(subprocess, 'call')

    def test_login_doesnt_append_certcheck_by_default(self, mock_subprocess):
        self.instance._execute_command([])
        assert "--no-certcheck" not in mock_subprocess.call_args[0][0]

    def test_login_appends_certcheck_for_linux_instance(self, mock_subprocess):
        linux_instance = PyTabCmd(linux=True)
        linux_instance._execute_command([])
        assert "--no-certcheck" in mock_subprocess.call_args[0][0]
