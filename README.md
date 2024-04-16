Please scroll down for the English readme.

bartimer は、カスタマイズ可能なタイマーとインターバルタイマー機能を備えたシンプルで使いやすいデスクトップアプリケーションです。

![スクリーンショット 2024-04-16 183257](https://github.com/willailora/bartimer/assets/166263028/ce7ba0ac-9e7e-4fe0-a9fc-6dfd0bed5e84)

特徴

    カスタマイズ可能なタイマー時間とインターバル時間の設定
    タイマーとインターバルのプログレスバーによる視覚的なフィードバック
    プリセット機能による設定の保存と呼び出し
    アラーム音の再生とボリューム調整
    フォントとフォントサイズの変更
    ウィンドウ設定の保存と復元
    最後に使用したプリセットの自動保存と読み込み

使い方

    タイマー時間とインターバル時間を設定します。時間(最大999)、分(最大59)、秒(最大59)を入力してください。
    タイマーとインターバルのプログレスバーの数を設定します。
    「Start」ボタンをクリックしてタイマーを開始します。
    「Stop」ボタンをクリックしてタイマーを一時停止します。
    「Resume」ボタンをクリックして一時停止したタイマーを再開します。
    プリセットを保存するには、「Save」ボタンをクリックし、プリセット番号（1〜5）を入力します。
    保存したプリセットを呼び出すには、対応するプリセットボタンをクリックします。
    プリセットは
    C:\Users\ユーザーネーム\.bartimer\
    にpresets.jsonとして保存されますので、直接編集も可能です。
    同梱のpresets.jsonを配置すれば、おすすめの設定が読み込できます。
    
    インターバルタイマーの時間・分・秒の設定を0にしてる場合は、タイマーを繰り返します。
    
    ウィンドウをドラッグアンドドロップすると、バーのサイズが横にも縦にも伸びます。アプリを起動して、スタートを押した後は、横方向に伸ばすことは出来ますが、縮めることはできなくなります。縦は何時でも変更可能です。横方向に縮めたい場合は、一旦アプリを閉じた後に、アプリを起動してスタートを押す前に変更してください。

同梱のプリセットの説明

    Preset1は所謂ポモドーロメソッド用のプリセットになっています。25分集中して、5分休憩する方法です。
    Preset2は5分間のタイマーを繰り返します。これはアンナ・レンブケ教授(スタンフォード大学医学部教授)のドーパミン中毒を改善するためのメソッド用のプリセットです。5分毎に何に集中していても、5分で別のことに切り替える訓練に使用します。
    Preset3は50分仕事をして10分休憩するというような場合に使用してください。
    Preset4は1時間毎にタイマーとインターバルが切り替わるだけです。
    Preset5は3秒に設定してあるので、アラーム音の確認などに使用してください。
    このプリセットをもとに自身が使いやすいようにカスタイマイズしてください。

設定

    フォントとフォントサイズを変更するには、対応するドロップダウンメニューとスピンボックスを使用します。
    アラーム音のボリュームを調整するには、ボリュームスライダーを使用します。
    アラーム音を有効または無効にするには、「Enable Alarm」チェックボックスを使用します。
    アラーム音を変更したい場合は、インストールフォルダにあるalarm.wavを同じ名前で差し替えてください。
    デフォルトのalarm.wavは
    https://otosozai.com/
    otosozai.com様のお知らせ音(かわいい)se_30101を使用しています。
    githubにはexe版以外ではalarm.wavは用意していませんので、ご自分でご用意ください。
    
    インストールフォルダにあるcolors.jsonを編集すると、様々なカラーを変更可能です。デフォルトはダークテーマっぽくしてあります。
    "progress_bar_background_color": "#444444",進行バーの背景色です。
    "progress_bar_border_color": "#555555",進行バーの縁取りの色です。
    "progress_bar_chunk_color": "#996633",通常のタイマーの進行バーの色です。
    "progress_bar_chunk_color_int": "#999900"インターバルタイマーのの進行バーの色です。

要件

    exe版はwindows10以上
    
    Python版は
    Python 3.6 以上
    PySide6

インストール

    exe版はダウンロードしたbartimer.zipを解凍してください。必要に応じて、解凍したフォルダに有るpresets.jsonをC:\Users\ユーザーネーム\.bartimerに保存してください。フォルダは一度起動して、適当な数値で一度プリセットをsaveすれば作成されます。

    リポジトリをクローンまたはダウンロードします。
    必要なライブラリをインストールします: pip install PySide6
    アプリケーションを起動します: python bartimer.py
    presets.jsonをC:\Users\ユーザーネーム\.bartimerに保存してください。フォルダは一度起動して、適当な数値で一度プリセットをsaveすれば作成されます。
    Python版はwindows以外でも使用できるはずですが、動作確認はしておりません。また、preset.jsonの保存フォルダもOSによって変わってくるはずです。

ライセンス
このプロジェクトはLGPLv3ライセンスの下で公開されています。

貢献
バグ報告、プルリクエストを歓迎します。

ドネーションをしてくれる方は以下のURLからお願いします。
https://ko-fi.com/ailorawill
<a href='https://ko-fi.com/M4M1WZ04Y' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

連絡先
プロジェクトに関する質問やコメントがある場合は、https://x.com/plionplionか、Discordで@willlionまでご連絡ください。

以下は英語用のReadmeです。

bartimer is a simple and user-friendly desktop application that provides customizable timer and interval timer functionality. Features

    Customizable timer and interval durations
    Visual feedback with progress bars for timer and interval
    Preset functionality to save and recall settings
    Alarm sound playback and volume adjustment
    Ability to change font and font size
    Saving and restoring window settings
    Automatic saving and loading of the last used preset

Usage

    Set the timer and interval durations. Enter hours (max 999), minutes (max 59), and seconds (max 59).
    Set the number of progress bars for the timer and interval.
    Click the "Start" button to begin the timer.
    Click the "Stop" button to pause the timer.
    Click the "Resume" button to resume a paused timer.
    To save a preset, click the "Save" button and enter a preset number (1-5).
    To recall a saved preset, click the corresponding preset button.
    Presets are saved as presets.json in C:\Users\username.bartimer, so you can edit them directly. If you place the included presets.json, you can load recommended settings.
    If the interval timer's hours, minutes, and seconds are set to 0, the timer will repeat.
    Dragging and dropping the window will stretch the bar size both horizontally and vertically. After launching the app and pressing start, you can stretch it horizontally but not shrink it. Vertical resizing is always possible. If you want to shrink it horizontally, close the app once, then change it before launching the app and pressing start.

Explanation of included presets

    Preset1 is a preset for the so-called Pomodoro method. It's a method of focusing for 25 minutes and taking a 5-minute break.
    Preset2 repeats a 5-minute timer. This is a preset for Professor Anna Lembke's (Stanford University School of Medicine) method for improving dopamine addiction. It is used to train switching to something else every 5 minutes, no matter what you are focusing on.
    Preset3 is for when you want to work for 50 minutes and take a 10-minute break.
    Preset4 simply switches between timer and interval every hour.
    Preset5 is set to 3 seconds, so use it to check the alarm sound, etc.
    Customize these presets to make them easier for you to use.

Settings

    To change the font and font size, use the corresponding dropdown menus and spinboxes.
    To adjust the volume of the alarm sound, use the volume slider.
    To enable or disable the alarm sound, use the "Enable Alarm" checkbox.
    If you want to change the alarm sound, replace the alarm.wav in the installation folder with the same name.
    The default alarm.wav uses the notification sound (cute) se_30101 from otosozai.com.
    alarm.wav is not provided on GitHub except for the exe version, so please prepare it yourself.
    By editing the colors.json in the installation folder, you can change various colors. The default is set to a dark theme-like appearance.
        "progress_bar_background_color": "#444444" is the background color of the progress bar.
        "progress_bar_border_color": "#555555" is the color of the border of the progress bar.
        "progress_bar_chunk_color": "#996633" is the color of the progress bar for the normal timer.
        "progress_bar_chunk_color_int": "#999900" is the color of the progress bar for the interval timer.

Requirements

    exe version: Windows 10 or later
    Python version:
        Python 3.6 or later
        PySide6

Installation

    For the exe version, extract the downloaded bartimer.zip. If necessary, save the presets.json in the extracted folder to C:\Users\username.bartimer. The folder will be created if you launch the app once and save a preset with appropriate values.
    Clone or download the repository.
    Install the required libraries: pip install PySide6
    Launch the application: python bartimer.py
    Save presets.json to C:\Users\username.bartimer. The folder will be created if you launch the app once and save a preset with appropriate values.
    The Python version should work on platforms other than Windows, but it has not been tested. Also, the folder for saving preset.json will likely change depending on the OS.

License
This project is released under the LGPLv3 license. 
Contributions
Bug reports and pull requests are welcome. If you would like to make a donation, please do so from the following URL:
https://ko-fi.com/ailorawill
<a href='https://ko-fi.com/M4M1WZ04Y' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

Contact
If you have any questions or comments about the project, please contact me at https://x.com/plionplion or on Discord at @willlion.
