from django.contrib import admin
from .modelos import PerfilUsuario, Turma, Disciplina, Aluno, Aula, Nota, Falta

admin.site.site_header = "Gestão Escolar"
admin.site.site_title = "Painel Escolar"
admin.site.index_title = "Administração do Sistema"


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ano', 'periodo']
    list_filter = ['ano', 'periodo']
    search_fields = ['nome']


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'turma', 'professor', 'carga_horaria']
    list_filter = ['turma', 'professor']
    search_fields = ['nome']


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ra', 'turma', 'ativo']
    search_fields = ['nome', 'ra']
    list_filter = ['turma', 'ativo']


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['disciplina', 'data', 'conteudo']
    list_filter = ['disciplina', 'data']
    date_hierarchy = 'data'
    search_fields = ['conteudo']


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'disciplina', 'bimestre', 'valor']
    list_filter = ['disciplina', 'bimestre']
    search_fields = ['aluno__nome', 'aluno__ra']


@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'aula', 'justificada']
    list_filter = ['justificada', 'aula__disciplina']
    search_fields = ['aluno__nome', 'justificativa']



@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo']
    list_filter = ['tipo']
