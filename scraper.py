# import requests
# from lxml import html
#these functions are all very simliar and simply 
#grab the images and titles of those images from a given website

#webscrapping cite: http://docs.python-guide.org/en/latest/scenarios/scrape/
#images and titles taken from: musclewiki.org

##################################################
########## Modified Scrapers #####################
##################################################
def getTraps():
	page = requests.get('https://musclewiki.org/Male/Traps')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	imagesDict[titles[0]] = [picSrc[0],picSrc[1]]
	imagesDict[titles[1]] = [picSrc[2]]
	return imagesDict
def getLowBack():
	page = requests.get('https://musclewiki.org/Male/Lowerback')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	if 'Exercises' in titles:
		titles.pop(0)
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getTricep():
	page = requests.get('https://musclewiki.org/Male/Triceps')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	if 'Exercises' in titles:
		titles.pop(0)
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
##################################################
######## Even Amount of images and titles ########
##################################################
def getShoulder():
	page = requests.get('https://musclewiki.org/Male/Shoulders')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getChest():
	page = requests.get('https://musclewiki.org/Male/Chest')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getBicep():
	page = requests.get('https://musclewiki.org/Male/Biceps')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getAbs():
	page = requests.get('https://musclewiki.org/Male/Abdominals')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getForearms():
	page = requests.get('https://musclewiki.org/Male/Forearms')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getQuads():
	page = requests.get('https://musclewiki.org/Male/Quads')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getTrapsMiddle():
	page = requests.get('https://musclewiki.org/Male/Traps_middle')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getBack():
	page = requests.get('https://musclewiki.org/Male/Back')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getHamstrings():
	page = requests.get('https://musclewiki.org/Male/Hamstrings')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getCalves():
	page = requests.get('https://musclewiki.org/Male/Calves')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
def getGlutes():
	page = requests.get('https://musclewiki.org/Male/Glutes')
	tree = html.fromstring(page.content)
	titles = tree.xpath('//span[@class="mw-headline"]/text()')
	picSrc = tree.xpath('//*[@id="workout-img"]/@src')
	imagesDict = dict()
	picCount = 0
	for title in titles:
		imagesDict[title] = [picSrc[picCount],picSrc[picCount+1]]
		picCount+=2
	return imagesDict
