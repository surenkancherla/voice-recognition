#siteUrl = ""

def getUrl(request):
	tempArr = request.url.split("/")
	siteUrl = tempArr[0] + "//" + tempArr[2]

	return siteUrl