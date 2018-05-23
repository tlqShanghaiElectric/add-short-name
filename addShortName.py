# -*- coding: utf-8 -*-
"""
Created on Mon May 14 12:32:02 2018

@author: 12600771
"""

# for channel, table & filter
# Caution: without enough test
def getShortName(rawName):
    newName = ""
    hifenFlag = False
    secondhifenIndex = -1
    lastIndex = -1
    
    for index in range(len(rawName)):
        char = rawName[index]
        if hifenFlag:
            if char.isupper():
                if (index - lastIndex >= 3):
                    newName += rawName[lastIndex:lastIndex+3]
                else:
                    newName += rawName[lastIndex:index]
                lastIndex = index
            elif char == '_':
                secondhifenIndex = index
                break
        elif char == '_':
            hifenFlag = True
            newName += rawName[0:index+1]
            lastIndex = index + 1

    if secondhifenIndex < 0:
        if (len(rawName) - lastIndex) >= 3:
            newName += rawName[lastIndex:lastIndex+3]
        else:
            newName += rawName[lastIndex:]
    else:
        if (secondhifenIndex - lastIndex) >= 3:
            newName += rawName[lastIndex:lastIndex+3]
            newName += rawName[secondhifenIndex:secondhifenIndex+2]
        else:
            newName += rawName[lastIndex:secondhifenIndex+2]
  
    if rawName[len(rawName)-1].isdigit():
        for i in range(-1, 0-len(rawName), -1):
            if rawName[i].isdigit():
                digitIndex = i
        newName += rawName[digitIndex:]
    return newName

def translateType(oldType):
    # five type: float, int, uint, bool, double
    typeDict = {"float":"REAL", "int":"DINT", "uint":"DWORD", "bool":"BOOL","double":"LREAL"}
    return typeDict.get(oldType)

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

from xml.etree.ElementTree import parse, Element, tostring

#filename = r"C:\Users\12600771\Desktop\Parameters.xml"
filename = r"C:\Users\tlqld\Desktop\Parameters.xml"
#doc = minidom.parse(filename)
#root = doc.documentElement

doc = parse(filename)
root = doc.getroot()
children = root.getchildren()
for child in children:
    childName = child.tag
    elements = root.find(childName).findall(childName[:-1]) #Channel, Table & Filter
    for element in elements:
        nameElement = element.find('Name')
        name = nameElement.text
        index = list(element).index(nameElement)
        shortNameElement = Element("ShortName")
        shortNameElement.text = getShortName(name)
        element.insert(index+1, shortNameElement)

 # Channels
channels = root.find("Channels").findall('Channel')
for channel in channels:
#     nameElement = channel.find('Name')
#     name = nameElement.text
#     index = list(channel).index(nameElement)
#     shortNameElement = Element("ShortName")
#     shortNameElement.text = getShortName(name)
#     channel.insert(index+1, shortNameElement)
    
    
    datatypeElement = channel.find('DataType')
    datatype = datatypeElement.text
    plcDataTypeElement = Element("PlcDataType")
    plcDataTypeElement.text = translateType(datatype)
    channel.append(plcDataTypeElement)
    channel.remove(datatypeElement)
       
    initialValueElement = channel.find('InitialValue')
    initialValue = initialValueElement.text
    valueElement = Element("Value")
    valueElement.text = initialValue
    channel.append(valueElement)
    channel.remove(initialValueElement)
    
# # Tables
# tables = root.find("Tables").findall("Table")
# for table in tables:
#     nameElement = table.find("Name")
#     name = nameElement.text
#     index = list(table).index(nameElement)
#     shortNameElement = Element("ShortName")
#     shortNameElement.text = getShortName(name)
#     table.insert(index+1, shortNameElement)


indent(root)
doc.write("newPar.xml", encoding="utf-8", xml_declaration=True)