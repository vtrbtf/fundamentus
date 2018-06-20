#!/usr/bin/env python3

import re
import urllib.request
import urllib.parse
import http.cookiejar

from lxml.html import fragment_fromstring
from collections import OrderedDict

def get_data(filters = {}, *args, **kwargs):
    url = 'http://www.fundamentus.com.br/resultado.php'
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'),
                         ('Accept', 'text/html, text/plain, text/css, text/sgml, */*;q=0.01')]

    # Aqui estão os parâmetros de busca das ações
    # Estão em branco para que retorne todas as disponíveis
    data = {'pl_min':'',
            'pl_max':'',
            'pvp_min':'',
            'pvp_max' :'',
            'psr_min':'',
            'psr_max':'',
            'divy_min':'',
            'divy_max':'',
            'pativos_min':'',
            'pativos_max':'',
            'pcapgiro_min':'',
            'pcapgiro_max':'',
            'pebit_min':'',
            'pebit_max':'',
            'fgrah_min':'',
            'fgrah_max':'',
            'firma_ebit_min':'',
            'firma_ebit_max':'',
            'margemebit_min':'',
            'margemebit_max':'',
            'margemliq_min':'',
            'margemliq_max':'',
            'liqcorr_min':'',
            'liqcorr_max':'',
            'roic_min':'',
            'roic_max':'',
            'roe_min':'',
            'roe_max':'',
            'liq_min':'100000',
            'liq_max':'',
            'patrim_min':'',
            'patrim_max':'',
            'divbruta_min':'',
            'divbruta_max':'',
            'tx_cresc_rec_min':'',
            'tx_cresc_rec_max':'',
            'setor':'',
            'negociada':'ON',
            'ordem':'1',
            'x':'28',
            'y':'16'}

    data.update(filters)

    with opener.open(url, urllib.parse.urlencode(data).encode('UTF-8')) as link:
        content = link.read().decode('ISO-8859-1')

    pattern = re.compile('<table id="resultado".*</table>', re.DOTALL)
    reg = re.findall(pattern, content)[0]
    page = fragment_fromstring(reg)
    lista = OrderedDict()

    for rows in page.xpath('tbody')[0].findall("tr"):
        lista.update({rows.getchildren()[0][0].getchildren()[0].text: {'cotacao': rows.getchildren()[1].text,
                                                                       'P/L': rows.getchildren()[2].text,
                                                                       'P/VP': rows.getchildren()[3].text,
                                                                       'PSR': rows.getchildren()[4].text,
                                                                       'DY': rows.getchildren()[5].text,
                                                                       'P/Ativo': rows.getchildren()[6].text,
                                                                       'P/Cap.Giro': rows.getchildren()[7].text,
                                                                       'P/EBIT': rows.getchildren()[8].text,
                                                                       'P/Ativ.Circ.Liq.': rows.getchildren()[9].text,
                                                                       'EV/EBIT': rows.getchildren()[10].text,
                                                                       'EBITDA': rows.getchildren()[11].text,
                                                                       'Mrg.Liq.': rows.getchildren()[12].text,
                                                                       'Liq.Corr.': rows.getchildren()[13].text,
                                                                       'ROIC': rows.getchildren()[14].text,
                                                                       'ROE': rows.getchildren()[15].text,
                                                                       'Liq.2m.': rows.getchildren()[16].text,
                                                                       'Pat.Liq': rows.getchildren()[17].text,
                                                                       'Div.Brut/Pat.': rows.getchildren()[18].text,
                                                                       'Cresc.5a': rows.getchildren()[19].text}})

    return lista

if __name__ == '__main__':
    from waitingbar import WaitingBar

    THE_BAR = WaitingBar('[*] Downloading...')
    pl_index = get_data({'pl_min': '1', 'pl_max': '30'})
    roe_index = get_data({'roe_min': '0.06'})
    pvp_index = get_data({'pvp_min': '0.00', 'pvp_max': '2'})
    liq_index = get_data({'liqcorr_min': '1'})
    mebit_index = get_data({'margemebit_min': '0.04'})

    THE_BAR.stop()

    print("")
    print("PL")
    print(len(pl_index))
    print("")
    print("ROE")
    print(len(roe_index))
    print("")
    print("PVP")
    print(len(pvp_index))
    print("")
    print("LIQ")
    print(len(liq_index))
    print("")
    print("M ebit")
    print(len(mebit_index))
    print("")
    print("------------------------------------------")

    pl_index = OrderedDict(sorted(pl_index.items(), key=lambda x: x[1]["P/L"]))
    roe_index = OrderedDict(sorted(roe_index.items(), key=lambda x: x[1]["ROE"], reverse=True))
    pvp_index = OrderedDict(sorted(pvp_index.items(), key=lambda x: x[1]["P/VP"]))
    liq_index = OrderedDict(sorted(liq_index.items(), key=lambda x: x[1]["Liq.Corr."], reverse=True))
    mebit_index = OrderedDict(sorted(mebit_index.items(), key=lambda x: x[1]["EBITDA"], reverse=True))

    #print_report(pvp_index)
    all_keys = list(pl_index.keys())
    all_keys.extend(list(roe_index.keys()))
    all_keys.extend(list(pvp_index.keys()))
    all_keys.extend(list(liq_index.keys()))
    all_keys.extend(list(mebit_index.keys()))

    common = {}
    for k in all_keys:
        if k in pl_index.keys() and k in roe_index.keys() and k in pvp_index.keys() and k in liq_index.keys() and k in mebit_index.keys():
            common[k] = list(pl_index.keys()).index(k) + list(roe_index.keys()).index(k) + list(pvp_index.keys()).index(k) + list(liq_index.keys()).index(k) + list(mebit_index.keys()).index(k)

    items = sorted(common.items(), key=lambda x: x[1])






    print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<14} {14:<7}'.format('Papel',
                                                                                                                                          'Cotação',
                                                                                                                                          'P/L',
                                                                                                                                          'P/VP',
                                                                                                                                          'PSR',
                                                                                                                                          'DY',
                                                                                                                                          'P/EBIT',
                                                                                                                                          'EV/EBIT',
                                                                                                                                          'EBITDA',
                                                                                                                                          'Mrg.Liq.',
                                                                                                                                          'Liq.Corr.',
                                                                                                                                          'ROIC',
                                                                                                                                          'ROE',
                                                                                                                                          'Div.Brut/Pat.',
                                                                                                                                          'Cresc.5a'))
    print('-'*154)


    for i in items[:25]:
        k = i[0]
        v = pl_index[k]
        print('{0:<7} {1:<7} {2:<10} {3:<7} {4:<10} {5:<7} {6:<10} {7:<10} {8:<10} {9:<11} {10:<11} {11:<7} {12:<11} {13:<14} {14:<7}'.format(k,
                                                                                                                                              v['cotacao'],
                                                                                                                                              v['P/L'],
                                                                                                                                              v['P/VP'],
                                                                                                                                              v['PSR'],
                                                                                                                                              v['DY'],
                                                                                                                                              v['P/EBIT'],
                                                                                                                                              v['EV/EBIT'],
                                                                                                                                              v['EBITDA'],
                                                                                                                                              v['Mrg.Liq.'],
                                                                                                                                              v['Liq.Corr.'],
                                                                                                                                              v['ROIC'],
                                                                                                                                              v['ROE'],
                                                                                                                                              v['Div.Brut/Pat.'],
                                                                                                                                              v['Cresc.5a']))



