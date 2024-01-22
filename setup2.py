from cx_Freeze import setup, Executable


# Configurações do executável
exe = Executable(
    script='main.py',
    base='Console',
)


# Configurações do setup
setup(
    name='NomeDoSeuProjeto',
    version='1.0',
    description='Descrição do seu projeto',
    options={
        'build_exe': {
            'packages': [
                'aiofiles', 'aiohttp', 'aiosignal', 'altgraph', 'appdirs',
                'attrs', 'auto-py-to-exe', 'beautifulsoup4', 'black',
                'blinker', 'bottle', 'bottle-websocket', 'capsolver-api',
                'certifi', 'cffi', 'charset-normalizer', 'click', 'colorama',
                'contourpy', 'CTkMessagebox', 'customtkinter', 'cx_Freeze',
                'cx_Logging', 'cycler', 'darkdetect', 'DateTime', 'Eel',
                'et-xmlfile', 'filelock', 'Flask', 'Flask-Cors', 'Flask-JWT-Extended',
                'Flask-Login', 'flask-marshmallow', 'Flask-SQLAlchemy', 'fonttools',
                'importlib-metadata', 'itsdangerous', 'Jinja2', 'kiwisolver', 'lief',
                'lxml', 'Markdown', 'MarkupSafe', 'marshmallow', 'marshmallow-sqlalchemy',
                'matplotlib', 'MouseInfo', 'mpmath', 'multidict', 'mypy-extensions',
                'nest-asyncio', 'networkx', 'numpy', 'openpyxl', 'outcome', 'packaging',
                'pandas', 'pathspec', 'pdfminer', 'pefile', 'Pillow', 'pip',
                'platformdirs', 'prettytable', 'PyAutoGUI', 'pybase64', 'pycparser',
                'pycryptodome', 'pyecharts', 'pyee', 'PyGetWindow', 'pyinstaller',
                'pyinstaller-hooks-contrib', 'PyJWT', 'PyMsgBox', 'pymssql', 'pyodbc',
                'pyparsing', 'PyPDF2', 'pyperclip', 'pyppeteer', 'PyRect', 'PyScreeze',
                'PySide6', 'PySide6-Addons', 'PySide6-Essentials', 'PySimpleGUI',
                'PySocks', 'python-dateutil', 'python-decouple', 'python-dotenv',
                'pytweening', 'pytz',  'requests', 'screeninfo',
                'selenium', 'setuptools', 'shiboken6', 'simplejson', 'six',
                'sniffio', 'sortedcontainers', 'soupsieve', 'SQLAlchemy', 'sympy',
                'torch', 'tqdm', 'trio', 'trio-websocket', 'typing_extensions',
                'tzdata', 'Unidecode', 'urllib3', 'wcwidth', 'webdriver-manager',
                'webdrivermanager', 'websockets', 'Werkzeug', 'wheel', 'whichcraft',
                'wsproto', 'XlsxWriter', 'xmltodict', 'yarl', 'zipp', 'zope.event',
                'zope.interface',
            ],
            'include_files': None,
        },
    },
    executables=[exe],
)
