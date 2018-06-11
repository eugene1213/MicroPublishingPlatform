import requests

class BootpayApi:

    base_url = 'https://api.bootpay.co.kr/'
    url_confirm = base_url + 'receipt/'
    url_cancel = base_url + 'cancel'

    def __init__(self, application_id, private_key):
        self.application_id = application_id
        self.pk = private_key

    def cancel(self, receipt_id, name, reason):
        url = self.url_cancel
        payload = {'application_id': self.application_id,
                   'private_key': self.pk,
                   'receipt_id': receipt_id,
                   'name': name,
                   'reason': reason}

        return requests.post(url, data=payload)

    def confirm(self, receipt_id):
        url = self.url_confirm + receipt_id
        payload = {'application_id': self.application_id, 'private_key': self.pk}
        return requests.get(url, params=payload)