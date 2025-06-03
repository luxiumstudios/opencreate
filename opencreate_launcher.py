import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QBrush, QPainterPath
from PyQt5.QtCore import Qt
from functools import partial

# Map app names to their launch commands and icon files
APPS = {
    "Inkscape": {"cmd": "inkscape", "icon": "inkscape.png"},
    "GIMP": {"cmd": "gimp", "icon": "gimp.png"},
    "Shotcut": {"cmd": "shotcut", "icon": "shotcut.png"},
    "Blender": {"cmd": "blender", "icon": "blender.png"},
    "Kdenlive": {"cmd": "kdenlive", "icon": "kdenlive.png"},
}

def rounded_pixmap(pixmap, radius):
    size = pixmap.size()
    mask = QPixmap(size)
    mask.fill(Qt.transparent)
    painter = QPainter(mask)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0.5, 0.5, size.width()-1, size.height()-1, radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return mask

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("openCreate")
        self.setFixedSize(240, 240)
        self.setWindowIcon(QIcon(APPS["Inkscape"]["icon"]))
        self.setStyleSheet("background-color: #080707;")
        self.init_ui()

    def init_ui(self):
        # Featured app section
        featured_label = QLabel("Featured: Inkscape")
        featured_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px; color: #fff;")

        # Icon and RUN button side by side, bottom-aligned
        icon_and_button_layout = QHBoxLayout()
        icon_and_button_layout.setContentsMargins(0, 0, 0, 0)
        icon_and_button_layout.setSpacing(12)

        # Use ClickableLabel for the featured icon
        featured_icon = ClickableLabel("Inkscape")
        pixmap = QPixmap(APPS["Inkscape"]["icon"]).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        featured_icon.setPixmap(pixmap)
        featured_icon.setFixedSize(70, 70)
        featured_icon.setStyleSheet("border: 1px solid #222; background: #181818;")
        featured_icon.setToolTip("Launch Inkscape")
        featured_icon.clicked.connect(lambda: self.launch_app("Inkscape"))

        run_btn = QPushButton("RUN")
        run_btn.setStyleSheet("""
            background: #4caf50; color: #fff; border: none; border-radius: 8px;
            padding: 10px 28px; font-size: 1.1rem; font-weight: bold;
        """)
        run_btn.setFixedHeight(38)
        run_btn.clicked.connect(lambda: self.launch_app("Inkscape"))

        # Add icon and button, both bottom-aligned
        icon_and_button_layout.addWidget(featured_icon, alignment=Qt.AlignBottom)
        icon_and_button_layout.addWidget(run_btn, alignment=Qt.AlignBottom)
        icon_and_button_layout.addStretch()

        # Stack label above icon+button
        featured_section = QVBoxLayout()
        featured_section.setContentsMargins(0, 0, 0, 0)
        featured_section.addWidget(featured_label)
        featured_section.addLayout(icon_and_button_layout)

        # Other apps section
        other_label = QLabel("Other apps")
        other_label.setStyleSheet("font-size: 13px; color: #aaa; margin-bottom: 8px;")

        other_icons_layout = QHBoxLayout()
        other_icons_layout.setContentsMargins(0, 0, 0, 0)
        other_icons_layout.setSpacing(12)
        for app in ["GIMP", "Shotcut", "Blender", "Kdenlive"]:
            icon_label = ClickableLabel(app)
            pixmap = QPixmap(APPS[app]["icon"]).scaled(38, 38, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(38, 38)
            icon_label.setStyleSheet("""
                border: 1px solid #222; background: #181818;
                margin-right: 0px;
            """)
            icon_label.setToolTip(f"Launch {app}")
            icon_label.clicked.connect(partial(self.launch_app, app))
            other_icons_layout.addWidget(icon_label, alignment=Qt.AlignBottom)

        # Layout to align the bottom of icons with the RUN button
        bottom_align_layout = QHBoxLayout()
        bottom_align_layout.addLayout(other_icons_layout)
        bottom_align_layout.addStretch()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.addLayout(featured_section)
        main_layout.addSpacing(30)
        main_layout.addWidget(other_label)
        main_layout.addLayout(bottom_align_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def launch_app(self, app_name):
        cmd = APPS[app_name]["cmd"]
        try:
            subprocess.Popen([cmd])
        except FileNotFoundError:
            QMessageBox.warning(self, "Not found", f"{app_name} is not installed or not in PATH.")

class ClickableLabel(QLabel):
    from PyQt5.QtCore import pyqtSignal
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QToolTip { color: #fff; background-color: #222; border: 1px solid #555; }")
    win = Launcher()
    win.show()
    sys.exit(app.exec_()) 