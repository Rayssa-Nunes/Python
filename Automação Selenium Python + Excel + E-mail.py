from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook
import win32com.client as win32
import re
import os
from time import sleep


class Scrappy:
    def __init__(self):
        self.navegador = webdriver.Chrome()
        self.navegador.get('https://telefonesimportados.netlify.app/index.html')

        self.lista_celulares = []
        self.num_pagina = 1
        self.iniciar()

    def iniciar(self):
        self.obter_email_usuario()
        self.coletar_dados_site(self.lista_celulares, self.num_pagina)
        self.criar_planilha()
        self.enviar_email()

    def obter_email_usuario(self):

        self.email = input('Digite seu e-mail (outlook ou hotmail) para receber o relatório de valores dos celulares: ').lower()
        self.email_valido = re.search(r'(.+)@(.+)\.(.+)', self.email)
        if 'outlook' in self.email or 'hotmail' in self.email:
            if self.email_valido:
                print('\033[32mE-mail válido!\033[m')
                sleep(2)
        else:
            print('\033[31mPor favor, informe um E-mail válido!\033[m')
            self.obter_email_usuario()

    def coletar_dados_site(self, lista_celulares, num_pagina):
        print(f'\033[32mLendo Página {self.num_pagina}\033[m')
        self.celulares = self.navegador.find_elements(By.CLASS_NAME, 'single-shop-product')

        for i in self.celulares:
            self.produto = i.find_element(By.TAG_NAME, 'h2').text
            self.preco = i.find_element(By.TAG_NAME, 'ins').text
            self.lista_celulares.append([self.produto, self.preco])

        self.ul = self.navegador.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/nav/ul')
        self.lista_ul = self.ul.text[:].split()
        if '»' in self.lista_ul:
            self.navegador.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div/nav/ul/li[7]/a').click()
            self.num_pagina += 1
            self.coletar_dados_site(lista_celulares, num_pagina)
        else:
            self.navegador.quit()
            return

    def criar_planilha(self):

        self.book = Workbook()
        self.book.create_sheet('celulares')
        self.celulares_page = self.book['celulares']
        self.celulares_page.append(['Produto', 'Preco'])
        for self.dados in self.lista_celulares:
            self.celulares_page.append(self.dados)

        self.book.save('Relatorio_celulares.xlsx')
        print('Planilha criada!')

    def enviar_email(self):
        print('Enviando o relatório para o e-mail informado...')
        self.caminho = os.getcwd()
        self.outlook = win32.Dispatch('outlook.application')
        self.mail = self.outlook.CreateItem(0)
        self.mail.To = self.email
        self.mail.Subject = 'Relatório de preços de celulares'
        self.mail.Body = '''
        Segue em anexo o Relatório de preços dos celulares, conforme solicitado.
        Qualquer dúvida estou à disposição.
        Att.,
        '''
        self.attachment = self.caminho + r'\Relatorio_celulares.xlsx'
        self.mail.Attachments.Add(self.attachment)
        self.mail.Send()
        print('E-mail enviado com Sucesso!')


start = Scrappy()
