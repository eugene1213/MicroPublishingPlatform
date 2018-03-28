from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def jwt_token_generator(user):
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token

# def password_reset_jwt_token_generatior(user):