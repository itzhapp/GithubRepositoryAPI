import requests
import sys
from bs4 import BeautifulSoup
import re
import json



def main(programmingLanguage, page):
    url = 'https://github.com/search?l=&p='+page+'&q=language%3A'+programmingLanguage+'+license%3Agpl&ref=advsearch&type=Repositories'
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    github = "https://github.com/"
    projectLinks = soup.find_all("a")
    projectDescriptions = soup.find_all("p")
    projectTags = soup.find_all("div")
    counter = 0
    result = []

    for row in projectLinks:
        responseString = str(row)
        if '"url":"' in responseString:
            sections = responseString.split(",")
            for segment in sections:
                if segment.startswith('"url":"'):
                    projectURL = segment.replace('"url":"', "").replace('"}', "")
                    segmentProjectURL = projectURL.split("/")
                    username = segmentProjectURL[3]
                    projectName = segmentProjectURL[4]
                    result.append([projectURL, username, projectName])

    for row in projectDescriptions:
        responseString = str(row)
        if '<p class="mb-1">' in responseString:
            projectDescription = responseString.replace('<p class="mb-1">', '').replace('</p>', '').replace('        ', '').replace('\n', '').replace('      ', '')
            result[counter].append(projectDescription)
            counter+=1

    ##Something to contribute too##

    #unique = []
    #for row in projectTags:
    #    responseString = str(row)
    #    try:
    #        found = re.findall(r'href="/topics/\w+', responseString)
    #        topics = str(found).replace('href="/topics/', "")
    #        if topics not in unique:
    #            unique.append(topics)
    #    except AttributeError:
    #        pass
    #
    #unique.pop(0)
    #unique.pop(0)
    #for i in range(len(result)-1):
    #    print(unique[i])
    #    result[i].append(unique[i])

    jsonString = ''
    for i in result:
        try:
            #myList = [{'name':i[2]}, {'link':i[0]}, {'description':i[3]}, {'tags':i[4]}]
            myList = [{'name':i[2]}, {'link':i[0]}, {'description':i[3]}]
            jsonString = jsonString + json.dumps(myList, indent=4)
        except:
            pass

    print(jsonString)
    return jsonString

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])