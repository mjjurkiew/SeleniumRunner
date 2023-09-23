import subprocess
import requests
import json
from urllib.request import urlretrieve
from zipfile import ZipFile


def get_current_chrome_version() -> str:
    version_bytes: bytes = subprocess.check_output(
        args=r'wmic datafile where name="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" get Version /value',
        shell=True
    )

    version: str = version_bytes.decode('utf-8').strip().split('=')[1]

    return version


def get_url_chromedriver(chrome_version: str) -> str:
    response: requests.Response = requests.request(method='GET',
                                                   url='https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')
    response_text: dict = json.loads(response.text)
    versions: list = response_text.get('versions')

    for version_data in versions:
        if version_data['version'][:5] == chrome_version[:5]:
            chrome_platforms = version_data['downloads']['chromedriver']
            for chrome_platform in chrome_platforms:
                if chrome_platform['platform'] == 'win64':
                    return chrome_platform['url']


def download_chromedriver(url: str, path: str) -> None:
    urlretrieve(url,
                path)


def unzip_chromedriver(path: str) -> None:
    with ZipFile(path, 'r') as zObject:
        zObject.extractall(
            path="chromedriver")
    zObject.close()


path: str = 'chromedriver.zip'

chrome_version: str = get_current_chrome_version()
url_download: str = get_url_chromedriver(chrome_version=chrome_version)
download_chromedriver(url=url_download, path=path)
unzip_chromedriver(path=path)
