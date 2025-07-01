"""テストモジュールがapiとuiモジュールをインポートできるようにするヘルパー。

分離デプロイ対応のパス設定を行います。
"""

import os
import sys

# api と ui ディレクトリをPythonパスに追加
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
api_path = os.path.join(project_root, "api")
ui_path = os.path.join(project_root, "ui")

sys.path.insert(0, api_path)
sys.path.insert(0, ui_path)
