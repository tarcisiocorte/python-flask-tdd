from protocols.http import HttpRequest, HttpResponse


class SignUpController:
    def handle(self, http_request: HttpRequest) -> HttpResponse:
        if not http_request.body.get("name"):
            return HttpResponse(
                status_code=400,
                body={"error": "Missing param: name"}
            )
        
        if not http_request.body.get("email"):
            return HttpResponse(
                status_code=400,
                body={"error": "Missing param: email"}
            )
        
        if not http_request.body.get("password"):
            return HttpResponse(
                status_code=400,
                body={"error": "Missing param: password"}
            )
        
        if not http_request.body.get("passwordConfirmation"):
            return HttpResponse(
                status_code=400,
                body={"error": "Missing param: passwordConfirmation"}
            )

        if http_request.body["password"] != http_request.body["passwordConfirmation"]:
            return HttpResponse(
                status_code=400,
                body={"error": "Password confirmation does not match password"}
            )

        return HttpResponse(
            status_code=200,
            body={"message": "User signed up successfully"}
        )
