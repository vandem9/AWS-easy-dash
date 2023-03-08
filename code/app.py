import boto3
import cfnresponse
import json
import traceback

import widgetHelper

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambdaHandler(event, context):

    logger.info(event)

    try:
        dashboardName = getResourceProperty(event, "DashboardName")

        if event['RequestType'] == "Delete":
            deleteDashboard(dashboardName)
            sendCfnresponse(event, context, "SUCCESS", {'DashboardName': dashboardName}, dashboardName)
        else:
            region = getResourceProperty(event, "Region")
            dashBoardResources = getResourceProperty(event, "Resources")
            widgetDict = widgetHelper.buildWidgetsDict()

            dashboardWidgets = []

            for resource in dashBoardResources:
                metricResourceType = resource['MetricResourceType']
                resourceReference = resource['ResourceReference']
                widget = widgetHelper.getWidgetObject(widgetDict, metricResourceType, resourceReference, region)

                dashboardWidgets.extend(widget)

            dashboardBody = {"widgets" : dashboardWidgets}

            putDashboard(dashboardName, dashboardBody)

            logger.info(dashboardName)
            logger.info(dashBoardResources)

            sendCfnresponse(event, context, "SUCCESS", {'DashboardName': dashboardName}, dashboardName)

    except Exception as e:
        logging.error(traceback.format_exc())
        sendCfnresponse(event, context, "FAILED", {'Error': str(e)}, None)

def deleteDashboard(dashboardName):
    client = boto3.client('cloudwatch')

    response = client.delete_dashboards(
        DashboardNames=[
            dashboardName,
        ]
    )

def putDashboard(dashboardName, dashboardBody):
    client = boto3.client('cloudwatch')

    response = client.put_dashboard(
        DashboardName=dashboardName,
        DashboardBody=json.dumps(dashboardBody)
    )


def sendCfnresponse(event, context, status, data, physicalResourceId=None):
    if status == "SUCCESS":
        cfnresponse.send(event, context, cfnresponse.SUCCESS,
                         data, physicalResourceId)
    else:
        logger.error(str(data))
        cfnresponse.send(event, context, cfnresponse.FAILED,
                         data, physicalResourceId)


def getResourceProperty(event, resourcePropertyName):
    recourseProperties = event['ResourceProperties']

    return recourseProperties[resourcePropertyName]










