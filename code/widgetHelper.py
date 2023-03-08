import os
import json

def getWidgetObject(widgetDict, metricResourceType, resourceReference, region):

    widget = json.dumps(widgetDict[metricResourceType])

    widget = widget.replace("ResourceNamePlaceholder", resourceReference)
    widget = widget.replace("RegionNamePlaceholder", region)

    return json.loads(widget)

def buildWidgetsDict():

    directory = 'awsresources'
    widgetsDict = {}

    for resource in os.listdir(directory):
        resourceFilePath = os.path.join(directory, resource)

        resourceFile = open(resourceFilePath, 'r')

        resourceDict = json.loads(resourceFile.read())

        widgetsDict.update(resourceDict)

    return widgetsDict

