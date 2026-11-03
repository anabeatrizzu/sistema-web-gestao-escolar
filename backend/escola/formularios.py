from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .modelos import Turma, Disciplina, Aluno, Aula


class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nome completo', max_length=150, required=False)
    email = forms.EmailField(label='E-mail', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'ano', 'periodo']


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'turma', 'professor', 'carga_horaria']


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'ra', 'data_nascimento', 'turma', 'ativo']
        widgets = {'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['disciplina', 'data', 'conteudo', 'objetivos', 'metodologia', 'observacoes']
        widgets = {'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
