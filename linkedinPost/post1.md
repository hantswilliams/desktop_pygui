# Post 

Creating local Apps (.exe/.app) with Python in 2024? 🤔

Over the past weekend I explored a few different tools for how to create a local, standalone desktop applications (.exe, .app) with Python for a upcoming hospital project where we will likely need to run things locally, windows server, no internet, no external connections. 

Long story short, seems like the easiest way in 2024 to do this is using a python packaged  pyinstaller - works for mac + linux + windows. Main drawback is you can only compile for the OS you are currently on (e.g., if im running this on my mac, I can only compile for mac). Also checked out py2app and py2exe, but my personal preference is pyinstaller as of right now.

For creating the interface, really focused on two packages to achieve that part: `tkinter` and `pyqt`. Tkinter is the built-in python library for creating GUIs, and is pretty easy to use, also very light weight from a package perspective if your focusing on low package size builds. While pyqt is has all the bells and whistles, and a bit more complex to use, but not too bad if your using chatGPT to help you out.

If you want to check out and perhaps get inspired by a simple project, here is the github repo - where if you go into tinker2.py - created a simple python app that utilizes tinker and pandas to read in a csv file and display the descriptives (.describe) in the table, and uses a local sqlite db to store the data.

What I discovered that i will explore next is using some flask-based packages to run a local app using the flask codebase (flaskwebgui, flask-desktop) which I'm more familiar with then tkinter/pyqt.