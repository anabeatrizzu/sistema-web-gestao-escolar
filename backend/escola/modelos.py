from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Turma(models.Model):
    PERIODOS = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('noite', 'Noite'),
    ]

    nome = models.CharField('Nome da Turma', max_length=50)
    ano = models.IntegerField('Ano Letivo')
    periodo = models.CharField('Período', max_length=20, choices=PERIODOS)

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering = ['ano', 'nome']

    def __str__(self):
        return f'{self.nome} ({self.ano})'


class Disciplina(models.Model):
    nome = models.CharField('Nome da Disciplina', max_length=100)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='disciplinas', verbose_name='Turma')
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Professor')
    carga_horaria = models.IntegerField('Carga Horária (h)', default=0)

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} - {self.turma}'

    def total_alunos(self):
        return self.turma.alunos.filter(ativo=True).count()

    def total_aulas(self):
        return self.aulas.count()


class Aluno(models.Model):
    nome = models.CharField('Nome Completo', max_length=150)
    ra = models.CharField('RA / Matrícula', max_length=20, unique=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT, related_name='alunos', verbose_name='Turma')
    ativo = models.BooleanField('Matrícula Ativa', default=True)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.ra})'

    def media_disciplina(self, disciplina):
        media = self.notas.filter(disciplina=disciplina).aggregate(Avg('valor'))['valor__avg']
        return round(media, 1) if media is not None else None

    def total_faltas(self, disciplina=None):
        qs = self.faltas.all()
        if disciplina:
            qs = qs.filter(aula__disciplina=disciplina)
        return qs.count()


class Aula(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='aulas', verbose_name='Disciplina')
    data = models.DateField('Data da Aula')
    conteudo = models.CharField('Conteúdo Ministrado', max_length=200)
    objetivos = models.TextField('Objetivos', blank=True)
    metodologia = models.TextField('Metodologia', blank=True)
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['-data']

    def __str__(self):
        return f'{self.disciplina.nome} - {self.data.strftime("%d/%m/%Y")}'


class Nota(models.Model):
    BIMESTRES = [
        (1, '1º Bimestre'),
        (2, '2º Bimestre'),
        (3, '3º Bimestre'),
        (4, '4º Bimestre'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='notas', verbose_name='Aluno')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name='Disciplina')
    bimestre = models.IntegerField('Bimestre', choices=BIMESTRES)
    valor = models.DecimalField('Nota', max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ('aluno', 'disciplina', 'bimestre')

    def __str__(self):
        return f'{self.aluno.nome} - {self.disciplina.nome} ({self.bimestre}º Bim: {self.valor})'

    @property
    def status(self):
        return 'Aprovado' if self.valor >= 6.0 else 'Recuperação'


class Falta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='faltas', verbose_name='Aluno')
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='faltas', verbose_name='Aula')
    justificada = models.BooleanField('Falta Justificada?', default=False)
    justificativa = models.CharField('Justificativa', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Falta'
        verbose_name_plural = 'Faltas'
        unique_together = ('aluno', 'aula')

    def __str__(self):
        return f'{self.aluno.nome} - {self.aula.data.strftime("%d/%m/%Y")}'
