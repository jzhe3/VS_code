import urllib.request,csv,requests
from urllib.parse import urlencode
from lxml import etree

csvFile = open("C:/Users/TOMORROW/Desktop/present/organization.csv", 'w+', newline="")
def get_page(offset):
    for i in range(1,3):
        params = {
            'pageIndex': str(i),
            'pageSize': '10',
            'districtId': offset,
        }
        url = 'https://gz.izyz.org/api/organization/listOrg.do?' + urlencode(params)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                json = response.json()
                get_node(response.json())
                # print(response.json())
        except requests.ConnectionError:
            pass
        #  广州市: 4028818811a15abe0111a1a517480004
        # https://gz.izyz.org/organization/index.do?districtId=8e9715d3444dd11701444dd446fa0008
def get_content(url1):
    url = 'https://gz.izyz.org/organization/detail.do?districtId=' + url1
    response = urllib.request.urlopen(url)
    savee = []
    myhtml = etree.HTML(response.read().decode('utf-8'))
    name= myhtml.xpath('//*[@id="activity_list"]/div[1]/div[1]/div/h1/text()')
    savee.append(name)
    child_organization =myhtml.xpath('//*[@id="activity_list"]/div[1]/div[1]/div/div/span[2]/text()')
    savee.append(child_organization)
    logo_time =myhtml.xpath('//*[@id="activity_list"]/div[1]/div[2]/div[2]/p[1]/span[2]/text()')
    savee.append(logo_time)
    num_human =myhtml.xpath('//*[@id="activity_list"]/div[1]/div[2]/div[2]/p[2]/span[2]/text()')
    savee.append(num_human)
    work_time = myhtml.xpath('//*[@id="activity_list"]/div[1]/div[2]/div[2]/p[3]/span[2]/text()')
    savee.append(work_time)
    email = myhtml.xpath('//*[@id="activity_list"]/div[1]/div[2]/div[2]/p[4]/span[2]/text()')
    savee.append(email)
    tel = myhtml.xpath('//*[@id="activity_list"]/div[1]/div[2]/div[2]/p[5]/span[2]/text()')
    savee.append(email)
    address = myhtml.xpath('//*[@id="activity_list"]/div[1]/div[2]/div[2]/p[6]/span[2]/text()')
    # print(address[0])
    if len(address) == 0:
        savee =[]
        print('error')
    else:
        lon=dizhijiexilon(address)
        lat = dizhijiexilat(address)
        if lon == 0 or lat == 0:
            savee =[]
            print('error')
        else:
            savee.append(address)
            savee.append(lon)
            savee.append(lat)
            writer = csv.writer(csvFile)
            try:
                writer.writerow(savee)
                print('ok')
                savee =[]
            except:
                print('error')
                savee =[]
def get_node(json):
    try:
        if json.get('data'):
            # print(json.get('data'))
            # item = json.get('data')
            nodes = json.get('data').get('records')
            for node in nodes:
                own = node.get('districtId')
                xiamian = node.get('haveChild')
                if not own in nodelist:
                    nodelist.append(own)
                    get_content(own)
                    print(own)
                    if xiamian ==1 :
                        get_page(own)
                else:
                    break
    except:
        print('有错')
nodelist= []

def dizhijiexilon(address):
    # address = '陕西省,西安市,临潼区新市办高庙村焦四组'
    url= 'http://api.map.baidu.com/geocoder?output=json&key=f247cdb592eb43ebac6ccd27f796e2d2&address='+str(address)
    response = requests.get(url)
    answer = response.json()
    try:
        lon = answer['result']['location']['lng']
        return lon
    except:
        return 0

def dizhijiexilat(address):
    # address = '陕西省,西安市,临潼区新市办高庙村焦四组'
    url= 'http://api.map.baidu.com/geocoder?output=json&key=f247cdb592eb43ebac6ccd27f796e2d2&address='+str(address)
    response = requests.get(url)
    answer = response.json()
    try:
        lat = answer['result']['location']['lat']
        return lat
    except:
        return 0

if __name__ == '__main__':
    get_page('4028818811a15abe0111a1a517480004')
    # get_content('f988e24c2b76561f012b931aa8411e8')
    # for i in nodelist:
    #     get_content(i)
        # f988e24c2b76561f012b931aa8411e80
