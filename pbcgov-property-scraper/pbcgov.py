# -*- coding: utf-8 -*-
import csv     
import requests
from bs4 import BeautifulSoup 
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from datetime import datetime

csv.register_dialect('myDialect1',
      quoting=csv.QUOTE_ALL,
      skipinitialspace=True)
file = open('11_20_2019 PB Tax Deed Auction List__scraped.csv', 'a')
writer = csv.writer(file, dialect='myDialect1')
writer.writerow(['Location', 'Location Street', 'Location Municipality', 'Owner', 'Mailing Address', 'Mailing Street', 'Mailing City', 'Mailing State', 'Mailing Zipcode', 'SaleDate', 'SalePrice','SaleType', 'parcel control number'])

address_list = [
	"00374123010000700",
	"00374123010000880",
	"00374133010010230",
	"00404324000005370",
	"00414309000001880",
	"00414310000001090",
	"00414435010000430",
	"00424313121150041",
	"00424323170092110",
	"00424329230450020",
	"00424411110080060",
	"00424414360020030",
	"00424422070022050",
	"00424424000007520",
	"00424424100991246",
	"00424424100991247",
	"00424513060530070",
	"00424515190081010",
	"00424611040000100",
	"00424622090115130",
	"00424630030001300",
	"00424706040030920",
	"00424708050135150",
	"00424715100023066",
	"00424715100036051",
	"00424726148512060",
	"00424730120064190",
	"00424708160020480",
	"00424731030031502",
	"00434417020120020",
	"06424703040000170",
	"06434704120000040",
	"04374342030070030",
	"06434719226360210",
	"08434507010010062",
	"08434516130021080",
	"04374331010300520",
	"12424613100610010",
	"08434522030020100",
	"12434616010590042",
	"12434617020050270",
	"12424613020000360",
	"30424112190351050",
	"38434422050000080",
	"50434322180016080",
	"52424215030002960",
	"48374217060000030",
	"48374218130000080",
	"48374218180000131",
	"48374218180000431",
	"48374218180000760",
	"48374218180700010",
	"48374218210000120",
	"48374218240000070",
	"48374219010001660",
	"48374219020001440",
	"48374220010090120",
	"48374220010100030",
	"50434322010020051",
	"48374208010040110",
	"48374218120001610",
	"48374218180000432",
	"38434421150760250",
	"38434421150820010",
	"60434032040003010",
	"48374218180700040",
	"68434209210001010",
	"68434221070002150",
	"38434427010260040",
	"38434427010260051",
	"38434427010260052",
	"72414314020140040",
	"72414323080000432",
	"72414326020050030",
	"56434228080050030",
	"56434229010000470",
	"56434229010000510",
	"56434229010250271",
	"56434229020190220",
	"56434229020190380",
	"56434229020210030",
	"56434229020210220",
	"56434229030080500",
	"56434229030150100",
	"56434229030150490",
	"73414408010450020",
	"56434229050060190",
	"56434229090020010",
	"56434229090020350",
	"56434229090020430",
	"56434229090030410",
	"56434229130070100",
	"73414417010860070",
	"56434230170010010",
	"48374218060030010",
	"48374218180000521",
	"48374218200020200",
	"56434232010250140",
	"56434232010390170",
	"74424312270073010",
	"74424312270172050",
	"56434233040020060",
	"70434418120000280",
	"74434315420066040",
	"74434319200021024",
	"74434317090009010",
	"74434318060014070",
	"74434318060023030",
	"74434320080011010",
	"74434322350010020",
	"74434328340001709",
	"74434333340040050",
	"74434333410030520",
	"74434403010004370",
	"56434232010210110",
	"56434232010380110",
	"58364414120000050"
]
session = requests.Session()

session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
	'Cookie': '_ga=GA1.2.990083083.1567017963; _gid=GA1.2.953115123.1567017963; BIGipServer~external~www.pbcgov.com_papa=rd102o00000000000000000000ffff978433b0o80; ASP.NET_SessionId=oluqmbqiyhhts22tefyfix4e; _gat_gtag_UA_117168590_1=1; _gat_gtag_UA_70407948_1=1'
})
session = requests.Session()

for address in address_list:
	url = 'https://pbcgov.org/papa/Asps/GeneralAdvSrch/NewSearchResults.aspx?srchType=MASTER&proptype=RE&srchVal={}&srchPCN='
	# 1009%20BIG%20TORCH%20ST
	r = session.get(url.format(address.replace(' ', '%20')))
	soup = BeautifulSoup(r.text, features="html.parser")
	# f = open('1.html', 'a')
	# f.write(r.text)
	# f.close()
	# print(soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[0])
	if soup.find('div', {'id': 'ownerInformationDiv'}):
		owner = soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[0].findAll('td', class_='TDValueLeft')[0].text
		mailing = (soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[1].findAll('td', class_='TDValueLeft')[0].text + soup.find('div', {'id': 'ownerInformationDiv'}).find('table').findAll('table')[1].findAll('td', class_='TDValueLeft')[2].text).strip().replace('\n\n', ',')
		mstreet = mailing.split(',')[0]
		mcity = ''
		mzipcode = ''
		mstate = ''
		if len(mailing.split(',')) >=2:
			scount = len(mailing.split(',')[1].split(' '))
			mcity = mailing.split(',')[1].replace(mailing.split(',')[1].split(' ')[scount - 3] + ' ' + mailing.split(',')[1].split(' ')[scount - 2] + ' ' + mailing.split(',')[1].split(' ')[scount - 1], '').strip()
			mzipcode = mailing.split(',')[1].split(' ')[scount - 2] + ' ' + mailing.split(',')[1].split(' ')[scount - 1].strip()
			mstate =  mailing.split(',')[1].split(' ')[scount - 3]
			# if mailing.split(',')[1].split('FL')[0]:
			# 	mcity = mailing.split(',')[1].split('FL')[0].strip()
			# if len(mailing.split(',')[1].split('FL')) >= 2:
			# 	mzipcode = mailing.split(',')[1].split('FL')[1].strip()
			# else:
			# 	if mailing.split(',')[1].split('NY')[0]:
			# 		mstate = 'NY'
			# 		mcity = mailing.split(',')[1].split('NY')[0].strip()
			# 	if len(mailing.split(',')[1].split('NY')) >= 2:
			# 		mstate = ''
			# 		mzipcode = mailing.split(',')[1].split('NY')[1].strip()

		location = (soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[0].text + ',' + soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[1].text).strip().replace('\n', '')

		lstreet = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[0].text.strip().replace('\n', '')
		lmunicipality = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[1].text.strip().replace('\n', '')
		pcn = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[2].text.strip()
		saledate = ''
		saleprice = ''
		saletype = ''
		if soup.find('table', {'id': 'MainContent_tblSalesInfo'}):
			saleinfo = soup.find('table', {'id': 'MainContent_tblSalesInfo'}).findAll('tr', class_='gridrow')[0]
			saledate = saleinfo.findAll('td')[0].text
			saleprice = saleinfo.findAll('td')[1].text
			saletype = saleinfo.findAll('td')[3].text.strip()
		lastsaledate = soup.find('div', {'id': 'propertyDetailDiv'}).findAll('td', class_='TDValueLeft')[5].text.strip()
		print(location, lstreet, lmunicipality, owner, mailing, mstreet, mcity, mstate, mzipcode, saledate, saleprice, saletype, pcn)
		writer.writerow([location, lstreet, lmunicipality, owner, mailing, mstreet, mcity, mstate, mzipcode, saledate, saleprice, saletype, pcn])

# print(r.text)