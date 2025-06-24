import datetime
from googleapiclient.discovery import build

# Инициализация YouTube API-клиента с использованием API-ключа
API_KEY = "AIzaSyCNcw2KUkiyUq15uA0M4PU9dZR43ijdFms"  # TODO: вставьте сюда ваш ключ API
youtube = build("youtube", "v3", developerKey=API_KEY)

# Указание идентификатора канала (handle или ID). Используем handle @moriartymega.
channel_handle = "moriartymega"  # без символа @ или с ним - библиотека принимает оба варианта
# Если у вас есть ID канала (начинающийся с UC) или legacy username, можно использовать их:
# channel_id = "UCxxxxxxxxxxxxx"
# request = youtube.channels().list(part="contentDetails", id=channel_id)

# Шаг 3. Получение ID плейлиста "uploads" данного канала
request = youtube.channels().list(
    part="contentDetails",
    forHandle=f"@{channel_handle}"
)
response = request.execute()

# Извлекаем ID плейлиста загруженных видео
uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Шаг 3 (продолжение). Получение всех видео из плейлиста загрузок
videos = []  # список для хранения информации о видео
next_page_token = None

while True:
    playlist_request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )
    playlist_response = playlist_request.execute()
    videos.extend(playlist_response["items"])
    next_page_token = playlist_response.get("nextPageToken")
    if not next_page_token:
        break  # выйдем из цикла, когда достигнем последней страницы

# Шаг 4. Обработка списка видео и форматирование даты публикации
print(f"{'Название видео':60} | Дата и время публикации")
print("-" * 80)
for item in videos:
    title = item["snippet"]["title"]                            # название видео
    published_at = item["contentDetails"]["videoPublishedAt"]   # время публикации (ISO 8601 формат)
    # Парсим строку времени в объект datetime
    dt = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    # Форматируем datetime в желаемый строковый вид
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    # Выводим название и время публикации, обрезая слишком длинные названия для красоты вывода
    print(f"{title[:58]:58} | {formatted_time}")
