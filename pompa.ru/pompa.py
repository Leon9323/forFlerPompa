#!/usr/bin/python2
# -*- coding: utf-8 -*-
import urllib
import datetime
from lxml.html import fromstring
from lxml.html import tostring
from lxml.etree import tostring
from lxml.builder import E
from lxml import etree
def getCountry():
    url = "http://www.pompa.ru/shops/"
    html = urllib.urlopen(url).read();
    page = fromstring(html);
    pathCountry = ".//*[@id='country']/option/text()";
    pathID = ".//*[@id='country']/option/@value";
    countryName = page.xpath(pathCountry);
    countryID = page.xpath(pathID);
    iteration = 0;
    Country = [];
    while len(countryID)>iteration:
        Country.append({"id":countryID[iteration], "name":countryName[iteration]});
        iteration=iteration+1;
    return Country;
def getNameCountry(country, cid):
    for i in country:
        if(unicode(cid) == i["id"]):
            return unicode(i["name"]);
def getCity(countryID):
    url = "http://www.pompa.ru/shops/?AJAX_CALL=Y&SECTION_ID="+str(countryID)+"&submit=ok";
    html = urllib.urlopen(url).read();
    page = fromstring(html);
    pathCity = ".//*[@id='city-list-"+str(countryID)+"']/option/text()";
    pathID = ".//*[@id='city-list-"+str(countryID)+"']/option/@value";
    cityName = page.xpath(pathCity);
    cityID = page.xpath(pathID);
    cityName.pop(0);
    cityID.pop(0);
    #r = [657, 823];
    return cityID;
    #return r;
def getData():
    #create xml
    #xml = etree.Element('companies', version="2.1");
    xml = etree.Element('companies', nsmap={'xi':"http://www.w3.org/2001/XInclude"}, version="2.1");
    #load country
    for country in getCountry():
        countryID = country["id"];
        #load city
        citiesID = getCity(countryID);
        Shops = [];
        for cityID in citiesID:
            #getCity
            url = "http://www.pompa.ru/shops/?AJAX_CALL=Y&SECTION_ID="+str(cityID)+"&submit=ok";
            html = urllib.urlopen(url).read();
            page = fromstring(html);
            pathTD = "count(//tr)";
            #число магазинов
            count = page.xpath(pathTD);
            count = int(count);
            i = 1;
            while count>=i:
                company = etree.Element("company");
                #id
                pathID = ".//*[@id='shops-list']/table/tr["+str(i)+"]/@id";
                uid = page.xpath(pathID);
                etree.SubElement(company, "company-id").text = uid[0];
                #name
                pathName = ".//*[@id='shops-list']/table/tr["+str(i)+"]/td[1]/strong/text()";
                name = page.xpath(pathName);
                etree.SubElement(company, "name", lang="ru").text = name[0];
                #adress&city
                pathCity = ".//*[@id='shops-list']/h2/text()";
                city = page.xpath(pathCity);
                pathAddress = ".//*[@id='shops-list']/table/tr["+str(i)+"]/td[2]/a/text()";
                address = page.xpath(pathAddress);
                clear_adress = address[0].replace("(","");
                clear_adress = clear_adress.replace(")","");
                clear_adress = clear_adress.replace('"',"");
                etree.SubElement(company, "address", lang="ru").text = u"город "+city[0]+", "+clear_adress;
                #phone
                pathPhone = ".//*[@id='shops-list']/table/tr["+str(i)+"]/td[2]/text()";
                phoneCompany = page.xpath(pathPhone);
                phone = etree.SubElement(company, "phone");
                try:
                    first = unicode(phoneCompany[1]).index(u"Тел. ")+5;
                    last = first+18;
                    resultPhone = unicode(phoneCompany[1])[first:last].strip();
                    if resultPhone[1] == u"-":
                        lastSymbol = resultPhone[2:len(resultPhone)].find(u"-");
                        resultPhone = resultPhone[0]+u"("+resultPhone[2:(lastSymbol+2)]+u") "+resultPhone[(lastSymbol+2+1):len(resultPhone)];
                except ValueError:
                    resultPhone = u"";
                etree.SubElement(phone, "number").text = resultPhone;
                etree.SubElement(phone, "ext");
                etree.SubElement(phone, "info");
                etree.SubElement(phone, "type").text = "phone";
                #country
                country = getNameCountry(getCountry(), countryID);
                etree.SubElement(company, "country", lang="ru").text = country;
                #lon
                pathLon = ".//*[@id='shops-list']/table/tr["+str(i)+"]/td[2]/a/@data-lon";
                lonMap = page.xpath(pathLon);
                etree.SubElement(company, "lon").text = lonMap[0];
                #lat
                pathLat = ".//*[@id='shops-list']/table/tr["+str(i)+"]/td[2]/a/@data-lat";
                latMap = page.xpath(pathLat);
                etree.SubElement(company, "lat").text = latMap[0];
                #rubric-id
                rubric="184107943";
                etree.SubElement(company, "rubric-id").text = rubric;
                #url
                site="http://www.pompa.ru";
                etree.SubElement(company, "url").text = site;
                #date
                date = datetime.date.today().strftime("%d.%m.%Y");
                etree.SubElement(company, "actualization-date").text = date;
                i=i+1;
                #print etree.tostring(company, xml_declaration=True, encoding="utf-8");
                xml.append(company);
        #a = etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8");
        #a = etree.tostring(xml, xml_declaration=True, encoding="utf-8");
        #write xml
        #with open('pompa.xml', 'w') as outfile:
            #outfile.write(a);
        #tree = etree.ElementTree(xml)
        #tree.write("pompa.xml")
        #print a;
    a = etree.tostring(xml, pretty_print=True, xml_declaration=True, encoding="utf-8");
    #print a;
    return a;
def main():
    result = getData();
    with open('pompa.xml', 'w') as outfile:
            outfile.write(result);
main();
