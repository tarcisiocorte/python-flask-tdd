class SignUpController:
    def handle(self, http_request):
        required_fields = ["name", "email", "password", "passwordConfirmation"]
        body = http_request.get("body", {})

        for field in required_fields:
            if field not in body or not body[field]:
                return {
                    "statusCode": 400,
                    "body": {"error": f"Missing param: {field}"}
                }

        if body["password"] != body["passwordConfirmation"]:
            return {
                "statusCode": 400,
                "body": {"error": "Password confirmation does not match password"}
            }

        return {
            "statusCode": 200,
            "body": {"message": "User signed up successfully"}
        }
