from src.channel import Channel


class Video:
    """Класс для видео"""

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.video_response = Channel.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                            id=self.video_id).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id

    def __str__(self):
        """Отображает информацию об объекте класса для пользователей"""
        return f'{self.video_title}'


class PLVideo(Video):
    """Класс для видео, который инициализируется id видео и id плейлиста"""

    def __init__(self, video_id, playlist_id):
        """Экземпляр инициализируется id видео, id плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
