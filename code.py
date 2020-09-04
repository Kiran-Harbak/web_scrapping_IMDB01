class IMDB01:
	def beautifulSoup(self):
		import requests
		from bs4 import BeautifulSoup 
		r=requests.get('https://www.imdb.com/search/title/?release_date=2017&sort=num_votes,desc&page=1')
		soup= BeautifulSoup(r.content,'html.parser')
		ll=soup.find(class_="lister-list")
		self.mns=[tag.find('a', recursive=False).get_text() for tag in ll.find_all(class_='lister-item-header')]
		
		self.rtgs=[tag.get_text() for tag in ll.select('.ratings-bar strong')]

		self.meta=[ int(tag.find(class_="metascore").get_text()) if tag.find(class_="inline-block ratings-metascore") else 0 for tag in ll.find_all(class_="ratings-bar") ]


		self.vote=[i for i in [tag.get_text() for tag in ll.select('.sort-num_votes-visible span')] if 'Votes:' not in i and '|' not in i and 'Gross:' not in i and '$' not in i]#'621,361', '557,827', etc
		# votes=[tag.get_text() for tag in ll.select('.sort-num_votes-visible span')]
		# self.vote=[i for i in votes if 'Votes:' not in i and '|' not in i and 'Gross:' not in i and '$' not in i]#Votes-'621,361', etc
		
		self.et=[ tag.find(class_="sort-num_votes-visible").get_text() if '$' in tag.find(class_="sort-num_votes-visible").get_text() else '$0M' for tag in ll.find_all(class_="lister-item-content") ]
		self.lst= [i.split('\n') for i in self.et]
		self.lst1=list()
		for i in self.lst:
			self.lst1.extend(i)
		self.gross=[ i for i in self.lst1 if 'M' in i and '$' in i]#$2.3M-41


	
	def selenium(self):
		from selenium import webdriver
		driver=webdriver.Chrome(r"C:/Users/Dell/Desktop/PythonBySagarSir/Web Scrapping/IMDB01/chromedriver.exe") 
		driver.maximize_window()
		driver.delete_all_cookies()  
		driver.get("https://www.imdb.com/search/title/?release_date=2017&sort=num_votes,desc&page=1")

		for i in range(0,7104):#From 0-5
			

			elems=driver.find_elements_by_xpath("//div[@class='nav']//a[@class='lister-page-next next-page'][contains(text(),'Next »')]")
			
			for ele in elems:
				self.src=ele.get_attribute("href")
				driver.get(ele.get_attribute("href"))

				obj.beautifulSoupExtend()

		driver.close()  
		driver.quit()

	def beautifulSoupExtend(self):
		import requests
		from bs4 import BeautifulSoup 
		r=requests.get(self.src)
		soup= BeautifulSoup(r.content,'html.parser')
			
		ll=soup.find(class_="lister-list")
		for tag in ll.find_all(class_='lister-item-header'):
			self.mns.append(tag.find('a', recursive=False).get_text())

		for tag in ll.select('.ratings-bar strong'):
			self.rtgs.append(tag.get_text())
		
		for tag in ll.find_all(class_="ratings-bar"):
			if tag.find(class_="inline-block ratings-metascore"):

				self.meta.append(int(tag.find(class_="metascore").get_text()))
			else:
				self.meta.append(0)

		for i in [tag.get_text() for tag in ll.select('.sort-num_votes-visible span')]:
			if 'Votes:' not in i and '|' not in i and 'Gross:' not in i and '$' not in i:
				self.vote.append(i)
		
		self.et=[ tag.find(class_="sort-num_votes-visible").get_text() if '$' in tag.find(class_="sort-num_votes-visible").get_text() else '$0M' for tag in ll.find_all(class_="lister-item-content") ]
		self.lst= [i.split('\n') for i in self.et]
		self.lst1=list()
		for i in self.lst:
			self.lst1.extend(i)
	 
		for i in self.lst1:
			if 'M' in i and '$' in i:
				self.gross.append(i)

	def printFun(self):
		print(f'Movies:{self.mns} LENGTH:{len(self.mns)}')
		print(f'Ratings:{self.rtgs} LENGTH:{len(self.rtgs)}')
		print(f'Meta-data:{self.meta} LENGTH:{len(self.meta)}')
		print(f'Votes:{self.vote} LENGTH:{len(self.vote)}')
		print(f'Gross:{self.gross} LENGTH:{len(self.gross)}')
		
	def csvFile(self):
		import pandas as pd
		d = {'Movies Name':self.mns, 'Ratings':self.rtgs, 'Meta-Score':self.meta, 'Votes':self.vote,'Gross':self.gross }
		df = pd.DataFrame(d)
		df.to_csv('C:/Users/Dell/Desktop/PythonBySagarSir/Web Scrapping/IMDB01/IMDB01.csv')
		df.head()
		print('-----------------CSV FILE IS READY!--------------------')

	def databaseSqlite3(self):
		import sqlite3
		con = sqlite3.connect('C:/Users/Dell/Desktop/PythonBySagarSir/Web Scrapping/IMDB01/IMDB01.db')
		c=con.cursor()
		c.execute('CREATE TABLE IMDB(Movies_Name text, Ratings text, Meta_Score text, Votes text, Gross text )')
		for i in range(50):
		    c.execute('INSERT INTO IMDB(Movies_Name, Ratings, Meta_Score, Votes, Gross ) values(?,?,?,?,?)',(self.mns[i], self.rtgs[i], self.meta[i], self.vote[i], self.gross[i] ))
		con.commit()
		print('-----------------DB FILE IS READY!--------------------')

obj=IMDB01()
obj.beautifulSoup()
obj.selenium()
obj.printFun()
obj.csvFile()
obj.databaseSqlite3()

