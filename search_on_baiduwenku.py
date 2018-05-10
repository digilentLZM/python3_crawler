from selenium import webdriver
from bs4 import BeautifulSoup
import bs4
import csv #保存为csv文件
import re #正则表达式
import time
t1 = time.time()
def get_urls(s,url = "https://wenku.baidu.com"):
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('User-Agent="Mozilla/5.0"')#设置headers
		options.add_argument('--headless')#Chrome无头模式
		driver = webdriver.Chrome(chrome_options = options)
		driver.get(url)
		kw = driver.find_element_by_id("kw")
		kw.send_keys(s)
		sb = driver.find_element_by_id("sb")
		sb.click()
		#html = driver.page_source
		# soup = BeautifulSoup(html,"html.parser")
		# urls = ''
		# urls = soup.find("a",attrs={'class':'last'}).attrs['href']
		# print(urls,"get urls succeed!")
		urls = driver.find_element_by_class_name("last").get_attribute("href")
		return urls
		
	except:
		print("get urls failed!")
		return ""

def get_html(url):
	try:
		options = webdriver.ChromeOptions()
		options.add_argument('User-Agent="Mozilla/5.0"')#设置headers
		options.add_argument('--headless')#Chrome无头模式
		driver = webdriver.Chrome(chrome_options = options)
		driver.get(url)
		#driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
		#driver.execute_script('alert("To Bottom")')
		print("获取第",int(driver.current_url.split('=')[-1])//10 + 1,"页中......")
		html = driver.page_source
		driver.quit()
		return html
	except:
		return ""


def fill_in_list(html,u):
	soup = BeautifulSoup(html,"html.parser")
	for dl in soup.find_all("dl"):
		try:
			x = []
			dt = dl.find("dt",attrs= {'class':'logFirstClickTime mb6 clearfix'})#bug
			span_title = dt.find("span").attrs["title"]
			a  = dt.find("a")
			x = [span_title,a.attrs["title"],a.attrs["href"]]
			span = dt.find("p",attrs = {'class':'fr'}).find_all("span")
			if len(span) > 1:
				x.append(span[1].string.replace('\n',''))
			else:
				x.append(span[0].string.replace('\n',''))
			dd = dl.find("dd",attrs = {'class':'clearfix'})
			f = dd.find("div",attrs = {'class':'detail lh21'})
			for em in f.children:
				if isinstance(em,bs4.element.NavigableString):
					x.append(em.replace('\n',''))
			x.append(f.find("a").string.replace('\n',''))
			u.append(x)
		except:
			pass

def create_a_file(s):
	with open("E://文档//" + s + ".csv","w",newline='')as f:
		writer = csv.writer(f)
		writer.writerow(['类型','文档名称','链接','评分','时间','页数','下载量','下载券'])
	f.close()

def fill_into_afile(L,s):
	with open("E://文档//" + s + ".csv","a",newline='')as f:
		writer = csv.writer(f)
		for li in L:
			writer.writerow(li[0:8])
		#writer.writerows(L)
	f.close()

def main():
	s = ''
	while not s:
		s = input("input what you want to search:")
	create_a_file(s)
	num = -1
	try:
		last_url = get_urls(s)
		num = int(last_url.split("=")[-1]) + 10
		u = re.compile(".+=")
		urls = u.search(last_url)
		url = urls.group(0)
		print(last_url)
		print("总共找到", (num + 1)//10, "页有关文档！")
	except:
		print("获取url失败！")

	for i in range(0,num,10):
		try:
			url_s = url + str(i)
			html = get_html(url_s)
			t = []
			fill_in_list(html,t)
			fill_into_afile(t,s)
		except:
			pass
main()
t2 = time.time()
print("totally cost %d"%((t2-t1)/60))
		
