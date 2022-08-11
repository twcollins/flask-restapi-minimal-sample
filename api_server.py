#!/usr/bin/env python3
# import requests
import logging
import os

from flask import Flask
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs

from healthcheck import HealthCheck, EnvironmentDump
from waitress import serve

log = logging.getLogger('logusage')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
# flask app and API instance

app = Flask(__name__)  # Flask app instance initiated
api = Api(app)  # Flask restful wraps Flask app around it.
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Usage API Project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)


# healthcheck and env spec
health = HealthCheck(app, "/healthcheck",success_ttl=300, failed_ttl=300)
envdump = EnvironmentDump(app, "/environment",include_python=False, include_os=False,
                          include_process=False, include_config=False)

# no-op - functionality removed for simplicity 
def health_status():
    return True, "Healthy - instance processing"
health.add_check(health_status)

# no-op - functionality removed for simplicity 
def application_data():
    return {"maintainer": "Maintaining team",
	        "git_repo": "sample"}
envdump.add_section("application", application_data)

# default landing page 
@app.route('/')
def home():
    return " <h2>Default app landing page - not used. </h2>      You probably want one of: <br />      <ul> <li>/healthcheck</li> <li>/environment</li> </ul>"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
#
# base data objects - # no-op - functionality removed for simplicity  and replaced with static string responses 

class UsageResponseSchema(Schema):
    # Add here to extend the response body ...
    message = fields.Str(default='Success')
    val = fields.Int(default=22)

class UsageRequestSchema(Schema):
    api_type = fields.String(required=True, description="API type")

class UsageAPI(MethodResource, Resource):  
    @doc(description='Usage API.', tags=['Usage'])  
    @marshal_with(UsageResponseSchema)  # marshalling with marshmallow library
    def get(self):
        '''
        Get method represents a GET API method
        '''
        return {'message': 'Sample GET for usage...'}


    @doc(description='Usage API.', tags=['Usage'])  
    # @use_kwargs(UsageResponseSchema, location=('json')) #version conflicts
    @use_kwargs(UsageResponseSchema)
    @marshal_with(UsageResponseSchema)  # marshalling
    def post(self, **kwargs):

        return {'message': 'Sample POST for usage...'}

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
# entrypoint 

api.add_resource(UsageAPI, '/usage')
docs.register(UsageAPI)


if __name__ == "__main__":
    if os.environ.get("USE_WERKZEUK") is not None:
        log.info("Running via werkzeug")
        app.run(debug=True)
    else:
        log.info("Running via waitress")
        serve(app, host='0.0.0.0', port=5000, threads=6)


