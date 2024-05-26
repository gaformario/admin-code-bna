from selenium import webdriver
url1='https://www.imdb.com/chart/moviemeter/?ref_=tt_ov_pop'
url2='https://www.imdb.com/chart/tvmeter/?ref_=tt_ov_pop'
popular='mysql+mysqlconnector://root:root@localhost/popular'
 
def criarDriver():
    return  webdriver.Edge()