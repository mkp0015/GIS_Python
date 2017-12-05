#import dependencies
import urllib

#set base url
baseurl = 'https://e4ftl01.cr.usgs.gov/MOLT/MOD09A1.005/'

#retrieve responses from URL
response = urllib.urlopen(baseurl)

#close response
response.close()

dataurl = baseurl + '2000.02.18/BROWSE.MOD09A1.A2000049.h18v05.005.2006268203812.1.jpg'

#let's retrieve information from this file (data url)
data_response = urllib.urlopen(dataurl)

#how to save this data to an output file:
outfile = r'C:\Users\mpullman\Desktop\ESS508\data_out.jpg'

#write binary information to file
with open(outfile, 'wb') as output:   
    output.write(data_response.read())

#close connection to data
data_response.close()

print dataurl
