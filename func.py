import io
import json
import logging
from string import Template
import oci
from oci.object_storage.models import CreatePreauthenticatedRequestDetails
from datetime import datetime, timedelta

from fdk import response

OBJECT_STORAGE_URL = "https://objectstorage.us-phoenix-1.oraclecloud.com"
UPLOAD_BUCKET = 'gregbucket'

def handler(ctx, data: io.BytesIO=None):
    # get 2 arguments from invoke: name and sessionid, for example {"name": "Greg", "sessionid":"S101"}
    try:
        body = json.loads(data.getvalue())
        name = body.get("name")
        sessionid = body.get("sessionid")
    except (Exception, ValueError) as ex:
        logging.error(str(ex))

    # create a PAR for bucket defined in UPLOAD_BUCKET
    signer = oci.auth.signers.get_resource_principals_signer()
    object_storage = oci.object_storage.ObjectStorageClient(config={}, signer=signer)
    time_expires = datetime.utcnow() + timedelta(minutes=5)
    par_details = CreatePreauthenticatedRequestDetails(name="par-"+name+"-"+sessionid, access_type='AnyObjectWrite', time_expires=time_expires )
    namespace = object_storage.get_namespace().data
    par = object_storage.create_preauthenticated_request(namespace, UPLOAD_BUCKET, par_details)
    par_url = OBJECT_STORAGE_URL + par.data.access_uri

    # prepare the HTML page to return to the user
    var_dict = { 'name':name, 'sessionid':sessionid, 'PAR_URL':par_url }
    html_file = open( 'fileupload.html' )
    templ_response = Template( html_file.read() )
    resp = templ_response.substitute(var_dict)

    # return the response in HTML
    return response.Response(
        ctx,
        response_data=resp,
        headers={"Content-Type": "text/html"}
    )
