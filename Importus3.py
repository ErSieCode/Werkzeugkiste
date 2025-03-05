import importlib
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from typing import List, Dict, Any, Set, Optional
import pkg_resources
import platform
import webbrowser
import threading
import time
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ModuleData:
    """
    Klasse zur Verwaltung der Modul-Datenbank
    """

    def __init__(self):
        # Dictionary mit Modulinformationen, kategorisiert
        self.modules_by_category = {
            "Frontend": [
                {"name": "Tkinter", "description": "Builtin GUI Toolkit",
                 "doc_url": "https://docs.python.org/3/library/tkinter.html"},
                {"name": "PyQt5", "description": "Python-Bindings für Qt5",
                 "doc_url": "https://www.riverbankcomputing.com/static/Docs/PyQt5/"},
                {"name": "PySide2", "description": "Offizielle Qt-Bindings",
                 "doc_url": "https://doc.qt.io/qtforpython/"},
                {"name": "Kivy", "description": "Framework für Multi-Touch UIs",
                 "doc_url": "https://kivy.org/doc/stable/"},
                {"name": "wxPython", "description": "Native GUI (Wrapper für wxWidgets)",
                 "doc_url": "https://wxpython.org/Phoenix/docs/html/"},
                {"name": "PySimpleGUI", "description": "Einfacher GUI Wrapper",
                 "doc_url": "https://pysimplegui.readthedocs.io/"},
                {"name": "DearPyGui", "description": "GPU-beschleunigte GUI",
                 "doc_url": "https://dearpygui.readthedocs.io/en/latest/"},
                {"name": "Toga", "description": "Native GUI für BeeWare",
                 "doc_url": "https://toga.readthedocs.io/en/latest/"},
                {"name": "PyGame", "description": "Game- und Multimedia-Framework",
                 "doc_url": "https://www.pygame.org/docs/"},
                {"name": "CustomTkinter", "description": "Modern UI elements for tkinter",
                 "doc_url": "https://github.com/TomSchimansky/CustomTkinter"},
                {"name": "ttkbootstrap", "description": "Themed tkinter widgets",
                 "doc_url": "https://ttkbootstrap.readthedocs.io/"},
                {"name": "Flexx", "description": "Pure Python UI toolkit", "doc_url": "https://flexx.readthedocs.io/"},
                {"name": "PySide6", "description": "Qt for Python (official)",
                 "doc_url": "https://doc.qt.io/qtforpython/"},
                {"name": "PyGObject", "description": "GTK+ 3 bindings for Python",
                 "doc_url": "https://pygobject.readthedocs.io/"},
                {"name": "Eel", "description": "HTML/JS GUI für Python", "doc_url": "https://github.com/ChrisKnott/Eel"}
            ],
            "Backend": [
                {"name": "Django", "description": "High-Level Webframework",
                 "doc_url": "https://docs.djangoproject.com/en/stable/"},
                {"name": "Flask", "description": "Lightweight web framework",
                 "doc_url": "https://flask.palletsprojects.com/"},
                {"name": "FastAPI", "description": "Modern, fast web framework",
                 "doc_url": "https://fastapi.tiangolo.com/"},
                {"name": "Tornado", "description": "Asynchronous networking library",
                 "doc_url": "https://www.tornadoweb.org/"},
                {"name": "Pyramid", "description": "Flexible web framework", "doc_url": "https://trypyramid.com/"},
                {"name": "Sanic", "description": "Async web framework", "doc_url": "https://sanic.readthedocs.io/"},
                {"name": "Falcon", "description": "API framework for building microservices",
                 "doc_url": "https://falconframework.org/"},
                {"name": "aiohttp", "description": "Async HTTP client/server", "doc_url": "https://docs.aiohttp.org/"},
                {"name": "Bottle", "description": "Simple WSGI web framework", "doc_url": "https://bottlepy.org/"},
                {"name": "CherryPy", "description": "Object-oriented web framework",
                 "doc_url": "https://cherrypy.org/"},
                {"name": "Quart", "description": "Asynchrones Flask", "doc_url": "https://pgjones.gitlab.io/quart/"},
                {"name": "Starlette", "description": "Lightweight ASGI framework",
                 "doc_url": "https://www.starlette.io/"},
                {"name": "Responder", "description": "Familiar HTTP Service Framework",
                 "doc_url": "https://github.com/taoufik07/responder"},
                {"name": "Masonite", "description": "Developer-centric Python web framework",
                 "doc_url": "https://docs.masoniteproject.com/"},
                {"name": "TurboGears", "description": "Web framework with best library approach",
                 "doc_url": "https://turbogears.org/"}
            ],
            "Web": [
                {"name": "requests", "description": "HTTP library", "doc_url": "https://requests.readthedocs.io/"},
                {"name": "Beautiful Soup", "description": "HTML/XML parser",
                 "doc_url": "https://www.crummy.com/software/BeautifulSoup/"},
                {"name": "Selenium", "description": "Browser automation",
                 "doc_url": "https://selenium-python.readthedocs.io/"},
                {"name": "httpx", "description": "Next-gen HTTP client", "doc_url": "https://www.python-httpx.org/"},
                {"name": "Scrapy", "description": "Web crawling framework", "doc_url": "https://scrapy.org/"},
                {"name": "lxml", "description": "XML and HTML processing", "doc_url": "https://lxml.de/"},
                {"name": "urllib3", "description": "HTTP client", "doc_url": "https://urllib3.readthedocs.io/"},
                {"name": "html5lib", "description": "Standards-compliant HTML parser",
                 "doc_url": "https://html5lib.readthedocs.io/"},
                {"name": "MechanicalSoup", "description": "Automate interaction with websites",
                 "doc_url": "https://mechanicalsoup.readthedocs.io/"},
                {"name": "pyppeteer", "description": "Puppeteer Python port",
                 "doc_url": "https://pyppeteer.github.io/pyppeteer/"},
                {"name": "playwright", "description": "Browser automation",
                 "doc_url": "https://playwright.dev/python/"},
                {"name": "parsel", "description": "HTML/XML data extraction library",
                 "doc_url": "https://parsel.readthedocs.io/"},
                {"name": "Werkzeug", "description": "WSGI web application library",
                 "doc_url": "https://werkzeug.palletsprojects.com/"},
                {"name": "uvicorn", "description": "ASGI web server", "doc_url": "https://www.uvicorn.org/"},
                {"name": "gunicorn", "description": "WSGI HTTP Server", "doc_url": "https://gunicorn.org/"}
            ],
            "Tooling": [
                {"name": "pytest", "description": "Testing framework", "doc_url": "https://docs.pytest.org/"},
                {"name": "tox", "description": "Automate testing", "doc_url": "https://tox.readthedocs.io/"},
                {"name": "black", "description": "Code formatter", "doc_url": "https://black.readthedocs.io/"},
                {"name": "flake8", "description": "Linting tool", "doc_url": "https://flake8.pycqa.org/"},
                {"name": "mypy", "description": "Static type checker", "doc_url": "https://mypy.readthedocs.io/"},
                {"name": "pipenv", "description": "Dependency management", "doc_url": "https://pipenv.pypa.io/"},
                {"name": "poetry", "description": "Dependency management", "doc_url": "https://python-poetry.org/"},
                {"name": "isort", "description": "Import sorter", "doc_url": "https://pycqa.github.io/isort/"},
                {"name": "bandit", "description": "Security linter", "doc_url": "https://bandit.readthedocs.io/"},
                {"name": "pre-commit", "description": "Git hooks framework", "doc_url": "https://pre-commit.com/"},
                {"name": "pylint", "description": "Code analysis for bug detection",
                 "doc_url": "https://pylint.pycqa.org/"},
                {"name": "virtualenv", "description": "Virtual environment creation",
                 "doc_url": "https://virtualenv.pypa.io/"},
                {"name": "pyright", "description": "Static type checker by Microsoft",
                 "doc_url": "https://github.com/microsoft/pyright"},
                {"name": "ruff", "description": "Fast Python linter",
                 "doc_url": "https://github.com/charliermarsh/ruff"},
                {"name": "pydantic", "description": "Data validation using type annotations",
                 "doc_url": "https://pydantic-docs.helpmanual.io/"}
            ],
            "Database": [
                {"name": "SQLAlchemy", "description": "SQL toolkit and ORM", "doc_url": "https://www.sqlalchemy.org/"},
                {"name": "peewee", "description": "Small ORM", "doc_url": "http://docs.peewee-orm.com/"},
                {"name": "pymongo", "description": "MongoDB driver", "doc_url": "https://pymongo.readthedocs.io/"},
                {"name": "psycopg2", "description": "PostgreSQL adapter", "doc_url": "https://www.psycopg.org/"},
                {"name": "mysql-connector-python", "description": "MySQL driver",
                 "doc_url": "https://dev.mysql.com/doc/connector-python/en/"},
                {"name": "redis-py", "description": "Redis client", "doc_url": "https://redis-py.readthedocs.io/"},
                {"name": "tortoise-orm", "description": "Async ORM", "doc_url": "https://tortoise-orm.readthedocs.io/"},
                {"name": "dataset", "description": "Database for lazy people",
                 "doc_url": "https://dataset.readthedocs.io/"},
                {"name": "mongoengine", "description": "MongoDB ODM",
                 "doc_url": "https://mongoengine-odm.readthedocs.io/"},
                {"name": "pony", "description": "ORM with query syntax", "doc_url": "https://ponyorm.org/"},
                {"name": "sqlite3", "description": "SQLite database interface",
                 "doc_url": "https://docs.python.org/3/library/sqlite3.html"},
                {"name": "aiomysql", "description": "Asyncio MySQL driver",
                 "doc_url": "https://aiomysql.readthedocs.io/"},
                {"name": "asyncpg", "description": "Asyncio PostgreSQL driver",
                 "doc_url": "https://magicstack.github.io/asyncpg/"},
                {"name": "aiosqlite", "description": "Asyncio SQLite driver",
                 "doc_url": "https://github.com/omnilib/aiosqlite"},
                {"name": "sqlmodel", "description": "SQLAlchemy + Pydantic",
                 "doc_url": "https://sqlmodel.tiangolo.com/"}
            ],
            "Big Data": [
                {"name": "pandas", "description": "Data analysis and manipulation",
                 "doc_url": "https://pandas.pydata.org/"},
                {"name": "numpy", "description": "Numerical computing", "doc_url": "https://numpy.org/"},
                {"name": "pyspark", "description": "Apache Spark interface",
                 "doc_url": "https://spark.apache.org/docs/latest/api/python/"},
                {"name": "dask", "description": "Parallel computing", "doc_url": "https://dask.org/"},
                {"name": "vaex", "description": "Out-of-memory dataframes", "doc_url": "https://vaex.io/"},
                {"name": "polars", "description": "Fast DataFrame library", "doc_url": "https://pola.rs/"},
                {"name": "modin", "description": "Accelerated pandas", "doc_url": "https://modin.readthedocs.io/"},
                {"name": "koalas", "description": "Pandas API on Apache Spark",
                 "doc_url": "https://koalas.readthedocs.io/"},
                {"name": "petastorm", "description": "Parquet datasets with ML frameworks",
                 "doc_url": "https://petastorm.readthedocs.io/"},
                {"name": "ray", "description": "Distributed computing", "doc_url": "https://ray.io/"},
                {"name": "xarray", "description": "N-D labeled arrays and datasets",
                 "doc_url": "https://xarray.pydata.org/"},
                {"name": "pyarrow", "description": "Apache Arrow and Parquet",
                 "doc_url": "https://arrow.apache.org/docs/python/"},
                {"name": "cudf", "description": "GPU DataFrame library",
                 "doc_url": "https://docs.rapids.ai/api/cudf/stable/"},
                {"name": "h5py", "description": "Interface to HDF5 format", "doc_url": "https://www.h5py.org/"},
                {"name": "datatable", "description": "Data table processing library",
                 "doc_url": "https://datatable.readthedocs.io/"}
            ],
            "IoT": [
                {"name": "paho-mqtt", "description": "MQTT client", "doc_url": "https://pypi.org/project/paho-mqtt/"},
                {"name": "micropython", "description": "Python for microcontrollers",
                 "doc_url": "https://micropython.org/"},
                {"name": "adafruit-circuitpython", "description": "CircuitPython libraries",
                 "doc_url": "https://circuitpython.org/"},
                {"name": "gpiozero", "description": "Simple Raspberry Pi GPIO",
                 "doc_url": "https://gpiozero.readthedocs.io/"},
                {"name": "RPi.GPIO", "description": "Raspberry Pi GPIO module",
                 "doc_url": "https://pypi.org/project/RPi.GPIO/"},
                {"name": "pyserial", "description": "Serial port access",
                 "doc_url": "https://pyserial.readthedocs.io/"},
                {"name": "bleak", "description": "Bluetooth Low Energy", "doc_url": "https://bleak.readthedocs.io/"},
                {"name": "esptool", "description": "ESP8266/ESP32 tool",
                 "doc_url": "https://github.com/espressif/esptool"},
                {"name": "pymodbus", "description": "Modbus protocol implementation",
                 "doc_url": "https://pymodbus.readthedocs.io/"},
                {"name": "pybluez", "description": "Bluetooth Python extension",
                 "doc_url": "https://pybluez.github.io/"},
                {"name": "pigpio", "description": "Raspberry Pi GPIO control",
                 "doc_url": "http://abyz.me.uk/rpi/pigpio/python.html"},
                {"name": "python-periphery", "description": "Linux peripheral I/O",
                 "doc_url": "https://python-periphery.readthedocs.io/"},
                {"name": "Pillow", "description": "Image processing library", "doc_url": "https://python-pillow.org/"},
                {"name": "smbus2", "description": "SMBus protocol",
                 "doc_url": "https://github.com/kplindegaard/smbus2"},
                {"name": "rpi-gpio-nfc", "description": "NFC on Raspberry Pi",
                 "doc_url": "https://github.com/StrayFeral/rpi-gpio-nfc"}
            ],
            "DevOps": [
                {"name": "ansible", "description": "Automation platform", "doc_url": "https://www.ansible.com/"},
                {"name": "docker", "description": "Docker API client", "doc_url": "https://docker-py.readthedocs.io/"},
                {"name": "fabric", "description": "SSH deployment tool", "doc_url": "https://www.fabfile.org/"},
                {"name": "paramiko", "description": "SSH implementation", "doc_url": "https://www.paramiko.org/"},
                {"name": "kubernetes", "description": "Kubernetes API client",
                 "doc_url": "https://github.com/kubernetes-client/python"},
                {"name": "boto3", "description": "AWS SDK",
                 "doc_url": "https://boto3.amazonaws.com/v1/documentation/api/latest/index.html"},
                {"name": "terraform-python", "description": "Terraform wrapper",
                 "doc_url": "https://github.com/beelit94/terraform-python"},
                {"name": "pulumi", "description": "Infrastructure as Code", "doc_url": "https://www.pulumi.com/"},
                {"name": "python-jenkins", "description": "Jenkins API client",
                 "doc_url": "https://python-jenkins.readthedocs.io/"},
                {"name": "salt", "description": "Remote execution framework",
                 "doc_url": "https://docs.saltproject.io/"},
                {"name": "azure-cli", "description": "Azure command-line interface",
                 "doc_url": "https://docs.microsoft.com/cli/azure/"},
                {"name": "google-cloud-python", "description": "Google Cloud client",
                 "doc_url": "https://googleapis.dev/python/google-api-core/latest/index.html"},
                {"name": "python-digitalocean", "description": "DigitalOcean API",
                 "doc_url": "https://github.com/koalalorenzo/python-digitalocean"},
                {"name": "openstack", "description": "OpenStack SDK",
                 "doc_url": "https://docs.openstack.org/openstacksdk/latest/"},
                {"name": "jenkinsapi", "description": "Jenkins API",
                 "doc_url": "https://github.com/pycontribs/jenkinsapi"}
            ],
            "Media": [
                {"name": "Pillow", "description": "Image processing", "doc_url": "https://pillow.readthedocs.io/"},
                {"name": "moviepy", "description": "Video editing", "doc_url": "https://zulko.github.io/moviepy/"},
                {"name": "pygame", "description": "Game development", "doc_url": "https://www.pygame.org/"},
                {"name": "opencv-python", "description": "Computer vision", "doc_url": "https://opencv.org/"},
                {"name": "pydub", "description": "Audio processing", "doc_url": "https://github.com/jiaaro/pydub"},
                {"name": "pyglet", "description": "Windowing and multimedia", "doc_url": "https://pyglet.org/"},
                {"name": "librosa", "description": "Audio analysis", "doc_url": "https://librosa.org/"},
                {"name": "mutagen", "description": "Audio metadata handling",
                 "doc_url": "https://mutagen.readthedocs.io/"},
                {"name": "ffmpeg-python", "description": "FFmpeg wrapper",
                 "doc_url": "https://github.com/kkroening/ffmpeg-python"},
                {"name": "pyaudio", "description": "Audio I/O",
                 "doc_url": "https://people.csail.mit.edu/hubert/pyaudio/"},
                {"name": "imageio", "description": "Image I/O", "doc_url": "https://imageio.github.io/"},
                {"name": "scikit-image", "description": "Image processing", "doc_url": "https://scikit-image.org/"},
                {"name": "manim", "description": "Mathematical animations", "doc_url": "https://docs.manim.community/"},
                {"name": "wand", "description": "ImageMagick binding", "doc_url": "https://docs.wand-py.org/"},
                {"name": "python-vlc", "description": "VLC media player binding",
                 "doc_url": "https://github.com/oaubert/python-vlc"}
            ],
            "Parse": [
                {"name": "pyyaml", "description": "YAML parser and emitter", "doc_url": "https://pyyaml.org/"},
                {"name": "json", "description": "JSON encoder and decoder",
                 "doc_url": "https://docs.python.org/3/library/json.html"},
                {"name": "csv", "description": "CSV file reading and writing",
                 "doc_url": "https://docs.python.org/3/library/csv.html"},
                {"name": "xml.etree.ElementTree", "description": "XML processing",
                 "doc_url": "https://docs.python.org/3/library/xml.etree.elementtree.html"},
                {"name": "configparser", "description": "INI file parser",
                 "doc_url": "https://docs.python.org/3/library/configparser.html"},
                {"name": "toml", "description": "TOML parser", "doc_url": "https://github.com/toml-lang/toml"},
                {"name": "ujson", "description": "Ultra fast JSON encoder and decoder",
                 "doc_url": "https://github.com/ultrajson/ultrajson"},
                {"name": "python-dateutil", "description": "Date parsing and manipulation",
                 "doc_url": "https://dateutil.readthedocs.io/"},
                {"name": "xmltodict", "description": "XML to dict converter",
                 "doc_url": "https://github.com/martinblech/xmltodict"},
                {"name": "arrow", "description": "Better dates and times", "doc_url": "https://arrow.readthedocs.io/"},
                {"name": "parse", "description": "Parse strings using format strings",
                 "doc_url": "https://github.com/r1chardj0n3s/parse"},
                {"name": "beautifulsoup4", "description": "HTML/XML parser",
                 "doc_url": "https://www.crummy.com/software/BeautifulSoup/"},
                {"name": "pyparsing", "description": "Parser generator",
                 "doc_url": "https://pyparsing-docs.readthedocs.io/"},
                {"name": "marshmallow", "description": "Object serialization/deserialization",
                 "doc_url": "https://marshmallow.readthedocs.io/"},
                {"name": "tomli", "description": "TOML parser (Python 3.6+)",
                 "doc_url": "https://github.com/hukkin/tomli"}
            ],
            "Security": [
                {"name": "cryptography", "description": "Cryptographic recipes", "doc_url": "https://cryptography.io/"},
                {"name": "passlib", "description": "Password hashing", "doc_url": "https://passlib.readthedocs.io/"},
                {"name": "pyOpenSSL", "description": "OpenSSL wrapper", "doc_url": "https://pyopenssl.org/"},
                {"name": "jwt", "description": "JSON Web Token", "doc_url": "https://pyjwt.readthedocs.io/"},
                {"name": "oauthlib", "description": "OAuth implementation",
                 "doc_url": "https://oauthlib.readthedocs.io/"},
                {"name": "bcrypt", "description": "Modern password hashing",
                 "doc_url": "https://github.com/pyca/bcrypt/"},
                {"name": "paramiko", "description": "SSHv2 protocol", "doc_url": "https://www.paramiko.org/"},
                {"name": "pyotp", "description": "One-time password library",
                 "doc_url": "https://github.com/pyauth/pyotp"},
                {"name": "authlib", "description": "Authentication library", "doc_url": "https://docs.authlib.org/"},
                {"name": "google-auth", "description": "Google Authentication",
                 "doc_url": "https://google-auth.readthedocs.io/"},
                {"name": "pynacl", "description": "Networking and cryptography library",
                 "doc_url": "https://pynacl.readthedocs.io/"},
                {"name": "python-gnupg", "description": "GnuPG interface", "doc_url": "https://gnupg.readthedocs.io/"},
                {"name": "py-argon2", "description": "Argon2 password hashing",
                 "doc_url": "https://argon2-cffi.readthedocs.io/"},
                {"name": "itsdangerous", "description": "Cryptographically sign data",
                 "doc_url": "https://itsdangerous.palletsprojects.com/"},
                {"name": "pyca", "description": "Python Cryptographic Authority", "doc_url": "https://github.com/pyca"}
            ],
            "APIs": [
                {"name": "requests-oauthlib", "description": "OAuth for Requests",
                 "doc_url": "https://requests-oauthlib.readthedocs.io/"},
                {"name": "python-twitter", "description": "Twitter API",
                 "doc_url": "https://github.com/bear/python-twitter"},
                {"name": "tweepy", "description": "Twitter API client", "doc_url": "https://www.tweepy.org/"},
                {"name": "google-api-python-client", "description": "Google APIs client",
                 "doc_url": "https://github.com/googleapis/google-api-python-client"},
                {"name": "facebook-sdk", "description": "Facebook SDK",
                 "doc_url": "https://facebook-sdk.readthedocs.io/"},
                {"name": "instagram-private-api", "description": "Instagram Private API",
                 "doc_url": "https://github.com/ping/instagram_private_api"},
                {"name": "praw", "description": "Reddit API wrapper", "doc_url": "https://praw.readthedocs.io/"},
                {"name": "stripe", "description": "Stripe API", "doc_url": "https://stripe.com/docs/api?lang=python"},
                {"name": "twilio", "description": "Twilio API client",
                 "doc_url": "https://www.twilio.com/docs/libraries/python"},
                {"name": "github3.py", "description": "GitHub API client",
                 "doc_url": "https://github3py.readthedocs.io/"},
                {"name": "pyTelegramBotAPI", "description": "Telegram Bot API",
                 "doc_url": "https://github.com/eternnoir/pyTelegramBotAPI"},
                {"name": "python-gitlab", "description": "GitLab API client",
                 "doc_url": "https://python-gitlab.readthedocs.io/"},
                {"name": "discord.py", "description": "Discord API client",
                 "doc_url": "https://discordpy.readthedocs.io/"},
                {"name": "slackclient", "description": "Slack API client",
                 "doc_url": "https://slack.dev/python-slackclient/"},
                {"name": "pyOpenWeatherMap", "description": "OpenWeatherMap API",
                 "doc_url": "https://github.com/csparpa/pyowm"}
            ],
            "Kompression": [
                {"name": "zipfile", "description": "ZIP archive handling",
                 "doc_url": "https://docs.python.org/3/library/zipfile.html"},
                {"name": "tarfile", "description": "TAR archive handling",
                 "doc_url": "https://docs.python.org/3/library/tarfile.html"},
                {"name": "gzip", "description": "Gzip support",
                 "doc_url": "https://docs.python.org/3/library/gzip.html"},
                {"name": "bz2", "description": "Bzip2 compression",
                 "doc_url": "https://docs.python.org/3/library/bz2.html"},
                {"name": "lzma", "description": "LZMA compression",
                 "doc_url": "https://docs.python.org/3/library/lzma.html"},
                {"name": "zlib", "description": "Zlib compression",
                 "doc_url": "https://docs.python.org/3/library/zlib.html"},
                {"name": "py7zr", "description": "7zip archive handling", "doc_url": "https://py7zr.readthedocs.io/"},
                {"name": "pyzipper", "description": "Extended zipfile with encryption",
                 "doc_url": "https://github.com/danifus/pyzipper"},
                {"name": "compress-pickle", "description": "Compressed pickle serialization",
                 "doc_url": "https://github.com/lucianopaz/compress_pickle"},
                {"name": "unrar", "description": "RAR archive handling",
                 "doc_url": "https://github.com/matiasb/python-unrar"},
                {"name": "zstandard", "description": "Zstandard compression",
                 "doc_url": "https://python-zstandard.readthedocs.io/"},
                {"name": "lz4", "description": "LZ4 compression", "doc_url": "https://python-lz4.readthedocs.io/"},
                {"name": "brotli", "description": "Brotli compression", "doc_url": "https://github.com/google/brotli"},
                {"name": "snappy", "description": "Snappy compression",
                 "doc_url": "https://github.com/andrix/python-snappy"},
                {"name": "blosc", "description": "Blosc compression",
                 "doc_url": "https://github.com/Blosc/python-blosc"}
            ],
            "Machine Learning": [
                {"name": "scikit-learn", "description": "Machine learning algorithms",
                 "doc_url": "https://scikit-learn.org/"},
                {"name": "tensorflow", "description": "Deep learning framework",
                 "doc_url": "https://www.tensorflow.org/"},
                {"name": "pytorch", "description": "Deep learning framework", "doc_url": "https://pytorch.org/"},
                {"name": "keras", "description": "High-level neural networks API", "doc_url": "https://keras.io/"},
                {"name": "xgboost", "description": "Gradient boosting framework",
                 "doc_url": "https://xgboost.readthedocs.io/"},
                {"name": "lightgbm", "description": "Gradient boosting framework",
                 "doc_url": "https://lightgbm.readthedocs.io/"},
                {"name": "catboost", "description": "Gradient boosting framework", "doc_url": "https://catboost.ai/"},
                {"name": "spacy", "description": "Natural language processing", "doc_url": "https://spacy.io/"},
                {"name": "nltk", "description": "Natural language toolkit", "doc_url": "https://www.nltk.org/"},
                {"name": "gensim", "description": "Topic modeling and document similarity",
                 "doc_url": "https://radimrehurek.com/gensim/"},
                {"name": "transformers", "description": "Hugging Face Transformers",
                 "doc_url": "https://huggingface.co/transformers/"},
                {"name": "fastai", "description": "Deep learning library", "doc_url": "https://docs.fast.ai/"},
                {"name": "scikit-image", "description": "Image processing", "doc_url": "https://scikit-image.org/"},
                {"name": "statsmodels", "description": "Statistical models", "doc_url": "https://www.statsmodels.org/"},
                {"name": "opencv-python", "description": "Computer vision", "doc_url": "https://opencv.org/"}
            ],
            "Visualization": [
                {"name": "matplotlib", "description": "Plotting library", "doc_url": "https://matplotlib.org/"},
                {"name": "seaborn", "description": "Statistical data visualization",
                 "doc_url": "https://seaborn.pydata.org/"},
                {"name": "plotly", "description": "Interactive plots", "doc_url": "https://plotly.com/python/"},
                {"name": "bokeh", "description": "Interactive web plots", "doc_url": "https://bokeh.org/"},
                {"name": "altair", "description": "Declarative statistical visualization",
                 "doc_url": "https://altair-viz.github.io/"},
                {"name": "holoviews", "description": "Data visualization library", "doc_url": "https://holoviews.org/"},
                {"name": "dash", "description": "Interactive web apps for visualization",
                 "doc_url": "https://dash.plotly.com/"},
                {"name": "pygal", "description": "SVG charts creator", "doc_url": "http://pygal.org/"},
                {"name": "folium", "description": "Leaflet.js maps",
                 "doc_url": "https://python-visualization.github.io/folium/"},
                {"name": "ggplot", "description": "ggplot2 port to Python", "doc_url": "https://github.com/yhat/ggpy"},
                {"name": "plotnine", "description": "Grammar of graphics",
                 "doc_url": "https://plotnine.readthedocs.io/"},
                {"name": "networkx", "description": "Network graphs", "doc_url": "https://networkx.org/"},
                {"name": "pydot", "description": "Graphviz interface", "doc_url": "https://github.com/pydot/pydot"},
                {"name": "graphviz", "description": "Graphviz interface",
                 "doc_url": "https://graphviz.readthedocs.io/"},
                {"name": "datashader", "description": "Big data visualization", "doc_url": "https://datashader.org/"}
            ],
            "Testing": [
                {"name": "pytest", "description": "Testing framework", "doc_url": "https://docs.pytest.org/"},
                {"name": "unittest", "description": "Unit testing framework",
                 "doc_url": "https://docs.python.org/3/library/unittest.html"},
                {"name": "nose2", "description": "Test runner", "doc_url": "https://docs.nose2.io/"},
                {"name": "mock", "description": "Mocking and testing library",
                 "doc_url": "https://docs.python.org/3/library/unittest.mock.html"},
                {"name": "pytest-cov", "description": "Code coverage plugin for pytest",
                 "doc_url": "https://pytest-cov.readthedocs.io/"},
                {"name": "selenium", "description": "Browser automation",
                 "doc_url": "https://selenium-python.readthedocs.io/"},
                {"name": "behave", "description": "BDD testing", "doc_url": "https://behave.readthedocs.io/"},
                {"name": "hypothesis", "description": "Property-based testing",
                 "doc_url": "https://hypothesis.readthedocs.io/"},
                {"name": "robotframework", "description": "Generic test automation",
                 "doc_url": "https://robotframework.org/"},
                {"name": "playwright", "description": "Browser automation",
                 "doc_url": "https://playwright.dev/python/"},
                {"name": "pytest-mock", "description": "Thin wrapper around mock",
                 "doc_url": "https://github.com/pytest-dev/pytest-mock/"},
                {"name": "pytest-xdist", "description": "Test parallelization",
                 "doc_url": "https://github.com/pytest-dev/pytest-xdist"},
                {"name": "pytest-django", "description": "Django testing with pytest",
                 "doc_url": "https://pytest-django.readthedocs.io/"},
                {"name": "pytest-asyncio", "description": "Asyncio testing with pytest",
                 "doc_url": "https://github.com/pytest-dev/pytest-asyncio"},
                {"name": "faker", "description": "Fake data generator", "doc_url": "https://faker.readthedocs.io/"}
            ]
        }

    def get_categories(self) -> List[str]:
        """
        Gibt die Liste aller verfügbaren Kategorien zurück
        """
        return list(self.modules_by_category.keys())

    def get_modules_by_category(self, category: str) -> List[Dict[str, str]]:
        """
        Gibt die Module einer bestimmten Kategorie zurück
        """
        if category in self.modules_by_category:
            return self.modules_by_category[category]
        return []

    def get_module_names(self) -> List[str]:
        """
        Gibt eine Liste aller Modulnamen zurück
        """
        all_modules = []
        for category_modules in self.modules_by_category.values():
            all_modules.extend([module["name"] for module in category_modules])
        return all_modules

    def search_modules(self, query: str) -> List[Dict[str, Any]]:
        """
        Sucht nach Modulen, die der Suchanfrage entsprechen

        Args:
            query: Die Suchanfrage

        Returns:
            Liste der gefundenen Module mit zusätzlichem Kategoriefeld
        """
        if not query:
            return []

        query = query.lower()
        results = []

        for category, modules in self.modules_by_category.items():
            for module in modules:
                # Suche im Namen
                if query in module["name"].lower():
                    # Füge Kategorie zum Modul hinzu
                    module_with_category = module.copy()
                    module_with_category["category"] = category
                    results.append(module_with_category)
                # Suche in der Beschreibung
                elif query in module["description"].lower():
                    module_with_category = module.copy()
                    module_with_category["category"] = category
                    results.append(module_with_category)

        return results

    def get_module_popularity(self, category: str) -> Dict[str, int]:
        """
        Erstellt ein simuliertes Popularitätsranking für Module einer Kategorie
        (In einer realen Anwendung würde dies basierend auf echten Daten wie PyPI-Downloads sein)
        """
        import random
        modules = self.get_modules_by_category(category)
        popularity = {}
        for i, module in enumerate(modules):
            # Erstellt simulierte Popularitätswerte, die ungefähr der Reihenfolge entsprechen
            # (mit etwas Zufall für Variation)
            popularity[module["name"]] = 10000 - (i * 800) + random.randint(-300, 300)
        return popularity


class ModuleChecker:
    """
    Klasse zur Überprüfung von Modulimporten
    """

    @staticmethod
    def check_importable(module_names: List[str]) -> Dict[str, bool]:
        """
        Überprüft, ob die angegebenen Module importiert werden können.

        Args:
            module_names: Liste der zu überprüfenden Modulnamen

        Returns:
            Dictionary mit Modulnamen als Schlüssel und
            Boolean-Werten, die angeben, ob der Import erfolgreich war
        """
        results = {}
        for module_name in module_names:
            try:
                # Normalisiere den Modulnamen für den Import
                import_name = module_name.lower().replace('-', '_')
                # Versuche, das Modul zu importieren
                importlib.import_module(import_name)
                results[module_name] = True
            except (ImportError, ModuleNotFoundError):
                results[module_name] = False
        return results

    @staticmethod
    def get_module_version(module_name: str) -> str:
        """
        Versucht, die Version eines Moduls zu ermitteln

        Args:
            module_name: Name des Moduls

        Returns:
            Versionsnummer als String oder "N/A" wenn nicht verfügbar
        """
        try:
            # Normalisiere den Modulnamen für den Import
            import_name = module_name.lower().replace('-', '_')
            # Versuche, das Modul zu importieren
            module = importlib.import_module(import_name)

            # Versuche, verschiedene Attribute für die Version zu finden
            if hasattr(module, "__version__"):
                return module.__version__
            if hasattr(module, "VERSION"):
                return str(module.VERSION)
            if hasattr(module, "version"):
                return str(module.version)

            # Wenn kein direktes Attribut gefunden wird, versuche pkg_resources
            try:
                return pkg_resources.get_distribution(module_name).version
            except (pkg_resources.DistributionNotFound, AttributeError):
                pass

            return "N/A"
        except (ImportError, ModuleNotFoundError):
            return "N/A"

    @staticmethod
    def get_module_install_command(module_name: str, platform_name: str = None) -> str:
        """
        Gibt den Befehl zum Installieren eines Moduls zurück, basierend auf der Plattform

        Args:
            module_name: Name des Moduls
            platform_name: Name der Plattform (Windows, Linux, macOS)

        Returns:
            Befehl zum Installieren des Moduls
        """
        if platform_name is None:
            platform_name = platform.system()

        if platform_name == "Windows":
            return f"pip install {module_name}"
        elif platform_name == "Linux":
            return f"python3 -m pip install {module_name}"
        elif platform_name == "Darwin":  # macOS
            return f"python3 -m pip install {module_name}"
        else:
            return f"pip install {module_name}"


class ConfigManager:
    """
    Klasse zur Verwaltung der Anwendungskonfiguration und zum Speichern/Laden der ausgewählten Module
    """

    def __init__(self):
        # Basisordner für die Konfiguration
        self.config_dir = os.path.join(os.path.expanduser("~"), ".python_module_explorer")

        # Stelle sicher, dass der Konfigurationsordner existiert
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

        # Pfad zur Konfigurationsdatei
        self.config_file = os.path.join(self.config_dir, "config.json")

        # Standardkonfiguration
        self.config = {
            "selected_modules": [],
            "theme": "light",  # light oder dark
            "language": "de",  # de oder en
            "window_size": "900x700",
            "auto_update": False
        }

        # Lade die Konfiguration, falls sie existiert
        self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Lädt die Konfiguration aus der Datei

        Returns:
            Die geladene Konfiguration oder die Standardkonfiguration
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Aktualisiere die Standardkonfiguration mit den geladenen Werten
                    self.config.update(loaded_config)
        except Exception as e:
            print(f"Fehler beim Laden der Konfiguration: {e}")

        return self.config

    def save_config(self) -> bool:
        """
        Speichert die Konfiguration in der Datei

        Returns:
            True, wenn das Speichern erfolgreich war, sonst False
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der Konfiguration: {e}")
            return False

    def get_selected_modules(self) -> List[str]:
        """
        Gibt die Liste der ausgewählten Module zurück

        Returns:
            Liste der Modulnamen
        """
        return self.config.get("selected_modules", [])

    def set_selected_modules(self, modules: List[str]) -> None:
        """
        Setzt die Liste der ausgewählten Module

        Args:
            modules: Liste der Modulnamen
        """
        self.config["selected_modules"] = modules
        self.save_config()

    def get_theme(self) -> str:
        """
        Gibt das aktuelle Theme zurück

        Returns:
            "light" oder "dark"
        """
        return self.config.get("theme", "light")

    def set_theme(self, theme: str) -> None:
        """
        Setzt das Theme

        Args:
            theme: "light" oder "dark"
        """
        if theme in ["light", "dark"]:
            self.config["theme"] = theme
            self.save_config()

    def get_language(self) -> str:
        """
        Gibt die aktuelle Sprache zurück

        Returns:
            "de" oder "en"
        """
        return self.config.get("language", "de")

    def set_language(self, language: str) -> None:
        """
        Setzt die Sprache

        Args:
            language: "de" oder "en"
        """
        if language in ["de", "en"]:
            self.config["language"] = language
            self.save_config()

    def get_window_size(self) -> str:
        """
        Gibt die Fenstergröße zurück

        Returns:
            Fenstergröße im Format "BreitexHöhe"
        """
        return self.config.get("window_size", "900x700")

    def set_window_size(self, size: str) -> None:
        """
        Setzt die Fenstergröße

        Args:
            size: Fenstergröße im Format "BreitexHöhe"
        """
        self.config["window_size"] = size
        self.save_config()


class ModuleExplorerApp:
    """
    Hauptanwendungsklasse für den Python-Modul-Explorer
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Python Module Explorer")

        # Initialisiere den Konfigurations-Manager
        self.config_manager = ConfigManager()

        # Setze die Fenstergröße aus der Konfiguration
        self.root.geometry(self.config_manager.get_window_size())

        # Speichere die Fenstergröße bei Änderung
        self.root.bind("<Configure>", self.on_window_resize)

        # Farbschema definieren (Grüntöne)
        self.colors = {
            'bg_light': '#e8f5e9',  # Heller Hintergrund
            'bg_medium': '#c8e6c9',  # Mittlerer Hintergrund
            'bg_dark': '#81c784',  # Dunklerer Hintergrund
            'accent': '#2e7d32',  # Akzentfarbe (satter grün)
            'accent_dark': '#1b5e20',  # Dunklere Akzentfarbe
            'text': '#212121',  # Text
            'text_light': '#757575'  # Heller Text
        }

        # Dunkles Farbschema
        self.dark_colors = {
            'bg_light': '#1b5e20',  # Heller Hintergrund (für dunkles Thema)
            'bg_medium': '#2e7d32',  # Mittlerer Hintergrund
            'bg_dark': '#388e3c',  # Dunklerer Hintergrund
            'accent': '#4caf50',  # Akzentfarbe
            'accent_dark': '#81c784',  # Dunklere Akzentfarbe (hier heller für Kontrast)
            'text': '#ffffff',  # Text
            'text_light': '#c8e6c9'  # Heller Text
        }

        # Wähle das Farbschema basierend auf dem konfigurierten Theme
        if self.config_manager.get_theme() == "dark":
            self.colors = self.dark_colors

        # Setze das ttk-Thema für ein modernes Erscheinungsbild
        self.style = ttk.Style()

        # Verwende das 'clam'-Thema als Basis (plattformübergreifend verfügbar)
        self.style.theme_use('clam')

        # Passe das Design an - Grünes Theme mit abgerundeten Ecken
        self._configure_styles()

        # Einstellen der Hintergrundfarbe für das Root-Fenster
        self.root.configure(background=self.colors['bg_light'])

        # Instanziiere die Moduldatenbank
        self.module_data = ModuleData()

        # Set zum Speichern der ausgewählten Module
        self.selected_modules = set(self.config_manager.get_selected_modules())

        # Status für die Echtzeit-Suche
        self.search_after_id = None

        # Erstelle die UI-Komponenten
        self.create_widgets()

        # Status für die aktuell angezeigte Kategorie
        self.current_category = None

        # NEUE FUNKTION: Aktive Module-Fenster und Bäume (für Updates der Auswahl)
        self.active_module_windows = {}
        self.active_module_trees = {}

    def _configure_styles(self):
        """
        Konfiguriert die ttk-Stile basierend auf dem aktuellen Farbschema
        """
        self.style.configure('TFrame', background=self.colors['bg_light'])
        self.style.configure('TButton',
                             font=('Helvetica', 11),
                             background=self.colors['accent'],
                             foreground='white',
                             borderwidth=0,
                             focuscolor=self.colors['accent_dark'],
                             lightcolor=self.colors['accent'],
                             darkcolor=self.colors['accent_dark'],
                             bordercolor=self.colors['accent_dark'],
                             padding=8)

        self.style.map('TButton',
                       background=[('active', self.colors['accent_dark']),
                                   ('pressed', self.colors['accent_dark'])],
                       relief=[('pressed', 'sunken')])

        self.style.configure('TLabel',
                             font=('Helvetica', 11),
                             background=self.colors['bg_light'],
                             foreground=self.colors['text'])

        self.style.configure('Header.TLabel',
                             font=('Helvetica', 18, 'bold'),
                             background=self.colors['bg_light'],
                             foreground=self.colors['accent_dark'])

        self.style.configure('SubHeader.TLabel',
                             font=('Helvetica', 14, 'bold'),
                             background=self.colors['bg_light'],
                             foreground=self.colors['accent'])

        self.style.configure('TLabelframe',
                             background=self.colors['bg_light'],
                             foreground=self.colors['text'],
                             bordercolor=self.colors['accent'])

        self.style.configure('TLabelframe.Label',
                             background=self.colors['bg_light'],
                             foreground=self.colors['accent_dark'],
                             font=('Helvetica', 12, 'bold'))

        self.style.configure('TEntry',
                             fieldbackground=self.colors['bg_medium'],
                             foreground=self.colors['text'],
                             padding=5)

        self.style.configure('Search.TEntry',
                             fieldbackground=self.colors['bg_medium'],
                             foreground=self.colors['text'],
                             padding=8,
                             font=('Helvetica', 12))

        # Treeview-Stil für Tabellen
        self.style.configure("Treeview",
                             background=self.colors['bg_light'],
                             foreground=self.colors['text'],
                             rowheight=30,  # Größere Zeilenhöhe für Touch-Bedienung
                             fieldbackground=self.colors['bg_light'],
                             font=('Helvetica', 11))

        self.style.configure("Treeview.Heading",
                             font=('Helvetica', 12, 'bold'),
                             background=self.colors['bg_dark'],
                             foreground="white" if self.config_manager.get_theme() == "light" else self.colors['text'])

        # Stil für Registerkarten
        self.style.configure('TNotebook',
                             background=self.colors['bg_light'])

        self.style.configure('TNotebook.Tab',
                             background=self.colors['bg_medium'],
                             foreground=self.colors['text'],
                             padding=[10, 5])

        self.style.map('TNotebook.Tab',
                       background=[('selected', self.colors['accent'])],
                       foreground=[('selected', 'white')])

        # Stil für Radiobuttons und Checkbuttons
        self.style.configure('TRadiobutton',
                             background=self.colors['bg_light'],
                             foreground=self.colors['text'],
                             font=('Helvetica', 11))

        self.style.configure('TCheckbutton',
                             background=self.colors['bg_light'],
                             foreground=self.colors['text'],
                             font=('Helvetica', 11))

        # Zusätzlicher Stil für den "Hinzufügen"-Button
        self.style.configure('Add.TButton',
                             font=('Helvetica', 11, 'bold'),
                             background=self.colors['accent'],
                             foreground='white',
                             padding=8)

        self.style.map('Add.TButton',
                       background=[('active', self.colors['accent_dark']),
                                   ('pressed', self.colors['accent_dark'])])

    def on_window_resize(self, event):
        """
        Speichert die Fenstergröße bei Änderung
        """
        # Nur speichern, wenn es sich um das Hauptfenster handelt
        if event.widget == self.root:
            # Warte einen Moment, bevor die Größe gespeichert wird
            if hasattr(self, "_resize_timer"):
                self.root.after_cancel(self._resize_timer)
            self._resize_timer = self.root.after(500, self._save_window_size)

    def _save_window_size(self):
        """
        Speichert die aktuelle Fenstergröße in der Konfiguration
        """
        if self.root.state() == "normal":  # Nur speichern, wenn nicht maximiert
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            self.config_manager.set_window_size(f"{width}x{height}")

    def create_widgets(self):
        """
        Erstellt die UI-Komponenten des Hauptfensters
        """
        # Hauptframe
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Top-Bereich mit Header und Einstellungen
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X)

        # Überschrift mit App-Logo
        header_frame = ttk.Frame(self.top_frame)
        header_frame.pack(side=tk.LEFT, fill=tk.Y)

        header_label = ttk.Label(header_frame,
                                 text="Python Module Explorer",
                                 style='Header.TLabel')
        header_label.pack(pady=(0, 5))

        # Beschreibung
        description = ttk.Label(header_frame,
                                text="Entdecke, teste und installiere Python-Module nach Kategorien",
                                wraplength=500)  # Für bessere Darstellung auf kleinen Bildschirmen
        description.pack(pady=(0, 5), anchor=tk.W)

        # Einstellungen-Bereich
        settings_frame = ttk.Frame(self.top_frame)
        settings_frame.pack(side=tk.RIGHT, fill=tk.Y, anchor=tk.NE)

        # Theme-Umschalter
        theme_var = tk.StringVar(value=self.config_manager.get_theme())
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(anchor=tk.E, pady=2)

        theme_label = ttk.Label(theme_frame, text="Theme:")
        theme_label.pack(side=tk.LEFT, padx=5)

        # Theme-Radiobuttons
        light_rb = ttk.Radiobutton(theme_frame, text="Hell",
                                   variable=theme_var, value="light",
                                   command=lambda: self.change_theme("light"))
        light_rb.pack(side=tk.LEFT, padx=2)

        dark_rb = ttk.Radiobutton(theme_frame, text="Dunkel",
                                  variable=theme_var, value="dark",
                                  command=lambda: self.change_theme("dark"))
        dark_rb.pack(side=tk.LEFT, padx=2)

        # Frame für fehlende Imports
        import_frame = ttk.Frame(self.main_frame)
        import_frame.pack(fill=tk.X, pady=10)

        import_label = ttk.Label(import_frame, text="Füge fehlende Imports hier ein:")
        import_label.pack(side=tk.LEFT, padx=5)

        # Eingabefeld für fehlende Imports
        self.missing_imports_var = tk.StringVar()
        self.missing_imports_entry = ttk.Entry(import_frame, textvariable=self.missing_imports_var,
                                               style="TEntry", width=40)
        self.missing_imports_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Button zum Hinzufügen der fehlenden Imports
        add_imports_button = ttk.Button(import_frame, text="Hinzufügen",
                                        command=self.add_missing_imports)
        add_imports_button.pack(side=tk.LEFT, padx=5)

        # Container für die ausgewählten Module
        self.selected_frame = ttk.LabelFrame(self.main_frame, text="Ausgewählte Module", padding=15)
        self.selected_frame.pack(fill=tk.X, pady=15)

        # Textfeld für ausgewählte Module mit etwas größerer Höhe für mobile Ansicht
        self.selected_text = scrolledtext.ScrolledText(self.selected_frame, height=4, width=50)
        self.selected_text.pack(fill=tk.X, expand=True, padx=5, pady=5)
        self.selected_text.configure(state='disabled', font=('Helvetica', 11),
                                     background=self.colors['bg_medium'])

        # Button-Frame für Aktionen
        self.action_frame = ttk.Frame(self.selected_frame)
        self.action_frame.pack(fill=tk.X, expand=True, pady=5)

        # Button-Frame für Import-Test und Löschen
        left_buttons = ttk.Frame(self.action_frame)
        left_buttons.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Button zum Import-Test
        self.import_test_button = ttk.Button(left_buttons, text="📦 Module testen",
                                             command=self.show_import_test_dialog)
        self.import_test_button.pack(side=tk.LEFT, padx=5)

        # Button zum Löschen aller ausgewählten Module
        self.clear_button = ttk.Button(left_buttons, text="🗑️ Liste leeren",
                                       command=self.clear_selected_modules)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # NEUE FUNKTION: Button zum Speichern der Auswahl
        self.save_button = ttk.Button(left_buttons, text="💾 Auswahl speichern",
                                      command=self.save_selection)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Button zum Generieren des Import-Codes
        self.generate_button = ttk.Button(self.action_frame, text="⚙️ Installationscode generieren",
                                          command=self.generate_import_code)
        self.generate_button.pack(side=tk.RIGHT, padx=5)

        # Container für die Kategoriebuttons
        self.categories_label = ttk.Label(self.main_frame,
                                          text="Modulkategorien:",
                                          style='SubHeader.TLabel')
        self.categories_label.pack(anchor=tk.W, pady=(15, 5))

        self.category_frame = ttk.Frame(self.main_frame)
        self.category_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Erstelle die Kategoriebuttons
        self._create_category_buttons()

        # Aktualisiere die Anzeige der ausgewählten Module
        self.update_selected_modules_display()

        # Binding für Enter-Taste im Import-Eingabefeld
        self.missing_imports_entry.bind("<Return>", lambda event: self.add_missing_imports())

    def _create_category_buttons(self):
        """
        Erstellt Buttons für jede Kategorie in einem Raster-Layout
        """
        categories = self.module_data.get_categories()

        # Für mobile-freundlicheres Layout: 2 Spalten statt 3
        # Passe die Anzahl der Spalten basierend auf der Fenstergröße an
        width = self.root.winfo_width()
        columns = 2 if width < 800 else 3
        rows = (len(categories) + columns - 1) // columns  # Runde auf

        # Frame für das scrollbare Kategorien-Grid
        self.canvas = tk.Canvas(self.category_frame, bg=self.colors['bg_light'],
                                highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.category_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack das Canvas und die Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Erstelle ein Raster mit der gewählten Anzahl an Spalten
        for i, category in enumerate(categories):
            row = i // columns
            col = i % columns

            # Erstelle einen Frame für jeden Button (für abgerundete Ecken)
            button_frame = ttk.Frame(self.scrollable_frame)
            button_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Erstelle Button mit Callback für die Kategorie
            # Benutze ein Canvas für abgerundete Ecken
            btn_canvas = tk.Canvas(button_frame, width=200, height=40,
                                   bg=self.colors['accent'],
                                   highlightthickness=0)
            btn_canvas.pack(fill="both", expand=True)

            # Zeichne abgerundetes Rechteck
            btn_canvas.create_rectangle(
                0, 0, 200, 40,
                fill=self.colors['accent'],
                outline=self.colors['accent'],
                width=0,
                tags="rect"
            )

            # Erstelle den Text auf dem Canvas
            btn_canvas.create_text(
                100, 20,
                text=category,
                fill="white",
                font=('Helvetica', 12),
                tags="text"
            )

            # Binde Klick-Event an den Canvas
            btn_canvas.tag_bind("rect", "<Button-1>",
                                lambda event, cat=category: self.show_category_modules(cat))
            btn_canvas.tag_bind("text", "<Button-1>",
                                lambda event, cat=category: self.show_category_modules(cat))

            # Hover-Effekt
            btn_canvas.tag_bind("rect", "<Enter>",
                                lambda event, canvas=btn_canvas: canvas.itemconfig(
                                    "rect", fill=self.colors['accent_dark']))
            btn_canvas.tag_bind("text", "<Enter>",
                                lambda event, canvas=btn_canvas: canvas.itemconfig(
                                    "rect", fill=self.colors['accent_dark']))

            btn_canvas.tag_bind("rect", "<Leave>",
                                lambda event, canvas=btn_canvas: canvas.itemconfig(
                                    "rect", fill=self.colors['accent']))
            btn_canvas.tag_bind("text", "<Leave>",
                                lambda event, canvas=btn_canvas: canvas.itemconfig(
                                    "rect", fill=self.colors['accent']))

        # Konfiguriere die Spalten, damit sie sich gleichmäßig ausdehnen
        for i in range(columns):
            self.scrollable_frame.columnconfigure(i, weight=1)

        # Mausrad-Unterstützung für das Canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        """
        Scrollt das Canvas mit dem Mausrad
        """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def change_theme(self, theme):
        """
        Wechselt zwischen hellem und dunklem Thema

        Args:
            theme: "light" oder "dark"
        """
        self.config_manager.set_theme(theme)

        # Aktualisiere die Farben
        if theme == "light":
            self.colors = {
                'bg_light': '#e8f5e9',  # Heller Hintergrund
                'bg_medium': '#c8e6c9',  # Mittlerer Hintergrund
                'bg_dark': '#81c784',  # Dunklerer Hintergrund
                'accent': '#4caf50',  # Akzentfarbe
                'accent_dark': '#2e7d32',  # Dunklere Akzentfarbe
                'text': '#212121',  # Text
                'text_light': '#757575'  # Heller Text
            }
        else:  # dark
            self.colors = self.dark_colors

        # Konfiguriere die Stile neu
        self._configure_styles()

        # Aktualisiere die Root-Hintergrundfarbe
        self.root.configure(background=self.colors['bg_light'])

        # Aktualisiere die Canvas-Hintergrundfarbe
        self.canvas.configure(background=self.colors['bg_light'])

        # Aktualisiere die Textfeld-Hintergrundfarbe
        self.selected_text.configure(background=self.colors['bg_medium'])

        # Zeige einen Hinweis an
        messagebox.showinfo("Theme geändert",
                            f"Das Theme wurde auf {theme} umgestellt. "
                            "Einige Elemente werden erst nach einem Neustart der Anwendung vollständig angepasst.")

    def add_missing_imports(self):
        """
        Fügt die im Textfeld eingegebenen fehlenden Imports zur Auswahlliste hinzu,
        filtert dabei Python-Schlüsselwörter und Standardmodule heraus
        """
        import_text = self.missing_imports_var.get().strip()

        if not import_text:
            messagebox.showinfo("Info", "Bitte gib mindestens einen Modulnamen ein.")
            return

        # Standardbibliotheken und Schlüsselwörter, die nicht installiert werden müssen
        python_std_libs = [
            "abc", "argparse", "array", "asyncio", "base64", "binascii", "bisect", "builtins",
            "calendar", "cmath", "collections", "concurrent", "contextlib", "copy", "csv",
            "ctypes", "datetime", "decimal", "difflib", "dis", "email", "enum", "errno",
            "fnmatch", "fractions", "functools", "gc", "getopt", "getpass", "glob", "hashlib",
            "heapq", "hmac", "html", "http", "importlib", "inspect", "io", "ipaddress",
            "itertools", "json", "keyword", "logging", "marshal", "math", "mimetypes",
            "multiprocessing", "netrc", "numbers", "operator", "os", "pathlib", "pickle",
            "pkgutil", "platform", "pprint", "random", "re", "reprlib", "secrets", "select",
            "shelve", "shlex", "shutil", "signal", "socket", "socketserver", "sqlite3",
            "statistics", "string", "stringprep", "struct", "subprocess", "sys", "tempfile",
            "textwrap", "threading", "time", "timeit", "token", "tokenize", "traceback",
            "turtle", "types", "typing", "unicodedata", "unittest", "urllib", "uuid",
            "warnings", "weakref", "webbrowser", "xml", "xmlrpc", "zipfile", "zipimport", "zlib"
        ]

        # Typings, die keine installierbaren Module sind
        typing_objects = [
            "Any", "Callable", "Dict", "Iterable", "List", "Optional", "Sequence", "Set",
            "Tuple", "TypeVar", "Union", "NewType", "Generic", "Type", "cast", "Final", "Protocol",
            "TypedDict", "Literal", "ClassVar", "NoReturn", "Never", "Annotated", "TypeAlias",
            "Self", "LiteralString", "RequiresTypeChecking"
        ]

        # Tkinter-spezifische Module und Klassen
        tkinter_objects = [
            "tk", "ttk", "messagebox", "scrolledtext", "filedialog", "colorchooser",
            "simpledialog", "Canvas", "Button", "Label", "Frame", "Entry", "Text",
            "Checkbutton", "Radiobutton", "Scale", "Scrollbar", "Listbox", "Menu",
            "Menubutton", "PanedWindow", "Spinbox", "LabelFrame"
        ]

        # Matplotlib-spezifische Module und Klassen
        matplotlib_objects = [
            "plt", "pyplot", "Figure", "Axes", "FigureCanvasTkAgg", "backend_tkagg",
            "matplotlib.pyplot", "matplotlib.backends.backend_tkagg"
        ]

        # Schlüsselwörter, die keine Module sind
        python_keywords = [
            "and", "as", "assert", "async", "await", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for", "from", "global",
            "if", "import", "in", "is", "lambda", "None", "nonlocal", "not", "or", "pass",
            "raise", "return", "True", "try", "while", "with", "yield"
        ]

        # Sammle und bereinige die Modulnamen aus dem Text
        # Unterstützt verschiedene Import-Stile und Trennzeichen
        import_text = import_text.replace('\n', ' ').replace(',', ' ').replace(';', ' ')
        parts = import_text.split()

        # Extrahiere Modulnamen aus den Importstatements
        modules_to_add = set()
        i = 0
        while i < len(parts):
            part = parts[i]

            # Überspringe Keywords
            if part in python_keywords:
                i += 1
                continue

            # Versuche, einen Modulnamen zu extrahieren
            module_name = part

            # Ignorieren von from/import-Konstrukten
            if i > 0 and parts[i - 1] == 'from':
                # Bei "from xyz import abc" ist xyz das Modul
                module_name = part
            elif i > 0 and parts[i - 1] == 'import':
                # Bei "import xyz as abc" ist xyz das Modul
                module_name = part
            elif i < len(parts) - 2 and parts[i + 1] == 'as':
                # Überspringe "as alias"-Teil
                i += 2

            # Ignoriere Module aus Standardbibliothek und Schlüsselwörter
            if (module_name not in python_std_libs and
                    module_name not in typing_objects and
                    module_name not in tkinter_objects and
                    module_name not in matplotlib_objects and
                    module_name not in python_keywords):

                # Bereinige den Modulnamen um eventuelle Untermodule
                # Beispiel: "requests.auth" -> "requests"
                base_module = module_name.split('.')[0]

                # PyPI-Namen sind oft anders als die Import-Namen
                # Prüfe auf bekannte Umbenennungen
                pypi_name = self._normalize_to_pypi_name(base_module)

                if pypi_name:
                    modules_to_add.add(pypi_name)

            i += 1

        # Schließe Duplikate aus
        modules_to_add = sorted(modules_to_add)

        # Wenn keine gültigen Module gefunden wurden
        if not modules_to_add:
            messagebox.showinfo("Info",
                                "Keine installierbaren Module in der Eingabe gefunden.\n"
                                "Python-Standardbibliotheken und Schlüsselwörter werden ignoriert.")
            return

        # Füge die Module zur Auswahlliste hinzu
        for module in modules_to_add:
            self.selected_modules.add(module)

        # Aktualisiere die Anzeige der ausgewählten Module
        self.update_selected_modules_display()

        # Aktualisiere alle Trees
        self.update_all_trees()

        # Leere das Eingabefeld
        self.missing_imports_var.set("")

        # Zeige eine Bestätigung
        messagebox.showinfo("Module hinzugefügt",
                            f"{len(modules_to_add)} installierbare Module wurden zur Liste hinzugefügt:\n"
                            f"{', '.join(modules_to_add)}")

    def _normalize_to_pypi_name(self, module_name):
        """
        Normalisiert einen Import-Namen zu einem PyPI-Paketnamen

        Args:
            module_name: Der Name des Moduls im Import

        Returns:
            Der PyPI-Name oder None, wenn kein installierbares Modul
        """
        # Mapping von Import-Namen zu PyPI-Namen
        # Hier können bekannte Abweichungen hinzugefügt werden
        pypi_mapping = {
            # Beispiele für abweichende Namen
            "bs4": "beautifulsoup4",
            "PIL": "pillow",
            "sklearn": "scikit-learn",
            # Weitere Mappings je nach Bedarf
        }

        # Direkte Zuordnung
        if module_name in pypi_mapping:
            return pypi_mapping[module_name]

        # Standardfall: Der Import-Name ist der PyPI-Name
        return module_name

    def on_module_select(self, event):
        """
        Wird aufgerufen, wenn ein Modul in der Tabelle angeklickt wird.
        Fügt das Modul zur Auswahlliste hinzu oder entfernt es.

        Args:
            event: Das Tabellen-Klick-Event
        """
        tree = event.widget
        region = tree.identify("region", event.x, event.y)

        if region == "cell":
            # Hole das ausgewählte Item und seine Werte
            item_id = tree.identify_row(event.y)
            if not item_id:
                return

            # Hole die Spalte, die angeklickt wurde
            column = tree.identify_column(event.x)
            column_index = int(column.replace('#', '')) - 1

            # Hole den Modulnamen aus dem Item
            values = tree.item(item_id, 'values')
            module_name = values[1]  # Index 1 entspricht der Spalte "name"

            # Wenn Doppelklick auf die Beschreibung erfolgt, zeige PyPI-Info
            if column_index == 2:  # Beschreibungsspalte
                self.show_pypi_info(module_name)
                return

            # Überprüfe, ob das Modul bereits ausgewählt ist
            if module_name in self.selected_modules:
                # Entferne das Modul aus der Auswahlliste
                self.selected_modules.remove(module_name)
                tree.set(item_id, "select", "☐")
            else:
                # Füge das Modul zur Auswahlliste hinzu
                self.selected_modules.add(module_name)
                tree.set(item_id, "select", "✅")

            # Aktualisiere die Anzeige der ausgewählten Module
            self.update_selected_modules_display()

            # Aktualisiere alle anderen Bäume
            self.update_all_trees()

    def show_pypi_info(self, module_name):
        """
        Zeigt Informationen zu einem Modul von PyPI an

        Args:
            module_name: Der Name des Moduls
        """
        # Erstelle ein neues Fenster für die PyPI-Info
        info_window = tk.Toplevel(self.root)
        info_window.title(f"PyPI-Info: {module_name}")
        info_window.geometry("600x400")
        info_window.configure(background=self.colors['bg_light'])
        info_window.transient(self.root)

        # Hauptframe
        frame = ttk.Frame(info_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Überschrift
        header = ttk.Label(frame, text=f"PyPI-Information: {module_name}",
                           style='Header.TLabel')
        header.pack(pady=(0, 15))

        # Infotext
        info_text = scrolledtext.ScrolledText(frame, width=70, height=12, font=('Helvetica', 11))
        info_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Füge Standardinformationen hinzu
        info_text.insert(tk.END, f"Modulname: {module_name}\n\n")

        # Versuche, Version und andere Informationen zu erhalten
        version = ModuleChecker.get_module_version(module_name)
        if version != "N/A":
            info_text.insert(tk.END, f"Installierte Version: {version}\n\n")

        # Füge einen Hinweis hinzu, dass Informationen von PyPI geladen werden
        info_text.insert(tk.END, "Lade Informationen von PyPI...\n")

        # Deaktiviere das Textfeld
        info_text.configure(state='disabled')

        # Button-Frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=15)

        # PyPI-Button
        pypi_button = ttk.Button(button_frame, text="Auf PyPI anzeigen",
                                 command=lambda: webbrowser.open(f"https://pypi.org/project/{module_name}/"))
        pypi_button.pack(side=tk.LEFT, padx=5)

        # Dokumentations-Button
        doc_button = ttk.Button(button_frame, text="Dokumentation",
                                command=lambda: self._open_doc_url(module_name))
        doc_button.pack(side=tk.LEFT, padx=5)

        # Schließen-Button
        close_button = ttk.Button(button_frame, text="Schließen",
                                  command=info_window.destroy)
        close_button.pack(side=tk.RIGHT, padx=5)

        # Starte einen Thread, um PyPI-Informationen zu laden
        thread = threading.Thread(target=self._load_pypi_info,
                                  args=(module_name, info_text, info_window))
        thread.daemon = True
        thread.start()

    def _load_pypi_info(self, module_name, info_text, window):
        """
        Lädt Informationen zu einem Modul von PyPI

        Args:
            module_name: Der Name des Moduls
            info_text: Das Textfeld für die Informationen
            window: Das Fenster, in dem die Informationen angezeigt werden
        """
        try:
            # Versuche, pip als Modul zu importieren, um Informationen über das Paket zu erhalten
            import pip._vendor.requests as requests

            # Mache eine Anfrage an die PyPI JSON API
            response = requests.get(f"https://pypi.org/pypi/{module_name}/json", timeout=5)

            if response.status_code == 200:
                # Parse die JSON-Antwort
                data = response.json()

                # Aktualisiere das Textfeld in der GUI (muss im Hauptthread erfolgen)
                window.after(0, lambda: self._update_pypi_info(info_text, data))
            else:
                # Fehler bei der Anfrage
                window.after(0, lambda: self._update_pypi_info_error(info_text,
                                                                     f"Fehler beim Laden der Informationen: Statuscode {response.status_code}"))
        except Exception as e:
            # Allgemeiner Fehler
            window.after(0, lambda: self._update_pypi_info_error(info_text,
                                                                 f"Fehler beim Laden der Informationen: {str(e)}"))

    def _update_pypi_info(self, info_text, data):
        """
        Aktualisiert das Textfeld mit den PyPI-Informationen

        Args:
            info_text: Das Textfeld für die Informationen
            data: Die PyPI-Daten als Dictionary
        """
        # Aktiviere das Textfeld zum Bearbeiten
        info_text.configure(state='normal')

        # Lösche den aktuellen Inhalt
        info_text.delete(1.0, tk.END)

        # Füge die Informationen hinzu
        info = data.get('info', {})
        releases = data.get('releases', {})

        # Modulname und Version
        name = info.get('name', 'N/A')
        version = info.get('version', 'N/A')
        info_text.insert(tk.END, f"Modulname: {name}\n")
        info_text.insert(tk.END, f"Aktuelle Version: {version}\n\n")

        # Zusammenfassung
        summary = info.get('summary', 'Keine Zusammenfassung verfügbar')
        info_text.insert(tk.END, f"Zusammenfassung:\n{summary}\n\n")

        # Autor
        author = info.get('author', 'N/A')
        author_email = info.get('author_email', 'N/A')
        info_text.insert(tk.END, f"Autor: {author}\n")
        if author_email != 'N/A':
            info_text.insert(tk.END, f"E-Mail: {author_email}\n")

        # Homepage und Dokumentation
        home_page = info.get('home_page', 'N/A')
        if home_page and home_page != 'N/A':
            info_text.insert(tk.END, f"\nHomepage: {home_page}\n")

        docs_url = info.get('docs_url', 'N/A')
        if docs_url and docs_url != 'N/A':
            info_text.insert(tk.END, f"Dokumentation: {docs_url}\n")

        # Lizenz
        license_info = info.get('license', 'N/A')
        info_text.insert(tk.END, f"\nLizenz: {license_info}\n\n")

        # Installation
        install_command = f"pip install {name}"
        info_text.insert(tk.END, f"Installation:\n{install_command}\n\n")

        # Abhängigkeiten
        requires_dist = info.get('requires_dist', [])
        if requires_dist:
            info_text.insert(tk.END, "Abhängigkeiten:\n")
            for dep in requires_dist[:10]:  # Begrenze auf 10 Abhängigkeiten
                info_text.insert(tk.END, f"- {dep}\n")

            if len(requires_dist) > 10:
                info_text.insert(tk.END, f"... und {len(requires_dist) - 10} weitere\n")

        # Deaktiviere das Textfeld wieder
        info_text.configure(state='disabled')

    def _update_pypi_info_error(self, info_text, error_message):
        """
        Aktualisiert das Textfeld mit einer Fehlermeldung

        Args:
            info_text: Das Textfeld für die Informationen
            error_message: Die Fehlermeldung
        """
        # Aktiviere das Textfeld zum Bearbeiten
        info_text.configure(state='normal')

        # Lösche den aktuellen Inhalt
        info_text.delete(1.0, tk.END)

        # Füge die Fehlermeldung hinzu
        info_text.insert(tk.END, f"Fehler beim Laden der PyPI-Informationen:\n\n{error_message}\n\n")
        info_text.insert(tk.END, "Versuche es später erneut oder besuche die PyPI-Website manuell.")

        # Deaktiviere das Textfeld wieder
        info_text.configure(state='disabled')

    def _open_doc_url(self, module_name):
        """
        Öffnet die Dokumentations-URL für ein Modul

        Args:
            module_name: Der Name des Moduls
        """
        # Suche nach dem Modul in allen Kategorien
        for category, modules in self.module_data.modules_by_category.items():
            for module in modules:
                if module["name"].lower() == module_name.lower():
                    # Öffne die Dokumentations-URL, wenn sie vorhanden ist
                    doc_url = module.get("doc_url", "")
                    if doc_url:
                        webbrowser.open(doc_url)
                        return

        # Wenn keine URL gefunden wurde, öffne die PyPI-Seite
        webbrowser.open(f"https://pypi.org/project/{module_name}/")

    def show_import_test_dialog(self):
        """
        Zeigt den Dialog zum Testen von Importen an
        """
        self.import_dialog = tk.Toplevel(self.root)
        self.import_dialog.title("Module Import Test")
        self.import_dialog.geometry("600x400")
        self.import_dialog.configure(background=self.colors['bg_light'])
        self.import_dialog.transient(self.root)
        self.import_dialog.grab_set()

        # Dialog-Inhalt
        frame = ttk.Frame(self.import_dialog, padding=25)
        frame.pack(fill=tk.BOTH, expand=True)

        # Überschrift
        header = ttk.Label(frame, text="Import-Test", style='Header.TLabel')
        header.pack(pady=(0, 15))

        # Beschreibung
        description = ttk.Label(frame,
                                text="Gib die Namen der Module ein, die du testen möchtest\n(durch Komma getrennt)",
                                wraplength=550)
        description.pack(pady=(0, 15))

        # Eingabefeld mit größerer Schrift für mobile Nutzung
        self.module_input = ttk.Entry(frame, width=50, font=('Helvetica', 12))
        self.module_input.pack(pady=(0, 20), fill=tk.X, ipady=5)  # ipady macht es höher
        self.module_input.focus_set()

        # Option, um fehlende Module automatisch zur Liste hinzuzufügen
        self.add_missing_var = tk.BooleanVar(value=True)
        add_missing_check = ttk.Checkbutton(frame,
                                            text="Fehlende Module automatisch zur Auswahlliste hinzufügen",
                                            variable=self.add_missing_var)
        add_missing_check.pack(anchor=tk.W, pady=(0, 15))

        # Beispieltext
        example = ttk.Label(frame,
                            text="Beispiel: numpy, pandas, matplotlib, requests",
                            font=('Helvetica', 10, 'italic'),
                            foreground=self.colors['text_light'])
        example.pack(pady=(0, 20))

        # Buttons mit besserem Styling für Touch-Bedienung
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)

        # Canvas für Abbrechen-Button mit abgerundeten Ecken
        cancel_canvas = tk.Canvas(btn_frame, width=120, height=40,
                                  bg=self.colors['bg_medium'],
                                  highlightthickness=0)
        cancel_canvas.pack(side=tk.LEFT, padx=(0, 10))

        # Zeichne abgerundetes Rechteck
        cancel_canvas.create_rectangle(
            0, 0, 120, 40,
            fill=self.colors['bg_medium'],
            outline=self.colors['bg_medium'],
            width=0,
            tags="rect"
        )

        # Text auf dem Canvas
        cancel_canvas.create_text(
            60, 20,
            text="Abbrechen",
            fill=self.colors['text'],
            font=('Helvetica', 12),
            tags="text"
        )

        # Binde Klick-Event
        cancel_canvas.tag_bind("rect", "<Button-1>",
                               lambda event: self.import_dialog.destroy())
        cancel_canvas.tag_bind("text", "<Button-1>",
                               lambda event: self.import_dialog.destroy())

        # Canvas für Test-Button mit abgerundeten Ecken
        test_canvas = tk.Canvas(btn_frame, width=150, height=40,
                                bg=self.colors['accent'],
                                highlightthickness=0)
        test_canvas.pack(side=tk.RIGHT)

        # Zeichne abgerundetes Rechteck
        test_canvas.create_rectangle(
            0, 0, 150, 40,
            fill=self.colors['accent'],
            outline=self.colors['accent'],
            width=0,
            tags="rect"
        )

        # Text auf dem Canvas
        test_canvas.create_text(
            75, 20,
            text="📦 Module testen",
            fill="white",
            font=('Helvetica', 12),
            tags="text"
        )

        # Binde Klick-Event
        test_canvas.tag_bind("rect", "<Button-1>",
                             lambda event: self.run_import_test())
        test_canvas.tag_bind("text", "<Button-1>",
                             lambda event: self.run_import_test())

        # Enter-Taste bindet an die Test-Funktion
        self.module_input.bind("<Return>", lambda event: self.run_import_test())

    def run_import_test(self):
        """
        Führt den Import-Test für die eingegebenen Module aus
        """
        input_text = self.module_input.get().strip()

        if not input_text:
            messagebox.showinfo("Info", "Bitte gib mindestens einen Modulnamen ein.")
            return

        # Extrahiere die Modulnamen und entferne Leerzeichen
        module_names = [name.strip() for name in input_text.split(',')]

        # Überprüfe die Module
        results = ModuleChecker.check_importable(module_names)

        # Erstelle die Ergebnismeldung
        success_modules = [name for name, success in results.items() if success]
        failed_modules = [name for name, success in results.items() if not success]

        message = "Testergebnisse:\n\n"

        if success_modules:
            message += "Erfolgreich importiert:\n"
            message += "\n".join(f"✅ {name}" for name in success_modules)
            message += "\n\n"

        if failed_modules:
            message += "Nicht importierbar:\n"
            message += "\n".join(f"❌ {name}" for name in failed_modules)
            message += "\n\n"
            message += "Hinweis: Diese Module müssen möglicherweise installiert werden.\n"
            message += "Du kannst sie mit 'pip install [modulname]' installieren."

        # Füge erfolgreiche Module zur Auswahlliste hinzu
        for module in success_modules:
            self.selected_modules.add(module)

        # Füge fehlende Module zur Auswahlliste hinzu, wenn die Option aktiviert ist
        if self.add_missing_var.get():
            for module in failed_modules:
                self.selected_modules.add(module)

        # Aktualisiere das Anzeigen der ausgewählten Module
        self.update_selected_modules_display()

        # Zeige die Ergebnisse an
        self.import_dialog.destroy()

        # Erstelle ein angepasstes Ergebnisfenster
        result_dialog = tk.Toplevel(self.root)
        result_dialog.title("Import-Testergebnisse")
        result_dialog.geometry("600x400")
        result_dialog.configure(background=self.colors['bg_light'])
        result_dialog.transient(self.root)
        result_dialog.grab_set()

        # Dialog-Inhalt
        frame = ttk.Frame(result_dialog, padding=25)
        frame.pack(fill=tk.BOTH, expand=True)

        # Überschrift
        header = ttk.Label(frame, text="Import-Testergebnisse", style='Header.TLabel')
        header.pack(pady=(0, 15))

        # Ergebnistext mit besserem Styling
        result_text = scrolledtext.ScrolledText(frame, width=70, height=12, font=('Helvetica', 11))
        result_text.insert(tk.END, message)
        result_text.configure(state='disabled', background=self.colors['bg_medium'])
        result_text.pack(fill=tk.BOTH, expand=True, pady=10)

        # Hinweis zur automatischen Hinzufügung
        if self.add_missing_var.get() and failed_modules:
            auto_add_text = "Fehlende Module wurden zur Auswahlliste hinzugefügt!"
            hint = ttk.Label(frame, text=auto_add_text, foreground=self.colors['accent_dark'],
                             font=('Helvetica', 12, 'bold'))
            hint.pack(pady=10)

        # OK-Button mit abgerundeten Ecken
        ok_canvas = tk.Canvas(frame, width=120, height=40,
                              bg=self.colors['accent'],
                              highlightthickness=0)
        ok_canvas.pack(pady=15)

        # Zeichne abgerundetes Rechteck
        ok_canvas.create_rectangle(
            0, 0, 120, 40,
            fill=self.colors['accent'],
            outline=self.colors['accent'],
            width=0,
            tags="rect"
        )

        # Text auf dem Canvas
        ok_canvas.create_text(
            60, 20,
            text="OK",
            fill="white",
            font=('Helvetica', 12, 'bold'),
            tags="text"
        )

        # Binde Klick-Event
        ok_canvas.tag_bind("rect", "<Button-1>",
                           lambda event: result_dialog.destroy())
        ok_canvas.tag_bind("text", "<Button-1>",
                           lambda event: result_dialog.destroy())

    def save_selection(self):
        """
        Speichert die aktuelle Auswahl in der Konfiguration
        """
        if not self.selected_modules:
            messagebox.showinfo("Info", "Es sind keine Module ausgewählt.")
            return

        # Speichere die ausgewählten Module
        self.config_manager.set_selected_modules(list(self.selected_modules))

        # Zeige Bestätigungsnachricht
        messagebox.showinfo("Auswahl gespeichert",
                            f"{len(self.selected_modules)} Module wurden gespeichert.\n"
                            "Sie werden beim nächsten Start der Anwendung automatisch geladen.")

    def show_category_modules(self, category: str):
        """
        Zeigt die Module einer ausgewählten Kategorie in einem neuen Fenster an

        Args:
            category: Der Name der Kategorie
        """
        # Hole die Module der ausgewählten Kategorie
        modules = self.module_data.get_modules_by_category(category)

        if not modules:
            messagebox.showinfo("Info", f"Keine Module in der Kategorie '{category}' gefunden.")
            return

        # Setze die aktuelle Kategorie
        self.current_category = category

        # Prüfe, ob bereits ein Fenster für diese Kategorie geöffnet ist
        if category in self.active_module_windows and self.active_module_windows[category].winfo_exists():
            # Bringe das Fenster in den Vordergrund
            self.active_module_windows[category].lift()
            # Aktualisiere die Auswahl in der Tabelle
            self._update_module_tree_selection(self.active_module_trees[category])
            return

        # Erstelle ein neues Fenster für die Modulliste
        module_window = tk.Toplevel(self.root)
        module_window.title(f"Module der Kategorie: {category}")
        module_window.geometry("900x600")  # Größeres Fenster für mehr Module
        module_window.configure(background=self.colors['bg_light'])
        module_window.transient(self.root)

        # Speichere das Fenster in der Liste der aktiven Fenster
        self.active_module_windows[category] = module_window

        # Binde das Schließen-Event, um das Fenster aus der Liste zu entfernen
        module_window.protocol("WM_DELETE_WINDOW",
                               lambda: self._on_module_window_close(category))

        # Hauptframe mit etwas Padding
        frame = ttk.Frame(module_window, padding=25)
        frame.pack(fill=tk.BOTH, expand=True)

        # Überschrift
        header = ttk.Label(frame, text=f"Top-15 Python-Module: {category}",
                           style='Header.TLabel')
        header.pack(pady=(0, 15))

        # Anleitung hinzufügen
        instruction = ttk.Label(frame,
                                text="Doppelklick auf ein Modul, um es zur Auswahlliste hinzuzufügen oder zu entfernen",
                                wraplength=800)
        instruction.pack(pady=(0, 15))

        # Erstelle die Tabelle mit den Moduldetails
        tree = self._create_module_table(frame, modules)

        # Speichere den Tree in der Liste der aktiven Trees
        self.active_module_trees[category] = tree

        # Button-Frame mit besserem Styling
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=15)

        # Canvas für Popularitäts-Button mit abgerundeten Ecken
        chart_canvas = tk.Canvas(button_frame, width=230, height=40,
                                 bg=self.colors['bg_dark'],
                                 highlightthickness=0)
        chart_canvas.pack(side=tk.LEFT, padx=5)

        # Zeichne abgerundetes Rechteck
        chart_canvas.create_rectangle(
            0, 0, 230, 40,
            fill=self.colors['bg_dark'],
            outline=self.colors['bg_dark'],
            width=0,
            tags="chart_rect"
        )

        # Text auf dem Canvas
        chart_canvas.create_text(
            115, 20,
            text="📊 Popularitätsdiagramm",
            fill="white",
            font=('Helvetica', 12),
            tags="chart_text"
        )

        # Binde Klick-Event
        chart_canvas.tag_bind("chart_rect", "<Button-1>",
                              lambda event: self.show_popularity_chart(category))
        chart_canvas.tag_bind("chart_text", "<Button-1>",
                              lambda event: self.show_popularity_chart(category))

        # Canvas für Alle-Auswählen-Button mit abgerundeten Ecken
        select_all_canvas = tk.Canvas(button_frame, width=180, height=40,
                                      bg=self.colors['accent'],
                                      highlightthickness=0)
        select_all_canvas.pack(side=tk.RIGHT, padx=5)

        # Zeichne abgerundetes Rechteck
        select_all_canvas.create_rectangle(
            0, 0, 180, 40,
            fill=self.colors['accent'],
            outline=self.colors['accent'],
            width=0,
            tags="select_rect"
        )

        # Text auf dem Canvas
        select_all_canvas.create_text(
            90, 20,
            text="✅ Alle auswählen",
            fill="white",
            font=('Helvetica', 12),
            tags="select_text"
        )

        # Binde Klick-Event
        select_all_canvas.tag_bind("select_rect", "<Button-1>",
                                   lambda event: self.select_all_modules(modules, tree))
        select_all_canvas.tag_bind("select_text", "<Button-1>",
                                   lambda event: self.select_all_modules(modules, tree))

    def _on_module_window_close(self, category):
        """
        Wird aufgerufen, wenn ein Modulfenster geschlossen wird

        Args:
            category: Die Kategorie des geschlossenen Fensters
        """
        # Entferne das Fenster aus der Liste der aktiven Fenster
        if category in self.active_module_windows:
            self.active_module_windows[category].destroy()
            del self.active_module_windows[category]

        # Entferne den Tree aus der Liste der aktiven Trees
        if category in self.active_module_trees:
            del self.active_module_trees[category]

    def _create_module_table(self, parent, modules: List[Dict[str, str]]):
        """
        Erstellt eine Tabelle mit den Moduldetails

        Args:
            parent: Das Elternelement für die Tabelle
            modules: Liste der Module mit ihren Details

        Returns:
            Der erstellte Treeview
        """
        # Erstelle ein Frame für den Treeview mit Scrollbar
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar mit angepasstem Styling
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview für die Tabelle
        columns = ("select", "name", "description", "version", "doc_url")

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                            yscrollcommand=scrollbar.set,
                            style="Treeview")

        # Definiere die Spaltenheader
        tree.heading("select", text="Auswählen")
        tree.heading("name", text="Modulname")
        tree.heading("description", text="Beschreibung")
        tree.heading("version", text="Aktuelle Version")
        tree.heading("doc_url", text="Dokumentation")

        # Definiere die Spaltenbreiten
        tree.column("select", width=80, anchor=tk.CENTER)
        tree.column("name", width=150)
        tree.column("description", width=300)
        tree.column("version", width=100)
        tree.column("doc_url", width=200)

        # Füge die Module zur Tabelle hinzu
        for i, module in enumerate(modules):
            # Versuche, die aktuelle Version des Moduls zu ermitteln
            version = ModuleChecker.get_module_version(module["name"])

            # Überprüfe, ob das Modul bereits ausgewählt ist
            select_text = "✅" if module["name"] in self.selected_modules else "☐"

            # Hole die URL für die Dokumentation
            doc_url = module.get("doc_url", "N/A")

            item_id = tree.insert("", tk.END, values=(
                select_text,
                module["name"],
                module["description"],
                version,
                doc_url
            ))

            # Setze den Tag für das Item, um später auf das Modul zugreifen zu können
            tree.item(item_id, tags=(module["name"],))

            # Alternativ graue und weiße Zeilen für bessere Lesbarkeit
            if i % 2 == 0:
                tree.item(item_id, tags=(module["name"], "even"))
            else:
                tree.item(item_id, tags=(module["name"], "odd"))

        # Konfiguriere Farbwechsel für Zeilen
        tree.tag_configure('even', background=self.colors['bg_light'])
        tree.tag_configure('odd', background=self.colors['bg_medium'])

        # Packe die Tabelle und verbinde sie mit der Scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=tree.yview)

        # Binde Doppelklick-Event an den Treeview, um ein Modul auszuwählen/abzuwählen
        tree.bind("<Double-1>", self.on_module_select)

        # Für Touch-Bedienung: Auch einfacher Klick auf die Auswahl-Spalte
        tree.bind("<ButtonRelease-1>", lambda event: self.on_table_click(event, tree))

        return tree

    def _update_module_tree_selection(self, tree):
        """
        Aktualisiert die Auswahl in einem Treeview basierend auf den ausgewählten Modulen

        Args:
            tree: Der zu aktualisierende Treeview
        """
        if not tree:
            return

        # Für jedes Item im Tree
        for item_id in tree.get_children():
            # Hole den Modulnamen
            values = tree.item(item_id, 'values')
            if not values:
                continue

            module_name = values[1]  # Index 1 entspricht der Spalte "name"

            # Aktualisiere den Auswahlstatus
            select_text = "✅" if module_name in self.selected_modules else "☐"
            tree.set(item_id, "select", select_text)

    def update_all_trees(self):
        """
        Aktualisiert die Auswahl in allen aktiven Treeviews
        """
        # Aktualisiere die Trees in allen geöffneten Modulfenstern
        for tree in self.active_module_trees.values():
            self._update_module_tree_selection(tree)

        # Aktualisiere auch den Suchergebniss-Tree, falls vorhanden
        if hasattr(self, 'search_results_tree') and self.search_results_tree.winfo_exists():
            self._update_module_tree_selection(self.search_results_tree)

    def on_module_select(self, event):
        """
        Wird aufgerufen, wenn ein Modul in der Tabelle angeklickt wird.
        Fügt das Modul zur Auswahlliste hinzu oder entfernt es.

        Args:
            event: Das Tabellen-Klick-Event
        """
        tree = event.widget
        region = tree.identify("region", event.x, event.y)

        if region == "cell":
            # Hole das ausgewählte Item und seine Werte
            item_id = tree.identify_row(event.y)
            if not item_id:
                return

            # Hole die Spalte, die angeklickt wurde
            column = tree.identify_column(event.x)

            # Hole den Modulnamen aus dem Item
            values = tree.item(item_id, 'values')
            module_name = values[1]  # Index 1 entspricht der Spalte "name"

            # Überprüfe, ob das Modul bereits ausgewählt ist
            if module_name in self.selected_modules:
                # Entferne das Modul aus der Auswahlliste
                self.selected_modules.remove(module_name)
                tree.set(item_id, "select", "☐")
            else:
                # Füge das Modul zur Auswahlliste hinzu
                self.selected_modules.add(module_name)
                tree.set(item_id, "select", "✅")

            # Aktualisiere die Anzeige der ausgewählten Module
            self.update_selected_modules_display()

            # Aktualisiere alle anderen Bäume
            self.update_all_trees()

    def on_table_click(self, event, tree):
        """
        Wird aufgerufen, wenn in der Tabelle geklickt wird.
        - Öffnet die Dokumentations-URL, wenn auf die URL-Spalte geklickt wird
        - Wählt das Modul aus/ab, wenn auf die Auswählen-Spalte geklickt wird

        Args:
            event: Das Tabellen-Klick-Event
            tree: Der Treeview
        """
        # Hole den ausgewählten Item und seine Werte
        item_id = tree.identify_row(event.y)
        if not item_id:
            return

        # Hole die angeklickte Spalte
        column = tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1

        values = tree.item(item_id, 'values')
        if not values:
            return

        # Wenn auf die Dokumentations-URL geklickt wurde
        if column_index == 4:  # Index 4 entspricht der Spalte "doc_url"
            url = values[4]

            # Öffne die URL im Standard-Browser
            if url and url != "N/A":
                webbrowser.open(url)

        # Wenn auf die Auswählen-Spalte geklickt wurde
        elif column_index == 0:  # Index 0 entspricht der Spalte "select"
            module_name = values[1]  # Index 1 entspricht der Spalte "name"

            # Überprüfe, ob das Modul bereits ausgewählt ist
            if module_name in self.selected_modules:
                # Entferne das Modul aus der Auswahlliste
                self.selected_modules.remove(module_name)
                tree.set(item_id, "select", "☐")
            else:
                # Füge das Modul zur Auswahlliste hinzu
                self.selected_modules.add(module_name)
                tree.set(item_id, "select", "✅")

            # Aktualisiere die Anzeige der ausgewählten Module
            self.update_selected_modules_display()

            # Aktualisiere alle anderen Bäume
            self.update_all_trees()

    def update_selected_modules_display(self):
        """
        Aktualisiert die Anzeige der ausgewählten Module im Hauptfenster
        """
        # Aktiviere das Textfeld zum Bearbeiten
        self.selected_text.configure(state='normal')

        # Lösche den aktuellen Inhalt
        self.selected_text.delete(1.0, tk.END)

        # Füge die ausgewählten Module ein
        if self.selected_modules:
            self.selected_text.insert(tk.END, ", ".join(sorted(self.selected_modules)))
        else:
            self.selected_text.insert(tk.END, "Keine Module ausgewählt")

        # Deaktiviere das Textfeld wieder
        self.selected_text.configure(state='disabled')

    def clear_selected_modules(self):
        """
        Leert die Liste der ausgewählten Module
        """
        # Bestätigungsdialog, wenn Module ausgewählt sind
        if self.selected_modules:
            confirm = messagebox.askyesno("Bestätigung",
                                          f"Willst du wirklich alle {len(self.selected_modules)} ausgewählten Module entfernen?")
            if not confirm:
                return

        self.selected_modules.clear()
        self.update_selected_modules_display()

        # Aktualisiere alle Trees
        self.update_all_trees()

    def select_all_modules(self, modules, tree):
        """
        Wählt alle Module einer Kategorie aus

        Args:
            modules: Liste der Module
            tree: Der Treeview mit den Modulen
        """
        # Füge alle Module zur Auswahlliste hinzu
        for module in modules:
            self.selected_modules.add(module["name"])

        # Aktualisiere die Anzeige der ausgewählten Module
        self.update_selected_modules_display()

        # Aktualisiere die Anzeige in der Tabelle
        for item_id in tree.get_children():
            values = tree.item(item_id, 'values')
            if values:
                tree.set(item_id, "select", "✅")

        # Aktualisiere alle anderen Bäume
        self.update_all_trees()

    def generate_import_code(self):
        """
        Generiert Code zum Importieren und Installieren der ausgewählten Module
        und zeigt diesen in einem neuen Fenster an
        """
        if not self.selected_modules:
            messagebox.showinfo("Info", "Bitte wähle mindestens ein Modul aus.")
            return

        # Erstelle ein neues Fenster für den generierten Code
        code_window = tk.Toplevel(self.root)
        code_window.title("Import und Installation der ausgewählten Module")
        code_window.geometry("800x700")  # Etwas größer für bessere Lesbarkeit
        code_window.configure(background=self.colors['bg_light'])

        # Hauptframe
        frame = ttk.Frame(code_window, padding=25)
        frame.pack(fill=tk.BOTH, expand=True)

        # Überschrift
        header = ttk.Label(frame, text="Importcode und Installationsbefehle",
                           style='Header.TLabel')
        header.pack(pady=(0, 20))

        # Sortierte Liste der Module
        module_list = sorted(self.selected_modules)
        module_string = " ".join(module_list)

        # Erstelle ein Notebook für die verschiedenen Code-Ansichten
        notebook = ttk.Notebook(frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Tab 1: Import-Code
        import_tab = ttk.Frame(notebook)
        notebook.add(import_tab, text="Import-Code")

        # Importcode erstellen
        import_code = "# Python Import-Anweisungen\n"
        for module in module_list:
            # Überprüfe, ob der Modulname Bindestriche enthält (für pip-Namen)
            if "-" in module:
                # Ersetze Bindestriche durch Unterstriche für den Import
                import_module = module.replace("-", "_")
                import_code += f"import {import_module}\n"
            else:
                import_code += f"import {module}\n"

        # Importcode-Section mit angepasstem Styling
        import_frame = ttk.Frame(import_tab, padding=15)
        import_frame.pack(fill=tk.BOTH, expand=True)

        # Größere Schrift und Zeilenhöhe für bessere Lesbarkeit auf Mobilgeräten
        import_text = scrolledtext.ScrolledText(import_frame, height=15, width=80,
                                                font=('Consolas', 12),
                                                background=self.colors['bg_medium'])
        import_text.insert(tk.END, import_code)
        import_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button-Frame für Import-Tab
        import_button_frame = ttk.Frame(import_tab)
        import_button_frame.pack(fill=tk.X, pady=10)

        # Styled Checkbutton für Import-Tests
        test_options_frame = ttk.Frame(import_button_frame)
        test_options_frame.pack(fill=tk.X, pady=10)

        test_var = tk.BooleanVar(value=True)
        test_checkbox = ttk.Checkbutton(test_options_frame,
                                        text="Import-Tests hinzufügen (empfohlen)",
                                        variable=test_var,
                                        command=lambda: self.update_import_code(import_text, module_list,
                                                                                test_var.get()))
        test_checkbox.pack(side=tk.LEFT, padx=5)

        # Button zum Kopieren des Importcodes (angepasstes Styling)
        copy_import_canvas = tk.Canvas(test_options_frame, width=160, height=35,
                                       bg=self.colors['accent'],
                                       highlightthickness=0)
        copy_import_canvas.pack(side=tk.RIGHT, padx=5)

        # Zeichne abgerundetes Rechteck
        copy_import_canvas.create_rectangle(
            0, 0, 160, 35,
            fill=self.colors['accent'],
            outline=self.colors['accent'],
            width=0,
            tags="copy_rect"
        )

        # Text auf dem Canvas
        copy_import_canvas.create_text(
            80, 17,
            text="📋 Code kopieren",
            fill="white",
            font=('Helvetica', 12),
            tags="copy_text"
        )

        # Binde Klick-Event
        copy_import_canvas.tag_bind("copy_rect", "<Button-1>",
                                    lambda event: self.copy_to_clipboard(import_text.get(1.0, tk.END)))
        copy_import_canvas.tag_bind("copy_text", "<Button-1>",
                                    lambda event: self.copy_to_clipboard(import_text.get(1.0, tk.END)))

        # Tab 2: Installationsbefehle
        install_tab = ttk.Frame(notebook)
        notebook.add(install_tab, text="Installationsbefehle")

        # Installationsbefehle-Section
        install_frame = ttk.Frame(install_tab, padding=15)
        install_frame.pack(fill=tk.BOTH, expand=True)

        # Größere Schrift für Installationsbefehle
        install_text = scrolledtext.ScrolledText(install_frame, width=80, height=20,
                                                 font=('Consolas', 12),
                                                 background=self.colors['bg_medium'])

        # Generiere Installationsbefehle für alle Betriebssysteme
        current_platform = platform.system()
        platform_note = f"# Dein System: {current_platform}\n\n"

        install_commands = f"{platform_note}# INSTALLATIONSBEFEHLE FÜR MODULE\n{'=' * 40}\n\n"

        # Windows-Befehle
        install_commands += f"### WINDOWS (CMD) ###\n"
        install_commands += f"pip install {module_string}\n\n"
        install_commands += f"### WINDOWS (PowerShell) ###\n"
        install_commands += f"& \"python\" -m pip install {module_string}\n\n"

        # Linux-Befehle
        install_commands += f"### LINUX ###\n"
        install_commands += f"python3 -m pip install {module_string}\n\n"
        install_commands += f"# Mit sudo:\n"
        install_commands += f"sudo python3 -m pip install {module_string}\n\n"

        # macOS-Befehle
        install_commands += f"### macOS ###\n"
        install_commands += f"python3 -m pip install {module_string}\n\n"

        # Virtuelle Umgebung
        install_commands += f"### VIRTUELLE UMGEBUNG ###\n"
        install_commands += f"# Aktiviere zuerst deine virtuelle Umgebung, dann:\n"
        install_commands += f"pip install {module_string}\n\n"

        install_commands += f"{'=' * 40}\n"
        install_commands += f"# INSTALLATIONSANLEITUNG\n"
        install_commands += f"{'=' * 40}\n\n"

        install_commands += f"1. WINDOWS:\n"
        install_commands += f"   - CMD: Öffne die Eingabeaufforderung und kopiere den Befehl\n"
        install_commands += f"   - PowerShell: Öffne PowerShell und kopiere den PowerShell-Befehl\n\n"

        install_commands += f"2. LINUX:\n"
        install_commands += f"   - Öffne ein Terminal\n"
        install_commands += f"   - Kopiere den Linux-Befehl\n"
        install_commands += f"   - Führe den Befehl aus (möglicherweise mit sudo)\n\n"

        install_commands += f"3. macOS:\n"
        install_commands += f"   - Öffne ein Terminal\n"
        install_commands += f"   - Kopiere den macOS-Befehl\n"
        install_commands += f"   - Führe den Befehl aus\n\n"

        install_commands += f"4. VIRTUELLE UMGEBUNG:\n"
        install_commands += f"   - Windows: .\\venv\\Scripts\\activate\n"
        install_commands += f"   - Linux/macOS: source venv/bin/activate\n"
        install_commands += f"   - Danach: pip install [Module]\n"

        install_text.insert(tk.END, install_commands)
        install_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Button-Frame für Installations-Tab
        install_button_frame = ttk.Frame(install_tab)
        install_button_frame.pack(fill=tk.X, pady=10)

        # Button zum Kopieren der Installationsbefehle
        copy_install_canvas = tk.Canvas(install_button_frame, width=220, height=35,
                                        bg=self.colors['accent'],
                                        highlightthickness=0)
        copy_install_canvas.pack(side=tk.RIGHT, padx=5)

        # Zeichne abgerundetes Rechteck
        copy_install_canvas.create_rectangle(
            0, 0, 220, 35,
            fill=self.colors['accent'],
            outline=self.colors['accent'],
            width=0,
            tags="copy_install_rect"
        )

        # Text auf dem Canvas
        copy_install_canvas.create_text(
            110, 17,
            text="📋 Installationsbefehle kopieren",
            fill="white",
            font=('Helvetica', 12),
            tags="copy_install_text"
        )

        # Binde Klick-Event
        copy_install_canvas.tag_bind("copy_install_rect", "<Button-1>",
                                     lambda event: self.copy_to_clipboard(install_text.get(1.0, tk.END)))
        copy_install_canvas.tag_bind("copy_install_text", "<Button-1>",
                                     lambda event: self.copy_to_clipboard(install_text.get(1.0, tk.END)))

        # Tab 3: Einzelne Module
        module_tab = ttk.Frame(notebook)
        notebook.add(module_tab, text="Einzelne Module")

        # Erstelle eine Liste mit einzelnen Installationsbefehlen
        module_frame = ttk.Frame(module_tab, padding=15)
        module_frame.pack(fill=tk.BOTH, expand=True)

        # Erklärung
        explanation = ttk.Label(module_frame,
                                text="Installationsbefehle für jedes Modul einzeln:")
        explanation.pack(anchor=tk.W, pady=5)

        # Liste mit einzelnen Modulen
        module_list_frame = ttk.Frame(module_frame)
        module_list_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(module_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Treeview für die Module
        columns = ("module", "command", "status")
        module_tree = ttk.Treeview(module_list_frame, columns=columns, show="headings",
                                   yscrollcommand=scrollbar.set,
                                   style="Treeview")

        # Definiere die Spaltenheader
        module_tree.heading("module", text="Modulname")
        module_tree.heading("command", text="Installationsbefehl")
        module_tree.heading("status", text="Status")

        # Definiere die Spaltenbreiten
        module_tree.column("module", width=150)
        module_tree.column("command", width=400)
        module_tree.column("status", width=100)

        # Füge die Module hinzu
        for i, module in enumerate(module_list):
            # Erstelle den Installationsbefehl
            command = ModuleChecker.get_module_install_command(module, current_platform)

            # Ermittle den Status (installiert oder nicht)
            status = "✅ Installiert" if ModuleChecker.check_importable([module])[module] else "❌ Nicht installiert"

            item_id = module_tree.insert("", tk.END, values=(
                module,
                command,
                status
            ))

            # Alternativ graue und weiße Zeilen für bessere Lesbarkeit
            if i % 2 == 0:
                module_tree.item(item_id, tags=("even",))
            else:
                module_tree.item(item_id, tags=("odd",))

        # Konfiguriere Farbwechsel für Zeilen
        module_tree.tag_configure('even', background=self.colors['bg_light'])
        module_tree.tag_configure('odd', background=self.colors['bg_medium'])

        # Packe die Tabelle und verbinde sie mit der Scrollbar
        module_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=module_tree.yview)

        # Button zum Kopieren eines einzelnen Befehls bei Klick
        module_tree.bind("<Double-1>", lambda e: self._copy_single_command(e, module_tree))

        # Schließen-Button unten
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=15)

        close_canvas = tk.Canvas(button_frame, width=150, height=40,
                                 bg=self.colors['bg_dark'],
                                 highlightthickness=0)
        close_canvas.pack(side=tk.RIGHT)

        # Zeichne abgerundetes Rechteck
        close_canvas.create_rectangle(
            0, 0, 150, 40,
            fill=self.colors['bg_dark'],
            outline=self.colors['bg_dark'],
            width=0,
            tags="close_rect"
        )

        # Text auf dem Canvas
        close_canvas.create_text(
            75, 20,
            text="Schließen",
            fill="white",
            font=('Helvetica', 12),
            tags="close_text"
        )

        # Binde Klick-Event
        close_canvas.tag_bind("close_rect", "<Button-1>",
                              lambda event: code_window.destroy())
        close_canvas.tag_bind("close_text", "<Button-1>",
                              lambda event: code_window.destroy())

        # Aktualisiere den Importcode mit Tests, wenn Checkbox aktiv ist
        if test_var.get():
            self.update_import_code(import_text, module_list, True)

    def _copy_single_command(self, event, tree):
        """
        Kopiert den Installationsbefehl für ein einzelnes Modul

        Args:
            event: Das Event
            tree: Der Treeview
        """
        # Hole das ausgewählte Item
        item_id = tree.identify_row(event.y)
        if not item_id:
            return

        # Hole die angeklickte Spalte
        column = tree.identify_column(event.x)

        # Hole den Befehl
        values = tree.item(item_id, 'values')
        if not values:
            return

        command = values[1]  # Index 1 ist die Befehlsspalte
        module_name = values[0]  # Index 0 ist der Modulname

        # Kopiere den Befehl
        self.root.clipboard_clear()
        self.root.clipboard_append(command)

        # Zeige eine Bestätigung
        messagebox.showinfo("Kopiert", f"Installationsbefehl für '{module_name}' wurde in die Zwischenablage kopiert.")

    def update_import_code(self, text_widget, module_list, include_tests):
        """
        Aktualisiert den Import-Code mit oder ohne Tests

        Args:
            text_widget: Das Textfeld mit dem Code
            module_list: Liste der Module
            include_tests: Boolean, ob Tests hinzugefügt werden sollen
        """
        # Lösche den aktuellen Inhalt
        text_widget.delete(1.0, tk.END)

        # Basis-Import-Code
        import_code = "# Python Import-Anweisungen\n"

        if include_tests:
            import_code += """
# Liste für fehlgeschlagene Importe
fehlende_module = []

print("Überprüfe Module...")
"""

            for module in module_list:
                # Überprüfe, ob der Modulname Bindestriche enthält
                if "-" in module:
                    import_module = module.replace("-", "_")
                    import_code += f"""
try:
    import {import_module}
    print("✅ {module} erfolgreich importiert")
except ImportError:
    print("❌ {module} nicht gefunden")
    fehlende_module.append("{module}")
"""
                else:
                    import_code += f"""
try:
    import {module}
    print("✅ {module} erfolgreich importiert")
except ImportError:
    print("❌ {module} nicht gefunden")
    fehlende_module.append("{module}")
"""

            import_code += """
# Zeige Installationsanweisungen für fehlende Module
if fehlende_module:
    print("\\nFolgende Module müssen installiert werden:")
    for modul in fehlende_module:
        print(f"  - {modul}")
    print("\\nInstallationsbefehl:")
    print(f"pip install {' '.join(fehlende_module)}")
else:
    print("\\nAlle Module wurden erfolgreich importiert!")
"""
        else:
            # Einfacher Import-Code ohne Tests
            for module in module_list:
                # Überprüfe, ob der Modulname Bindestriche enthält
                if "-" in module:
                    import_module = module.replace("-", "_")
                    import_code += f"import {import_module}\n"
                else:
                    import_code += f"import {module}\n"

        # Füge den aktualisierten Code ein
        text_widget.insert(tk.END, import_code)

    def copy_to_clipboard(self, text):
        """
        Kopiert Text in die Zwischenablage

        Args:
            text: Der zu kopierende Text
        """
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Info", "Text wurde in die Zwischenablage kopiert.")

    def show_popularity_chart(self, category: str):
        """
        Zeigt ein Balkendiagramm mit der Popularität der Module einer Kategorie

        Args:
            category: Der Name der Kategorie
        """
        # Hole die Popularitätsdaten für die Kategorie
        popularity_data = self.module_data.get_module_popularity(category)

        if not popularity_data:
            messagebox.showinfo("Info", "Keine Popularitätsdaten verfügbar.")
            return

        # Erstelle ein neues Fenster für das Diagramm
        chart_window = tk.Toplevel(self.root)
        chart_window.title(f"Modulpopularität: {category}")
        chart_window.geometry("800x600")
        chart_window.configure(background=self.colors['bg_light'])

        # Frame für das Diagramm
        frame = ttk.Frame(chart_window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Überschrift
        header = ttk.Label(frame, text=f"Modulpopularität: {category}",
                           style='Header.TLabel')
        header.pack(pady=(0, 20))

        # Erstelle die Matplotlib-Figur
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor(self.colors['bg_light'])
        ax.set_facecolor(self.colors['bg_light'])

        # Sortiere die Daten für eine bessere Darstellung
        sorted_data = dict(sorted(popularity_data.items(), key=lambda x: x[1], reverse=True))

        # Erstelle das Balkendiagramm mit angepassten Farben
        bars = ax.bar(sorted_data.keys(), sorted_data.values(),
                      color=self.colors['accent'], edgecolor=self.colors['accent_dark'])

        # Anpassen der Achsen
        ax.set_ylabel('Popularität (Downloads/Monat)', color=self.colors['text'])
        ax.set_title(f'Popularität der Python-Module ({category})',
                     color=self.colors['accent_dark'], fontsize=14, fontweight='bold')

        # Farben für die Achsen und Beschriftungen anpassen
        ax.tick_params(axis='x', colors=self.colors['text'])
        ax.tick_params(axis='y', colors=self.colors['text'])

        for spine in ax.spines.values():
            spine.set_color(self.colors['text_light'])

        # Drehe die x-Achsenbeschriftungen für bessere Lesbarkeit
        plt.xticks(rotation=45, ha='right', color=self.colors['text'])

        # Werte über den Balken anzeigen
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 Punkte vertikaler Offset
                        textcoords="offset points",
                        ha='center', va='bottom',
                        color=self.colors['text'])

        # Passe das Layout an
        plt.tight_layout()

        # Erstelle ein Canvas für die Matplotlib-Figur
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Button zum Speichern des Diagramms
        save_button_frame = ttk.Frame(frame)
        save_button_frame.pack(fill=tk.X, pady=10)

        save_canvas = tk.Canvas(save_button_frame, width=180, height=40,
                                bg=self.colors['accent'],
                                highlightthickness=0)
        save_canvas.pack(side=tk.RIGHT)

        # Zeichne abgerundetes Rechteck
        save_canvas.create_rectangle(
            0, 0, 180, 40,
            fill=self.colors['accent'],
            outline=self.colors['accent'],
            width=0,
            tags="save_rect"
        )

        # Text auf dem Canvas
        save_canvas.create_text(
            90, 20,
            text="💾 Diagramm speichern",
            fill="white",
            font=('Helvetica', 12),
            tags="save_text"
        )

        # Binde Klick-Event
        save_canvas.tag_bind("save_rect", "<Button-1>",
                             lambda event: self._save_chart(fig, category))
        save_canvas.tag_bind("save_text", "<Button-1>",
                             lambda event: self._save_chart(fig, category))

    def _save_chart(self, fig, category):
        """
        Speichert das Diagramm als Bilddatei

        Args:
            fig: Die Matplotlib-Figur
            category: Die Kategorie für den Dateinamen
        """
        # Verzeichnis für die Diagramme erstellen, falls es nicht existiert
        charts_dir = os.path.join(self.config_manager.config_dir, "charts")
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)

        # Dateiname mit Zeitstempel
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(charts_dir, f"modulepopularity_{category}_{timestamp}.png")

        # Speichere das Diagramm
        fig.savefig(filename, facecolor=fig.get_facecolor(), bbox_inches='tight', dpi=300)

        # Zeige eine Erfolgsmeldung
        messagebox.showinfo("Diagramm gespeichert",
                            f"Das Diagramm wurde als\n{filename}\ngespeichert.")


def check_python_version():
    """
    Überprüft, ob die Python-Version kompatibel ist

    Returns:
        True, wenn die Version kompatibel ist, sonst False
    """
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 6):
        messagebox.showerror("Python-Version nicht unterstützt",
                             "Diese Anwendung benötigt Python 3.6 oder neuer.\n"
                             f"Du verwendest Python {major}.{minor}.")
        return False
    return True


def main():
    """
    Hauptfunktion zum Starten der Anwendung
    """
    # Überprüfe die Python-Version
    if not check_python_version():
        return

    root = tk.Tk()
    root.title("Python Module Explorer")

    # Setze ein minimales Fenster
    root.minsize(800, 600)

    # Versuche, ein Anwendungssymbol zu setzen
    try:
        # Für Windows
        if platform.system() == "Windows":
            root.iconbitmap(default="python.ico")
        # Für Linux und macOS
        else:
            logo = tk.PhotoImage(file="python.png")
            root.iconphoto(True, logo)
    except Exception:
        # Ignoriere Fehler beim Setzen des Icons
        pass

    # Erstelle die Anwendung
    app = ModuleExplorerApp(root)

    # Starte die Hauptschleife
    root.mainloop()


if __name__ == "__main__":
    main()