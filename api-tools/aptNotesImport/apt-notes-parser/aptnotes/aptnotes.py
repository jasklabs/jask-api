import requests
import re
import hashlib


class AptNotes:
    """
    APTNOTES : API class to handle connection to github
    """
    base_url = 'https://raw.githubusercontent.com/aptnotes/data'
    raw_notes_url = '{0}/master/APTnotes.json'.format(base_url)

    @classmethod
    def get_reports(cls):
        """
        Get all reports data from Gitlab
        :return: List of Reports objects
        """
        try:
            notes = requests.get(cls.raw_notes_url)
        except Exception as e:
            raise Exception(e)
        else:
            if notes.status_code != 200:
                notes.raise_for_status()
            else:
                reports = []
                for note in notes.json():
                    reports.append(Report(note))
                return reports


class Report:
    """
    Report objects based on APTNotes information
    """

    def __init__(self, note):
        self.year = note.get('Year', None)
        self.link = note.get('Link', None)
        self.sha1 = note.get('SHA-1', None)
        self.source = note.get('Source', None)
        self.date = note.get('Date', None)
        self.filename = note.get('Filename', None)
        self.title = note.get('Title', None)
        self.sha256 = None
        self.md5 = None

    @property
    def box_shared_name(self):
        return self.link.rsplit('/', 1)[1]

    @property
    def box_file_id(self):
        try:
            page = requests.get(self.link)
        except Exception as e:
            raise Exception(e)
        else:
            if page.status_code != 200:
                page.raise_for_status()
            else:
                match = re.search(b'\s+data-file-id="(\d+)"\s+', page.content, re.MULTILINE)
                if match and len(match.groups()) > 0:
                    return int(match.groups()[0])

    def get_file_content(self):
        box_download_link = 'https://app.box.com/index.php?rm=box_download_shared_file&shared_name={0}&file_id=f_{1}'
        url = box_download_link.format(self.box_shared_name, self.box_file_id)
        try:
            page = requests.get(url=url)
        except Exception as e:
            raise Exception(e)
        else:
            if page.status_code != 200:
                page.raise_for_status()
            elif hashlib.sha1(page.content).hexdigest() != self.sha1:
                raise Exception('Downloaded file\'s SHA1 doesn\'t match that from APTNotes.')
            else:
                self.sha256 = hashlib.sha256(page.content).hexdigest()
                self.md5 = hashlib.md5(page.content).hexdigest()
                return page.content
