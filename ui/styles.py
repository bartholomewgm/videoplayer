STYLE = """
QMainWindow {
    background-color: #000000;
}

QWidget {
    background-color: transparent;
    color: #ffffff;
    font-family: 'Segoe UI', 'Inter', sans-serif;
}

QMenuBar {
    background-color: rgba(18, 18, 18, 200);
    color: white;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

QMenuBar::item:selected {
    background-color: #1db954;
    color: black;
}

QMenu {
    background-color: rgba(30, 30, 35, 220);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
}

QMenu::item:selected {
    background-color: #1db954;
    color: black;
}

QScrollBar:vertical {
    background: rgba(18, 18, 18, 150);
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    min-height: 40px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 0.5);
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
"""
