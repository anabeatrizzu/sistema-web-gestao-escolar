import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.configuracoes')

from gestao.wsgi import application  # noqa: E402
from gestao.bootstrap import preparar  # noqa: E402

preparar()
app = application
