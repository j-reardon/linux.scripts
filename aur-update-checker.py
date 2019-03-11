from os import listdir
import aur

print ("Checking for AUR package updates...")
aur_packages = listdir(aur.__directory__)
for package in aur_packages:
    local_version = aur.local_version(package)
    aur_version = aur.remote_version(package)
    if (local_version != aur_version):
        print("{0} - local={1}  AUR={2}".format(package, local_version, aur_version))
    else:
        print("{0} - up to date".format(package))

