from PIL import Image
from PIL.ExifTags import TAGS

# filename = "DJI_0131.JPG"
# extension = filename.split('.')[-1]
# if (extension == 'jpg') | (extension == 'JPG') | (extension == 'jpeg') | (extension == 'JPEG'):
#     try:
#         img = Image.open(filename)
#         info = img.getexif()
#         exif = {}
#         for tag, value in info.items():
#             decoded = TAGS.get(tag, tag)
#             exif[decoded] = value
#         # from the exif data, extract gps
#         exifGPS = exif['GPSInfo']
#         latData = exifGPS[2]
#         lonData = exifGPS[4]
#         # calculae the lat / long
#         latDeg = latData[0][0] / float(latData[0][1])
#         latMin = latData[1][0] / float(latData[1][1])
#         latSec = latData[2][0] / float(latData[2][1])
#         lonDeg = lonData[0][0] / float(lonData[0][1])
#         lonMin = lonData[1][0] / float(lonData[1][1])
#         lonSec = lonData[2][0] / float(lonData[2][1])
#         # correct the lat/lon based on N/E/W/S
#         Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
#         if exifGPS[1] == 'S': Lat = Lat * -1
#         Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
#         if exifGPS[3] == 'W': Lon = Lon * -1
#         # print file
#         msg = "There is GPS info in this picture located at " + str(Lat) + "," + str(Lon)
#         print (msg)
# # kmlheader = '<?xml version="1.0" encoding="UTF-8"?>' + '<kml xmlns="http://www.opengis.net/kml/2.2">'
# # kml = ('<Placemark><name>%s</name><Point><coordinates>%6f,%6f</coordinates></Point></Placemark></kml>') % (
# #     filename, Lon, Lat)
# # with open(filename + '.kml', "w") as f:
# #     f.write(kmlheader + kml)
# # print
# # 'kml file created'
#     except:
#         print ('There is no GPS info in this picture')
#         pass



#2ㅇㅏㄴ
# image = Image.open("/Users/leehoseop/PycharmProjects/SVS_Data_Creator/panorama_images/sejong_gumgang_bridge/sejong_gumgang_bridge_00000.JPG")
# info = image._getexif();
# image.close()
#
# # 새로운 딕셔너리 생성
#
# taglabel = {}
#
# for tag, value in info.items():
#     decoded = TAGS.get(tag, tag)
#     taglabel[decoded] = value
#
# print(taglabel)
#
# print(taglabel['DateTimeOriginal'])
# print(taglabel['DateTimeDigitized'])
# print(taglabel['DateTime'])
#
# print(taglabel['GPSInfo'])

from PIL import Image

from PIL.ExifTags import TAGS

import webbrowser

image = Image.open("/Users/leehoseop/PycharmProjects/SVS_Data_Creator/panorama_images/sejong_gumgang_bridge/sejong_gumgang_bridge_00000.JPG")
info = image._getexif();
image.close()

# 새로운 딕셔너리 생성

taglabel = {}

for tag, value in info.items():
    decoded = TAGS.get(tag, tag)
    taglabel[decoded] = value

exifGPS = taglabel['GPSInfo']
latData = exifGPS[2]
lonData = exifGPS[4]

# 도, 분, 초 계산
latDeg = latData[0][0] / float(latData[0][1])
latMin = latData[1][0] / float(latData[1][1])
latSec = latData[2][0] / float(latData[2][1])

lonDeg = lonData[0][0] / float(lonData[0][1])
lonMin = lonData[1][0] / float(lonData[1][1])
lonSec = lonData[2][0] / float(lonData[2][1])

# 도, 분, 초로 나타내기
Lat = str(int(latDeg)) + "°" + str(int(latMin)) + "'" + str(latSec) + "\"" + exifGPS[1]
Lon = str(int(lonDeg)) + "°" + str(int(lonMin)) + "'" + str(lonSec) + "\"" + exifGPS[3]

webbrowser.open_new("https://www.google.com/maps/place/" + Lat + "+" + Lon)

