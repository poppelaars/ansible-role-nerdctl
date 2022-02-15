"""Role testing files using testinfra."""


def test_users(host):
    user = host.user("container")
    assert user.exists
    assert user.shell == "/bin/bash"
    assert user.home == "/home/container"


def test_dbus(host):
    with host.sudo('container'):
        dbus_service = host.service("dbus")
        assert dbus_service.is_running
        assert dbus_service.is_enabled


def test_install_nerdctl(host):
    with host.sudo('container'):
        nerdctl_tar_gz = host.file("/home/container/nerdctl.tar.gz")
        assert nerdctl_tar_gz.exists
        assert nerdctl_tar_gz.is_file

        dot_local = host.file("/home/container/.local")
        assert dot_local.exists
        assert dot_local.is_directory

        tar_gz_is_unpacked = host.file("/home/container/.local/bin/containerd-rootless-setuptool.sh")
        assert tar_gz_is_unpacked.exists
        assert tar_gz_is_unpacked.is_file

        containerd_service = host.file("/home/container/.config/systemd/user/containerd.service")
        assert containerd_service.exists
        assert containerd_service.is_file

        dot_bash_profile = host.file("/home/container/.bash_profile")
        assert dot_bash_profile.exists
        assert dot_bash_profile.is_file
        assert "export XDG_RUNTIME_DIR=\"/run/user/$(id -u)\";" in dot_bash_profile.content_string

