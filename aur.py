import os
import subprocess
import git
from urllib import request
from json import loads

__directory__ = "{0}/.aur/".format(os.environ['HOME'])
__url__ = "https://aur.archlinux.org/packages/{0}.git"

def local_version(package):
    pkg_ver = ""
    pkg_rel = ""
    pkgbuild_file_path = __directory__ + package + "/PKGBUILD"
    with open(pkgbuild_file_path) as f:
        for line in f:
            if "pkgver" in line:
                split = line.strip('\n').split('=')
                pkg_ver = split[1]
            if "pkgrel" in line:
                split = line.strip('\n').split('=')
                pkg_rel = split[1]
            if pkg_ver and pkg_rel:
                break
    pkg_ver_split = pkg_ver.split('.')
    return "{0}.{1}.{2}-{3}".format(pkg_ver_split[0], pkg_ver_split[1], pkg_ver_split[2], pkg_rel)


def remote_version(package):
    aur_rpc_url = "https://aur.archlinux.org/rpc/?v=5&type=search&by=name&arg="
    response = request.urlopen(aur_rpc_url + package)
    data = response.read()
    package_info = loads(data)
    for result in package_info["results"]:
        if result["Name"] == package:
            return result["Version"]

def update(package):
    package_directory = "{0}{1}".format(__directory__, package)
    g = git.Git(package_directory)
    g.reset(hard=True)
    g.clean('-fd')
    g.pull()
    upgrade(package)
    
def install(package):
    if any(f == package for f in os.listdir(__directory__)):
        print("{0} is already installed, try aur.update() to install the latest version".format(package))
        return
    clone(package)
    upgrade(package)

def upgrade(package):
    package_directory = "{0}{1}".format(__directory__, package)
    os.chdir(package_directory)
    subprocess.call(["makepkg"])
    built_package = list(filter(lambda x: "pkg.tar.xz" in x, os.listdir(package_directory)))[0]
    subprocess.call(["sudo", "pacman", "-U", built_package])

def clone(package):
    os.chdir(__directory__)
    git.Repo().clone(__url__.format(package))

