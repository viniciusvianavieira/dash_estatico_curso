# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.options import Options


class wb_brazil_journal:

    def __init__(self):

        pass

    def pegando_noticias(self):

        options = Options()
        options.headless = True

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)

        url = 'https://braziljournal.com/categoria/economia/'

        driver.get(url)

        todas_noticias = driver.find_element("xpath", '/html') 

        html_not = todas_noticias.get_attribute('outerHTML')

        driver.quit()

        soup = BeautifulSoup(html_not, 'html.parser')

        caixas_noticias = soup.find_all("figcaption", class_ = 'boxarticle-infos') 

        df_noticias = pd.DataFrame(columns=['manchete', 'subtopico', 'link'], index=[0, 1, 2, 3])

        df_noticias

        for i, noticia in enumerate(caixas_noticias):

            subtobico = noticia.find("p", class_ = 'boxarticle-infos-tag').text
            manchete = noticia.find("h2", class_ = 'boxarticle-infos-title').text
            link = noticia.find("h2", class_ = 'boxarticle-infos-title').a['href']

            df_noticias.loc[i, 'subtopico'] = subtobico
            df_noticias.loc[i, 'manchete'] = manchete
            df_noticias.loc[i, 'link'] = link

            if i == 3:

                break

        return df_noticias
    

if __name__ == "__main__":

    ws_bj = wb_brazil_journal()

    noticias = ws_bj.pegando_noticias()

    print(noticias.to_csv("ws.csv"))
