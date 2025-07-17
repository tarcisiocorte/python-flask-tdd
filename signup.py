class SignUpController:
    def handle(self, http_request):
        body = http_request.get("body", {})
        if "name" not in body or not body["name"]:
            return {
                "statusCode": 400,
                "body": {"error": "Missing param: name"}
            }
        
        return {
            "statusCode": 200,
            "body": {"message": "User signed up successfully"}
        }
