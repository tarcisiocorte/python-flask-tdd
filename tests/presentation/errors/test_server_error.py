from presentation.errors.server_error import ServerError


def test_server_error_hides_internal_exception_message():
    error = ServerError(Exception("database password leaked"))

    assert str(error) == "Internal server error"
    assert error.stack == "database password leaked"
