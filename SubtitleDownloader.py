# -*- coding: iso-8859-1 -*-
import os
import sys
import zipfile
import argparse
from collections import namedtuple
from bs4 import BeautifulSoup as bs
import requests


class SubDownloader(object):
    def __init__(self, path, language=10):
        self.path = path
        self.cookies = dict(LanguageFilter=str(language))

        self.baseurl = 'http://subscene.com'
        self.searchurl = 'http://subscene.com/subtitles/release.aspx?q={0}'

        self.session = requests.session()
        useragent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
        self.session.headers.update({'User-Agent': useragent})

        self.releases = self.get_releases()

    def get_releases(self):
        release = namedtuple('release', 'name path')
        releases = []
        file_extensions = ('.mkv', '.mp4', '.avi')

        for dirname in [name for name in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, name))]:
            path = os.path.join(self.path, dirname)

            #Check if subtitle file already exists in folder.
            skip = False
            for f in os.listdir(path):
                if f.endswith(('.sub', '.srt')):
                    skip = True
                    break
            if skip:
                continue

            releases.append(release(name=dirname, path=path))

        for filename in [name for name in os.listdir(self.path) if name.endswith(file_extensions)]:
            releases.append(release(name=filename, path=self.path))

        return releases

    def search(self, release):
        req = self.session.get(self.searchurl.format(release.name), cookies=self.cookies)

        if req.url.startswith('http://subscene.com/subtitles/title.aspx?q='):
            print "No subtitles could be found for {0}".format(release.name)
            return False

        subtitle = namedtuple('subtitle', 'name url')
        subtitles = []

        soup = bs(req.text)

        table = soup.find('tbody')

        try:
            rows = table.findAll('tr')
            for tr in rows:
                url = self.baseurl + tr.find('a')['href']
                name = tr.findAll('span')[1].text.strip()
                subtitles.append(subtitle(name=name, url=url))
        except:
            print "No subtitle for {0} could be found.".format(release.name).decode('iso-8859-1')
            return False

        return self.download_subtitle(subtitles[0].url, release)

    def download_subtitle(self, url, release):
        soup = bs(self.session.get(url).text)
        downloadurl = self.baseurl + soup.find('a', id='downloadButton')['href']
        filepath = os.path.join(release.path, release.name)

        req = self.session.get(downloadurl)
        with open(filepath + '.zip', "wb") as code:
            code.write(req.content)

        print "Downloaded subtitle for {0}".format(release.name).decode('iso-8859-1')

        with zipfile.ZipFile(filepath + '.zip') as zf:
            for filename in zf.namelist():

                data = zf.read(filename)
        with open(os.path.join(release.path, filename), "wb") as code:
            code.write(data)
        os.remove(filepath + '.zip')

    def download_all(self):
        for x in self.releases:
            self.search(x)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads subtitles for all releases in a folder.')
    parser.add_argument("path", nargs='?', help="Path to folder, defaults to current directory", default='.')
    parser.add_argument("-l", "--language", type=int ,help="Sets the language filter, defaults to English", default=13)
    args = parser.parse_args()

    sd = SubDownloader(args.path, language=args.language)
    sd.download_all()
