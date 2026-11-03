from django.core.management import call_command


def preparar():
    call_command('migrate', interactive=False, verbosity=0)
