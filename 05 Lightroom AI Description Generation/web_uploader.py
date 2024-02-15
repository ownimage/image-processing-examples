import pysftp
import urllib.parse

from jproperties import Properties


class WebUploader:
    def __init__(self, properties_file='web_uploader.properties'):
        p = Properties()
        self.properties = p
        with open(properties_file, "rb") as f:
            p.load(f, encoding='utf-8')

        self.connection = {
            'host': p['HOST'].data,
            'username': p['USERNAME'].data,
            'password': p['PASSWORD'].data,
        }
        self.base_url = p['BASE_URL'].data

        self.cnopts = pysftp.CnOpts()
        self.cnopts.hostkeys = None

    def upload_file(self, local_file, filename, connection=None):
        connection = self.connection if connection is None else connection
        with pysftp.Connection(host=connection['host'], username=connection['username'],
                               password=connection['password'],
                               cnopts=self.cnopts) as sftp:
            sftp.put(local_file, filename)
        return self.base_url + urllib.parse.quote(filename)
