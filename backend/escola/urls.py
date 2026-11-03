from django.urls import path
from . import visualizacao as v

urlpatterns = [
    path('', v.inicio, name='inicio'),

    path('turmas/', v.TurmaLista.as_view(), name='turma_lista'),
    path('turmas/nova/', v.TurmaNova.as_view(), name='turma_novo'),
    path('turmas/<int:pk>/editar/', v.TurmaEditar.as_view(), name='turma_editar'),
    path('turmas/<int:pk>/excluir/', v.TurmaExcluir.as_view(), name='turma_excluir'),

    path('disciplinas/', v.DisciplinaLista.as_view(), name='disciplina_lista'),
    path('disciplinas/nova/', v.DisciplinaNova.as_view(), name='disciplina_novo'),
    path('disciplinas/<int:pk>/editar/', v.DisciplinaEditar.as_view(), name='disciplina_editar'),
    path('disciplinas/<int:pk>/notas/', v.notas, name='notas'),
    path('disciplinas/<int:pk>/excluir/', v.DisciplinaExcluir.as_view(), name='disciplina_excluir'),

    path('alunos/', v.AlunoLista.as_view(), name='aluno_lista'),
    path('alunos/novo/', v.AlunoNovo.as_view(), name='aluno_novo'),
    path('alunos/<int:pk>/editar/', v.AlunoEditar.as_view(), name='aluno_editar'),
    path('alunos/<int:pk>/excluir/', v.AlunoExcluir.as_view(), name='aluno_excluir'),

    path('aulas/', v.AulaLista.as_view(), name='aula_lista'),
    path('aulas/nova/', v.AulaNova.as_view(), name='aula_novo'),
    path('aulas/<int:pk>/editar/', v.AulaEditar.as_view(), name='aula_editar'),
    path('aulas/<int:pk>/frequencia/', v.frequencia, name='frequencia'),
    path('aulas/<int:pk>/excluir/', v.AulaExcluir.as_view(), name='aula_excluir'),
]
