import re
import requests
import networkx as nx
from bs4 import BeautifulSoup
from collections import defaultdict
import math

station_coordinate_locationTT = {}
filter_station_pattern = re.compile(r'\w+')


def getStations(trs):
    res = []
    title = trs[0].find_all('th')
    if title[0].text.strip() == "车站名称":
        index = 0
    elif title[1].text.strip() == "车站名称" and len(trs[1].find_all('th')) != 0:
        index = 0
    else:
        index = 1
    for tr in trs[1:]:
        tds = tr.find_all("td")
        if len(tds) > 1:
            res += [filter_station_pattern.findall(tds[index].text)[0]]
    return res


def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def bfs(graph, start):
    visited= [start]
    seen = set()
    while visited:
        frontier = visited.pop()
        if frontier in seen:
            continue
        for successor in graph[frontier]:
            if successor in seen:
                continue
            visited = [successor] + visited   # 广义优先搜素(用队列来进行)
            # visited = visited + successor   # 深度优先搜素(用栈来进行)
        seen.add(frontier)
    return seen


def search(start, destination, graph, sort_candidate):
    pathes = [[start]]
    visited = set()
    while pathes:
        path = pathes.pop(0)
        frontier = path[-1]
        if frontier in visited:
            continue
        for city in graph[frontier]:
            if city in path: continue
            new_path = path +[city]
            pathes.append(new_path)
            if city == destination:
                print(new_path)
                return new_path
        visited.add(frontier)
        pathes = sort_candidate(pathes)  # sort function for controlling serarch strategy


def get_geo_distance(origin, destination):
    return geo_distance(station_coordinate_locationTT[origin], station_coordinate_locationTT[destination])


def get_path_distance(path):
    distance = 0
    for i, station in enumerate(path[:-1]):
        distance += get_geo_distance(station, path[i+1])
    return distance


def transfer_station_first(pathes):
    return sorted(pathes, key=len)


def transfer_as_much_as_possible(pathes):
    return sorted(pathes, key=len, reverse=True)


def shortest_path_first(pathes):
    return sorted(pathes, key=get_path_distance)


if __name__ == '__main__':
    common_link = "https://baike.baidu.com"
    url = 'https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485'

    # Getting url response
    headers = {"User-Agent": "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    response = requests.get(url, headers=headers, allow_redirects=False)
    # response.apparent_encoding  for getting 编码方式
    # response.encoding = "utf-8"
    html = response.content.decode(encoding='utf-8')

    # Getting all train routes
    soup = BeautifulSoup(html)
    caption = soup.find('caption')
    contents = caption.next_sibling.find_all('a')
    pattern = re.compile(r'href=\"(.*)\" ')
    temp = [''.join(pattern.findall(str(content))) for content in contents]
    router_links = sorted(list(set(temp)))

    # Getting all stations with extra invalid stations
    train_station_T = defaultdict(list)
    pattern1 = re.compile(r'\w+站')
    for router_link in router_links:
        respond_link = requests.get(common_link + router_link, headers=headers, allow_redirects=False)
        # respond_link.encoding = "utf-8"
        soup1 = BeautifulSoup(respond_link.content.decode(encoding='utf-8'))
        for a in soup1.find_all("caption"):
            if re.findall("车站列表", a.text):
                find_station_list = a
                break
            elif re.findall("车站信息", a.text):
                find_station_list = a
        next_siblings = find_station_list.next_sibling.find_all("tr")
        stations = getStations(next_siblings)
        train_station_T[find_station_list.text] = stations

    # 北京地铁站坐标
    coordinate_location_url = "http://ifamily.wang/2018/06/21/2018-06-20/"
    res_coordinate_location = requests.get(coordinate_location_url)
    # res_coordinate_location.encoding = "utf-8"
    html_coordinate_location = res_coordinate_location.content.decode(encoding='utf-8')
    soup = BeautifulSoup(html_coordinate_location, from_encoding="utf8")
    station_coordinate_location = defaultdict(list)
    station_name_pattern = re.compile(r'\w+')
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all("td")
        name = station_name_pattern.findall(tds[1].text)[0]
        if name[-1] == "站":
            name = name[:-1]
        station_coordinate_location[name + "站"] = (float(tds[-2].text), float(tds[-1].text))

    station_coordinate_location['2号航站楼站'] = station_coordinate_location.get("T2航站楼站")
    station_coordinate_location.pop("T2航站楼站")
    station_coordinate_location['3号航站楼站'] = station_coordinate_location.get("T3航站楼站")
    station_coordinate_location.pop("T3航站楼站")

    # 2. Preprocessing data from page source
    station_connection = defaultdict(list)
    train_station_TT = defaultdict(list)

    for key, value in station_coordinate_location.items():
        if value != []:
            station_coordinate_locationTT[key] = value

    for key, values in train_station_T.items():
        for value in values:
            if station_coordinate_locationTT.get(value) != None:
                train_station_TT[key].append(value)

    print(train_station_TT)
    print(station_coordinate_locationTT)
    for key, values in train_station_TT.items():
        for index, value in enumerate(values[:-1]):
            station_connection[value].append(values[index + 1])
            station_connection[values[index + 1]].append(value)

    # Ploting train staions and their edges
    # station_location2 = nx.Graph(station_connection)
    # nx.draw(station_location2, station_coordinate_locationTT, with_labels=False, node_size=10)


    # 3. Build the search agent
    search('天通苑站', '2号航站楼站', station_connection, sort_candidate=shortest_path_first)

