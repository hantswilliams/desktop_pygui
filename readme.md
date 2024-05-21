# To create an executable file for a python script, you can use pyinstaller.:

1. Install pyinstaller: `pip install pyinstaller` in either your global environment or a virtual environment.

2. For creating the CSV app, first run with just python to make sure it works: 
    - `python tinker2_csv.py`

3. Then after conforming that, to turn it into a app file with pyinstaller:
    - ```pyinstaller --onedir --noconsole --name "csv-analysis" --add-data "csv_app.db:." --add-data "python-icon.png:." tinker2_csv.py --icon=python-icon.icns```

        - `--onedir` - creates a folder with the app files
        - `--noconsole` - does not show the console when running the app
        - `--name` - name of the app
        - `--add-data` - adds the database file and icon to the app
            - for this, we have the database file and icon in the same directory as the script, so we use `.` to indicate that
        - `--icon` - adds the icon to the app
            - for mac apps, you need to convert the icon to a .icns file, you can use an online converter for this.

