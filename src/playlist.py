from src.channel import Channel
import isodate
import datetime


class PlayList:
    """Класс для плейлиста"""

    def __init__(self, playList_id):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playList_id = playList_id
        self.playList_response = Channel.youtube.playlists().list(id=self.playList_id,
                                                                  part='snippet',
                                                                  maxResults=50,
                                                                  ).execute()
        self.title = self.playList_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.playList_id

    @property
    def video_response(self):
        """
        Возвращает информацию о видео плейлиста - создан для дальнейшего использования
        в методах total_duration и show_best_video
        """
        playlist_videos = Channel.youtube.playlistItems().list(playlistId=self.playList_id,
                                                               part='contentDetails',
                                                               maxResults=50,
                                                               ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = Channel.youtube.videos().list(part='contentDetails,statistics',
                                                       id=','.join(video_ids)
                                                       ).execute()
        return video_response

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)
        """
        duration = datetime.timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        max_like_count = 0
        video_url = ''
        for video in self.video_response['items']:
            video_id = video['id']
            like_count = int(video['statistics']['likeCount'])
            if like_count >= max_like_count:
                max_like_count = like_count
                video_url = 'https://youtu.be/' + video_id
        return video_url
