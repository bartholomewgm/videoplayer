"""
Главное окно приложения
Объединяет все виджеты и управляет логикой
"""

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
    """Главное окно видеоплеера"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.resize(1400, 800)
        
        # ========== ЯДРО ==========
        self.player = VideoPlayer()
        self.history = HistoryManager()
        self.current_file_path = None

        # ========== ИНТЕРФЕЙС ==========
        self.controls = ControlsWidget()
        self.playlist = PlaylistWidget()
        self.video_info = VideoInfoWidget()

        self.setup_ui()
        self.setup_connections()
        self.setup_shortcuts()

        self.setStyleSheet(STYLE)
        
        # ========== ПОЛНОЭКРАННЫЙ РЕЖИМ ==========
        self.cursor_timer = None
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def setup_ui(self):
        """Создаёт структуру интерфейса"""
        # Видео виджет
        video_layout = QVBoxLayout()
        video_layout.addWidget(self.player.video_widget)
        video_layout.addWidget(self.video_info)
        video_layout.addWidget(self.controls)
        video_layout.setStretch(0, 1)
        video_layout.setStretch(1, 0)
        video_layout.setStretch(2, 0)
        
        # Основной лейаут (плейлист слева, видео справа)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.playlist)
        main_layout.addLayout(video_layout, stretch=1)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def setup_connections(self):
        """Подключает сигналы и слоты"""
        # Кнопки управления
        self.controls.prev_button.clicked.connect(self.prev_video)
        self.controls.play_button.clicked.connect(self.play_pause)
        self.controls.next_button.clicked.connect(self.next_video)
        
        # Ползунки
        self.controls.volume_slider.valueChanged.connect(self.player.set_volume)
        self.controls.position_slider.sliderMoved.connect(self.player.set_position)
        
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
        """Глобальные горячие клавиши"""
        # Открыть файл
        QShortcut(QKeySequence("Ctrl+O"), self).activated.connect(self.open_file)
        
        # Полноэкранный режим
        QShortcut(QKeySequence("F"), self).activated.connect(self.toggle_fullscreen)
        QShortcut(QKeySequence("F11"), self).activated.connect(self.toggle_fullscreen)
        QShortcut(QKeySequence("Esc"), self).activated.connect(self.exit_fullscreen)
        
        # Play/Pause
        QShortcut(QKeySequence("Space"), self).activated.connect(self.play_pause)
        QShortcut(QKeySequence("K"), self).activated.connect(self.play_pause)
        
        # Перемотка
        QShortcut(QKeySequence("Right"), self).activated.connect(lambda: self.player.forward(5000))
        QShortcut(QKeySequence("Left"), self).activated.connect(lambda: self.player.backward(5000))
        
        # Навигация по плейлисту
        QShortcut(QKeySequence("N"), self).activated.connect(self.next_video)
        QShortcut(QKeySequence("P"), self).activated.connect(self.prev_video)
        
        # Выход
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)

    # ========== ПОЛНОЭКРАННЫЙ РЕЖИМ ==========
    
    def toggle_fullscreen(self):
        """Переключает полноэкранный режим"""
        if self.isFullScreen():
            self.showNormal()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.playlist.setVisible(True)
            self.video_info.setVisible(True)
            self.controls.set_fullscreen_mode(False)
            if self.cursor_timer:
                self.cursor_timer.stop()
                self.cursor_timer = None
        else:
            self.showFullScreen()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.playlist.setVisible(False)
            self.video_info.setVisible(False)
            self.controls.set_fullscreen_mode(True)
            self.start_cursor_timer()
    
    def exit_fullscreen(self):
        """Выход из полноэкранного режима"""
        if self.isFullScreen():
            self.toggle_fullscreen()
    
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
    
    def mouseMoveEvent(self, event):
        """При движении мыши показываем курсор"""
        if self.isFullScreen():
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self.start_cursor_timer()
        super().mouseMoveEvent(event)
    
    def keyPressEvent(self, event):
        """Резервная обработка клавиш"""
        if event.key() in (Qt.Key.Key_F11, Qt.Key.Key_F):
            self.toggle_fullscreen()
        elif event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)

    # ========== УПРАВЛЕНИЕ ВИДЕО ==========
    
    def open_file(self):
        """Открывает файл через диалоговое окно"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Video", "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv *.flv)"
        )
        if file_name:
            self.load_video(file_name)

    def load_video(self, file_path):
        """Загружает видео файл"""
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
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить видео:\n{file_path}")
    
    def wait_for_duration(self, file_path, attempts=0):
        """Ожидает получения длительности видео"""
        duration = self.player.duration()
        if duration > 0:
            self.video_info.update_info(file_path, duration)
        elif attempts < 20:
            QTimer.singleShot(100, lambda: self.wait_for_duration(file_path, attempts + 1))

    def play_selected_video(self, item):
        """Воспроизводит выбранное из плейлиста видео"""
        row = self.playlist.row(item)
        file_path = self.playlist.get_video_path(row)
        if file_path:
            self.load_video(file_path)

    def play_pause(self):
        """Play/Pause"""
        if self.player.is_playing():
            self.player.pause()
            self.controls.set_play_button_state(False)
        else:
            self.player.play()
            self.controls.set_play_button_state(True)

    def next_video(self):
        """Следующее видео"""
        file_path = self.playlist.next_video()
        if file_path:
            self.load_video(file_path)

    def prev_video(self):
        """Предыдущее видео"""
        file_path = self.playlist.previous_video()
        if file_path:
            self.load_video(file_path)

    def change_speed(self, text):
        """Изменяет скорость воспроизведения"""
        try:
            speed = float(text.replace("x", ""))
            self.player.set_speed(speed)
        except ValueError:
            pass

    def update_position(self, position):
        """Обновляет позицию на ползунке и время"""
        self.controls.position_slider.blockSignals(True)
        self.controls.position_slider.setValue(position)
        self.controls.position_slider.blockSignals(False)
        
        duration = self.player.duration()
        self.controls.update_time_display(position, duration)

    def update_duration(self, duration):
        """Обновляет максимальное значение ползунка"""
        self.controls.position_slider.setRange(0, duration)
        if self.current_file_path and duration > 0:
            self.video_info.update_info(self.current_file_path, duration)

    def on_media_state_changed(self, is_playing):
        """Обновляет состояние кнопки play/pause"""
        self.controls.set_play_button_state(is_playing)

    def handle_player_error(self, error_message):
        """Обрабатывает ошибки плеера"""
        QMessageBox.critical(self, "Ошибка плеера", error_message)

    def closeEvent(self, event):
        """Обработка закрытия окна"""
        if self.cursor_timer:
            self.cursor_timer.stop()
            self.cursor_timer = None
        
        if self.current_file_path:
            position = self.player.get_position()
            self.history.save_video(self.current_file_path, position)
        self.history.close()
        event.accept()