# utils.py
from django.db import transaction
from .models import *

def manter_limite_apuracoes_piscofins(apc, limite=5):
    """
    Mantém no máximo `limite` registros de ApuracaoPisCofins
    para o mesmo ano e mês. Remove o registro mais antigo
    quando ultrapassar o limite.
    """

    ano = apc.ano
    mes = apc.mes

    with transaction.atomic():
        qs = ApuracaoPisCofins.objects.filter(ano=ano, mes=mes)
        total = qs.count()

        if total >= limite:
            registro_mais_antigo = qs.order_by('data_entrada').first()
            registro_mais_antigo.delete()

        apc.save()



def manter_limite_apuracoes_apls(apsl, limite=5):
    """
    Mantém no máximo `limite` registros de ApuracaoPisCofins
    para o mesmo ano e mês. Remove o registro mais antigo
    quando ultrapassar o limite.
    """

    ano = apsl.ano
    mes = apsl.mes

    with transaction.atomic():
        qs = ApuracaoPSL.objects.filter(ano=ano, mes=mes)
        total = qs.count()

        if total >= limite:
            registro_mais_antigo = qs.order_by('data_cadastro').first()
            registro_mais_antigo.delete()

        apsl.save()
    pass



def manter_limite_apuracoes_apuracao_pis_cofins_apr(apc, limite=5):

    ano = apc.ano
    mes = apc.mes

    with transaction.atomic():
        qs = ApuracaoPisCofinsAPR.objects.filter(ano=ano, mes=mes)
        total = qs.count()

        if total >= limite:
            registro_mais_antigo = qs.order_by('data_entrada').first()
            registro_mais_antigo.delete()

        apc.save()
    pass

def vincular_contas_e_ramos_apc(apc, contas, ramos):
    """
    Garante a gravação das contas e ramos vinculados a um
    ApuracaoPisCofinsAPR já persistido.
    """
    with transaction.atomic():

        for conta in contas:
            conta.apuracao_piscofins_apr = apc

        for ramo in ramos:
            ramo.apuracao_piscofins_apr = apc

        if contas:
            ContaApuracaoPisCofinsAPR.objects.bulk_create(contas)

        if ramos:
            RamoAgrupadoPisCofinsAPR.objects.bulk_create(ramos)


def vincular_relatorios_agrupados_apuracao_pis_cofins_apr_1(apc):
    with transaction.atomic():
        if apc.relatorio_sinpag:
            for movimento in apc.movimentos_sinpag:
                movimento.apuracao_piscofins_apr = apc
            RamoAgrupadoPisCofinsRelatorioSinpag.objects.bulk_create(apc.movimentos_sinpag)

        if apc.relatorio_sinpagac:
            for movimento in apc.movimentos_sinpagac:
                movimento.apuracao_piscofins_apr = apc
            RamoAgrupadoPisCofinsRelatorioSinpagac.objects.bulk_create(apc.movimentos_sinpagac)

        if apc.relatorio_salvados_vendidos:
            for movimento in apc.movimentos_salvados_vendidos:
                movimento.apuracao_piscofins_apr = apc
            RamoAgrupadoPisCofinsRelatorioSalvadosVendidos.objects.bulk_create(apc.movimentos_salvados_vendidos)

        if apc.relatorio_recuperados:
            for movimento in apc.movimentos_recuperados:
                movimento.apuracao_piscofins_apr = apc
            RamoAgrupadoPisCofinsRelatorioRecuperados.objects.bulk_create(apc.movimentos_recuperados)

    pass


def vincular_relatorios_agrupados_apuracao_pis_cofins_apr(apc):
    """
    Vincula e persiste os movimentos de relatórios associados
    a uma ApuracaoPisCofinsAPR já existente.
    """
    with transaction.atomic():

        configuracoes = [
            (
                apc.relatorio_sinpag,
                apc.movimentos_sinpag,
                RamoAgrupadoPisCofinsRelatorioSinpag,
            ),
            (
                apc.relatorio_sinpagac,
                apc.movimentos_sinpagac,
                RamoAgrupadoPisCofinsRelatorioSinpagac,
            ),
            (
                apc.relatorio_salvados_vendidos,
                apc.movimentos_salvados_vendidos,
                RamoAgrupadoPisCofinsRelatorioSalvadosVendidos,
            ),
            (
                apc.relatorio_recuperados,
                apc.movimentos_recuperados,
                RamoAgrupadoPisCofinsRelatorioRecuperados,
            ),
        ]

        for ativo, movimentos, model in configuracoes:
            if not ativo or not movimentos:
                continue

            for movimento in movimentos:
                movimento.apuracao_piscofins_apr = apc

            model.objects.bulk_create(movimentos)
