import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.configuracoes')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Não foi possível carregar o Django.") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
