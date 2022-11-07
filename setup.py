import argparse
import os
from typing import Optional
import requests
import selectolax.parser
import re


DIRECTORY = 'server'


def download_installer(version: str) -> str:
    response = requests.get(f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html')
    if not response.ok:
        print(f'Could not download jar for version {version}!')
        exit(1)

    parser = selectolax.parser.HTMLParser(response.text)
    installer_url_dirty = parser.css_first('.download > .links > .link-boosted > a').attributes['href']
    print(installer_url_dirty)
    installer_url = re.match("^.+&url=(.*)", installer_url_dirty).group(1)
    print(installer_url)
    installer_name = installer_url.split("/")[-1]

    if not os.path.exists(DIRECTORY):
        os.mkdir(DIRECTORY)

    os.system(f'wget -O {DIRECTORY}/{installer_name} {installer_url}')
    return installer_name


def install(installer_name: str, backup: Optional[str]):
    os.system(f'java -jar {DIRECTORY}/{installer_name} --installServer {DIRECTORY}/')
    os.system(f'rm {DIRECTORY}/{installer_name}')
    os.system(f'rm {installer_name}.log')

    if backup is None:
        return

    os.system(f'tar -xzf {backup}')
    if os.path.exists(f"{DIRECTORY}/world"):
        os.system(f'rm -r {DIRECTORY}/world')
    os.system(f'mv world {DIRECTORY}/')

    with open(f'{DIRECTORY}/user_jvm_args.txt', 'a') as f:
        f.write('\n-Xmx7168M -Xms2048M')

    with open(f'{DIRECTORY}/run.sh', 'r') as f:
        lines = map(lambda l: l.replace('"$@"', 'nogui "$@"'), f.readlines())
        print(lines)

    with open(f'{DIRECTORY}/run.sh', 'w') as f:
        f.writelines(lines)

    with open(f'{DIRECTORY}/eula.txt', 'w') as f:
        f.write('eula=true')


def main():
    arg_parser = argparse.ArgumentParser(prog='Setup')
    arg_parser.add_argument('-v', '--version', required=True)
    arg_parser.add_argument('-b', '--backup')
    args = arg_parser.parse_args()

    version: str = args.version
    backup: Optional[str] = args.backup
    print(version, backup)

    installer_name = download_installer(version)
    print(installer_name)

    install(installer_name, backup)


if __name__ == '__main__':
    main()
