import requests

url = 'https://bwfworldtour.bwfbadminton.com/tournament/3350/princess-sirivannavari-thailand-masters-2019/results/podium/'

print(requests.get(url).text)
