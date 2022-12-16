import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
# import importlib
import re


class Scrape:

	# def getAlbumCoverURL(artist_name, song_name):
	# 	artist_name = artist_name.replace('.', '').replace(' ','').replace("'", "").lower()
	# 	song_name = song_name.replace(' ','-').replace("'", "").lower()

	# 	track_slug = '-'.join([artist_name, song_name])
	# 	client_access_token = '3u-fiiKZSn0n4jUO-cuxNamghC92pdYZQrnbzzb7AxuEMjnPcbJU71i5rytUhipZ'
	# 	base_url = 'https://api.genius.com'
	# 	path = 'search/'
	# 	request_uri = '/'.join([base_url, path])
	# 	# query = 'jcole-change'
	# 	params = {'q': track_slug}

	# 	token = 'Bearer {}'.format(client_access_token)
	# 	headers = {'Authorization' : token}

	# 	r = requests.get(request_uri, params=params, headers=headers)
	# 	json = r.json()

	# 	print(json)
	# 	album_img = json['response']['hits'][0]['result']['header_image_url']
	# 	return 

	def getAlbumCoverURL(artist_name, song_name):
		artist_name = artist_name.replace('.', '').replace(' ','-').replace("'", "").lower()
		song_name = song_name.replace(' ','-').replace("'", "").lower()

		track_slug = '-'.join([artist_name, song_name])
		base_url = 'https://genius.com/{}-lyrics'.format(track_slug)

		r = requests.get(base_url)
		soup = BeautifulSoup(r.text, 'html.parser')

		imgs = soup.select('img[class="cover_art-image"]')
		imgs = str(imgs)
		start_idx = imgs.find('src=')
		imgs = imgs[start_idx+5::]
		last_idx = imgs.find('"')
		imgs = imgs[:last_idx]

		return imgs

	# def getSongLyrics(artist_name, song_name):
	# 	artist_name = artist_name.replace('.', '').replace(' ','').replace("'", "").lower()
	# 	song_name, sep, tail = song_name.partition('(')
	# 	song_name = song_name.strip().replace(' ','').replace("'", "").replace(".", "").lower()
	# 	lyric_url = 'https://www.azlyrics.com/lyrics/{}/{}.html'.format(artist_name, song_name)
	# 	r = requests.get(lyric_url)

	# 	start_idx = r.text.find('that. -->')
	# 	lyrics = r.text[start_idx::]
	# 	last_idx = lyrics.find('</div>')
	# 	lyrics = lyrics[10:last_idx]
	# 	lyrics = lyrics.replace('<br>', '')
	# 	return lyrics
	# 	# soup = BeautifulSoup(r.text, 'html.parser')

	# 	# print(soup.prettify())

	def getSongLyrics(artist_name, song_name):
		artist_name = artist_name.replace('.', '').replace(' ','-').replace("'", "").lower()
		song_name = song_name.replace('(', '').replace(')', '').strip().replace(' ','-').replace("'", "").replace('#', '').replace('&amp;', 'and').replace(".", "").replace(',', '').replace('+', '').replace('?','').lower()

		song_name = song_name.split('-ft')[0].strip()
		song_name = re.sub('-+', '-', song_name)

		track_slug = '-'.join([artist_name, song_name])
		lyric_url = 'https://genius.com/{}-lyrics'.format(track_slug)

		# browser = webdriver.Chrome('D:/Program Files (x86)/Drivers/chromedriver.exe')
		# browser.get(lyric_url)
		# html = browser.page_source
		session = requests.Session()

		headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}

		r = requests.get(lyric_url, stream=None, allow_redirects=True, timeout=10)
		# print(lyric_url)

		soup = BeautifulSoup(r.text, 'html.parser')
		lyrics = soup.find(class_="lyrics")

		# print(lyrics)
		if lyrics is None:
			return "404"
		else:
			return lyrics.text

	def getTrackList(artist_name, album_name):

		artist_name = artist_name.replace('.', '').replace(' ','-').lower()
		album_name = album_name.replace('.',' ').strip().replace(' ', '-').lower()

		album_url = 'https://genius.com/albums/{}/{}'.format(artist_name, album_name)
		r = requests.get(album_url)

		soup = BeautifulSoup(r.text, 'html.parser')
		muddy_list = soup.select('h3[class="chart_row-content-title"]')

		tracks = []
		for ele in muddy_list:
			ele = str(ele)
			start_idx = ele.find('e">')
			last_idx = ele.find('<s')
			track = ele[start_idx+3:last_idx].strip()
			tracks.append(track)

		return tracks

	def createSlug(artist_name, song_name):
		artist_name = artist_name.replace('.', '').replace(' ','').replace("'", "").lower()
		song_name = song_name.replace('(', '').replace(')', '').strip().replace(' ','-').replace("'", "").replace('#', '').replace('&amp;', 'and').replace(".", "").replace(',', '').replace('+', '').replace('?','').lower()

		song_name = song_name.split('-ft')[0].strip()
		song_name = re.sub('-+', '-', song_name)

		track_slug = '-'.join([artist_name, song_name])

		return track_slug.strip('-')


# print(Scrape.getSongLyrics('Bob Dylan', "Rainy Day Women #12 & 35"))
