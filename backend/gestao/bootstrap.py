import datetime

from django.contrib.auth.models import User
from django.core.management import call_command

USUARIO = 'admin'
SENHA = 'admin123'


def preparar():
    call_command('migrate', interactive=False, verbosity=0)
    if User.objects.filter(username=USUARIO).exists():
        return
    from escola.modelos import Turma, Disciplina, Aluno, Aula, Nota

    prof = User.objects.create_superuser(USUARIO, 'admin@escola.com', SENHA, first_name='Professor Demo')
    turma = Turma.objects.create(nome='9º A', ano=2026, periodo='manha')
    turma2 = Turma.objects.create(nome='1º Médio B', ano=2026, periodo='tarde')
    mat = Disciplina.objects.create(nome='Matemática', turma=turma, professor=prof, carga_horaria=80)
    Disciplina.objects.create(nome='Português', turma=turma, professor=prof, carga_horaria=80)
    Disciplina.objects.create(nome='História', turma=turma2, professor=prof, carga_horaria=60)
    nomes = ['Ana Souza', 'Bruno Lima', 'Carla Dias', 'Daniel Rocha', 'Eduarda Alves']
    alunos = [Aluno.objects.create(nome=n, ra=f'2026{i:03d}', turma=turma) for i, n in enumerate(nomes, 1)]
    Aluno.objects.create(nome='Felipe Costa', ra='2026010', turma=turma2)
    Aula.objects.create(disciplina=mat, data=datetime.date.today(), conteudo='Equações do 1º grau',
                        objetivos='Resolver equações simples')
    for i, a in enumerate(alunos):
        Nota.objects.create(aluno=a, disciplina=mat, bimestre=1, valor=5 + i)
