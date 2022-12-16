import requests
from bs4 import BeautifulSoup
from lxml.html import fromstring
from itertools import cycle
import traceback

class Scrape:
	proxies = ""
	proxy_pool = ""

	def __init__(self):
		self.proxies = self.get_proxies()
		self.proxy_pool = cycle(self.proxies)

	def get_proxies(self):
	    url = 'https://free-proxy-list.net/'
	    response = requests.get(url)
	    parser = fromstring(response.text)
	    proxies = set()
	    for i in parser.xpath('//tbody/tr')[:10]:
	        if i.xpath('.//td[7][contains(text(),"yes")]'):
	            #Grabbing IP and corresponding PORT
	            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
	            proxies.add(proxy)
	    return proxies

	def getAlbumCoverURL(self, artist_name, song_name):
		artist_name = artist_name.replace('.', '').replace(' ','').replace("'", "").lower()
		song_name = song_name.replace(' ','-').replace("'", "").lower()

		track_slug = '-'.join([artist_name, song_name])
		client_access_token = '3u-fiiKZSn0n4jUO-cuxNamghC92pdYZQrnbzzb7AxuEMjnPcbJU71i5rytUhipZ'
		base_url = 'https://api.genius.com'
		path = 'search/'
		request_uri = '/'.join([base_url, path])
		# query = 'jcole-change'
		params = {'q': track_slug}

		token = 'Bearer {}'.format(client_access_token)
		headers = {'Authorization' : token}

		r = requests.get(request_uri, params=params, headers=headers)
		json = r.json()

		album_img = json['response']['hits'][0]['result']['header_image_url']
		return album_img

	def getSongLyrics(self, artist_name, song_name):
		artist_name = artist_name.replace('.', '').replace(' ','').replace("'", "").lower()
		song_name, sep, tail = song_name.partition('(')
		song_name = song_name.strip().replace(' ','-').replace("'", "").replace(".", "").lower()
		lyric_url = 'https://www.azlyrics.com/lyrics/{}/{}.html'.format(artist_name, song_name)

		proxy = next(self.proxy_pool)
		while(proxy):
			try:
				r = requests.get(lyric_url, proxies={'http':proxy, 'https':proxy})

				start_idx = r.text.find('that. -->')
				lyrics = r.text[start_idx::]
				last_idx = lyrics.find('</div>')
				lyrics = lyrics[10:last_idx]
				lyrics = lyrics.replace('<br>', '')

				if lyrics == "":
					proxy = next(self.proxy_pool)
				else:
					return lyrics
			except:
				print('Request denied, going next')
				proxy = next(self.proxy_pool)

		return 'Failed'
		# soup = BeautifulSoup(r.text, 'html.parser')

		# print(soup.prettify())

	def getTrackList(self, artist_name, album_name):
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

	def createSlug(self, artist_name, song_name):
		artist_name = artist_name.replace('.', '').replace(' ','').replace("'", "").lower()
		song_name = song_name.replace(' ','-').replace("'", "").lower()

		track_slug = '-'.join([artist_name, song_name])

		return track_slug.strip('-')
