import json
from flask import request
from pydialogflow_fulfillment import DialogflowResponse, DialogflowRequest
from pydialogflow_fulfillment.response import SimpleResponse, OutputContexts
import logging

def webhook(request):
    dialogflow_response = DialogflowResponse()
    try:
        dialog_fulfillment = DialogflowRequest(request.data) 
        action = dialog_fulfillment.get_action()
        if action == "welcome":
            dialogflow_response.add(SimpleResponse("This is a simple text response","This is a simple text response"))
        else:
            dialogflow_response.add(SimpleResponse("This is a fallback text response","This is a fallback text response"))
        # dialogflow_response.fulfillment_messages = dialog_fulfillment.request_data["queryResult"]["fulfillmentMessages"]

    except Exception as e:
        logging.error(e)
        dialogflow_response = DialogflowResponse()
        dialogflow_response.add(SimpleResponse("Something went wrong.","Something went wrong."))
        return json.loads(dialogflow_response.get_final_response())

    return json.loads(dialogflow_response.get_final_response())