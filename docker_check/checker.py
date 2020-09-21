import base64
import os.path
import subprocess
import sys
import typing as t


def has_dockerenv() -> bool:
    return os.path.exists('/.dockerenv')


def has_docker_in_proc_1_cgroup() -> t.Union[bool, None]:
    if not os.path.exists('/proc/1/cgroup'):
        return False

    with open('/proc/1/cgroup', 'r') as f:
        if 'docker' in f.read():
            return True
    return False


def has_cexecsvc() -> bool:
    cmd = ["Get-Service", "-Name", "cexecsvc", "-ErrorAction", "SilentlyContinue"]
    cmd = ' '.join(cmd)
    cmd = base64.b64encode(cmd.encode('utf-16le'))
    cmd = cmd.decode("utf-8")
    cmd = 'PowerShell -encodedCommand "{}"'.format(cmd)
    output = subprocess.run(cmd, shell=True)
    return output


def is_inside_container() -> t.Union[bool, None]:
    WINDOWS = sys.platform == "win32"
    if WINDOWS:
        if has_cexecsvc():
            return True

        return False

    if has_dockerenv():
        return True

    if has_docker_in_proc_1_cgroup():
        return True

    return None
