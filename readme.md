# To create: 

1. Making app file with pyinstaller for tinker app (tinker.py):
    - ```pyinstaller --onedir --noconsole --name "csv-analysis" --add-data "csv_app.db:." --add-data "python-icon.png:." tinker2_csv.py --icon=python-icon.icns```
        - run with optimizations add: `pyinstaller --onedir --optimize 1 --noconsole --add-data "csv_app.db:." tinker2.py`
    - ```pyinstaller --onedir --noconsole --add-data "tasks.db:." tinker4.py```
        - this will create a folder called `dist` with the app file in it.
        - `--noconsole` will hide the console window.
        - `--add-data` will add the `tasks.db` file to the app.
        - `--onedir` will create a folder with the app file in it.
        - interesting if you use onefile it fails, versus onedir works fine - e.g., no reload

## Old 

0. Building with nuitka:
    - ```python -m nuitka --enable-plugin=tk-inter --standalone --macos-create-app-bundle tinker2.py```

1. Making app file: with py2app for `pygui` or `tinker` (pygui1.py or tinker2.py): 
    - ```python setup_pygui.py py2app```
    - ```python setup_tinker.py py2app -A``` (for debug mode)