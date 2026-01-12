from django.urls import path
from .views import *

app_name = 'ibs'

urlpatterns = [
    path('', home_page,name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('Cadastro/', cadastro_page, name='cadastro'),
    path('resetar-senha/', resetar_senha, name='resetar-senha'),

    #Paginas de consultas
    path('Consulta-psl/', consulta_psl_page, name='consulta-psl'),
    path('Consulta-pis-cofins/', consulta_pis_cofins_page, name='consulta-pis-cofins'),


    #Consultas
    path('Consultar-pis-cofins/', consultar_pis_cofins, name='consultar-pis-cofins'),
    path('Consultar-psl/', consultar_psl, name='consultar-psl'),
    path('Consultar-pis-cofins-apr/', consultar_pis_cofins_apr, name='consultar-pis-cofins-apr'),

    path('Cadastro-Conta-Calculo-Base-psl/', cadastro_base_calculo_psl,
         name='cadastro-conta-base-psl'),

    path('Cadastro-pis-cofins-aberto-ramo/', cadastro_pis_cofins_aberto_ramo,
         name='cadastro-pis-cofins-aberto-ramo'),

    path('Consulta-pis-cofins-aberto-ramo/', consulta_pis_cofins_page_aberto_ramo, name='consulta-pis-cofins-aberto-ramo'),
    path('Calcular-pis-cofins-aberto-ramo/<int:ano>/<int:mes>', calcular_pis_cofins_aberto_ramo, name='calcular-pis-cofins-aberto-ramo'),
    path('Carregar-dados-pis-cofins-aberto-ramo/', carregar_dados_pis_cofins_aberto_ramo, name='carregar-dados-pis-cofins-aberto-ramo'),


    path('Cadastro-pis-cofins/', cadastro_pis_cofins, name='cadastro-pis-cofins'),
    path('Cadastro-psl/', cadastro_psl, name='cadastro-psl'),


    path('Carregar-dados-pis-cofins/', carregar_dados_pis_cofins, name='carregar-dados-pis-cofins'),
    path('Calcular-pis-cofins/', calcular_pis_cofins, name='calcular-pis-cofins'),

    path('Calcular-psl/', calcular_psl, name='calcular-psl'),

    path('Carregar-Dados-psl/', carregar_dados_psl, name='carregar-dados-psl'),



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

    path('Cadastrar-Conta-Calculo-Base-psl/', cadastrar_base_calculo_psl,
         name='cadastrar-conta-base-psl'),

    path('exportar-csv-pis-cofins/<int:ano>/<int:mes>/', exportar_csv_pis_cofins, name='exportar_csv_pis_cofins'),
    path('exportar-csv-psl/<int:ano>/<int:mes>/', exportar_csv_pis_cofins, name='exportar_csv_pis_cofins'),
]
