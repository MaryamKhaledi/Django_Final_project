from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('54727638452F3539534A567847594B597A6662527247624E6A6A447854737769305766736474634A4344493D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{code} کد تایید شما '
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)