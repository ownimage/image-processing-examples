import logging
import os

from jproperties import Properties

from web_uploader import WebUploader
from image_util import get_image


class SlackNotifier:

    def __init__(self, properties_file='slack_notifier.properties', get_image=get_image, web_uploader=WebUploader()):
        p = Properties()
        self.properties = p
        with open(properties_file, "rb") as f:
            p.load(f, encoding='utf-8')

        self.THUMBNAIL_SIZE = int(p['NOTIFIER_THUMBNAIL_SIZE'].data)
        self.web_uploader = web_uploader
        self.get_image = get_image

    def send_notification_with_image(self, message, dirpath, image_filename, channel=None):
        full_image_filename = os.path.join(dirpath, image_filename)
        img = self.get_image(full_image_filename, self.THUMBNAIL_SIZE)
        saved_filename = f'{image_filename}.jpg'
        full_saved_filename = f'temp\\{saved_filename}'
        img.save(full_saved_filename)
        img.close()

        image_url = self.web_uploader.upload_file(full_saved_filename, saved_filename)

        message = self.__escape_string(message)
        slack_url = self.__get_slack_url(channel)

        curl = ('curl -X POST -H "Content-type: application/json" ' +
                '--data "{\'text\':\'' + message +
                '\', \'attachments\':[{\'fallback\':\'text\', \'image_url\':\'' + image_url + '\'}]}" ' +
                slack_url)
        print(curl)
        os.system(curl)

    def send_notification(self, message, channel=None):

        message = self.__escape_string(message)
        slack_url = self.__get_slack_url(channel)

        curl = ('curl -X POST -H "Content-type: application/json" ' +
                '--data "{\'text\':\'' + message +'\'}" ' +
                slack_url)
        print(curl)
        os.system(curl)

    def __get_slack_url(self, channel):
        property_name = 'NOTIFIER_SLACK_URL' if channel is None else 'NOTIFIER_SLACK_URL.' + channel
        return self.properties[property_name].data

    def __escape_string(self, message):
        return message.replace('\\', '\\\\').replace('\n', '  ').replace('"', '-').replace('\'', '')

