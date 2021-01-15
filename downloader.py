import requests
import json
import sys
import os
import threading
import re
from datetime import datetime


sub = "memes"
time = "day"
limit = 1
headers = {'User-Agent': 'Periodical Image Downloader',}
dled = []
imgnumber = 0
extensions = ['.jpg', '.png', '.jpeg', '.gif', '.mp4', '.webm', '.gifv']
links = []
finished_links = []
threads = []

p = requests.get('https://www.reddit.com/r/{}/top.json?sort=top&t={}&limit={}'.format(sub, time, limit), headers=headers)
p_json = json.loads(p.text)

if not os.path.isdir(sub+'/'):
	os.makedirs(sub+'/'+'/json_file')

with open(sub+'/json_file/r_{}_top_{}_of_{}.json'.format(sub, limit, time), 'w') as f:
	f.write(p.text)

for a in p_json['data']['children']:
	link = a['data']['url']
	if 'gfycat' in link or 'imgur' in link or 'i.redd.it' in link or link.endswith(tuple(extensions)):
		links.append(link)

def download(url, file_name):
	print(file_name)
	with open(sub+'/'+file_name, "wb") as file:
		response = requests.get(url, headers=headers)
		file.write(response.content)

print('Processing links')

for c in links:
	if "imgur.com" in c:
		if '/a/' in c or '/gallery/' in c:
			finished_links.append(c)

		elif c.endswith(tuple(extensions)):
			if c.endswith('.gifv'):
				newurl = c.replace(".gifv",".mp4")
				finished_links.append(newurl)

			else:
				finished_links.append(c)

		else:
			html_page = requests.get(c)
			if html_page.status_code == 404:
				print('404: skipping')
			else:
				print(c)
				print(c)
				print(c)
				print(c)
				imgur_id = c.split('/')[-1]
				try:
					link = re.findall('(?:href|src)="(?:https?:)?(\/\/i\.imgur\.com\/{}\.\S+?)"'.format(imgur_id), html_page.text)[0]
					link = 'https:' + link
					finished_links.append(link)
				except IndexError:
					print('IndexError on link {}'.format(c))
					fixedlink = c.split('?')[0]
					print(fixedlink)
					pass

	elif "i.redd.it" in c or "i.reddituploads.com" in c:
		finished_links.append(c)

	elif "gfycat.com" in c and not c.endswith('.webm'):
		gfycat_id = c.split('/')[-1]
		link = 'http://giant.gfycat.com/{}.webm'.format(gfycat_id)
		finished_links.append(link)

	elif c.endswith(tuple(extensions)):
		finished_links.append(c)

print('Downloading images')
try:
	for d in finished_links:
		imgnumber += 1
		a_imgnumber = 0
		a_threads = []
		donelinks = []
		if '/a/' in d or '/gallery/' in d:
			if not os.path.isdir(sub + '/' + str(imgnumber)):
				os.makedirs(sub + '/' + str(imgnumber))
			html_page = requests.get(d + '/layout/blog')
			if html_page.status_code == 404:
				print('404: skipping')
			else:
				imglinks = re.findall(r'\.*?{"hash":"([a-zA-Z0-9]+)".*?"ext":"(\.[a-zA-Z0-9]+)".*?', html_page.text)
				for i in imglinks:
					try:
						if i[0]+i[1] not in donelinks:
							a_imgnumber += 1
							if i[1] == '.gif':
								ext = '.mp4'
							else:
								ext = i[1]
							g = threading.Thread(target=download, args=('https://i.imgur.com/'+i[0]+ext, str(imgnumber) + '/' + str(a_imgnumber) + ext))
							a_threads.append(g)
							g.start()
							donelinks.append(i[0]+i[1])
					except KeyboardInterrupt:
						print('\nCtrl-C Pressed; Finishing current threads then stopping...')
						for f in a_threads:
							f.join()
						sys.exit()
				for f in a_threads:
					f.join()
		else:
			# filename, file_extension = os.path.splitext(os.path.basename(d))
			t = threading.Thread(target=download, args=(d, os.path.basename(d)))
			t.start()
			threads.append(t)

	for e in threads:
		e.join()

except KeyboardInterrupt:
	print('\nCtrl-C Pressed; Finishing current threads then stopping...')
	for e in threads:
		e.join()
	sys.exit()
