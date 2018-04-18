#coding=utf-8
import urllib2,sys,time,datetime,os,pymysql.cursors
poidata_file=open("poidata.txt","a")
err_file=open("errspiodataread.txt","a")
read_file=open("szreadedpoi.txt","a")
errpoidatas={}
allpoidatas={}
readpoilinks={}
poidatas = {}
poiids_file = open("poiid.txt","r")



connection = pymysql.connect(host='127.0.0.1', port=3306, user='test', password='test', db='poi', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()


for lines in poiids_file:
        data = lines.strip("\n")
        if ":" in data or "--" in data:
                pass
        else:
                allpoidatas[data]=""
                pass
readed_file = open("szreadedpoi.txt","r")
for lines in readed_file:
        data = lines.strip("\n")
        poidatas[data]="readed"
pagenum=0
hdr = {
        'Host':"www.poi86.com",
       'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
       'Connection': 'keep-alive'
       }
alldatanum=len (allpoidatas)-1

for key in allpoidatas:
          
        poiPageUrl="http://www.poi86.com/poi/"+key+".html"
        if poiPageUrl in poidatas :
                print "Exist Page:"
                print poiPageUrl
                print "readed Next--->"
                pass
                continue
        try:
                print "POI page:", poiPageUrl
                poiPageInfo=urllib2.urlopen(poiPageUrl)        
        except Exception,e:
                print 'openERR:'
                print poiPageUrl
                print str(e)
                if  "Forbidden" in str(e):
                        for n in range(0,10):
                                print "banned!!!!!!!!"                                                                                       
                        os.system(r"rasphone -h 051213869974")  
                        os.system(r"rasdial 051213869974 051213869974 085564") 
                        os.system("run_getpoiDatas.bat")
                        sys.exit(9)
                err_file.write(poiPageUrl+'\n'+str(e)+"\n")
                err_file.flush()
                pass
                continue
        try:   
                if poiPageInfo:
                        poiPageDetial=poiPageInfo.read()                                                                                                       
                        if "警告!由于你恶意访问,您的IP已被记录!" in poiPageDetial:
                                for n in range(0,10):
                                        print "banned!!!!!!!!"
                                os.system(r"rasphone -h 051213869974")  
                                os.system(r"rasdial 051213869974 051213869974 085564") 
                                os.system("run_getpoiDatas.bat")       
                                sys.exit(9)
                        
                        else:
                                id= int(key)
                                name= poiPageDetial[poiPageDetial.index("<h1>")+4:poiPageDetial.index("</h1>")].strip("\n").strip("\"")

                                poiPageDetial=poiPageDetial[poiPageDetial.index("所属省份"):]
                                poiPageDetial=poiPageDetial[poiPageDetial.index("<a")+1:]
                                province=poiPageDetial[poiPageDetial.index(">")+1:poiPageDetial.index("</a>")].strip("\n").strip("\"")
                                if ">" in province:
                                        province=province[province.index(">"+1):]


                                poiPageDetial=poiPageDetial[poiPageDetial.index("所属城市"):]
                                poiPageDetial=poiPageDetial[poiPageDetial.index("<a")+1:]
                                city=poiPageDetial[poiPageDetial.index(">")+1:poiPageDetial.index("</a>")].strip("\n").strip("\"")
                                if ">" in city:
                                        city=city[city.index(">"+1):]

                                poiPageDetial=poiPageDetial[poiPageDetial.index("所属区县"):]
                                poiPageDetial=poiPageDetial[poiPageDetial.index("<a")+1:]
                                district=poiPageDetial[poiPageDetial.index(">")+1:poiPageDetial.index("</a>")].strip("\n").strip("\"")
                                if ">" in district:
                                        district=district[district.index(">"+1):]

                                poiPageDetial=poiPageDetial[poiPageDetial.index("详细地址"):]
                                address=poiPageDetial[poiPageDetial.index("</span>")+8:poiPageDetial.index("</li>")].strip("\n").strip("\"")
                                
                                poiPageDetial=poiPageDetial[poiPageDetial.index("电话号码"):]
                                phone=poiPageDetial[poiPageDetial.index("</span>")+8:poiPageDetial.index("</li>")].strip("\n").strip("\"")

                                poiPageDetial=poiPageDetial[poiPageDetial.index("所属分类"):]
                                poiPageDetial=poiPageDetial[poiPageDetial.index("a"):]
                                sort=poiPageDetial[poiPageDetial.index(">")+1:poiPageDetial.index("</a>")].strip("\n").strip("\"")
                                if ">" in sort:
                                        sort=sort[sort.index(">"+1):]

                                poiPageDetial=poiPageDetial[poiPageDetial.index("所属标签"):]
                                poiPageDetial=poiPageDetial[poiPageDetial.index("a"):]
                                tag=poiPageDetial[poiPageDetial.index(">")+1:poiPageDetial.index("</a>")].strip("\n").strip("\"")
                                if ">" in tag:
                                        tag=tag[tag.index(">"+1):]

                                poiPageDetial=poiPageDetial[poiPageDetial.index("大地坐标"):]
                                earthGPS=poiPageDetial[poiPageDetial.index("</span>")+8:poiPageDetial.index("</li>")].strip("\n").strip("\"")

                                poiPageDetial=poiPageDetial[poiPageDetial.index("火星坐标"):]
                                marsGPS=poiPageDetial[poiPageDetial.index("</span>")+8:poiPageDetial.index("</li>")].strip("\n").strip("\"")
                                
                                poiPageDetial=poiPageDetial[poiPageDetial.index("百度坐标"):]
                                baiduGPS=poiPageDetial[poiPageDetial.index("</span>")+8:poiPageDetial.index("</li>")].strip("\n").strip("\"")
                                
                                sqlValues="'"+key+"','"+name+"','"+province+"','"+ city+"','"+district+"','"+ address+"','"+phone +"','"+ sort +"','"+ tag +"','"+ earthGPS+"','"+ marsGPS+"','"+ baiduGPS+"'"
                                sql ="INSERT INTO `data` (`id`, `name`, `province`, `city`, `district`, `address`, `phone`, `sort`, `tag`, `earthGPS`, `marsGPS`, `baiduGPS`) VALUES (" + sqlValues+ ")"
                                try:
                                        cursor.execute(sql)
                                        connection.commit()
                                except Exception,e:
                                        err_file.write(poiPageUrl+'\n'+str(e)+"\n")
                                        err_file.flush()
                                        print "save err"
                                        print str(e)
                                        pass
                                        continue
                                poi=key+"---"+name+"---"+province+"---"+ city+"---"+district+"---"+ address+"---"+phone +"---"+ sort +"---"+ tag +"---"+ earthGPS+"---"+ marsGPS+"---"+ baiduGPS
                                poidata_file.write(poi.strip("\n"))
                                poidata_file.flush()
                                poidatas[poiPageUrl]=poi
                                read_file.write(poiPageUrl+"\n")
                                read_file.flush()                                                                                                     
        except Exception,e:
                print 'saveERR:'
                print str(e)
                err_file.write(poiPageUrl+'\n'+str(e)+"\n")
                err_file.flush()
                if  "Forbidden" in str(e):
                        for n in range(0,10):
                                print "banned!!!!!!!!"
                        os.system(r"rasphone -h 051213869974")  
                        os.system(r"rasdial 051213869974 051213869974 085564") 
                        os.system("run_getpoiDatas.bat")
                        sys.exit(9)
                pass	
                continue
db.close()     
poidata_file.close()
err_file.close()
read_file.close()

for n in range(0,20):
        print "finished!!!!!!!!"
os.system("run_getpoiDatas.bat")