from PyQt6.QtCore import QUrl, pyqtSignal, QObject
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QObject):
    """
    Обёртка над QMediaPlayer с удобными методами управления
    """

    # Сигналы
    media_state_changed = pyqtSignal(bool)  # True = воспроизведение
    error_occurred = pyqtSignal(str)
    position_changed = pyqtSignal(int)
    duration_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.video_widget = QVideoWidget()

        self.player.setAudioOutput(self.audio)
        self.player.setVideoOutput(self.video_widget)

        self.audio.setVolume(0.5)

        # Подключаем сигналы (ИСПРАВЛЕНО)
        self.player.playbackStateChanged.connect(
            self._on_playback_state_changed)
        self.player.errorOccurred.connect(self._on_error)
        # НЕ подключаем positionChanged и durationChanged напрямую к сигналам
        # Вместо этого используем промежуточные методы
        self.player.positionChanged.connect(self._on_position_changed)
        self.player.durationChanged.connect(self._on_duration_changed)

    def load_video(self, file_path: str) -> bool:
        try:
            url = QUrl.fromLocalFile(file_path)
            if not url.isLocalFile():
                self.error_occurred.emit(f"Файл не найден: {file_path}")
                return False
            self.player.setSource(url)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Ошибка загрузки: {str(e)}")
            return False

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_playing(self) -> bool:
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    def set_position(self, position: int):
        self.player.setPosition(position)

    def get_position(self) -> int:
        return self.player.position()

    def position(self) -> int:
        return self.player.position()

    def duration(self) -> int:
        return self.player.duration()

    def set_volume(self, value: int):
        self.audio.setVolume(max(0.0, min(1.0, value / 100)))

    def set_speed(self, speed: float):
        self.player.setPlaybackRate(speed)

    def forward(self, milliseconds: int = 10000):
        new_pos = self.player.position() + milliseconds
        self.player.setPosition(min(new_pos, self.player.duration()))

    def backward(self, milliseconds: int = 10000):
        new_pos = self.player.position() - milliseconds
        self.player.setPosition(max(0, new_pos))

    # =========================
    # ВНУТРЕННИЕ ОБРАБОТЧИКИ
    # =========================

    def _on_playback_state_changed(self, state):
        is_playing = (state == QMediaPlayer.PlaybackState.PlayingState)
        self.media_state_changed.emit(is_playing)

    def _on_error(self, error, error_string):
        self.error_occurred.emit(f"Ошибка: {error_string}")

    def _on_position_changed(self, position):
        """Прокидываем сигнал дальше"""
        self.position_changed.emit(position)

    def _on_duration_changed(self, duration):
        """Прокидываем сигнал дальше"""
        self.duration_changed.emit(duration)
