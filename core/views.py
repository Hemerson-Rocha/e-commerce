from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ContatoForm, ProdutoModelForm
from .models import Produto

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }

    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)# o form pode ou nao ter dados

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()

            messages.success(request, 'Email enviado com sucesso')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar email')


    context = {
        'form' : form,
    }

    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():

                form.save()

                messages.success(request, 'produto salvo com sucesso')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'erro ao salvar produto')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form,
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')

