"""
Панель управления видеоплеером
Содержит кнопки: Prev, Play/Pause, Next
"""

from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QSlider, 
    QComboBox, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from pathlib import Path


class ControlsWidget(QWidget):
    """Виджет панели управления"""

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_icons()
        self.setStyleSheet(self._get_styles())
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.setSingleShot(True)
        self.auto_hide_timer.timeout.connect(self.hide_controls)
        self.is_controls_visible = True

    def setup_ui(self):
        """Создаёт элементы интерфейса"""
        # ===== КНОПКИ =====
        self.prev_button = QPushButton()
        self.play_button = QPushButton()
        self.next_button = QPushButton()
        
        for btn in [self.prev_button, self.play_button, self.next_button]:
            btn.setFixedSize(50, 36)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # ===== ПОЛЗУНКИ =====
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 100)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(100)
        
        # ===== ВРЕМЯ =====
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setMinimumWidth(120)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # ===== СКОРОСТЬ =====
        self.speed_box = QComboBox()
        self.speed_box.addItems(["0.5x", "1.0x", "1.25x", "1.5x", "2.0x"])
        self.speed_box.setCurrentText("1.0x")
        self.speed_box.setFixedWidth(75)
        self.speed_box.setFixedHeight(32)
        
        # ===== ЛЕЙАУТ =====
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addStretch()
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.position_slider, stretch=1)
        bottom_layout.addWidget(self.time_label)
        bottom_layout.addWidget(self.speed_box)
        bottom_layout.addWidget(self.volume_slider)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.setContentsMargins(20, 12, 20, 12)
        main_layout.setSpacing(10)
        
        self.setLayout(main_layout)
        self.setMinimumHeight(90)

    def setup_icons(self):
        """Загружает иконки из папки icons"""
        icons_dir = Path(__file__).parent.parent / "icons"
        
        self.play_icon_path = icons_dir / "play.png"
        self.pause_icon_path = icons_dir / "pause.png"
        
        # Загружаем иконки
        icon_map = {
            self.prev_button: "previous.png",
            self.next_button: "next.png",
        }
        
        for button, filename in icon_map.items():
            icon_path = icons_dir / filename
            if icon_path.exists():
                button.setIcon(QIcon(str(icon_path)))
                button.setIconSize(Qt.QSize(24, 24))
        
        # Play/Pause
        if self.play_icon_path.exists():
            self.play_button.setIcon(QIcon(str(self.play_icon_path)))
            self.play_button.setIconSize(Qt.QSize(24, 24))

    def set_play_button_state(self, is_playing: bool):
        """Меняет иконку play/pause"""
        if is_playing:
            if self.pause_icon_path and self.pause_icon_path.exists():
                self.play_button.setIcon(QIcon(str(self.pause_icon_path)))
            else:
                self.play_button.setText("⏸️")
        else:
            if self.play_icon_path and self.play_icon_path.exists():
                self.play_button.setIcon(QIcon(str(self.play_icon_path)))
            else:
                self.play_button.setText("▶️")

    def _get_styles(self):
        """CSS стили"""
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
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                font-weight: 500;
                font-family: 'Segoe UI', monospace;
            }
            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 12px;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #1db954;
                color: black;
            }
        """

    def update_time_display(self, current_ms: int, total_ms: int):
        """Обновляет время"""
        current_str = self._format_time(current_ms)
        total_str = self._format_time(total_ms)
        self.time_label.setText(f"{current_str} / {total_str}")
    
    def _format_time(self, ms: int) -> str:
        seconds = ms // 1000
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    # ===== АВТОСКРЫТИЕ =====
    
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