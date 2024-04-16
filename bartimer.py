import sys
import os
import json
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QMessageBox, QInputDialog, QComboBox, QSpinBox, QFontComboBox, QSlider, QCheckBox
from PySide6.QtCore import QTimer, Qt, QDateTime, QSettings, QUrl
from PySide6.QtGui import QFont
from PySide6.QtMultimedia import QSoundEffect

def resource_path(relative_path):
    """リソースファイルの絶対パスを取得するヘルパーメソッド"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class IntervalTimerManager:
    def __init__(self):
        self.start_time = None
        self.pause_time = None
        self.total_paused_duration = 0

    def start(self):
        self.start_time = QDateTime.currentDateTime()
        self.pause_time = None
        self.total_paused_duration = 0

    def pause(self):
        if self.start_time and not self.pause_time:
            self.pause_time = QDateTime.currentDateTime()

    def resume(self):
        if self.pause_time:
            current_time = QDateTime.currentDateTime()
            self.total_paused_duration += self.pause_time.msecsTo(current_time)
            self.pause_time = None

    def get_elapsed_time(self):
        if not self.start_time:
            return 0
        if self.pause_time:
            return self.pause_time.msecsTo(self.start_time) - self.total_paused_duration
        current_time = QDateTime.currentDateTime()
        return self.start_time.msecsTo(current_time) - self.total_paused_duration

class TimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('bartimer')
        self.presets = {}
        self.timer_bars_count = 0
        self.interval_bars_count = 0
        self.elapsed_time = 0
        self.remaining_timer_duration = 0
        self.remaining_interval_duration = 0
        self.active_timer = None
        self.interval_start_time = None
        self.load_colors()
        self.apply_colors()

        self.alarm_sound = QSoundEffect()
        self.alarm_sound.setSource(QUrl.fromLocalFile(resource_path('alarm.wav')))
        self.alarm_sound.setLoopCount(1)
        self.alarm_sound.setVolume(1.0)

        main_layout = QVBoxLayout()

        self.timer_layout = QHBoxLayout()
        self.timer_layout.setSpacing(1)
        self.timer_layout.setContentsMargins(1, 1, 1, 1)
        self.timer_bars = []
        main_layout.addLayout(self.timer_layout)

        settings_layout = QVBoxLayout()

        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel('Font:'))
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.change_font)
        font_layout.addWidget(self.font_combo)

        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel('Font Size:'))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(1)
        self.font_size_spin.setMaximum(100)
        self.font_size_spin.setValue(24)
        self.font_size_spin.valueChanged.connect(self.change_font_size)
        font_size_layout.addWidget(self.font_size_spin)

        settings_layout.addLayout(font_layout)
        settings_layout.addLayout(font_size_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #333333;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #444444;
                color: #ffffff;
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QProgressBar {
                background-color: #444444;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #666600;
            }
        """)

        main_layout = QVBoxLayout()

        self.timer_layout = QHBoxLayout()
        self.timer_layout.setSpacing(1)
        self.timer_layout.setContentsMargins(1, 1, 1, 1)
        self.timer_bars = []
        main_layout.addLayout(self.timer_layout)

        settings_layout = QVBoxLayout()
        timer_duration_layout = QHBoxLayout()
        timer_duration_layout.addWidget(QLabel('Timer Duration:'))
        self.timer_hours_input = QLineEdit()
        self.timer_hours_input.setPlaceholderText('HH')
        timer_duration_layout.addWidget(self.timer_hours_input)
        self.timer_minutes_input = QLineEdit()
        self.timer_minutes_input.setPlaceholderText('MM')
        timer_duration_layout.addWidget(self.timer_minutes_input)
        self.timer_seconds_input = QLineEdit()
        self.timer_seconds_input.setPlaceholderText('SS')
        timer_duration_layout.addWidget(self.timer_seconds_input)
        settings_layout.addLayout(timer_duration_layout)

        self.remaining_time_label = QLabel('Remaining Time: 00:00:00', self)
        self.remaining_time_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.remaining_time_label)

        settings_layout.addWidget(QLabel('Timer Bars'))
        self.timer_bars_input = QLineEdit()
        settings_layout.addWidget(self.timer_bars_input)

        interval_duration_layout = QHBoxLayout()
        interval_duration_layout.addWidget(QLabel('Interval Duration:'))
        self.interval_hours_input = QLineEdit()
        self.interval_hours_input.setPlaceholderText('HH')
        interval_duration_layout.addWidget(self.interval_hours_input)
        self.interval_minutes_input = QLineEdit()
        self.interval_minutes_input.setPlaceholderText('MM')
        interval_duration_layout.addWidget(self.interval_minutes_input)
        self.interval_seconds_input = QLineEdit()
        self.interval_seconds_input.setPlaceholderText('SS')
        interval_duration_layout.addWidget(self.interval_seconds_input)
        settings_layout.addLayout(interval_duration_layout)

        settings_layout.addWidget(QLabel('Interval Bars'))
        self.interval_bars_input = QLineEdit()
        settings_layout.addWidget(self.interval_bars_input)

        button_layout = QHBoxLayout()
        start_button = QPushButton('Start')
        start_button.clicked.connect(self.start_timer)
        button_layout.addWidget(start_button)
        stop_button = QPushButton('Stop')
        stop_button.clicked.connect(self.stop_timer)
        button_layout.addWidget(stop_button)
        settings_layout.addLayout(button_layout)
        resume_button = QPushButton('Resume')
        resume_button.clicked.connect(self.resume_timer)
        button_layout.addWidget(resume_button)

        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel('Font:'))
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.change_font)
        font_layout.addWidget(self.font_combo)

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel('Alarm Volume:'))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.change_volume)
        volume_layout.addWidget(self.volume_slider)
        settings_layout.addLayout(volume_layout)

        self.alarm_enabled_checkbox = QCheckBox('Enable Alarm')
        self.alarm_enabled_checkbox.setChecked(True)
        settings_layout.addWidget(self.alarm_enabled_checkbox)
        font_size_layout = QHBoxLayout()
        font_size_layout.addWidget(QLabel('Font Size:'))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(1)
        self.font_size_spin.setMaximum(100)
        self.font_size_spin.setValue(12)
        self.font_size_spin.valueChanged.connect(self.change_font_size)
        font_size_layout.addWidget(self.font_size_spin)

        settings_layout.addLayout(font_layout)
        settings_layout.addLayout(font_size_layout)

        preset_layout = QHBoxLayout()
        self.preset_buttons = []
        for i in range(1, 6):
            preset_button = QPushButton(f'Preset {i}')
            preset_button.clicked.connect(lambda _, i=i: self.load_preset(i))
            preset_layout.addWidget(preset_button)
            self.preset_buttons.append(preset_button)
        settings_layout.addLayout(preset_layout)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_preset)
        settings_layout.addWidget(save_button)

        main_layout.addLayout(settings_layout)
        self.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.interval_timer = QTimer()
        self.interval_timer.timeout.connect(self.update_interval)

        self.settings = QSettings('TimerApp', 'Settings')
        self.load_window_settings()
        self.load_presets()
        self.load_last_preset()

    def change_volume(self, value):
        self.alarm_sound.setVolume(value / 100)

    def change_font(self, font):
        font.setPointSize(self.font_size_spin.value())
        self.remaining_time_label.setFont(font)

    def change_font_size(self, font_size):
        font = self.remaining_time_label.font()
        font.setPointSize(font_size)
        self.remaining_time_label.setFont(font)

    def get_presets_file_path(self):
        config_dir = os.path.join(os.path.expanduser('~'), '.bartimer')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        return os.path.join(config_dir, 'presets.json')

    def save_presets(self):
        presets_path = self.get_presets_file_path()
        try:
            with open(presets_path, 'w') as file:
                json.dump(self.presets, file)
        except IOError as e:
            QMessageBox.warning(self, 'Save Error', f'Failed to save presets: {e}')

    def load_presets(self):
        presets_path = self.get_presets_file_path()
        try:
            with open(presets_path, 'r') as file:
                self.presets = json.load(file)
                for preset_number in self.presets:
                    self.preset_buttons[int(preset_number) - 1].setEnabled(True)
        except FileNotFoundError:
            self.presets = {}
            for preset_button in self.preset_buttons:
                preset_button.setEnabled(False)

    def load_colors(self):
        colors_path = resource_path('colors.json')
        try:
            with open(colors_path, 'r') as file:
                self.colors = json.load(file)
        except FileNotFoundError:
            self.colors = {
                "background_color": "#333333",
                "text_color": "#ffffff",
                "input_background_color": "#444444",
                "input_text_color": "#ffffff",
                "button_background_color": "#555555",
                "button_hover_color": "#666666",
                "progress_bar_background_color": "#444444",
                "progress_bar_border_color": "#555555",
                "progress_bar_chunk_color": "#666600",
                "progress_bar_chunk_color_int": "#ff0000"
            }

    def apply_colors(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {self.colors['background_color']};
                color: {self.colors['text_color']};
            }}
            QLineEdit {{
                background-color: {self.colors['input_background_color']};
                color: {self.colors['input_text_color']};
            }}
            QPushButton {{
                background-color: {self.colors['button_background_color']};
                color: {self.colors['text_color']};
            }}
            QPushButton:hover {{
                background-color: {self.colors['button_hover_color']};
            }}
            QProgressBar {{
                background-color: {self.colors['progress_bar_background_color']};
                border: 1px solid {self.colors['progress_bar_border_color']};
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {self.colors['progress_bar_chunk_color']};
            }}
        """)

    def start_timer(self):
        try:
            self.elapsed_time = 0
            self.start_time = QDateTime.currentDateTime()
            timer_hours = int(self.timer_hours_input.text())
            timer_minutes = int(self.timer_minutes_input.text())
            timer_seconds = int(self.timer_seconds_input.text())

            # 時間、分、秒の最大値をチェック
            if timer_hours > 999:
                raise ValueError("Hours cannot exceed 999.")
            if timer_minutes > 59:
                raise ValueError("Minutes cannot exceed 59.")
            if timer_seconds > 59:
                raise ValueError("Seconds cannot exceed 59.")

            self.timer_duration = (timer_hours * 3600 + timer_minutes * 60 + timer_seconds) * 1000
            self.remaining_timer_duration = self.timer_duration  # タイマーの残り時間を更新
            self.timer_bars_count = int(self.timer_bars_input.text())

            interval_hours = int(self.interval_hours_input.text())
            interval_minutes = int(self.interval_minutes_input.text())
            interval_seconds = int(self.interval_seconds_input.text())

            # 時間、分、秒の最大値をチェック
            if interval_hours > 999:
                raise ValueError("Hours cannot exceed 999.")
            if interval_minutes > 59:
                raise ValueError("Minutes cannot exceed 59.")
            if interval_seconds > 59:
                raise ValueError("Seconds cannot exceed 59.")

            self.interval_duration = (interval_hours * 3600 + interval_minutes * 60 + interval_seconds) * 1000
            self.remaining_interval_duration = self.interval_duration  # インターバルの残り時間を更新
            self.interval_bars_count = int(self.interval_bars_input.text())
            self.interval_start_time = None  # インターバルタイマーの開始時刻を初期化
            self.interval_manager = IntervalTimerManager()

            self.create_timer_bars(self.timer_bars_count)
            self.current_timer_bar = 0
            self.current_interval_bar = 0
            self.timer.start(self.remaining_timer_duration // (self.timer_bars_count * 100))
            self.update_remaining_time_display()  # タイマー開始時に残り時間を更新
            self.active_timer = 'timer'

            # タイマーバーの色を設定
            for bar in self.timer_bars:
                bar.setStyleSheet(f"""
                    QProgressBar::chunk {{
                        background-color: {self.colors['progress_bar_chunk_color']};
                    }}
                """)

            # インターバルタイマーが0秒の場合、インターバルをスキップしてタイマーを繰り返す
            if self.interval_duration == 0:
                self.interval_bars_count = 0

                for bar in self.timer_bars:
                    bar.setStyleSheet(f"""
                        QProgressBar::chunk {{
                            background-color: {self.colors['progress_bar_chunk_color']};
                        }}
                    """)

        except ValueError as e:
            QMessageBox.warning(self, 'Invalid Input', str(e))

    def stop_timer(self):
        if self.active_timer == 'timer' and self.timer.isActive():
            self.timer.stop()
            self.remaining_timer_duration = max(self.remaining_timer_duration, 0)
        elif self.active_timer == 'interval' and self.interval_timer.isActive():
            self.interval_timer.stop()
            self.remaining_interval_duration = max(self.remaining_interval_duration, 0)
            self.interval_start_time = None  # インターバルタイマーの開始時刻をNoneに設定
            self.interval_manager.pause()  # インターバルマネージャを一時停止
        self.update_remaining_time_display()

    def resume_timer(self):
        if self.active_timer == 'timer' and not self.timer.isActive():
            self.timer.start(self.remaining_timer_duration // (self.timer_bars_count * 100))
        elif self.active_timer == 'interval' and not self.interval_timer.isActive():
            self.interval_manager.resume()  # インターバルマネージャを再開
            elapsed_time = self.interval_manager.get_elapsed_time()
            self.remaining_interval_duration = max(self.interval_duration - elapsed_time, 0)
            # 残り時間に基づいてインターバルを再計算
            interval = max(1, self.remaining_interval_duration // (self.interval_bars_count * 100))
            self.interval_timer.start(interval)
            self.interval_timer.setInterval(interval)
        self.update_remaining_time_display()

    def create_timer_bars(self, bars_count):
        # 既存のバーを削除
        for bar in self.timer_bars:
            self.timer_layout.removeWidget(bar)
            bar.deleteLater()
        self.timer_bars.clear()

        # 新しいバーを作成
        for i in range(bars_count):
            bar = QProgressBar()
            bar.setOrientation(Qt.Vertical)
            bar.setMinimum(0)
            bar.setMaximum(100)
            self.timer_layout.addWidget(bar)
            self.timer_bars.append(bar)

        # タイマーの切り替わり時にもウィンドウの現在のサイズに基づいてバーのサイズを更新
        QTimer.singleShot(0, self.update_timer_bars)

    def update_timer_bars(self):
        # プログレスバーが一つもない場合は、処理をスキップ
        if not self.timer_bars:
            return

        layout_width = self.timer_layout.contentsRect().width()
        spacing_width = self.timer_layout.spacing() * (len(self.timer_bars) - 1)
        # len(self.timer_bars)が0でないことが保証されているため、ZeroDivisionErrorは発生しない
        bar_width = max((layout_width - spacing_width) // len(self.timer_bars), 1)
        for bar in self.timer_bars:
            bar.setFixedWidth(bar_width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_timer_bars()

    def update_timer(self):
        if self.current_timer_bar < self.timer_bars_count:
            self.timer_bars[self.current_timer_bar].setValue(self.timer_bars[self.current_timer_bar].value() + 1)
            if self.timer_bars[self.current_timer_bar].value() == 100:
                self.current_timer_bar += 1
                if self.current_timer_bar == self.timer_bars_count:
                    self.timer.stop()

                if self.current_timer_bar == self.timer_bars_count:
                    self.timer.stop()

                    # インターバルタイマーが0秒の場合、インターバルをスキップしてタイマーを繰り返す
                    if self.interval_duration == 0:
                        if self.alarm_enabled_checkbox.isChecked():
                            self.alarm_sound.play()
                        self.current_timer_bar = 0
                        self.create_timer_bars(self.timer_bars_count)
                        self.update_timer_bars()
                        self.remaining_timer_duration = self.timer_duration
                        self.timer.start(self.remaining_timer_duration // (self.timer_bars_count * 100))
                        self.active_timer = 'timer'

                        # タイマーバーの色を設定
                        for bar in self.timer_bars:
                            bar.setStyleSheet(f"""
                                QProgressBar::chunk {{
                                    background-color: {self.colors['progress_bar_chunk_color']};
                                }}
                            """)
                    else:
                        if self.alarm_enabled_checkbox.isChecked():
                            self.alarm_sound.play()
                        self.current_interval_bar = 0
                        self.create_timer_bars(self.interval_bars_count)
                        self.update_timer_bars()
                        self.remaining_interval_duration = self.interval_duration
                        interval = self.remaining_interval_duration // (self.interval_bars_count * 100)
                        self.interval_timer.start(interval)
                        self.interval_start_time = QDateTime.currentDateTime()  # インターバルタイマーの開始時刻を更新
                        self.interval_manager.start()  # インターバルマネージャの開始時刻も更新
                        self.interval_timer.setInterval(interval)
                        self.active_timer = 'interval'
                        for bar in self.timer_bars:
                            bar.setStyleSheet(f"""
                                QProgressBar::chunk {{
                                    background-color: {self.colors['progress_bar_chunk_color_int']};
                                }}
                            """)

        self.remaining_timer_duration = max(self.remaining_timer_duration - self.timer.interval(), 0)
        self.update_remaining_time_display()

    def update_interval(self):
        if self.current_interval_bar < self.interval_bars_count:
            self.timer_bars[self.current_interval_bar].setValue(self.timer_bars[self.current_interval_bar].value() + 1)
            if self.timer_bars[self.current_interval_bar].value() == 100:
                self.current_interval_bar += 1
                if self.current_interval_bar == self.interval_bars_count:
                    self.interval_timer.stop()
                    if self.alarm_enabled_checkbox.isChecked():
                        self.alarm_sound.play()
                    self.current_timer_bar = 0
                    self.create_timer_bars(self.timer_bars_count)
                    self.update_timer_bars()
                    self.remaining_timer_duration = self.timer_duration
                    self.timer.start(self.remaining_timer_duration // (self.timer_bars_count * 100))
                    self.active_timer = 'timer'
                    for bar in self.timer_bars:
                        bar.setStyleSheet(f"""
                            QProgressBar::chunk {{
                                background-color: {self.colors['progress_bar_chunk_color']};
                            }}
                        """)
        
        elapsed_time = self.interval_manager.get_elapsed_time()
        self.remaining_interval_duration = max(self.interval_duration - elapsed_time, 0)
        self.update_remaining_time_display()

    def update_remaining_time_display(self):
        if self.active_timer == 'timer':
            remaining_time_ms = max(self.remaining_timer_duration, 0)
        elif self.active_timer == 'interval':
            remaining_time_ms = max(self.remaining_interval_duration, 0)
        else:
            self.remaining_time_label.setText('Remaining Time: 00:00:00.000')
            return

        # 残り時間をミリ秒、秒、分、時間に変換
        remaining_time_s, milliseconds = divmod(remaining_time_ms, 1000)
        hours, remainder = divmod(remaining_time_s, 3600)
        minutes, seconds = divmod(remainder, 60)

        # ラベルを更新
        self.remaining_time_label.setText(f'Remaining Time: {hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}')

    def load_preset(self, preset_number):
        if str(preset_number) in self.presets:
            preset = self.presets[str(preset_number)]
            self.timer_hours_input.setText(str(preset['timer_hours']))
            self.timer_minutes_input.setText(str(preset['timer_minutes']))
            self.timer_seconds_input.setText(str(preset['timer_seconds']))
            self.timer_bars_input.setText(str(preset['timer_bars']))
            self.interval_hours_input.setText(str(preset['interval_hours']))
            self.interval_minutes_input.setText(str(preset['interval_minutes']))
            self.interval_seconds_input.setText(str(preset['interval_seconds']))
            self.interval_bars_input.setText(str(preset['interval_bars']))

    def save_preset(self):
        preset_number, ok = QInputDialog.getInt(self, 'Save Preset', 'Enter preset number (1-5):', minValue=1, maxValue=5)
        if ok:
            try:
                timer_hours = int(self.timer_hours_input.text())
                timer_minutes = int(self.timer_minutes_input.text())
                timer_seconds = int(self.timer_seconds_input.text())
                interval_hours = int(self.interval_hours_input.text())
                interval_minutes = int(self.interval_minutes_input.text())
                interval_seconds = int(self.interval_seconds_input.text())

                # 時間、分、秒の最大値をチェック
                if timer_hours > 999 or interval_hours > 999:
                    raise ValueError("Hours cannot exceed 999.")
                if timer_minutes > 59 or interval_minutes > 59:
                    raise ValueError("Minutes cannot exceed 59.")
                if timer_seconds > 59 or interval_seconds > 59:
                    raise ValueError("Seconds cannot exceed 59.")

                self.presets[str(preset_number)] = {
                    'timer_hours': timer_hours,
                    'timer_minutes': timer_minutes,
                    'timer_seconds': timer_seconds,
                    'timer_bars': int(self.timer_bars_input.text()),
                    'interval_hours': interval_hours,
                    'interval_minutes': interval_minutes,
                    'interval_seconds': interval_seconds,
                    'interval_bars': int(self.interval_bars_input.text())
                }
                self.save_presets()
                self.preset_buttons[preset_number - 1].setEnabled(True)
            except ValueError as e:
                QMessageBox.warning(self, 'Invalid Input', str(e))

    def load_last_preset(self):
        last_preset = self.settings.value('last_preset')
        if last_preset:
            self.load_preset(int(last_preset))

    def closeEvent(self, event):
        self.save_window_settings()
        try:
            current_preset = {
                'timer_hours': int(self.timer_hours_input.text()),
                'timer_minutes': int(self.timer_minutes_input.text()),
                'timer_seconds': int(self.timer_seconds_input.text()),
                'timer_bars': int(self.timer_bars_input.text()),
                'interval_hours': int(self.interval_hours_input.text()),
                'interval_minutes': int(self.interval_minutes_input.text()),
                'interval_seconds': int(self.interval_seconds_input.text()),
                'interval_bars': int(self.interval_bars_input.text())
            }
            # 値の検証を追加
            for key in ['timer_hours', 'interval_hours']:
                if current_preset[key] > 999:
                    raise ValueError(f"{key} cannot exceed 999.")
            for key in ['timer_minutes', 'timer_seconds', 'interval_minutes', 'interval_seconds']:
                if current_preset[key] > 59:
                    raise ValueError(f"{key} cannot exceed 59.")
            
            last_preset = None
            for preset_number, preset in self.presets.items():
                if preset == current_preset:
                    last_preset = preset_number
                    break
            if last_preset is None:
                last_preset = len(self.presets) + 1
                self.presets[str(last_preset)] = current_preset
                self.save_presets()
            self.settings.setValue('last_preset', last_preset)
        except ValueError as e:
            QMessageBox.warning(self, 'Invalid Input', str(e))
            event.ignore()
            return
        event.accept()

    def save_window_settings(self):
        self.settings.setValue('window_geometry', self.saveGeometry())
        self.settings.setValue('font', self.font_combo.currentFont().toString())
        self.settings.setValue('font_size', self.font_size_spin.value())

    def load_window_settings(self):
        geometry = self.settings.value('window_geometry')
        if geometry:
            self.restoreGeometry(geometry)
        font_string = self.settings.value('font')
        if font_string:
            font = QFont()
            font.fromString(font_string)
            self.font_combo.setCurrentFont(font)
            self.change_font(font)
        font_size = self.settings.value('font_size')
        if font_size:
            self.font_size_spin.setValue(int(font_size))
        self.change_font_size(int(font_size))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer_app = TimerApp()
    timer_app.show()
    sys.exit(app.exec())