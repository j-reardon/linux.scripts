import os
import subprocess
import git
from urllib import request
from json import loads
from os import listdir

__directory__ = "{0}/.aur/".format(os.environ['HOME'])
__url__ = "https://aur.archlinux.org/{0}.git"

def get_local_version(package):
    pkg_ver = ""
    pkg_rel = ""
    pkgbuild_file_path = __directory__ + package + "/PKGBUILD"
    with open(pkgbuild_file_path) as f:
        for line in f:
            if "pkgver" in line:
                split = line.strip('\n').split('=')
                pkg_ver = split[1].strip("'")
            if "pkgrel" in line:
                split = line.strip('\n').split('=')
                pkg_rel = split[1].strip("'")
            if pkg_ver and pkg_rel:
                break
    pkg_ver_split = pkg_ver.split('.')
    if len(pkg_ver_split) > 2:
        return "{0}.{1}.{2}-{3}".format(pkg_ver_split[0], pkg_ver_split[1], pkg_ver_split[2], pkg_rel)
    else:
        return "{0}.{1}-{2}".format(pkg_ver_split[0], pkg_ver_split[1], pkg_rel)

def get_remote_version(package):
    aur_rpc_url = "https://aur.archlinux.org/rpc/?v=5&type=search&by=name&arg="
    response = request.urlopen(aur_rpc_url + package)
    data = response.read()
    package_info = loads(data)
    for result in package_info["results"]:
        if result["Name"] == package:
            return result["Version"]

def has_update(package):
    local_version = get_local_version(package)
    aur_version = get_remote_version(package)
    if local_version != aur_version:
        print("{0} {1} -> {2}".format(package, local_version, aur_version))
        return True
    return False

def check_for_updates():
    print("Checking for AUR package updates...")
    for package in listdir(__directory__):
        has_update(package)

def update(package):
    if package is None:
        print("you must specify a package to be updated")
        return
    package_directory = "{0}{1}".format(__directory__, package)
    print("performing update inside {0}".format(package_directory))
    g = git.Git(package_directory)
    g.reset(hard=True)
    g.clean('-fd')
    g.pull()
    upgrade(package)
    
def update_all():
    for package in listdir(__directory__):
        if has_update(package):
            update(package)

def install(package):
    if any(f == package for f in os.listdir(__directory__)):
        print("{0} is already installed, try aur.update() to install the latest version".format(package))
        return
    clone(package)
    upgrade(package)

def upgrade(package):
    print("building and installing {0}...".format(package))
    package_directory = "{0}{1}".format(__directory__, package)
    os.chdir(package_directory)
    subprocess.call(["makepkg", "-si"])

def clone(package):
    clone_url = __url__.format(package)
    print("cloning {0}...".format(clone_url))
    os.chdir(__directory__)
    package_directory = "{0}{1}".format(__directory__, package)
    if not os.path.exists(package_directory):
        os.makedirs(package_directory)
    git.Repo.clone_from(clone_url, package_directory)

