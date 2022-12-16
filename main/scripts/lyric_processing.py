import requests
from nltk.corpus import cmudict

text = """Now I was barely seventeen with a pocket full of hope
Screamin', dollar and a dream with my closet lookin' broke
"""

text = """And my nigga's lookin' clean, gettin' caught up with that dope
Have you ever served a fiend with a pocket full of soap?
Nigga I can tell you things that you probably shouldn't know
Have you ever heard the screams when the body hit the floor?
Flashbacks to the pain, wakin' up, cold sweats
Six o'clock in the mornin', gotta hit the BoFlex
Get my weight up on the block, keep watch for the cops
God they love to serve a nigga three hots and a cot
Nowadays crime pays like a part time job
And the drought got me prayin' for a car time vibe
Summer Rain come again
Numb the pain 'cause it's hard for a felon
In my mind I been cryin', know it's wrong but I'm sellin'
Eyes wellin' up with tears
Thinkin' 'bout my niggas dead in the dirt
Immortalized on this shirt """


lines = text.split('\n')

url = "http://api.datamuse.com/words"

# sl - Sounds Like: Not rhymes, but similiar letters
# sp - Spelled Like: Similiar spellings, better for rhymes
# rel_[code] - Related to: 
# [codes] : rhy - rhymes | nry - near rhymes "*o?e"

# r = requests.get(url, params={'rel_rhy': 'hope', 'md' : 'f r'})

arpabet = cmudict.dict()

rhymes = {}

# Vowel Pronunciation Tags
# OW1 AH0 AY1 OW0 EH1 IH1 AA0 AE1 ER0 AA1 EY1 AO1 UW0 IH0 AE0 ER1 IY1

pron_vowels = ['AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER', 'EY', 'IH', 'IX', 'IY', 'OW', 'OY', 'UH', 'UW', 'UX']
stress_aux = ['0', '1', '2']

pron_stress = [pron + stress for pron in pron_vowels for stress in stress_aux]

all_words = []

rhymes = {}

banned = ['a', 'the', 'and', 'in', 'of']

num_lines = 3
count = 0

rhy_lines = []

for line in lines:
	words = line.replace(',', '').replace('.', '').replace("' ", 'g ').replace("'s", '').replace('?', '').lower().split(' ')

	for word in words:
		if word == "" or word in banned:
			continue

		if word == "nigga":
			word = "bigger"

		if word not in arpabet:
			continue

		word_vowels = []
		for ele in arpabet[word][0]:
			if ele in pron_stress:
				word_vowels.append(ele[:2])

		try:
			rhymes[word_vowels[-1]].append(word)
		except:
			rhymes[word_vowels[-1]] = [word]


	if count >= num_lines:
		count = 0
		rhy_lines.append(rhymes)
		rhymes = {}

	count += 1

for ele in rhy_lines:
	print('_---------------------------------------_')
	print(ele)

# for ele in r.json():
# 	if 'score' in ele.keys():
# 		pron = ele['tags'][0]
# 		pron = pron[5:]

# 		rhymes[ele['word']] = ele['score']
# 	# print(ele)


# # print(rhymes)
