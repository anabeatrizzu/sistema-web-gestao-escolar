from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .modelos import PerfilUsuario, Turma, Disciplina, Aluno, Aula


class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nome completo', max_length=150, required=False)
    email = forms.EmailField(label='E-mail', required=False)

    tipo = forms.ChoiceField(label='Eu sou', choices=PerfilUsuario.TIPOS, widget=forms.RadioSelect)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')

    def save(self, commit=True):
        usuario = super().save(commit=commit)
        if commit:
            PerfilUsuario.objects.create(usuario=usuario, tipo=self.cleaned_data['tipo'])
        return usuario


class FormDono(forms.ModelForm):
    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        for nome, campo in self.fields.items():
            if hasattr(campo, 'queryset') and hasattr(campo.queryset.model, 'dono'):
                campo.queryset = campo.queryset.filter(dono=usuario)

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.dono = self.usuario
        if hasattr(obj, 'professor'):
            obj.professor = self.usuario
        if commit:
            obj.save()
        return obj


class TurmaForm(FormDono):
    class Meta:
        model = Turma
        fields = ['nome', 'ano', 'periodo']


class DisciplinaForm(FormDono):
    class Meta:
        model = Disciplina
        fields = ['nome', 'turma', 'carga_horaria']


class AlunoForm(FormDono):
    class Meta:
        model = Aluno
        fields = ['nome', 'ra', 'data_nascimento', 'turma', 'ativo']
        widgets = {'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}

    def clean_ra(self):
        ra = self.cleaned_data['ra']
        qs = Aluno.objects.filter(dono=self.usuario, ra=ra).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Já existe aluno com este RA.')
        return ra


class AulaForm(FormDono):
    class Meta:
        model = Aula
        fields = ['disciplina', 'data', 'conteudo', 'objetivos', 'metodologia', 'observacoes']
        widgets = {'data': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}
