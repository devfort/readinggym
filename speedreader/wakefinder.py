import subprocess

from django.conf import settings
from django.contrib.staticfiles.finders import FileSystemFinder


class WakeAssetsFinder(FileSystemFinder):
    def __init__(self):
        subprocess.call([settings.WAKE_ASSETS._wake])
        super(WakeAssetsFinder, self).__init__()
