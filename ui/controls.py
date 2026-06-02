from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QSlider,
    QComboBox, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt, QTimer


class ControlsWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setStyleSheet(self._get_styles())

        # Делаем виджет прозрачным
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Для автоматического скрытия в полноэкранном режиме
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.setSingleShot(True)
        self.auto_hide_timer.timeout.connect(self.hide_controls)
        self.is_controls_visible = True

    def setup_ui(self):
        # Кнопки управления
        self.prev_button = QPushButton("⏮️")
        self.play_button = QPushButton("▶️")
        self.next_button = QPushButton("⏭️")
        self.open_button = QPushButton("📂")
        self.fullscreen_button = QPushButton("⛶")

        # Настройка прямоугольных кнопок
        for btn in [self.prev_button, self.play_button, self.next_button,
                    self.open_button, self.fullscreen_button]:
            btn.setFixedSize(50, 36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Ползунки
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 100)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(100)

        # Время
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setMinimumWidth(120)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Скорость
        self.speed_box = QComboBox()
        self.speed_box.addItems(["0.5x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_box.setCurrentText("1.0x")
        self.speed_box.setFixedWidth(75)
        self.speed_box.setFixedHeight(32)

        # Ряд кнопок
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addSpacing(15)
        buttons_layout.addWidget(self.open_button)
        buttons_layout.addWidget(self.fullscreen_button)
        buttons_layout.addStretch()

        # Нижняя панель с ползунками
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.position_slider, stretch=1)
        bottom_layout.addWidget(self.time_label)
        bottom_layout.addWidget(self.speed_box)
        bottom_layout.addWidget(self.volume_slider)

        # Главный лейаут
        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.setContentsMargins(20, 12, 20, 12)
        main_layout.setSpacing(10)

        self.setLayout(main_layout)
        self.setMinimumHeight(90)

    def set_play_button_state(self, is_playing: bool):
        if is_playing:
            self.play_button.setText("⏸️")
        else:
            self.play_button.setText("▶️")

    def _get_styles(self):
        return """
            QWidget {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: 500;
            }
            
            QPushButton:hover {
                background-color: #1db954;
                color: black;
            }
            
            QPushButton:pressed {
                background-color: #1aa34a;
            }
            
            QSlider::groove:horizontal {
                height: 4px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 2px;
            }
            
            QSlider::handle:horizontal {
                background: #1db954;
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            
            QSlider::sub-page:horizontal {
                background: #1db954;
                border-radius: 2px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #1ed760;
            }
            
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                font-weight: 500;
                font-family: 'Segoe UI', 'Monaco', monospace;
            }
            
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 12px;
                font-weight: 500;
            }
            
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 4px;
            }
            
            QComboBox QAbstractItemView::item {
                padding: 6px 10px;
                border-radius: 4px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background-color: #1db954;
                color: black;
            }
        """

    def update_time_display(self, current_ms: int, total_ms: int):
        current_str = self._format_time(current_ms)
        total_str = self._format_time(total_ms)
        self.time_label.setText(f"{current_str} / {total_str}")

    def _format_time(self, ms: int) -> str:
        seconds = ms // 1000
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    # =========================
    # АВТОМАТИЧЕСКОЕ СКРЫТИЕ
    # =========================

    def show_controls(self):
        self.setVisible(True)
        self.is_controls_visible = True

    def hide_controls(self):
        if not self.underMouse():
            self.setVisible(False)
            self.is_controls_visible = False

    def start_hide_timer(self):
        self.auto_hide_timer.start(2000)

    def reset_hide_timer(self):
        if not self.isVisible():
            self.show_controls()
        self.auto_hide_timer.start(2000)

    def stop_hide_timer(self):
        self.auto_hide_timer.stop()

    def set_fullscreen_mode(self, is_fullscreen: bool):
        if is_fullscreen:
            self.show_controls()
            self.start_hide_timer()
        else:
            self.stop_hide_timer()
            self.show_controls()

    def mouseMoveEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'isFullScreen') and self.parent().isFullScreen():
            self.reset_hide_timer()
        super().mouseMoveEvent(event)

    def enterEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'isFullScreen') and self.parent().isFullScreen():
            self.stop_hide_timer()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'isFullScreen') and self.parent().isFullScreen():
            self.start_hide_timer()
        super().leaveEvent(event)
