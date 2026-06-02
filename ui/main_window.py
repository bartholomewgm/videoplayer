from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFileDialog,
    QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShortcut, QKeySequence

from ui.controls import ControlsWidget
from ui.playlist import PlaylistWidget
from ui.video_info import VideoInfoWidget
from ui.styles import STYLE

from core.player import VideoPlayer
from core.history import HistoryManager


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.resize(1400, 800)

        # Core
        self.player = VideoPlayer()
        self.history = HistoryManager()
        self.current_file_path = None

        # UI
        self.controls = ControlsWidget()
        self.playlist = PlaylistWidget()
        self.video_info = VideoInfoWidget()

        self.setup_ui()
        self.setup_connections()
        self.setup_shortcuts()  # Глобальные горячие клавиши

        self.setStyleSheet(STYLE)

        # Для полноэкранного режима
        self.cursor_timer = None

        # Включаем возможность получать события клавиатуры
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setup_ui(self):
        # Видео виджет
        video_layout = QVBoxLayout()
        video_layout.addWidget(self.player.video_widget)
        video_layout.addWidget(self.video_info)
        video_layout.addWidget(self.controls)
        video_layout.setStretch(0, 1)
        video_layout.setStretch(1, 0)
        video_layout.setStretch(2, 0)

        # Основной лейаут
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.playlist)
        main_layout.addLayout(video_layout, stretch=1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_connections(self):
        # Кнопки
        self.controls.open_button.clicked.connect(self.open_file)
        self.controls.play_button.clicked.connect(self.play_pause)
        self.controls.prev_button.clicked.connect(self.prev_video)
        self.controls.next_button.clicked.connect(self.next_video)
        self.controls.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        # Слайдеры
        self.controls.volume_slider.valueChanged.connect(
            self.player.set_volume)
        self.controls.position_slider.sliderMoved.connect(
            self.player.set_position)

        # Скорость
        self.controls.speed_box.currentTextChanged.connect(self.change_speed)

        # Плейлист
        self.playlist.itemDoubleClicked.connect(self.play_selected_video)

        # Сигналы плеера
        self.player.position_changed.connect(self.update_position)
        self.player.duration_changed.connect(self.update_duration)
        self.player.media_state_changed.connect(self.on_media_state_changed)
        self.player.error_occurred.connect(self.handle_player_error)

    def setup_shortcuts(self):
        """Глобальные горячие клавиши (работают всегда)"""
        # Полноэкранный режим
        self.fullscreen_shortcut = QShortcut(QKeySequence("F"), self)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)

        self.fullscreen_shortcut2 = QShortcut(QKeySequence("F11"), self)
        self.fullscreen_shortcut2.activated.connect(self.toggle_fullscreen)

        # Выход из полноэкранного
        self.escape_shortcut = QShortcut(QKeySequence("Esc"), self)
        self.escape_shortcut.activated.connect(self.exit_fullscreen)

        # Play/Pause
        self.play_shortcut = QShortcut(QKeySequence("Space"), self)
        self.play_shortcut.activated.connect(self.play_pause)

        self.play_shortcut2 = QShortcut(QKeySequence("K"), self)
        self.play_shortcut2.activated.connect(self.play_pause)

        # Перемотка
        self.forward_shortcut = QShortcut(QKeySequence("Right"), self)
        self.forward_shortcut.activated.connect(
            lambda: self.player.forward(5000))

        self.backward_shortcut = QShortcut(QKeySequence("Left"), self)
        self.backward_shortcut.activated.connect(
            lambda: self.player.backward(5000))

        # Следующее/предыдущее видео
        self.next_shortcut = QShortcut(QKeySequence("N"), self)
        self.next_shortcut.activated.connect(self.next_video)

        self.prev_shortcut = QShortcut(QKeySequence("P"), self)
        self.prev_shortcut.activated.connect(self.prev_video)

        # Открыть файл
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_shortcut.activated.connect(self.open_file)

        # Выход из программы
        self.quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.quit_shortcut.activated.connect(self.close)

    def exit_fullscreen(self):
        """Выход из полноэкранного режима"""
        if self.isFullScreen():
            self.toggle_fullscreen()

    # =========================
    # FULLSCREEN
    # =========================

    def toggle_fullscreen(self):
        """Переключает полноэкранный режим"""
        if self.isFullScreen():
            self.showNormal()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.playlist.setVisible(True)
            self.video_info.setVisible(True)
            if hasattr(self.controls, 'set_fullscreen_mode'):
                self.controls.set_fullscreen_mode(False)
            if self.cursor_timer:
                self.cursor_timer.stop()
                self.cursor_timer = None
        else:
            self.showFullScreen()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.playlist.setVisible(False)
            self.video_info.setVisible(False)
            if hasattr(self.controls, 'set_fullscreen_mode'):
                self.controls.set_fullscreen_mode(True)
            self.start_cursor_timer()

    def start_cursor_timer(self):
        """Запускает таймер для скрытия курсора"""
        if self.cursor_timer:
            self.cursor_timer.stop()

        self.cursor_timer = QTimer()
        self.cursor_timer.setSingleShot(True)
        self.cursor_timer.timeout.connect(self.hide_cursor)
        self.cursor_timer.start(2000)

    def hide_cursor(self):
        """Скрывает курсор в полноэкранном режиме"""
        if self.isFullScreen():
            self.setCursor(Qt.CursorShape.BlankCursor)

    def show_cursor(self):
        """Показывает курсор"""
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):
        """При движении мыши показываем курсор и панель управления"""
        if self.isFullScreen():
            self.show_cursor()
            self.start_cursor_timer()
        super().mouseMoveEvent(event)

    # =========================
    # KEY PRESS (резервный вариант)
    # =========================

    def keyPressEvent(self, event):
        """Резервная обработка клавиш (на случай если QShortcut не сработал)"""
        key = event.key()

        # Полноэкранный режим
        if key == Qt.Key.Key_F11 or key == Qt.Key.Key_F:
            self.toggle_fullscreen()
        elif key == Qt.Key.Key_Escape and self.isFullScreen():
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)

    # =========================
    # VIDEO CONTROLS
    # =========================

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Video", "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)"
        )
        if file_name:
            self.load_video(file_name)

    def load_video(self, file_path):
        if self.player.load_video(file_path):
            saved_position = self.history.get_position(file_path)
            if saved_position > 0:
                self.player.set_position(saved_position)

            self.video_info.update_info(file_path, 0)

            self.player.play()
            self.playlist.add_video(file_path)
            self.current_file_path = file_path
            self.controls.set_play_button_state(True)

            self.wait_for_duration(file_path)
        else:
            QMessageBox.warning(
                self, "Ошибка", f"Не удалось загрузить видео:\n{file_path}")

    def wait_for_duration(self, file_path, attempts=0):
        duration = self.player.duration()
        if duration > 0:
            self.video_info.update_info(file_path, duration)
        elif attempts < 20:
            QTimer.singleShot(100, lambda: self.wait_for_duration(
                file_path, attempts + 1))

    def play_selected_video(self, item):
        row = self.playlist.row(item)
        file_path = self.playlist.get_video_path(row)
        if file_path:
            self.load_video(file_path)

    def play_pause(self):
        if self.player.is_playing():
            self.player.pause()
            self.controls.set_play_button_state(False)
        else:
            self.player.play()
            self.controls.set_play_button_state(True)

    def next_video(self):
        file_path = self.playlist.next_video()
        if file_path:
            self.load_video(file_path)

    def prev_video(self):
        file_path = self.playlist.previous_video()
        if file_path:
            self.load_video(file_path)

    def change_speed(self, text):
        try:
            speed = float(text.replace("x", ""))
            self.player.set_speed(speed)
        except ValueError:
            pass

    def update_position(self, position):
        self.controls.position_slider.blockSignals(True)
        self.controls.position_slider.setValue(position)
        self.controls.position_slider.blockSignals(False)

        duration = self.player.duration()
        self.controls.update_time_display(position, duration)

    def update_duration(self, duration):
        self.controls.position_slider.setRange(0, duration)
        if self.current_file_path and duration > 0:
            self.video_info.update_info(self.current_file_path, duration)

    def on_media_state_changed(self, is_playing):
        self.controls.set_play_button_state(is_playing)

    def handle_player_error(self, error_message):
        QMessageBox.critical(self, "Ошибка плеера", error_message)

    def closeEvent(self, event):
        if self.cursor_timer:
            self.cursor_timer.stop()
            self.cursor_timer = None

        if self.current_file_path:
            position = self.player.get_position()
            self.history.save_video(self.current_file_path, position)
        self.history.close()
        event.accept()
