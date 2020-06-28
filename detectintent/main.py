import dialogflow
import json
from flask import request, jsonify
from google.protobuf.json_format import MessageToJson
from google.protobuf.struct_pb2 import Struct
from google.protobuf.struct_pb2 import Value

def detect_intent(request):
    response = {
        'status_code': 500,
        'message': 'Failed to fetch data from dialogflow.',
        'data': []
    }

    try:
        request_json = request.get_json(silent=True, force=True)

        project_id = "build-agent-local"
        session_client = dialogflow.SessionsClient.from_service_account_json('key.json')

        payload = {'project_id': project_id, 'session_id': request_json.get("session_id")}
        struct_pb = Struct(fields={
            key: Value(string_value=value) for key, value in payload.items()
        })
        params = dialogflow.types.QueryParameters(
            time_zone="PST", payload=struct_pb)
        session = session_client.session_path(project_id, request_json.get("session_id"))

        text_input = dialogflow.types.TextInput(
            text=request_json.get("text"), language_code='en-US')
        query_input = dialogflow.types.QueryInput(text=text_input)
        df_response = session_client.detect_intent(
            session=session, query_input=query_input, query_params=params)

        # Convert proto object and serialize it to a json format string.
        json_obj = MessageToJson(df_response)

        result = json.loads(json_obj)
        response['status_code'] = 200
        response['data'] = result
        response['message'] = "Successfully fetched response from dialogflow."
    except Exception as e:
        print(e)

    return jsonify(response)