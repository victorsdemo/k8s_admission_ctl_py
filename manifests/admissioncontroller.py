from flask import Flask, request, jsonify
import logging
import json

webhook = Flask(__name__)
webhook.logger.setLevel(logging.INFO)


# Our validation route to receive the webhook request.  We'll use this in our Admission Configuration K8s manifest
@webhook.route('/validate', methods=['POST'])
def validating_webhook():
    request_info = request.get_json()
    k8sobject = "K8s object"

    # Sneak preview into the schema.  The Unique ID for each request lives here
    uid = request_info["request"].get("uid")

    ####### Lets check the scheme of the k8sobject for something we can deny access on!  Perhaps check for privileged flag in the SecurityContext or using the 'latest" as an image tag
    # Serializing json
    request_json = json.dumps(request_info, indent=4)
    # To see the requests and create rules to start we will save the request to a file.  We can delete this for prod
    with open('/tmp/' + uid, 'w') as file:
        file.write(request_json)

    # Set a default of everything is blocked
    result = False

    ####### End of your code

    # Set the variable called 'result' of the check to True if the k8sobject passes and False if we should BLOCK the object from becoming persistent

    if result == True:

        response = f"\nAC Workshop cleared object {k8sobject} as compliant with admission policy.\n"
        webhook.logger.info(f'Object {k8sobject} passed security checks. Allowing the request.')

    else:
        response = f"\nAC Workshop found the object {k8sobject} in violation of admission policy.\n"
        webhook.logger.error(f'Object {k8sobject} failed security checks. Request rejected!')

    return admission_response(result, uid, response)

# a simple function to format our response. Reference: https://kubernetes.io/docs/reference/config-api/apiserver-admission.v1/
def admission_response(allowed, uid, message):
    return jsonify({"apiVersion": "admission.k8s.io/v1",
                    "kind": "AdmissionReview",
                    "response": {
                         "allowed": allowed,
                         "uid": uid,
                         "status": {
                           "code": 403,
                           "message": message
                         }
                       }
                    })


if __name__ == '__main__':
    webhook.run(host='0.0.0.0', port=1701)