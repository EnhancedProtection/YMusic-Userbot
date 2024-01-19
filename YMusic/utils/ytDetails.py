from youtubesearchpython import VideosSearch

def searchYt(query) :
	query = str(query)
	videosResult= VideosSearch(query, limit=1)
	Result = videosResult.result()
	title = Result["result"][0]["title"]
	duration = Result["result"][0]["duration"]
	link = Result["result"][0]["link"]
	return title, duration, link