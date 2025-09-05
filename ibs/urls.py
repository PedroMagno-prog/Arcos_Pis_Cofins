from django.urls import path
from .views import *

app_name = 'ibs'

urlpatterns = [
    path('', home_page,name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('Cadastro/', cadastro_page, name='cadastro'),
    path('resetar-senha/', resetar_senha, name='resetar-senha'),

    path('Cadastro-pis-cofins/', cadastro_pis_cofins, name='cadastro-pis-cofins'),
    path('Carregar-dados-pis-cofins/', carregar_dados_pis_cofins, name='carregar-dados-pis-cofins'),
    path('Calcular-pis-cofins/', calcular_pis_cofins, name='calcular-pis-cofins'),

    path('Cadastrar/', cadastrar, name='cadastrar'),
    path('Lista/', lista_page, name='lista'),
    path('Cadastro-Ibs/', cadastro_ibs_page, name='cadastro-ibs'),
    path('Enviar-Ibs/', enviar_ibs, name='enviar-ibs'),

    path('Cadastro-balancete/', cadastro_balancete, name='cadastro-balancete'),
    path('Cadastrar-balancete/', cadastrar_balancete, name='cadastrar-balancete'),

    path('Cadastro-relatorio/', cadastro_relatorio, name='cadastro-relatorio'),
    path('Cadastrar-relatorio/', cadastrar_relatorio, name='cadastrar-relatorio'),

    path('Lista-balancetes/', lista_balancetes, name='lista-balancetes'),
    path('Listar-balancetes/', listar_balancetes, name='listar-balancetes'),



    path('Exibir-Contas/<int:codigo>', exibir_contas_balancete, name='exibir-contas'),

    path('Cadastro-Conta-Calculo-Base-pis-cofins/', cadastro_base_calculo_pis_cofins,
         name='cadastro-conta-base-pis-cofins'),
    path('Cadastro-Conta-Calculo-Base-irpj-csll/', cadastro_base_calculo_irpj_csll,
         name='cadastro-conta-base-irpj-csll'),

    path('Base-Calculo-Lista/', lista_base_calculo, name='base-calculo-lista'),

    path('Listar-base-calculo/<int:codigo>',carregar_contas_base_calculo , name='carregar-contas-base-calculo'),

    path('Cadastrar-Conta-Calculo-Base-pis-cofins/', cadastrar_base_calculo_pis_cofins,
         name='cadastrar-conta-base-pis-cofins'),

    path('Cadastrar-Conta-Calculo-Base-irpj-csll/', cadastrar_base_calculo_irpj_csll,
         name='cadastrar-conta-base-irpj-csll'),

    path('exportar-csv/<int:ano>/<int:mes>/', exportar_csv_pis_cofins, name='exportar_csv_pis_cofins'),
]
