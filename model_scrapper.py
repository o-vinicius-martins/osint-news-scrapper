import requests
from bs4 import BeautifulSoup


class Scrapper:
    
    def __init__(self, site):
        self.site = site
        self.news = {}
                    
    def print_all(self):

        for k, v, in self.news.items():
            print(f'-> {k} - {v}')
        print(f'{len(self.news)} notícias exibidas.')

    def update_news(self):

# === GLOBO ===
        if self.site == 'globo':
            url = 'https://www.globo.com/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \\(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}
            page = requests.get(url=url, headers=browsers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias = soup.find_all('a')
            tag_class1 = 'post__title'
            tag_class2 = 'post-multicontent__link--title__text'

            news_dict_globo = {}

            for noticia in noticias:
                if noticia.h2 != None:
                    if tag_class1 in noticia.h2.get('class') or tag_class2 in noticia.h2.get('class'):
                        news_dict_globo[noticia.h2.text] = noticia.get('href')
            
            self.news = news_dict_globo

# === R7 ===
        elif self.site == 'r7':
            url = 'https://www.r7.com/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \\(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

            page = requests.get(url=url, headers=browsers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias = soup.find_all('div')
            news_dict_r7 = {}
            data_tb_title = 'true'

            for noticia in noticias:
                try:
                    if data_tb_title in noticia.h3.get('data-tb-title'):
                        if noticia.span and noticia.span != '':
                            news_dict_r7[f'{noticia.span.text}'] = noticia.a.get('href')
                        elif noticia.a.text != '':
                            news_dict_r7[f'{noticia.a.get('title')}'] = noticia.a.get('href')
                except:
                    pass
            
            itens_a_remover = [chave for chave in news_dict_r7.keys() if chave == '' or chave == ' ']

            for item in itens_a_remover:
                del news_dict_r7[item]

            self.news = news_dict_r7

# === VEJA ===
        elif self.site == 'veja':
            url = 'https://veja.abril.com.br/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \\(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

            page = requests.get(url=url, headers=browsers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias = soup.find_all('a')
            tag_class3 = 'title'
            tag_class4 = 'related-article'

            news_dict_veja = {}

            for noticia in noticias:

                if noticia.h2 is not None:
                    if noticia.h2.get('class') and tag_class3 in noticia.h2.get('class'):
                        news_dict_veja[noticia.h2.text.replace('\n', '')] = noticia.get('href')

                elif noticia.h3 is not None:
                    if noticia.h3.get('class') and tag_class3 in noticia.h3.get('class'):
                        news_dict_veja[noticia.h3.text.replace('\n', '')] = noticia.get('href')

                elif noticia.p is not None:
                    if noticia.get('class') and tag_class4 in noticia.get('class'):
                        news_dict_veja[noticia.p.text.replace('\n', '')] = noticia.get('href')

            self.news = news_dict_veja

# === TERRA DO MANDU ===
        elif self.site == 'terra do mandu':
            url = 'https://terradomandu.com.br/'
            browsers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \\(KHTML, like Gecko) Chrome / 86.0.4240.198Safari / 537.36"}

            page = requests.get(url=url, headers=browsers)

            resposta = page.text
            soup = BeautifulSoup(resposta, 'html.parser')

            noticias_links = soup.find_all('a')
            noticias_divs = soup.find_all('div')

            tag_manchete1 = 'noticia_destaque_1' # a
            tag_manchete2 = 'noticia_destaque_2' # a
            tag_noticia_grande = 'boxNoticiaGrande' # div
            tag_noticia_carrossel = 'noticiasSwipe' # a

            news_dict_terra_do_mandu = {}

            for noticia in noticias_links:
                if noticia.h3 is not None:
                    if tag_manchete1 in noticia.get('class') or tag_manchete2 in noticia.get('class'):
                        news_dict_terra_do_mandu[noticia.h3.text.replace('\n', '')] = noticia.get('href')

                    elif tag_noticia_carrossel in noticia.get('class'):
                        news_dict_terra_do_mandu[noticia.h3.text.replace('\n', '')] = noticia.get('href')

            for noticia in noticias_divs:
                if noticia.h3 is not None:
                    if tag_noticia_grande in noticia.get('class'):
                        news_dict_terra_do_mandu[noticia.h3.text.replace('\n', '')] = noticia.h3.a.get('href')

            self.news = news_dict_terra_do_mandu


