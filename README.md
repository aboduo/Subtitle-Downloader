Subtitle Downloader
=========

Scans a folder for releases and gets avaliable subtitles from SubScene. Automatically extracts the downloaded .zip file.

Usage
-
```python SubtitleDownloader.py <path> -l language
```

If run without path argument, the current directory will be scanned.
Language defaults to English, but can be set using a language code (int).

```
Danish: 10
English: 13
Norwegian: 30
Swedish: 39
```

The rest can be found by looking at the source here:
http://subscene.com/filter

Requirements
-
* Python 2.6/2.7
* Requests >= 1.0.0
* BeautifulSoup >= 4.0.0

Version
-

1.0

License
-
WTFPL