

```shell
$ python -m venv .venv
$ pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
$ pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple    
$ pyinstaller --onefile --hidden-import=PIL .\photo-to-foler-by-year.py
$ pyinstaller --onefile --hidden-import=PIL .\photo-to-foler-by-year-gui.py
```