import json
import os
from googleapiclient.discovery import build


# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('YOUTUBE_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    # создан специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.__channel_id
        channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        """Геттер для __channel_id"""
        return self.__channel_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return cls.youtube

    def to_json(self, file_name):
        """Сохраняет в файл значения атрибутов экземпляра `Channel`."""
        channel_info = {'channel_id': self.__channel_id,
                        'title': self.title,
                        'description': self.description,
                        'url': self.url,
                        'subscriber_count': self.subscriber_count,
                        'video_count': self.video_count,
                        'view_count': self.view_count
                        }
        file_name_full = os.path.join(os.path.abspath('..'), 'homework-2', file_name)
        with open(file_name_full, 'w', encoding='UTF-8') as file:
            json.dump(channel_info, file, ensure_ascii=False)
