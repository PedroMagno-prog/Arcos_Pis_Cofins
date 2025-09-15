from django.shortcuts import render, loader, HttpResponse, redirect
from django.http import HttpResponse, Http404
import csv
from django.urls import reverse_lazy, reverse
from .forms import UsuarioCadastroForm
from .models import UsuarioModel, BaseCalculoPisCofins
from .const import *
import hmac
from .util import *
from django.db.models import Q
from django.db.models import Max
from hmac import compare_digest
from functools import wraps


def autenticar_usuario(request):
    print("autenticar_usuario")
    if request.session.get('usuario') is not None:
        return True
    else:
        print("usuario nao autenticado")
        return False


def criar_sessao(request, usuario):
    request.session['usuario'] = dict(nome=usuario.nome, id=usuario.codigo, perfil=usuario.perfil)
    request.session.set_expiry(3600) # expira a sessao de 1 hora
    request.session.modified = True
    print("sessao criada pro usuario")
    pass

def logout(request):
    try:
        request.session.flush()
        print("Usuário deslogado")
        return redirect(reverse('ibs:login'))

    except Exception as ex:
        msg = ex.args
        return render(request, LOGIN_PAGE, {'msg_login' : msg})

def login(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            senha = criptografar_senha(request.POST['senha'])

            usuario = UsuarioModel.objects.filter(email =email).first()


            if not usuario:
                msg = 'Usuario não cadastrado no sistema.'
                return render(request, LOGIN_PAGE,
                              {'msg_login': msg})

            if not compare_digest(usuario.senha, senha):
                msg = 'Usuario e senha incorretos.'
                return render(request, LOGIN_PAGE,
                              {'msg_login': msg})

            if usuario.precisa_trocar_senha:
                criar_sessao(request, usuario)
                return redirect("ibs:resetar-senha")

            print(usuario)
            criar_sessao(request, usuario)
            return redirect(reverse('ibs:home'))


        else:
            raise Exception('Erro, use POST para formulários')

    except Exception as ex:
        return render(request, LOGIN_PAGE,
                      {'msg_login': 'Erro no formulário preencha todos os campos.'
                              + str(ex.args)})

    pass


def login_required_usuario(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        usuario = request.session.get('usuario')
        if not usuario or usuario.get('perfil') not in [Perfil.USUARIO, Perfil.ADMIN]:
            return render(request, LOGIN_PAGE)
        return view_func(request, *args, **kwargs)
    return wrapper


def login_required_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        usuario = request.session.get('usuario')
        if not usuario:
            return redirect('ibs:login')

        if usuario.get('perfil') != Perfil.ADMIN:
            return render(request, HOME_PAGE)
        return view_func(request, *args, **kwargs)
    return wrapper


def montar_dados_tela_pis_cofins(ano, mes, base):
    relatorio_sinpag = RelatorioSINPAG.objects.filter(ano=ano, mes=mes).first()
    relatorio_sinpagac = RelatorioSINPAGAC.objects.filter(ano=ano, mes=mes).first()
    relatorio_salvados_vendidos = RelatorioSalvadosVendidosNovos.objects.filter(ano=ano, mes=mes).first()
    relatorio_recuperados = RelatorioRecuperadosNovo.objects.filter(ano=ano, mes=mes).first()
    balancete = Balancete.objects.filter(ano=ano, mes=mes).first() # Último balancete cadastrado

    if balancete:
        balancete = Balancete.objects.filter(ano=balancete.ano, mes=balancete.mes).latest('versao')
        print('Codigo do balancete : ', balancete.codigo)

        # Todas as contas cadastradas. Seus ID, Descrição e Tipo.
        base_calculo_pis = ContaBaseCalculoPisCofins.objects.all()

        contas = []
        add_movimento_conta_base_calculo = []

        for base_calculo in base_calculo_pis:
            contas_balancetes = ContaBalancete.objects.filter(conta_do_razao=base_calculo.conta,
                                                            balancete_id=balancete.codigo).all()
            print('----' * 10)
            print(contas_balancetes)
            print('----' * 10)

            if contas_balancetes:
                conta_balancete = contas_balancetes[0]
                # Soma de contas do balancete -> informar o tipo movimento da base de calculo, e as contas do balancete.
                conta_balancete.movimento = soma_contas_balancete(base_calculo.tipo_conta, contas_balancetes=contas_balancetes)
                add_movimento_conta_base_calculo.append(conta_balancete.movimento)
                conta_balancete.movimento = locale_br(conta_balancete.movimento)
                contas.append(conta_balancete)

        balancete.contas = contas
        base_calculo = 0
        for valor in add_movimento_conta_base_calculo:
            base_calculo += valor

        base_calculo = locale_br(base_calculo)

        print('Base de calculo :', base_calculo)
        if relatorio_sinpag:
            relatorio_sinpag.soma_vr_cos_ced = locale_br(relatorio_sinpag.soma_vr_cos_ced)
            relatorio_sinpag.soma_vr_mov = locale_br(relatorio_sinpag.soma_vr_mov)
            relatorio_sinpag.dif_soma_cos_ced_vr_mov = locale_br(relatorio_sinpag.dif_soma_cos_ced_vr_mov)

        if relatorio_sinpagac:
            relatorio_sinpagac.soma_vr_mov = locale_br(relatorio_sinpagac.soma_vr_mov)

        if relatorio_recuperados:
            relatorio_recuperados.dif_soma_baixa_ind_res_salv = locale_br(
                relatorio_recuperados.dif_soma_baixa_ind_res_salv)
            relatorio_recuperados.soma_baixa_ind = locale_br(relatorio_recuperados.soma_baixa_ind)
            relatorio_recuperados.soma_baixa_res = locale_br(relatorio_recuperados.soma_baixa_res)
            relatorio_recuperados.soma_baixa_salv = locale_br(relatorio_recuperados.soma_baixa_salv)

        if relatorio_salvados_vendidos:
            relatorio_salvados_vendidos.soma_vr_mov = locale_br(relatorio_salvados_vendidos.soma_vr_mov)

        if base:
            dados = dict(relatorio_sinpagac=relatorio_sinpagac, relatorio_sinpag=relatorio_sinpag,
                         relatorio_recuperados=relatorio_recuperados,
                         relatorio_salvados_vendidos=relatorio_salvados_vendidos,
                         balancete=balancete, ano=ano, mes=convert_mes_texto(mes), base=base, base_calculo=base_calculo)
            return dados

        dados = dict(relatorio_sinpagac=relatorio_sinpagac, relatorio_sinpag=relatorio_sinpag,
                     relatorio_recuperados=relatorio_recuperados,
                     relatorio_salvados_vendidos=relatorio_salvados_vendidos,
                     balancete=balancete, ano=ano, mes=convert_mes_texto(mes), base_calculo=base_calculo)

        return dados
    else:
        raise Exception('Balancete não encontrado.')


from django.contrib import messages

@login_required_usuario
def resetar_senha(request):
    try:
        if request.method == "POST":
            nova_senha = request.POST.get("senha")
            conf_senha = request.POST.get("confSenha")

            if not nova_senha or not conf_senha:
                messages.error(request, "Preencha os dois campos de senha.")
            elif nova_senha != conf_senha:
                messages.error(request, "As senhas não coincidem.")
            else:
                usuario_data = request.session.get("usuario")
                usuario = UsuarioModel.objects.get(codigo=usuario_data["id"])
                usuario.senha = criptografar_senha(nova_senha)
                usuario.precisa_trocar_senha = False
                usuario.save()
                messages.success(request, "Senha alterada com sucesso.")
                return redirect("ibs:home")

        return render(request, "pages/resetar-senha.html")

    except Exception as ex:
        print(ex)
        msg = ex.args
        return render(request, RESETAR_SENHA_PAGE, {'msg': msg})



@login_required_usuario
def home_page(request):
    return render(request, HOME_PAGE)
    pass

@login_required_usuario
def login_page(request):
    return render(request, LOGIN_PAGE)

@login_required_admin
def cadastro_page(request):
    form = UsuarioCadastroForm()
    return render(request, CADASTRO_PAGE, {'form': form})

@login_required_usuario
def cadastro_ibs_page(request):

    return render(request, CADASTRO_IBS_PAGE)
    pass

@login_required_usuario
def cadastro_balancete(request):
    return render(request, BALANCETE_CADASTRO_PAGE)
    pass
@login_required_usuario
def cadastro_base_calculo_pis_cofins(request):
    return render(request, CADASTRO_BASE_CALCULO_PIS_COFINS_PAGE)
    pass

@login_required_usuario
def cadastro_base_calculo_irpj_csll(request):
    return render(request, CADASTRO_BASE_CALCULO_IRPJ_CSLL_PAGE)
    pass

@login_required_usuario
def cadastro_pis_cofins(request):
    return render(request, CADASTRO_PIS_COFINS_PAGE)
    pass

@login_required_usuario
def lista_base_calculo(request):
    return render(request)
    pass

@login_required_usuario
def lista_balancetes(request):

    return render(request, BALANCETE_LISTA_PAGE)
    pass
@login_required_usuario
def cadastro_relatorio(request):
    return render(request, CADASTRO_RELATORIO_PAGE)
    pass

@login_required_admin
def lista_page(request):
    usuarios = UsuarioModel.objects.all()
    return render(request, LISTA_PAGE, {'usuarios': usuarios})

@login_required_usuario
def carregar_dados_pis_cofins(request):
    try:
        if request.method == 'POST':

            ano = request.POST['ano']
            mes = request.POST['mes']

            if ano is None or len(ano) <= 0:
                msg = 'Informe o ano do balancete.'
                return render(request, CADASTRO_PIS_COFINS_PAGE, {'msg': msg})

            elif mes is None or len(mes) <= 0:
                msg = 'Informe o mês do balancete.'
                return render(request, CADASTRO_PIS_COFINS_PAGE, {'msg': msg})

                # Salvando o ano e mês na sessão
                request.session['ano_selecionado'] = ano
                request.session['mes_selecionado'] = mes

            ano = int(ano)
            mes = int(mes)
            dados = montar_dados_tela_pis_cofins(ano, mes, None)
            return render(request, CADASTRO_PIS_COFINS_PAGE, {'dados' : dados,
                                                              'ano' :  ano, 'mes' :  mes})



        else:
            raise Exception('Erro, Use POST para formulários.')


    except Exception as ex:
        msg = ex.args
        return render(request, CADASTRO_PIS_COFINS_PAGE, {'msg': msg})

    pass

@login_required_usuario
def carregar_contas_base_calculo(request, codigo):
    try:
        if codigo:
             if codigo == 1:
                 contas = ContaBaseCalculoPisCofins.objects.all()
                 print(request.path)
                 return render(request, CADASTRO_BASE_CALCULO_PIS_COFINS_PAGE, {'contas' :  contas})

             elif codigo == 2:
                 contas = ContaBaseCalculoIRPJCSLL.objects.all()
                 return render(request, CADASTRO_BASE_CALCULO_IRPJ_CSLL_PAGE, {'contas' :  contas})

             else:
                 raise Exception('Erro, o tipo de conta não foi informada.')


        else:
            raise Exception('Erro, o tipo de conta não foi informada.')


    except Exception as ex:
        msg = 'Erro ao listar contas, ' + ex.msg
        return render(request, request.path, {'msg' :  msg})
    pass

@login_required_usuario
def cadastrar(request):
    try:
        if request.method == 'POST':
            form = UsuarioCadastroForm(request.POST)
            if form.is_valid():
                usuario = UsuarioModel()
                usuario.nome = form.cleaned_data['nome']
                usuario.email = form.cleaned_data['email']
                usuario.perfil = form.cleaned_data['perfil']
                usuario.senha = form.cleaned_data['senha']
                usuario.precisa_trocar_senha = form.cleaned_data['precisa_trocar_senha']  # 👈 aqui
                confSenha = form.cleaned_data['confSenha']

                if usuario.nome is None or len(usuario.nome) <= 0:
                    msg = 'Informe o nome.'

                elif usuario.email is None or len(usuario.email) <= 0:
                    msg = 'Informe o email.'

                elif usuario.senha is None or confSenha is None:
                    msg = 'Informe a senha e a confirmação de senha.'

                elif not hmac.compare_digest(usuario.senha, confSenha):
                    msg = 'As senhas devem estar corretas.'

                else:
                    usuario.senha = criptografar_senha(usuario.senha)
                    usuario.save()
                    msg = 'Usuário cadastrado com sucesso.'

                return render(request, CADASTRO_PAGE, {'form': UsuarioCadastroForm(),
                                                       'msg': msg})
            else:
                msg = form.erros
                raise Exception('FormErrors, ' + str(msg))
        else:
            raise Exception('MethodEnvioError, Use POST para formulários.')

    except Exception as ex:
        msg = ex.args
        return render(request, CADASTRO_PAGE, {'form': UsuarioCadastroForm(),
                                               'msg': msg})
    pass

@login_required_usuario
def enviar_ibs(request):
    try:
        if request.method == "POST":

            receitas = load_receitas(request.FILES['receitas'])
            despesas = load_despesas(request.FILES['despesas'])

            nome = request.POST['nome']
            receitas_garantidores = request.POST['receitas-garantidores']

            if receitas_garantidores is None or len(receitas_garantidores) <= 0:
                return render(request, HOME_PAGE, {'msg':
                                                       'Informe a receita, caso não possua informe o valor zero.'})

            if nome is None or len(nome) <= 0:
                return render(request, HOME_PAGE, {'msg' :  'Informe o nome.'})

            empresa = EmpresaModel()
            empresa.nome = nome
            receitas_garantidores = float(receitas_garantidores)
            receitas_garantidores_calculada_ibs = (receitas_garantidores * 17.7) / 100
            receitas_garantidores_calculada_cbs = (receitas_garantidores * 8.8) / 100
            receitas_garantidores_calculada_iva_dual = receitas_garantidores_calculada_ibs + receitas_garantidores_calculada_cbs

            resumos, total_resumos = calcular_somatorio_receitas(receitas)

            somatorio_despesas = calcular_somatorio_despesas(despesas)


            perc  = calcular_percentual_media_receita_despesas(total_resumos,somatorio_despesas )

            resumos, total_credito = calcular_credito_por_municipio(resumos, perc)
            resumos, total_base_calculo = calcular_base_calculo_(resumos)
            resumos, total_iva = calcular_valor_iva(resumos)
            resumos, total_cbs = calcular_valor_cbs(resumos)
            resumos, total_ibs = calcular_valor_ibs(resumos)


            for resumo in resumos:
                resumo.valor = locale_br(resumo.valor)
                resumo.credito_municipio = locale_br(resumo.credito_municipio)
                resumo.base_calculo = locale_br(resumo.base_calculo)
                resumo.iva = locale_br(resumo.iva)
                resumo.ibs = locale_br(resumo.ibs)
                resumo.cbs = locale_br(resumo.cbs)



            empresa.resumos = resumos
            empresa.total_resumos = locale_br(total_resumos)
            empresa.total_credito = locale_br(total_credito)
            empresa.total_base_calculo = locale_br(total_base_calculo)
            empresa.total_iva = locale_br(total_iva + receitas_garantidores_calculada_iva_dual )
            empresa.total_ibs = locale_br(total_ibs + receitas_garantidores_calculada_ibs)
            empresa.total_cbs = locale_br(total_cbs + receitas_garantidores_calculada_cbs)

            print(resumos)


            '''
            for i in range(0, 10):
                print(receitas[i])
                print('-' * 100)
            '''
            '''
            for i in range(0, 10):
                print(despesas[i])
                print('-' * 100)
            '''
            #print(despesas)


        return render(request, CADASTRO_IBS_PAGE, {'empresa':  empresa,
                                           'somatorio' :  locale_br( somatorio_despesas),
                                                   'receitas_garantidores_calculada_ibs': locale_br(receitas_garantidores_calculada_ibs),
                                                   'receitas_garantidores_calculada_cbs':locale_br( receitas_garantidores_calculada_cbs),
                                                   'receitas_garantidores_calculada_iva_dual': locale_br( receitas_garantidores_calculada_iva_dual),

                                                   })

    except Exception as ex:
        print(ex.args)
        return render(request, CADASTRO_IBS_PAGE, {'msg':  'Erro no formulário preencha todos os campos.' + str(ex.args)})
    pass

@login_required_usuario
def cadastrar_balancete(request):
    try:
        if request.method == 'POST':
            balancete = Balancete()
            ano = request.POST['ano']
            mes = request.POST['mes']
            contas = load_contas_do_balancete(request.FILES['balancetes'])


            if ano is None or len(ano) <= 0:
                msg = 'Informe o ano do balancete.'
                return render(request, BALANCETE_CADASTRO_PAGE, {'msg' :  msg})

            elif mes is None or len(mes) <= 0:
                msg = 'Informe o mês do balancete.'
                return render(request, BALANCETE_CADASTRO_PAGE, {'msg' :  msg})

            elif contas is None or len(contas) <= 0:
                msg = 'Insira o arquivo do balancete.'
                return render(request, BALANCETE_CADASTRO_PAGE, {'msg' :  msg})


            balancete.ano = int(ano)
            balancete.mes = int(mes)
            print('DADOS DO BALANCETE OK ')

            # Efetuar uma busca e verificar numero de versão do documento.
            balancete_antigo = Balancete.objects.filter(ano=balancete.ano, mes=balancete.mes).all()
            print(balancete_antigo)
            if balancete_antigo:
                balancete_antigo = Balancete.objects.filter(ano=balancete.ano, mes=balancete.mes).latest('versao')
                print(balancete_antigo)
                balancete.versao = balancete_antigo.versao + 1

            else:
                balancete.versao = 1

            balancete.save()
            print('BALANCETES')


            for conta in contas:
                print('CODIGO BALANCETE' + str(balancete.codigo))
                conta.balancete = balancete
                conta.saldo_acumulado = convert_valor(conta.saldo_acumulado)
                conta.saldo_anterior = convert_valor(conta.saldo_anterior)
                conta.movimento = convert_valor(conta.movimento)
                conta.debitos = convert_valor(conta.debitos)
                conta.creditos= convert_valor(conta.creditos)
                print(conta)
                conta.save()
                print("*********************")



            msg = 'Balancete enviado com sucesso.'

            return render(request, BALANCETE_CADASTRO_PAGE, {'msg': msg})


        else:
            raise Exception('MethodEnvioError, Use POST para formulários.')

    except Exception as ex:
        print(ex.args)
        return render(request, BALANCETE_CADASTRO_PAGE, {'msg':  'Erro no formulário preencha todos os campos.' + str(ex.args)})
        pass

@login_required_usuario
def listar_balancetes(request):
    try:
        if request.method == 'POST':
            ano = request.POST['ano']
            mes = request.POST['mes']

            if ano is None or len(ano) <= 0:
                msg = 'Informe o ano do balancete.'
                return render(request, BALANCETE_CADASTRO_PAGE, {'msg':  msg})

            elif mes is None or len(mes) <= 0:
                msg = 'Informe o mês do balancete.'
                return render(request, BALANCETE_CADASTRO_PAGE, {'msg':  msg})

            ano = int(ano)
            mes = int(mes)

            balancetes = Balancete.objects.filter(ano=ano, mes=mes).all()




            return render(request, BALANCETE_LISTA_PAGE, {'balancetes' : balancetes })

        else:
            raise Exception('MethodEnvioError, Use POST para formulários.')

    except Exception as ex:
        print(ex.args)
        return render(request, BALANCETE_LISTA_PAGE, {
            'msg':  'Erro no formulário preencha todos os campos.' + str(ex.args)})
        pass
@login_required_usuario
def cadastrar_base_calculo_pis_cofins(request):
    try:
        if request.method == "POST":
            conta = request.POST['conta']
            descricao = request.POST['descricao']
            tipo_conta = request.POST['tipo']

            if not conta or not descricao:
                msg = 'Erro, por favor preencha todos os campos.'
                return render(request, CADASTRO_BASE_CALCULO_PIS_COFINS_PAGE, {'msg' :  msg})
            # Trava para evitar Contas Duplicadas
            if ContaBaseCalculoPisCofins.objects.filter(conta=conta).exists(): # Conta  já existe no banco?
                msg = f'Erro: A conta {conta} já está cadastrada.' # sim?
                return render(request, CADASTRO_BASE_CALCULO_PIS_COFINS_PAGE, {'msg': msg})


        conta_pis_cofins = ContaBaseCalculoPisCofins()
        conta_pis_cofins.conta = conta
        conta_pis_cofins.descricao = descricao
        conta_pis_cofins.tipo_conta = int(tipo_conta)
        conta_pis_cofins.save()
        msg = 'Base de cálculo adicionada com sucesso.'

        return render(request, CADASTRO_BASE_CALCULO_PIS_COFINS_PAGE, {'msg' :  msg})

    except Exception as ex:
        print(ex.args)
        return render(request, CADASTRO_BASE_CALCULO_PIS_COFINS_PAGE,
                      {'msg': 'Erro no formulário preencha todos os campos.' + str(ex)})
    pass

@login_required_usuario
def cadastrar_base_calculo_irpj_csll(request):
    try:
        if request.method == "POST":
            conta = request.POST['conta']
            descricao = request.POST['descricao']

            if not conta or not descricao:
                msg = 'Erro, por favor preencha todos os campos.'
                return render(request, CADASTRO_BASE_CALCULO_IRPJ_CSLL_PAGE, {'msg' :  msg })


        conta_irpj_csll = ContaBaseCalculoIRPJCSLL()
        conta_irpj_csll.conta = conta
        conta_irpj_csll.descricao = descricao
        msg = 'Base de cálculo adicionada com sucesso.'
        conta_irpj_csll.save()

        return render(request, CADASTRO_BASE_CALCULO_IRPJ_CSLL_PAGE, {'msg' :  msg})

    except Exception as ex:
        print(ex.args)
        return render(request, CADASTRO_BASE_CALCULO_IRPJ_CSLL_PAGE,
                      {'msg': 'Erro no formulário preencha todos os campos.' + str(ex)})
    pass

@login_required_usuario
def exibir_contas_balancete(request, codigo):
    try:
        if codigo:
            codigo = int(codigo)
            balancete = Balancete.objects.filter(codigo=codigo).first()
            print(balancete)
            contas = ContaBalancete.objects.filter(Q(balancete=balancete) | Q(balancete__isnull=True)).all()
            print(contas)
            balancete.contas = contas
            for conta in balancete.contas:
                conta.debitos = locale_br(conta.debitos)
                conta.movimento = locale_br(conta.movimento)
                conta.saldo_anterior = locale_br(conta.saldo_anterior)
                conta.saldo_acumulado = locale_br(conta.saldo_acumulado)

            balancetes = [balancete]
            print(balancete.contas)
            return render(request, BALANCETE_LISTA_PAGE, {'balancetes' :  balancetes})


    except Exception as ex:
        return render(request, BALANCETE_LISTA_PAGE,
                      {'msg': 'Erro ao carregar as contas do balancete.' + str(ex.args)})


    pass

@login_required_usuario
def cadastrar_relatorio(request):
    try:
        if request.method == 'POST':
            relatorio = None
            ano = request.POST['ano']
            mes = request.POST['mes']
            tipo = request.POST['tipo']

            if ano is None or len(ano) <= 0:
                msg = 'Informe o ano do relatório.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            elif mes is None or len(mes) <= 0:
                msg = 'Informe o mês do relatório.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            elif tipo is None or len(tipo) <= 0:
                msg = 'Informe o tipo de relatório.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            if int(tipo) == 1:
                relatorio = RelatorioSINPAG()
                relatorio.ano = int(ano)
                relatorio.mes = int(mes)

                movimentos = load_movimentos_relatorio_sinpag(request.FILES['relatorio'])
                calculos = calculos_sinpag(movimentos)

                if movimentos is None or len(movimentos) <= 0:
                    msg = 'Erro, informe o relatório.'
                    return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

                relatorio_antigo = RelatorioSINPAG.objects.filter(ano=ano, mes=mes).first()

                if relatorio_antigo:
                    relatorio_antigo.delete()

                relatorio.soma_vr_mov = calculos[0]
                relatorio.soma_vr_cos_ced = calculos[1]
                relatorio.dif_soma_cos_ced_vr_mov =calculos[2]
                relatorio.save()

                print(locale_br(calculos[0]))
                print(locale_br(calculos[1]))
                print(locale_br(calculos[2]))


                for movimento in movimentos:
                    movimento.relatorio = relatorio
                    # Comentado para teste no heroku
                    #movimento.save()


                msg = 'Relatório enviado com sucesso.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            elif int(tipo) == 2:
                relatorio = RelatorioSINPAGAC()
                relatorio.ano = int(ano)
                relatorio.mes = int(mes)

                movimentos = load_movimentos_relatorio_sinpagac(request.FILES['relatorio'])
                calculos = calculos_sinpagac(movimentos)

                relatorio_antigo = RelatorioSINPAGAC.objects.filter(ano=ano, mes=mes).first()

                if relatorio_antigo:
                    relatorio_antigo.delete()

                if movimentos is None or len(movimentos) <= 0:
                    msg = 'Erro, informe o relatório.'
                    return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

                relatorio.soma_vr_mov = calculos
                relatorio.save()

                for movimento in movimentos:
                    movimento.relatorio = relatorio
                    movimento.save()

                msg = 'Relatório enviado com sucesso.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            elif int(tipo) == 2:
                relatorio = RelatorioSINPAGAC()
                relatorio.ano = int(ano)
                relatorio.mes = int(mes)

                movimentos = load_movimentos_relatorio_sinpagac(request.FILES['relatorio'])

                relatorio_antigo = RelatorioSINPAGAC.objects.filter(ano=ano, mes=mes).first()

                if relatorio_antigo:
                    relatorio_antigo.delete()

                if movimentos is None or len(movimentos) <= 0:
                    msg = 'Erro, informe o relatório.'
                    return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

                relatorio.save()

                for movimento in movimentos:
                    movimento.relatorio = relatorio
                    movimento.vr_mov = convert_valor(movimento.vr_mov)
                    movimento.save()

                msg = 'Relatório enviado com sucesso.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            elif int(tipo) == 3:
                relatorio = RelatorioSalvadosVendidosNovos()
                relatorio.ano = int(ano)
                relatorio.mes = int(mes)

                movimentos = load_movimentos_relatorio_salvados_vendidos_novos(request.FILES['relatorio'])
                calculo = calculos_salvados_vendidos_novos(movimentos)

                relatorio_antigo = RelatorioSalvadosVendidosNovos.objects.filter(ano=ano, mes=mes).first()

                if relatorio_antigo:
                    relatorio_antigo.delete()

                if movimentos is None or len(movimentos) <= 0:
                    msg = 'Erro, informe o relatório.'
                    return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

                relatorio.soma_vr_mov = calculo
                relatorio.save()

                for movimento in movimentos:
                    movimento.relatorio = relatorio
                    movimento.vr_mov = convert_valor(movimento.vr_mov)
                    #movimento.save()

                msg = 'Relatório enviado com sucesso.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            elif int(tipo) == 4:
                relatorio = RelatorioRecuperadosNovo()
                relatorio.ano = int(ano)
                relatorio.mes = int(mes)

                movimentos = load_movimentos_relatorio_recuperados_novo(request.FILES['relatorio'])
                calculos = calculos_recuperados_novos(movimentos)

                relatorio_antigo = RelatorioRecuperadosNovo.objects.filter(ano=ano, mes=mes).first()

                if relatorio_antigo:
                    relatorio_antigo.delete()

                if movimentos is None or len(movimentos) <= 0:
                    msg = 'Erro, informe o relatório.'
                    return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

                relatorio.dif_soma_baixa_ind_res_salv = calculos[0]
                relatorio.soma_baixa_ind = calculos[1]
                relatorio.soma_baixa_res = calculos[2]
                relatorio.soma_baixa_salv = calculos[3]

                relatorio.save()

                for movimento in movimentos:
                    movimento.relatorio = relatorio
                    #movimento.vr_mov = convert_valor(movimento.vr_mov)
                    # Comentado para testes no heroku
                    #movimento.save()

                msg = 'Relatório enviado com sucesso.'
                return render(request, CADASTRO_RELATORIO_PAGE, {'msg': msg})

            else:
                raise Exception('Erro, tipo de relatório não encontrado.')


        else:
            raise Exception('Error, use post para formulários.')

    except Exception as ex:
        print(ex.args)
        return render(request, CADASTRO_RELATORIO_PAGE,
                      {'msg': 'Erro no formulário preencha todos os campos.' + str(ex.args)})

    pass

@login_required_usuario
def calcular_pis_cofins(request):
    try:
        if request.method == 'POST':
            retencao_pis = request.POST['retencao-pis'] or '0'
            compensacao_pis = request.POST['compensacao-pis'] or '0'
            retencao_cofins = request.POST['retencao-cofins'] or '0'
            compensacao_cofins = request.POST['compensacao-cofins'] or '0'
            ano = request.POST['ano']
            mes = request.POST['mes']

            # Salvando o ano e mês na sessão
            request.session['ano_selecionado'] = ano
            request.session['mes_selecionado'] = mes

            print('ANO BALANCETE : '  + str(ano))
            print('MES BALANCETE : '  + str(mes))
            print('Retenção PIS :' + retencao_pis)
            print('Compensação PIS : ' + compensacao_pis)

            base = BaseCalculoPisCofins()
            base.ano = int(ano)
            base.mes = int(mes)

            balancete = Balancete.objects.filter(ano=ano, mes=mes).first()

            if balancete:
                balancete = Balancete.objects.filter(ano=balancete.ano, mes=balancete.mes).latest('versao')

                base_calculo_pis = ContaBaseCalculoPisCofins.objects.all()

                contas = []

                for base_calculo in base_calculo_pis:
                    contas_balancetes = ContaBalancete.objects.filter(conta_do_razao=base_calculo.conta,
                                                                      balancete_id=balancete.codigo).all()

                    if contas_balancetes:
                        conta_balancete = contas_balancetes[0]
                        # Soma de contas do balancete -> informar o tipo movimento da base de calculo, e as contas do balancete.
                        conta_balancete.movimento = soma_contas_balancete(base_calculo.tipo_conta,
                                                                          contas_balancetes=contas_balancetes)
                        contas.append(conta_balancete)

                balancete.contas = contas
                soma_receita = calcular_soma_receitas(balancete.contas)
                base.soma_receita_balancete = soma_receita

                relatorio_sinpag = RelatorioSINPAG.objects.filter(ano=ano, mes=mes).first()
                relatorio_sinpagac = RelatorioSINPAGAC.objects.filter(ano=ano, mes=mes).first()
                relatorio_salvados_vendidos = RelatorioSalvadosVendidosNovos.objects.filter(ano=ano, mes=mes).first()
                relatorio_recuperados = RelatorioRecuperadosNovo.objects.filter(ano=ano, mes=mes).first()

                # Calculo final com a possibilidade de um relatorio não estar presente.
                if not relatorio_sinpag:
                    relatorio_sinpag = RelatorioSINPAG()
                    relatorio_sinpag.dif_soma_cos_ced_vr_mov = 0
                    relatorio_sinpag.soma_vr_mov = 0
                    relatorio_sinpag.soma_vr_cos_ced = 0

                if not relatorio_sinpagac:
                    relatorio_sinpagac = RelatorioSINPAGAC()
                    relatorio_sinpagac.soma_vr_mov = 0

                if not relatorio_recuperados:
                    relatorio_recuperados = RelatorioRecuperadosNovo()
                    relatorio_recuperados.soma_baixa_ind = 0
                    relatorio_recuperados.soma_baixa_salv = 0
                    relatorio_recuperados.soma_baixa_res = 0
                    relatorio_recuperados.dif_soma_baixa_ind_res_salv = 0

                if not relatorio_salvados_vendidos:
                    relatorio_salvados_vendidos = RelatorioSalvadosVendidosNovos()
                    relatorio_salvados_vendidos.soma_vr_mov = 0

                dif_soma_receita_sinpag_sinpagac = base.soma_receita_balancete + (
                    relatorio_sinpag.dif_soma_cos_ced_vr_mov + relatorio_sinpagac.soma_vr_mov)

                base_calculo = (dif_soma_receita_sinpag_sinpagac - ( relatorio_recuperados.dif_soma_baixa_ind_res_salv + \
                    relatorio_salvados_vendidos.soma_vr_mov)) * -1

                print(dif_soma_receita_sinpag_sinpagac)
                print(base_calculo)

                base.pis_retido = float(retencao_pis.replace(",", "."))
                base.compensacao_pis = float(compensacao_pis.replace(",", "."))
                base.cofins_retido = float(retencao_cofins.replace(",", "."))
                base.compensacao_cofins = float(compensacao_cofins.replace(",", "."))

                base.pis = base_calculo * 0.0065
                base.pis_recolher = base.pis - (base.pis_retido + base.compensacao_pis)
                base.pis_darf = base.pis_recolher

                base.cofins = base_calculo * 0.04
                base.cofins_recolher = base.cofins - (base.cofins_retido + base.compensacao_cofins)
                base.cofins_darf = base.cofins_recolher

                # base.pis = locale_br(base.pis)  {possível simplificação!}
                dados_para_sessao_e_tela = {
                    'pis_valor_str': locale_br(base.pis),
                    'pis_recolher_str': locale_br(base.pis_recolher),
                    'pis_darf_str': locale_br(base.pis_darf),
                    'pis_retido_str': locale_br(base.pis_retido),
                    'pis_compensado_str': locale_br(base.compensacao_pis),
                    'cofins_valor_str': locale_br(base.cofins),
                    'cofins_recolher_str': locale_br(base.cofins_recolher),
                    'cofins_darf_str': locale_br(base.cofins_darf),
                    'cofins_retido_str': locale_br(base.cofins_retido),
                    'cofins_compensado_str': locale_br(base.compensacao_cofins)
                }
                request.session['ultimo_calculo_pis_cofins'] = dados_para_sessao_e_tela
                # base.pis = locale_br(base.pis)  {possível simplificação!}
                base.pis = dados_para_sessao_e_tela['pis_valor_str']
                base.pis_recolher = dados_para_sessao_e_tela['pis_recolher_str']
                base.pis_darf = dados_para_sessao_e_tela['pis_darf_str']
                base.pis_retido = dados_para_sessao_e_tela['pis_retido_str']
                base.compensacao_pis = dados_para_sessao_e_tela['pis_compensado_str']
                base.cofins = dados_para_sessao_e_tela['cofins_valor_str']
                base.cofins_recolher = dados_para_sessao_e_tela['cofins_recolher_str']
                base.cofins_darf = dados_para_sessao_e_tela['cofins_darf_str']
                base.cofins_retido = dados_para_sessao_e_tela['cofins_retido_str']
                base.compensacao_cofins = dados_para_sessao_e_tela['cofins_compensado_str']

                dados = montar_dados_tela_pis_cofins(base.ano, base.mes, base)
                print(base)
                context = {
                    'dados': dados,
                    'msg_1': 'Dados gerados com sucesso.',
                    # Lemos da sessão para garantir que os campos sejam pré-preenchidos
                    'ano_selecionado': request.session.get('ano_selecionado'),
                    'mes_selecionado': request.session.get('mes_selecionado'),
                    # Também passamos 'ano' e 'mes' para compatibilidade com o template
                    'ano': int(request.session.get('ano_selecionado', 0)),
                    'mes': int(request.session.get('mes_selecionado', 0)),
                }
                return render(request, CADASTRO_PIS_COFINS_PAGE, context)
            else:
                raise Exception('Balancete não encontrado.')

        else:
            raise Exception('Erro, use POST para formulários ')


    except Exception as ex:
        print(ex.args)
        context = {
            'msg_1': 'Erro, ' + str(ex.args),
            'ano_selecionado': request.session.get('ano_selecionado'),
            'mes_selecionado': request.session.get('mes_selecionado'),
            'ano': int(request.session.get('ano_selecionado', 0)),
            'mes': int(request.session.get('mes_selecionado', 0)),
        }
        return render(request, CADASTRO_PIS_COFINS_PAGE, context)

@login_required_usuario
def exportar_csv_pis_cofins(request, ano, mes):
    """
    Exporta um relatório CSV completo contendo:
        Contas e o movimento
        Relatórios (SINPAGAC, etc.)
        Apuração de PIS/COFINS
    cada seção é separada por uma linha em branco.
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="Apuracao_Pis_Cofins_{convert_mes_texto(mes)}{ano}.csv"'

    writer = csv.writer(response, delimiter=';')

    # --- Bloco de Dados (Relatórios e Balancete) ---
    try:
        # Buscamos todos os dados de uma vez para sermos mais eficientes
        dados_csv = montar_dados_tela_pis_cofins(ano, mes, None)

        # --- Parte 1: Detalhamento do Balancete ---
        balancete = dados_csv.get('balancete')

        if balancete and hasattr(balancete, 'contas'):
            contas_do_balancete = balancete.contas

            if contas_do_balancete:
                fieldnames_contas = ['Conta do Razao', 'Descricao', 'Movimento']
                writer.writerow(fieldnames_contas)

                for conta in contas_do_balancete:
                    movimento_limpo = limpar_string_moeda(conta.movimento)
                    writer.writerow([
                        conta.conta_do_razao,
                        conta.periodo,
                        movimento_limpo
                    ])
                writer.writerow(['', 'Base de Calculo:', limpar_string_moeda(dados_csv.get('base_calculo'))])
            else:
                writer.writerow(['Balancete encontrado, mas sem contas para exibir.'])
        else:
            writer.writerow(['Nenhum dado do balancete encontrado para este período.'])

        writer.writerow([])

        # --- Parte 2: Relatórios Consolidados ---
        fieldnames_relatorios = ['Tipo', 'Mes/Ano', 'Valor']
        writer.writerow(fieldnames_relatorios)
        # Relatório SINPAG
        relatorio_sinpag = dados_csv.get('relatorio_sinpag')
        writer.writerow(['SINPAG', str(mes) + '/' + str(ano),
                         relatorio_sinpag.dif_soma_cos_ced_vr_mov]) if relatorio_sinpag else 'SINPAG nao encontrado'
        # Relatório SINPAGAC
        relatorio_sinpagac = dados_csv.get('relatorio_sinpagac')
        writer.writerow(['SINPAGAC', str(mes) + '/' + str(ano),
                         relatorio_sinpagac.soma_vr_mov]) if relatorio_sinpagac else 'SINPAGAC nao encontrado'
        # Relatório SALVADOS VENDIDOS
        relatorio_salvados = dados_csv.get('relatorio_salvados_vendidos')
        writer.writerow(['SALVADOS', str(mes) + '/' + str(ano),
                         relatorio_salvados.soma_vr_mov]) if relatorio_salvados else 'SALVADOS nao encontrado'
        # Relatório RECUPERADOS
        relatorio_recuperados = dados_csv.get('relatorio_recuperados')
        writer.writerow(['RECUPERADOS', str(mes) + '/' + str(ano), # ERRO: str(mes + '/' + ano)
                         relatorio_recuperados.dif_soma_baixa_ind_res_salv]) if relatorio_recuperados else 'RECUPERADOS nao encontrado'
    except Exception as e:
        writer.writerow([])  # Separador antes do erro
        writer.writerow([f"Erro ao buscar relatórios ou balancete: {e}"])

    writer.writerow([])

    # --- Parte 3: Apuração PIS/COFINS da Sessão ---
    dados_calculo = request.session.get('ultimo_calculo_pis_cofins', {})

    if dados_calculo:
        fieldnames_calculo = ['Imposto', 'Valor Apurado', 'Retido', 'Compensado', 'a Recolher']
        writer.writerow(fieldnames_calculo)

        writer.writerow([
            'PIS', dados_calculo.get('pis_valor_str', ''), dados_calculo.get('pis_retido_str', ''),
            dados_calculo.get('pis_compensado_str', ''), dados_calculo.get('pis_recolher_str', '')
        ])
        writer.writerow([
            'COFINS', dados_calculo.get('cofins_valor_str', ''), dados_calculo.get('cofins_retido_str', ''),
            dados_calculo.get('cofins_compensado_str', ''), dados_calculo.get('cofins_recolher_str', '')
        ])
    else:
        writer.writerow(['Nenhum cálculo recente encontrado na sessão para exportar.'])

    return response