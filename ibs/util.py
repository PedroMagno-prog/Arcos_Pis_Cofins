from .models import *
import csv
import locale
import io
import hashlib

def criptografar_senha(senha: str) -> str:
    """
    Return SHA3-256 hex digest of the given password.
    """
    return hashlib.sha3_256(senha.encode()).hexdigest()
    pass


def locale_br(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    #locale.setlocale(locale.LC_ALL, 'pt_BR')
    locale.currency(543921.94, symbol=True, grouping=True)
    return locale.currency(valor, symbol=True, grouping=True)

def limpar_string_moeda(valor):
    """
    Recebe um número ou uma string (ex: "R$ -12345,67") e formata
    para o padrão contábil brasileiro (ex: "-1.234.567,89"),
    ideal para exportação em CSV.
    """
    numero_float = 0
    sinal = ''

    # Isola o sinal para tratá-lo no final
    if '-' in valor:
        sinal = '-'

    # Limpa a string de qualquer caractere não numérico, exceto a vírgula decimal
    valor_numerico_str = ''.join(c for c in valor if c.isdigit() or c == ',')
    # Converte para o formato de float padrão do Python (com ponto decimal)
    valor_numerico_str = valor_numerico_str.replace(',', '.')

    try:
        numero_float = float(valor_numerico_str)
    except (ValueError, TypeError):
        return valor  # Se a conversão falhar, retorna o valor original

    # --- Passo 2: Formatar o número para o padrão brasileiro ---
    # Separa a parte inteira da decimal, já arredondando para 2 casas
    parte_inteira_str, parte_decimal_str = f"{abs(numero_float):.2f}".split('.')

    # Adiciona os separadores de milhar (.) na parte inteira
    parte_inteira_com_pontos = ""
    for i, digito in enumerate(reversed(parte_inteira_str)):
        if i > 0 and i % 3 == 0:
            # Insere um ponto a cada 3 dígitos
            parte_inteira_com_pontos = "." + parte_inteira_com_pontos
        parte_inteira_com_pontos = digito + parte_inteira_com_pontos

    # --- Passo 3: Juntar tudo ---
    # Reconstrói o número com o sinal (se houver), a parte inteira formatada
    # e a parte decimal separada por vírgula.
    return f"{sinal}{parte_inteira_com_pontos},{parte_decimal_str}"

def calcular_aliquota_ibs(codigo_servico=float):
    if codigo_servico == 1001:
        return 26.5
    elif codigo_servico == 1714 or codigo_servico == 1719:
        return 18.55
    elif codigo_servico == 401 or codigo_servico == 4.23:
        return 10.6
    else:
        return 26.5
    pass

def convert_valor(valor) :
    # --- Início da Alteração ---
    # 1. Verificamos se o valor, sem espaços, é um hífen.
    if valor.strip() == '-':
        # 2. Se for, retornamos a string '0' e a função termina aqui.
        return '0'
    # --- Fim da Alteração ---

    if '.' in valor:
        valor = valor.replace('.', '')
        valor = valor.replace(',', '.')
    else:
        valor = valor.replace(',', '.')

    return valor
    pass

def load_receitas(myfile):
    receitas = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader)
    for row in reader:
        if len(row[0]) > 0:
            receita = ReceitaModel()
            receita.cnpj_tomador = row[0]
            receita.municipio_tomador = row[1]
            receita.cnpj_cliente = row[3]
            receita.razao_social = row[5]
            receita.numero_nota = row[6]
            receita.codigo_servico = row[7]
            receita.data_do_servico = row[8]
            receita.valor = row[9]
            receita.municipio_cliente = row[14]
            receitas.append(receita)
    return receitas

    pass

def load_despesas(myfile):
    despesas = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader)
    for row in reader:
        if len(row[0]) > 0:
            despesa = DespesaModel()
            despesa.cnpj_tomador = row[0]
            despesa.municipio_tomador = row[1]
            despesa.razao_social = row[5]
            despesa.numero_nota = row[6]
            despesa.codigo_servico = row[7]
            despesa.data_lancamento = row[8]
            despesa.valor = row[9]
            despesa.aliquota = row[10]
            despesa.cidade_prestador = row[14]
            despesa.optante_simples = row[15]
            despesas.append(despesa)
    return despesas

def calcular_somatorio_receitas(receitas):
    municipios = ('SAO PAULO', 'RIO DE JANEIRO', 'LONDRINA', 'OSASCO')
    resumos = []
    for m in municipios:
        valor_total = 0
        resumo = ResumoModel()
        resumo.municipio = m
        resumo.codigo_servico = '1001'
        for receita in receitas:
            if receita.municipio_cliente == m and receita.codigo_servico == '1001':
                valor_r = float(convert_valor(receita.valor))
                valor_total += valor_r

        resumo.valor = valor_total
        resumos.append(resumo)
        valor_total = 0

    total_resumos = 0
    for resumo in resumos:
        total_resumos += resumo.valor
    return resumos, total_resumos
    pass

def calcular_somatorio_despesas(despesas):
    valor = 0
    for despesa in despesas:
        valor += float(convert_valor(despesa.valor))
    return valor


def calcular_percentual_media_receita_despesas(total_receitas, total_despesas):
    perc = total_despesas / total_receitas

    return perc
    pass

def calcular_credito_por_municipio(resumos, perc):
    total_credito = 0
    for resumo in resumos:
        resumo.credito_municipio = resumo.valor * perc
        total_credito += resumo.credito_municipio

    return resumos, total_credito

def calcular_base_calculo_(resumos):
    total_base_calculo = 0
    for resumo in resumos:
        resumo.base_calculo = resumo.valor - resumo.credito_municipio
        total_base_calculo += resumo.base_calculo

    return resumos, total_base_calculo

def calcular_valor_iva(resumos):
    aliquota = 26.5
    total_iva = 0
    for resumo in resumos:
        resumo.iva = resumo.base_calculo * (aliquota / 100)
        total_iva +=resumo.iva

    return resumos, total_iva



def calcular_valor_ibs(resumos):
    aliquota = 17.7
    total_ibs = 0
    for resumo in resumos:
        resumo.ibs = resumo.base_calculo * (aliquota / 100)
        total_ibs += resumo.ibs

    return resumos, total_ibs


def calcular_valor_cbs(resumos):
    aliquota = 8.8
    total_cbs = 0
    for resumo in resumos:
        resumo.cbs = resumo.base_calculo * (aliquota / 100)
        total_cbs += resumo.cbs

    return resumos, total_cbs


def load_contas_do_balancete(myfile):
    balancetes = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)
    for row in reader:
            print(row)
            conta = ContaBalancete()
            conta.conta_do_razao = row[0]
            conta.periodo = row[1]
            conta.grupo_ramo = row[2]
            conta.nome_conta = row[3]
            conta.saldo_anterior = row[4]
            conta.debitos = row[5]
            conta.creditos = row[6]
            conta.movimento = row[7]
            conta.saldo_acumulado = row[8]
            balancetes.append(conta)
            pass
    return balancetes
    pass

def load_movimentos_relatorio_sinpag(myfile):
    movimentos = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)
    for row in reader:
            movimento = MovimentacaoSINPAG()
            movimento.cod_cia = row[1]
            movimento.dt_base = row[2]
            movimento.cod_ramo = row[4]
            movimento.num_sin = row[5]
            movimento.num_apol = row[6]
            movimento.cpf_ben = row[10]
            movimento.vr_cos_ced = convert_valor(row[15])
            movimento.vr_mov = convert_valor(row[16])
            movimento.tp_sin = int(row[18])
            movimentos.append(movimento)

            pass
    return movimentos
    pass

def calculos_sinpag(movimentos):
    soma_vr_mov =0
    soma_vr_cos_ced =0
    dif_soma_vr_mod_cos_ced = 0

    for movimento in movimentos:
        if movimento.tp_sin == 1 or movimento.tp_sin == 3:
            soma_vr_mov = soma_vr_mov + float(movimento.vr_mov)
            soma_vr_cos_ced = soma_vr_cos_ced + float(movimento.vr_cos_ced)

    dif_soma_vr_mod_cos_ced = soma_vr_mov - soma_vr_cos_ced

    return soma_vr_mov, soma_vr_cos_ced, dif_soma_vr_mod_cos_ced

    pass




def load_movimentos_relatorio_sinpagac(myfile):
    movimentos = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)
    for row in reader:
            movimento = MovimentacaoSINPAGAC()
            movimento.cod_cia = row[1]
            movimento.dt_base = row[2]
            movimento.cod_coss = row[5]
            movimento.num_sin = row[6]
            movimento.num_apol= row[7]
            movimento.vr_mov = convert_valor(row[12])
            movimento.tp_sin = int(row[13])
            movimento.g_cpf_bnf = row[17]
            movimentos.append(movimento)
            pass
    return movimentos
    pass

def calculos_sinpagac(movimentos):
    soma_vr_mov = 0
    for movimento in movimentos:
        if movimento.tp_sin == 1:
            soma_vr_mov = soma_vr_mov + float(movimento.vr_mov)
        pass
    return soma_vr_mov
    pass


def load_movimentos_relatorio_salvados_vendidos(myfile):
    movimentos = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)
    for row in reader:
            movimento = MovimentacaoSalvadosVendidos()
            movimento.cod_cia = row[0]
            movimento.cod_ctabal = row[1]
            movimento.cod_classe = row[2]
            movimento.receita_baixa = convert_valor(row[5])
            movimento.bx_dep_prej = row[6]
            movimento.bx_val_cont_ganho = row[7]
            movimentos.append(movimento)
            pass
    return movimentos
    pass

def load_movimentos_relatorio_salvados_vendidos_novos(myfile):
    movimentos = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)

    for row in reader:
            movimento = MovimentacaoSalvadosVendidosNovos()
            movimento.cod_cia = row[1]
            movimento.dt_base = row[2]
            movimento.tipo_mov = row[3]
            movimento.cod_ramo = row[4]
            movimento.num_sin = row[5]
            movimento.cpf_ben = row[10]
            movimento.vr_mov = convert_valor(row[16])
            movimento.tp_sin = row[18]
            movimentos.append(movimento)
            pass
    return movimentos
    pass


# Alteração no calculo somente tipo 209 e 210
def calculos_salvados_vendidos_novos(movimentos):
    soma_vr_mov = 0
    for movimento in movimentos:

        if movimento.tipo_mov == '209' or movimento.tipo_mov == '210':
            print(movimento.tipo_mov)
            soma_vr_mov = soma_vr_mov + float(movimento.vr_mov)
    return soma_vr_mov

def calculos_salvados_vendidos(movimentos):
    soma_receita_baixa_positiva = 0

    for movimento in movimentos:
        if float(movimento.receita_baixa) > 0:
            soma_receita_baixa_positiva = soma_receita_baixa_positiva + float(movimento.receita_baixa)

    return soma_receita_baixa_positiva
    pass



def load_movimentos_relatorio_recuperados_novo(myfile):
    movimentos = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)
    for row in reader:
            movimento = MovimentacaoRecuperadosNovo()
            movimento.tipo_sin = row[1]
            movimento.num_sin = row[2]
            movimento.cod_ramo = row[4]
            movimento.baixa_ind = convert_valor(row[23])
            movimento.baixa_salv = convert_valor(row[26])
            movimento.baixa_res = convert_valor(row[27])
            print(movimento)
            movimentos.append(movimento)

            pass
    return movimentos
    pass


def load_movimentos_relatorio_recuperados(myfile):
    movimentos = []
    file = myfile.read().decode('utf-8')
    reader = csv.reader(io.StringIO(file), delimiter=';')
    next(reader, None)
    for row in reader:
            movimento = MovimentacaoRecuperados()
            movimento.cod_cia = row[0]
            movimento.num_sin = row[2]
            movimento.dt_base = ''
            movimento.cod_ramo = row[4]
            movimento.descricao = row[7]
            movimento.cod_prod = row[10]
            movimento.mes_ind =convert_valor(row[17])
            print(row[17])
            movimento.baixa_total = row[28]
            movimentos.append(movimento)
            pass
    return movimentos
    pass

def calculos_recuperados_novos(movimentos):
    dif_soma_baixa_ind_res_salv = 0
    soma_baixa_ind = 0
    soma_baixa_res = 0
    soma_baixa_salv = 0
    for movimento in movimentos:
        if movimento.tipo_sin == '1':
             soma_baixa_ind = soma_baixa_ind + float(movimento.baixa_ind)
             soma_baixa_res = soma_baixa_res + float(movimento.baixa_res)
             soma_baixa_salv = soma_baixa_salv + float(movimento.baixa_salv)

    print('Soma Baixa Ind', soma_baixa_ind)
    print('Soma Baixa Res', soma_baixa_res)
    print('Soma Baiva salv', soma_baixa_salv)
    dif_soma_baixa_ind_res_salv = soma_baixa_ind + soma_baixa_salv + soma_baixa_res
    print('Soma vr mov', dif_soma_baixa_ind_res_salv)
    return dif_soma_baixa_ind_res_salv, soma_baixa_ind, soma_baixa_res, soma_baixa_salv

def calculos_recuperados(movimentos):
    soma_mes_ind = 0
    for movimento in movimentos:
        soma_mes_ind = soma_mes_ind + float(movimento.mes_ind)
    return soma_mes_ind

def calcular_soma_receitas(contas):
    soma = 0
    for conta in contas:
        soma = conta.movimento + soma
    return soma
    pass


def convert_mes_texto(mes):
    if mes == 1:
        return 'Janeiro'
    elif mes == 2:
        return 'Fevereiro'
    elif mes == 3:
        return 'Março'
    elif mes == 4:
        return 'Abril'
    elif mes == 5:
        return 'Maio'
    elif mes == 6:
        return 'Junho'
    elif mes == 7:
        return 'Julho'
    elif mes == 8:
        return 'Agosto'
    elif mes == 9:
        return 'Setembro'
    elif mes == 10:
        return 'Outubro'
    elif mes == 11:
        return 'Novembro'
    elif mes == 12:
        return 'Dezembro'
    return None
    pass

# Função para calcular a soma dos contas do balancete pelo tipo de conta informado pela
# base de calculo informado no PIS / COFINS.
def verificar_tipo_conta(tipo_conta, soma):

    if tipo_conta == 1:
        # CREDORA
        if soma <= 0:
            return soma
        pass
    elif tipo_conta == 2:
        # DEVEDORA
        if soma >= 0:
            return soma
        pass

    elif tipo_conta == 3:
        return soma
        pass

    return 0
    pass

# Função para calcular a soma dos contas do balancete pelo tipo de conta informado pela
# base de calculo informado no PIS / COFINS.
def soma_contas_balancete(tipo_conta, contas_balancetes):
    soma = 0
    for conta in contas_balancetes: # varre o balancete procurando pelas contas de mesmo ID (conta-base)
        soma += conta.movimento

    soma = verificar_tipo_conta(tipo_conta, soma)
    return soma
    pass
