from django.utils.translation import gettext_lazy as _
from django import forms
from .models import UsuarioModel, Perfil


class UsuarioCadastroForm(forms.Form):

    nome = forms.CharField(max_length=100, label='Nome ',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'
                           })
                           )

    email = forms.CharField(max_length=50, label='Email ',
                            widget=forms.TextInput(attrs={
                                'class' :  'form-control'
                            }))

    perfil = forms.ChoiceField(
        choices=Perfil.choices,
        label="Perfil",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    senha = forms.CharField(max_length=50, label='Senha ',
                            widget=forms.PasswordInput(attrs={
                                'class' :  'form-control'
                            }),)

    confSenha = forms.CharField(max_length=50,label='Confirmar senha',
                            widget=forms.PasswordInput(attrs={
                                'class' :  'form-control'
                            }),)

    precisa_trocar_senha = forms.BooleanField(
        label="Trocar senha no primeiro acesso?",
        required=False,
        initial=True,   # por padrão já vem marcado
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


    pass


class BaseCalculoCadastroForm(forms.Form):

    ano = forms.IntegerField(label='Ano ',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'
                           })
                           )

    mes = forms.IntegerField(label='Mês ',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'
                           })
                           )

    pass


class ContaBaseCalculoCadastroForm(forms.Form):

    conta = forms.CharField(max_length=100, label='Conta ',
                           widget=forms.TextInput(attrs={
                               'class': 'form-control'
                           })
                           )

    descricao = forms.CharField(max_length=50, label='Descrição ',
                            widget=forms.TextInput(attrs={
                                'class': 'form-control'
                            }))
    pass
