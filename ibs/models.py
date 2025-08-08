from django.db import models


# Create your models here.
class Login:
    def __init__(self, login=None, senha=None):
        self._login = login
        self._senha = senha
        pass

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value
        pass

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, value):
        self._senha = value
        pass

    pass

class UsuarioModel(models.Model):
    class Meta:
        db_table = 'usuario'

    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    senha = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f'{self.codigo}, {self.nome}, {self.email}, {self.senha}'

    def __repr__(self):
        return f'{self.codigo}, {self.nome}, {self.email}, {self.senha}'

    pass

# Create your models here.
class ReceitaModel():

    def __init__(self, cnpj_tomador = None, municipio_tomador = None,
                 municipio_cliente = None,
                 cnpj_cliente = None, razao_social =None,
                 numero_nota = None,
                 codigo_servico = None,
                 valor = None, data_do_servico=None,
                 data_recebimento=None):
        self.cnpj_tomador = cnpj_tomador
        self.municipio_tomador =municipio_tomador
        self.municipio_cliente = municipio_cliente
        self.cnpj_cliente = cnpj_cliente
        self.razao_social = razao_social
        self.numero_nota = numero_nota
        self.codigo_servico = codigo_servico
        self.valor = valor
        self.data_do_servico = data_do_servico
        self.data_recebimento = data_recebimento

        pass

    def __str__(self):
        return f'{self.cnpj_tomador}, {self.municipio_tomador},' \
               f'{self.municipio_cliente}, {self.cnpj_cliente},' \
               f'{self.razao_social}, {self.numero_nota},' \
               f'{self.codigo_servico}, {self.valor},' \
               f'{self.data_do_servico}, {self.data_recebimento}'

    def __repr__(self):
        return f'{self.cnpj_tomador}, {self.municipio_tomador},' \
               f'{self.municipio_cliente}, {self.cnpj_cliente},' \
               f'{self.razao_social}, {self.numero_nota},' \
               f'{self.codigo_servico}, {self.valor},' \
               f'{self.data_do_servico},{self.data_recebimento}'

    pass


class DespesaModel():

    def __init__(self, cnpj_tomador=None, municipio_tomador=None,
                 cidade_prestador=None,
                 razao_social=None,
                 numero_nota=None,
                 codigo_servico=None,
                 valor=None, data_lancamento=None,
                 aliquota= None,
                 optante_simples = None,
                 data_recebimento=None):
        self.cnpj_tomador = cnpj_tomador
        self.municipio_tomador = municipio_tomador
        self.cidade_prestador = cidade_prestador
        self.razao_social = razao_social
        self.numero_nota = numero_nota
        self.codigo_servico = codigo_servico
        self.valor = valor
        self.aliquota = aliquota
        self.data_lancamento = data_lancamento
        self.optante_simples = optante_simples
        self.data_recebimento = data_recebimento



        pass

    def __str__(self):
        return f'{self.cnpj_tomador}, {self.municipio_tomador},' \
               f'{self.cidade_prestador}, {self.optante_simples},' \
               f'{self.aliquota},' \
               f'{self.razao_social}, {self.numero_nota},' \
               f'{self.codigo_servico}, {self.valor},' \
               f'{self.data_lancamento}, {self.data_recebimento}'

    def __repr__(self):
        return f'{self.cnpj_tomador}, {self.municipio_tomador},' \
               f'{self.cidade_prestador}, {self.optante_simples},' \
               f'{self.aliquota},' \
               f'{self.razao_social}, {self.numero_nota},' \
               f'{self.codigo_servico}, {self.valor},' \
               f'{self.data_lancamento},{self.data_recebimento}'

    pass


class ResumoModel():

    def __init__(self, municipio = None, valor = None, codigo_servico = None,
                 credito_municipio=None):
        self.municipio = municipio
        self.valor = valor
        self.codigo_servico = codigo_servico
        self.credito_municipio=credito_municipio
        self.base_calculo = 0
        self.iva = 0
        self.ibs = 0
        self.cbs = 0
        pass

    def __str__(self):
        return f'{self.municipio}, {self.valor},' \
               f'{self.credito_municipio}' \
               f'{self.ibs}' \
               f'{self.cbs}' \
               f'{self.iva}' \
               f'{self.base_calculo}' \
               f'{self.codigo_servico}'

    def __repr__(self):
        return f'{self.municipio}, {self.valor},' \
               f'{self.credito_municipio}' \
               f'{self.base_calculo}' \
               f'{self.ibs}' \
               f'{self.cbs}' \
               f'{self.iva}' \
               f'{self.codigo_servico}'

    pass

class EmpresaModel():

    def __init__(self, nome = None, resumos = None, ):
        self.resumos = resumos
        self.nome = nome
        self.total_resumos = 0
        self.total_credito = 0
        self.total_base_calculo = 0
        self.total_iva = 0
        self.total_ibs = 0
        self.total_cbs = 0

    def __str__(self):
        return f' {self.nome}, {self.resumos}, {self.total_resumos}, ' \
               f'{self.total_credito}'

    def __repr__(self):
        return f'{self.nome}, {self.resumos}, {self.total_resumos}' \
               f'{self.total_credito}'

# SISTEMA SOMPO

class ContaBaseCalculoIRPJCSLL(models.Model):

    class Meta:
        db_table = 'contabasecalculoirpjcsll'

    codigo = models.AutoField(primary_key=True)
    conta = models.CharField(null=False, max_length=255)
    descricao = models.CharField(null=False, max_length=255)
    data_cadastro = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.codigo}, {self.conta}, {self.descricao}, {self.data_cadastro}'

    def __repr__(self):
        return f'{self.codigo}, {self.conta}, {self.descricao}, {self.data_cadastro}'


    pass


class ContaBaseCalculoPisCofins(models.Model):

    class Meta:
        db_table = 'contabasecalculopiscofins'

    codigo = models.AutoField(primary_key=True)
    conta = models.CharField(null=False, max_length=255)
    descricao = models.CharField(null=False, max_length=255)
    data_cadastro = models.DateField(auto_now_add=True)
    vigencia = models.BooleanField(default=True)


    class TipoConta(models.IntegerChoices):
        # - CREDORA - negativo
        CREDORA = 1
        # + DEVEDORA - positivo
        DEVEDORA = 2
        # + CONTA MISTA, não considerar no calculo
        CREDORA_DEVEDORA = 3

    tipo_conta = models.IntegerField(
        choices=TipoConta.choices,
        default=TipoConta.CREDORA
    )

    def __str__(self):
        return f'{self.codigo}, {self.conta}, {self.descricao}, {self.data_cadastro}, ' \
               f'{self.tipo_conta}, {self.vigencia}'

    def __repr__(self):
        return f'{self.codigo}, {self.conta}, {self.descricao}, {self.data_cadastro}, ' \
               f'{self.tipo_conta}, {self.vigencia}'
    pass


class Balancete(models.Model):

    class Meta:
        db_table = 'balancete'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)

    versao = models.IntegerField(null=False)

    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada}, {self.versao}'

    def __repr__(self):
        return f'{self.ano}, {self.mes}, {self.data_entrada}, {self.versao}'

    pass


class ContaBalancete(models.Model):
    class Meta:
        db_table = 'contabalancete'

    codigo = models.AutoField(primary_key=True)
    conta_do_razao = models.CharField(null=False, max_length=255)
    periodo = models.CharField(null=False, max_length=255)
    saldo_anterior = models.FloatField(null=False)
    debitos = models.FloatField(null=False)
    creditos = models.FloatField(null=False)
    movimento = models.FloatField(null=False)
    saldo_acumulado = models.FloatField(null=False)
    grupo_ramo = models.CharField(null=False, max_length=255, default='')
    nome_conta = models.CharField(null=False, max_length=255, default='')

    balancete = models.ForeignKey(Balancete, on_delete=models.SET_NULL,
                                   null=True)

    def __str__(self):
        return f'{self.conta_do_razao}, {self.periodo}, {self.saldo_anterior}, {self.debitos}, {self.creditos},' \
               f'{self.movimento}, {self.saldo_acumulado}, {self.grupo_ramo}, {self.nome_conta}'

    def __repr__(self):
        return f'{self.conta_do_razao}, {self.periodo}, {self.saldo_anterior}, {self.debitos}, {self.creditos},' \
               f'{self.movimento}, {self.saldo_acumulado}, {self.grupo_ramo}, {self.nome_conta}'
    pass


class RelatorioSINPAGAC(models.Model):

    class Meta:
        db_table = 'relatoriosinpagac'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)
    soma_vr_mov = models.FloatField(null=False)

    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada}, {self.soma_vr_mov}'

    def __repr__(self):
        return f'{self.ano}, {self.mes}, {self.data_entrada}, {self.soma_vr_mov}'

    pass


class MovimentacaoSINPAGAC(models.Model):

    class Meta:
        db_table = 'movimentacaosinpagac'

    codigo = models.AutoField(primary_key=True)
    vr_mov = models.FloatField(null=False)
    cod_cia = models.CharField(null=False, max_length=255)
    dt_base = models.CharField(null=False, max_length=255)
    cod_coss= models.CharField(null=False, max_length=255)
    num_sin = models.CharField(null=False, max_length=255)
    num_apol = models.CharField(null=False, max_length=255)
    g_cpf_bnf = models.CharField(null=False, max_length=255)
    tp_sin = models.IntegerField(null=False, default=0)

    relatorio = models.ForeignKey(RelatorioSINPAGAC, related_name='movimentacoes',
                                  on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        return f'{self.codigo}, {self.vr_mov}, {self.cod_cia}, {self.dt_base}, ' \
               f'{self.cod_coss}, {self.num_sin}, {self.num_apol}, {self.g_cpf_bnf}, {self.tp_sin}'

    def __repr__(self):
        return f'{self.codigo}, {self.vr_mov}, {self.cod_cia}, {self.dt_base}, ' \
               f'{self.cod_coss}, {self.num_sin}, {self.num_apol}, {self.g_cpf_bnf}, {self.tp_sin}'

    pass


class RelatorioSINPAG(models.Model):

    class Meta:
        db_table = 'relatoriosinpag'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)
    soma_vr_mov = models.FloatField(null=False)
    soma_vr_cos_ced = models.FloatField(null=False)
    dif_soma_cos_ced_vr_mov = models.FloatField(null= False)
    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada}, {self.soma_vr_mov}, ' \
               f'{self.soma_vr_cos_ced}, {self.dif_soma_cos_ced_vr_mov}'

    def __repr__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada}, {self.soma_vr_mov}, ' \
               f'{self.soma_vr_cos_ced}, {self.dif_soma_cos_ced_vr_mov}'

    pass


class MovimentacaoSINPAG(models.Model):

    class Meta:
        db_table = 'movimentacaosinpag'

    codigo = models.AutoField(primary_key=True)
    num_sin = models.CharField(null=False, max_length=255)
    cpf_ben = models.CharField(null=False, max_length=255)
    dt_base = models.CharField(null=False, max_length=255)
    num_apol = models.CharField(null=False, max_length=255)
    cod_ramo = models.CharField(null=False, max_length=255)
    cod_cia = models.CharField(null=False, max_length=255)
    vr_mov = models.FloatField(null=False, max_length=255)
    vr_cos_ced = models.FloatField(null=False)
    tp_sin = models.IntegerField(null=False, default=0)

    relatorio = models.ForeignKey(RelatorioSINPAG, related_name='movimentacoes',
                                  on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        return f'{self.codigo}, {self.vr_mov},{self.vr_cos_ced}, {self.num_apol}, {self.num_sin},' \
               f'{self.cpf_ben}, {self.cod_cia}, {self.cod_ramo}, {self.dt_base}, {self.tp_sin}'

    def __repr__(self):
        return f'{self.codigo}, {self.vr_mov},{self.vr_cos_ced}, {self.num_apol}, {self.num_sin},' \
               f'{self.cpf_ben}, {self.cod_cia}, {self.cod_ramo}, {self.dt_base}, {self.tp_sin}'

    pass



class RelatorioSalvadosVendidosNovos(models.Model):

    class Meta:
        db_table = 'relatoriosalvendnovos'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)
    soma_vr_mov = models.FloatField(null=False)

    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada}, {self.soma_vr_mov}'

    def __repr__(self):
        return f'{self.ano}, {self.mes}, {self.data_entrada}, {self.soma_vr_mov}'

    pass


class RelatorioSalvadosVendidos(models.Model):

    class Meta:
        db_table = 'relatoriosalvend'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)
    soma_positivo_receita_baixa = models.FloatField(null=False)

    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada}, {self.soma_positivo_receita_baixa}'

    def __repr__(self):
        return f'{self.ano}, {self.mes}, {self.data_entrada}, {self.soma_positivo_receita_baixa}'

    pass

class MovimentacaoSalvadosVendidos(models.Model):
    class Meta:
        db_table = 'movimentacaosalvend'

    codigo = models.AutoField(primary_key=True)
    cod_cia = models.CharField(null=False, max_length=255)
    dt_base = models.CharField(null=False, max_length=255)
    cod_ctabal = models.CharField(null=False, max_length=255)
    cod_classe = models.CharField(null=False, max_length=255)
    receita_baixa = models.FloatField(null=False)
    bx_dep_prej = models.FloatField(null=False)
    bx_val_cont_ganho = models.FloatField(null=False)

    relatorio = models.ForeignKey(RelatorioSalvadosVendidos, related_name='movimentacoes',
                                  on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.dt_base}, ' \
               f'{self.cod_ctabal}, {self.cod_classe}, {self.receita_baixa}' \
               f'{self.bx_dep_prej}, {self.bx_val_cont_ganho}'

    def __repr__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.dt_base}, ' \
               f'{self.cod_ctabal}, {self.cod_classe}, {self.receita_baixa}' \
               f'{self.bx_dep_prej}, {self.bx_val_cont_ganho}'

    pass


class MovimentacaoSalvadosVendidosNovos(models.Model):
    class Meta:
        db_table = 'movimentacaosalvendnovos'

    codigo = models.AutoField(primary_key=True)
    cod_cia = models.CharField(null=False, max_length=255)
    dt_base = models.CharField(null=False, max_length=255)

    tipo_mov = models.CharField(null=False, max_length=255)
    cod_ramo = models.CharField(null=False, max_length=255)
    cpf_ben = models.CharField(null=False, max_length=255)
    num_sin = models.CharField(null=False, max_length=255)
    vr_mov = models.FloatField(null=False, max_length=255)
    tp_sin = models.IntegerField(null=False)

    relatorio = models.ForeignKey(RelatorioSalvadosVendidosNovos, related_name='movimentacoes',
                                  on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.dt_base}, ' \
               f'{self.tipo_mov}, {self.cod_ramo}, {self.cpf_ben}' \
               f'{self.num_sin}, {self.vr_mov}, {self.tp_sin}'

    def __repr__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.dt_base}, ' \
               f'{self.tipo_mov}, {self.cod_ramo}, {self.cpf_ben}' \
               f'{self.num_sin}, {self.vr_mov}, {self.tp_sin}'

    pass


class RelatorioRecuperados(models.Model):

    class Meta:
        db_table = 'relatoriorecuperados'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)
    soma_mes_ind = models.FloatField(null=False)

    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada},' \
               f'{self.soma_mes_ind}'

    def __repr__(self):
        return f'{self.ano}, {self.mes}, {self.data_entrada}, ' \
               f'{self.soma_mes_ind}'

    pass


class MovimentacaoRecuperados(models.Model):
    class Meta:
        db_table = 'movimentacaorecuperados'

    codigo = models.AutoField(primary_key=True)
    cod_cia = models.CharField(null=False, max_length=255)
    num_sin = models.CharField(null=False, max_length=255)
    cod_ramo = models.CharField(null=False, max_length=255)
    descricao = models.CharField(null=False, max_length=255)
    mes_ind = models.FloatField(null=False)
    dt_base = models.CharField(null=False, max_length=255)
    baixa_total = models.FloatField(null=False)
    cod_prod = models.CharField(null=False, max_length=255)

    relatorio = models.ForeignKey(RelatorioRecuperados, related_name='movimentacoes',
                                  on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.num_sin}' \
               f'{self.cod_ramo}, {self.descricao}, {self.mes_ind}. {self.dt_base},' \
               f'{self.baixa_total}, {self.cod_prod}'

    def __repr__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.num_sin}' \
               f'{self.cod_ramo}, {self.descricao}, {self.mes_ind}. {self.dt_base},' \
               f'{self.baixa_total}, {self.cod_prod}'

    pass

class RelatorioRecuperadosNovo(models.Model):

    class Meta:
        db_table = 'relatoriorecuperadosnovo'

    codigo = models.AutoField(primary_key=True)
    data_entrada = models.DateField(auto_now_add=True)
    ano = models.IntegerField(null=False, blank=False)
    mes = models.IntegerField(null=False, blank=False)
    dif_soma_baixa_ind_res_salv = models.FloatField(null=False)

    soma_baixa_ind = models.FloatField(null=False, default=0)
    soma_baixa_res = models.FloatField(null=False, default=0)
    soma_baixa_salv = models.FloatField(null=False, default=0)

    def __str__(self):
        return f'{self.ano}, {self.mes},{self.data_entrada},' \
               f'{self.soma_baixa_ind}, {self.soma_baixa_res}, {self.soma_baixa_salv},' \
               f'{self.dif_soma_baixa_ind_res_salv}'

    def __repr__(self):
        return f'{self.ano}, {self.mes}, {self.data_entrada}, ' \
               f'{self.soma_baixa_ind}, {self.soma_baixa_res}, {self.soma_baixa_salv},' \
               f'{self.dif_soma_baixa_ind_res_salv}'

    pass


class MovimentacaoRecuperadosNovo(models.Model):
    class Meta:
        db_table = 'movimentacaorecuperadosnovo'

    codigo = models.AutoField(primary_key=True)
    cod_cia = models.CharField(null=False, max_length=255)
    num_sin = models.CharField(null=False, max_length=255)
    cod_ramo = models.CharField(null=False, max_length=255)
    dt_base = models.CharField(null=False, max_length=255)
    num_apol = models.CharField(null=False, max_length=255)
    baixa_ind = models.FloatField(null=False, max_length=255, default= 0)
    baixa_salv = models.FloatField(null=False, max_length=255,default= 0)
    baixa_res = models.FloatField(null=False, max_length=255 , default= 0)

    relatorio = models.ForeignKey(RelatorioRecuperadosNovo, related_name='movimentacoes',
                                  on_delete=models.CASCADE,
                                  null=True)

    def __str__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.num_sin}' \
               f'{self.cod_ramo}, {self.dt_base}, {self.num_apol}, {self.baixa_ind}, {self.baixa_salv}, {self.baixa_res}'

    def __repr__(self):
        return f'{self.codigo}, {self.cod_cia}, {self.num_sin}' \
               f'{self.cod_ramo}, {self.dt_base}, {self.num_apol},{self.baixa_ind}, {self.baixa_salv}, {self.baixa_res}'

    pass



class BaseCalculoPisCofins(models.Model):
    class Meta:
        db_table = 'basecalculopiscofins'

    codigo = models.AutoField(primary_key=True)
    soma_receita_balancete = models.FloatField(null=False)
    data_entrada = models.DateTimeField(auto_now_add=True)
    ano = models.IntegerField(null=False, default=0)
    mes = models.IntegerField(null=False, default=0)

    pis_retido = models.FloatField(null=False, default=0)
    compensacao_pis = models.FloatField(null=False, default=0)
    pis_recolher = models.FloatField(null=False)
    pis_check = models.FloatField(null=False)
    pis_darf = models.FloatField(null=False)
    pis_dif_darf_recolher = models.FloatField(null=False)
    pis_contabilizar = models.FloatField(null=False)
    pis = models.FloatField(null=False)

    cofins_retido = models.FloatField(null=False, default=0)
    compensacao_cofins = models.FloatField(null=False, default=0)
    cofins_recolher = models.FloatField(null=False)
    cofins_check = models.FloatField(null=False)
    cofins_darf = models.FloatField(null=False)
    cofins_dif_darf_recolher = models.FloatField(null=False)
    cofins_contabilizar = models.FloatField(null=False)
    cofins = models.FloatField(null=False)

    def __str__(self):
        return f'{self.codigo}, {self.soma_receita_balancete}, {self.pis_retido}, {self.compensacao_pis},' \
               f'{self.pis_recolher}, {self.pis_check}, {self.pis_recolher}, {self.pis_darf}, {self.pis_dif_darf_recolher},' \
               f'{self.pis_contabilizar}, {self.pis} '\
               f'{self.cofins_retido}, {self.compensacao_cofins}, ' \
               f'{self.cofins_recolher}, {self.pis_check}, {self.cofins_recolher}, {self.cofins_darf}, {self.cofins_dif_darf_recolher}, ' \
               f'{self.cofins_contabilizar}, {self.cofins}, {self.ano}, {self.mes}'

    def __repr__(self):
        return f'{self.codigo}, {self.soma_receita_balancete}, {self.pis_retido}, {self.compensacao_pis},' \
               f'{self.pis_recolher}, {self.pis_check}, {self.pis_recolher}, {self.pis_darf}, {self.pis_dif_darf_recolher},' \
               f'{self.pis_contabilizar}, {self.pis} '\
               f'{self.cofins_retido}, {self.compensacao_cofins}, ' \
               f'{self.cofins_recolher}, {self.pis_check}, {self.cofins_recolher}, {self.cofins_darf}, {self.cofins_dif_darf_recolher}, ' \
               f'{self.cofins_contabilizar}, {self.cofins}, {self.ano}, {self.mes}'


    pass

