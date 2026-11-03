from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .modelos import Turma, Disciplina, Aluno, Aula, Nota, Falta
from .formularios import TurmaForm, DisciplinaForm, AlunoForm, AulaForm, CadastroUsuarioForm


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f'Cadastro realizado com sucesso! Bem-vindo(a), {usuario.username}.')
            return redirect('inicio')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'telas/cadastro.html', {'form': form})


@login_required
def inicio(request):
    disciplinas = Disciplina.objects.filter(professor=request.user)
    ultimas_aulas = Aula.objects.filter(disciplina__professor=request.user)[:5]
    return render(request, 'escola/inicio.html', {
        'disciplinas': disciplinas,
        'ultimas_aulas': ultimas_aulas,
    })


class Lista(LoginRequiredMixin, ListView):
    template_name = 'escola/lista.html'
    titulo = ''
    colunas = []  # (cabecalho, atributo)
    extras = []   # (texto, nome da url com pk)
    rota = ''     # prefixo das urls: turma -> turma_novo, turma_editar...

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, colunas=self.colunas, rota=self.rota, extras=self.extras)
        ctx['linhas'] = [
            {'obj': o, 'valores': [getattr(o, c[1]) for c in self.colunas]}
            for o in ctx['object_list']
        ]
        return ctx


class Formulario(LoginRequiredMixin):
    template_name = 'escola/formulario.html'
    titulo = ''
    rota = ''

    def get_success_url(self):
        return reverse_lazy(self.rota + '_lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(titulo=self.titulo, rota=self.rota)
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Salvo com sucesso.')
        return super().form_valid(form)


class Exclusao(LoginRequiredMixin, DeleteView):
    template_name = 'escola/confirma_exclusao.html'
    rota = ''

    def get_success_url(self):
        return reverse_lazy(self.rota + '_lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['rota'] = self.rota
        return ctx

    def form_valid(self, form):
        try:
            resposta = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, 'Não é possível excluir: há registros ligados a este item.')
            return redirect(self.get_success_url())
        messages.success(self.request, 'Excluído com sucesso.')
        return resposta


# Turma
class TurmaLista(Lista):
    model = Turma
    titulo = 'Turmas'
    rota = 'turma'
    colunas = [('Nome', 'nome'), ('Ano', 'ano'), ('Período', 'periodo')]


class TurmaNova(Formulario, CreateView):
    model = Turma
    form_class = TurmaForm
    titulo = 'Nova turma'
    rota = 'turma'


class TurmaEditar(Formulario, UpdateView):
    model = Turma
    form_class = TurmaForm
    titulo = 'Editar turma'
    rota = 'turma'


class TurmaExcluir(Exclusao):
    model = Turma
    rota = 'turma'


# Disciplina
class DisciplinaLista(Lista):
    model = Disciplina
    titulo = 'Disciplinas'
    rota = 'disciplina'
    extras = [('Notas', 'notas')]
    colunas = [('Nome', 'nome'), ('Turma', 'turma'), ('Professor', 'professor'), ('Carga horária', 'carga_horaria')]


class DisciplinaNova(Formulario, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    titulo = 'Nova disciplina'
    rota = 'disciplina'


class DisciplinaEditar(Formulario, UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    titulo = 'Editar disciplina'
    rota = 'disciplina'


class DisciplinaExcluir(Exclusao):
    model = Disciplina
    rota = 'disciplina'


# Aluno
class AlunoLista(Lista):
    model = Aluno
    titulo = 'Alunos'
    rota = 'aluno'
    colunas = [('Nome', 'nome'), ('RA', 'ra'), ('Turma', 'turma'), ('Ativo', 'ativo')]


class AlunoNovo(Formulario, CreateView):
    model = Aluno
    form_class = AlunoForm
    titulo = 'Novo aluno'
    rota = 'aluno'


class AlunoEditar(Formulario, UpdateView):
    model = Aluno
    form_class = AlunoForm
    titulo = 'Editar aluno'
    rota = 'aluno'


class AlunoExcluir(Exclusao):
    model = Aluno
    rota = 'aluno'


# Aula
class AulaLista(Lista):
    model = Aula
    titulo = 'Aulas'
    rota = 'aula'
    extras = [('Frequência', 'frequencia')]
    colunas = [('Data', 'data'), ('Disciplina', 'disciplina'), ('Conteúdo', 'conteudo')]


class AulaNova(Formulario, CreateView):
    model = Aula
    form_class = AulaForm
    titulo = 'Nova aula'
    rota = 'aula'


class AulaEditar(Formulario, UpdateView):
    model = Aula
    form_class = AulaForm
    titulo = 'Editar aula'
    rota = 'aula'


class AulaExcluir(Exclusao):
    model = Aula
    rota = 'aula'


@login_required
def frequencia(request, pk):
    aula = get_object_or_404(Aula, pk=pk)
    alunos = aula.disciplina.turma.alunos.filter(ativo=True)
    if request.method == 'POST':
        faltosos = request.POST.getlist('faltou')
        for aluno in alunos:
            if str(aluno.pk) in faltosos:
                Falta.objects.get_or_create(aluno=aluno, aula=aula)
            else:
                Falta.objects.filter(aluno=aluno, aula=aula).delete()
        messages.success(request, 'Frequência salva.')
        return redirect('aula_lista')
    faltas = set(aula.faltas.values_list('aluno_id', flat=True))
    linhas = [{'aluno': a, 'faltou': a.pk in faltas} for a in alunos]
    return render(request, 'escola/frequencia.html', {'aula': aula, 'linhas': linhas})


@login_required
def notas(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    alunos = disciplina.turma.alunos.filter(ativo=True)
    if request.method == 'POST':
        for aluno in alunos:
            for bim in range(1, 5):
                valor = request.POST.get(f'nota_{aluno.pk}_{bim}', '').strip().replace(',', '.')
                if valor == '':
                    Nota.objects.filter(aluno=aluno, disciplina=disciplina, bimestre=bim).delete()
                    continue
                try:
                    v = float(valor)
                except ValueError:
                    messages.error(request, f'Nota inválida para {aluno.nome}.')
                    return redirect('notas', pk=pk)
                if not 0 <= v <= 10:
                    messages.error(request, f'Nota de {aluno.nome} deve ficar entre 0 e 10.')
                    return redirect('notas', pk=pk)
                Nota.objects.update_or_create(
                    aluno=aluno, disciplina=disciplina, bimestre=bim, defaults={'valor': v})
        messages.success(request, 'Notas salvas.')
        return redirect('disciplina_lista')
    existentes = {(n.aluno_id, n.bimestre): n.valor for n in disciplina.nota_set.all()}
    linhas = [
        {'aluno': a, 'notas': [{'bim': b, 'valor': existentes.get((a.pk, b), '')} for b in range(1, 5)]}
        for a in alunos
    ]
    return render(request, 'escola/notas.html', {'disciplina': disciplina, 'linhas': linhas})
