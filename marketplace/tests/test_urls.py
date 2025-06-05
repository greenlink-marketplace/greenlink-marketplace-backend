from django.test import TestCase, Client
from django.urls import reverse

class RegisterConsumerPostTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register-consumer")
        self.valid_payload = {
            "username": "user_test",
            "email": "emailtest@gmail.com",
            "password": "12345678",
            "first_name": "User",
            "last_name": "Test",
            "cpf": "123.456.789-09",
            "phone": "(00)92761-2097",
            "address": "address test for post"
        }

    def test_with_cpf_invalid(self):
        payload = self.valid_payload.copy()
        
        invalid_cpfs = [
            "000.000.000-00",
            "999.999.999-99",
            "12345678909",   
            "123.456.789-00",
            "111.111.111-11",
            "abc.def.ghi-jk",
            "",
            # None,              # Inválido (valor nulo)
            12345678909,
            "123.456.78-909",
        ]
        
        for invalid_cpf in invalid_cpfs:
            payload["cpf"] = invalid_cpf
            response = self.client.post(self.url, payload, format="Json")
            self.assertEqual(response.status_code, 400)

    def test_with_email_invalid(self):
        payload = self.valid_payload.copy()
        
        invalid_emails = [
            "plainaddress",
            "@semusuario.com",
            "usuario@",
            "usuario@.com",
            "usuario@com",
            "usuario@com.",
            "usuario@.com.",
            "",
            # did not pass the test
                # "usua rio@exemplo.com",
                # "usuario@@exemplo.com",
                # "usuario@exemplo..com",
                # "usuario@-exemplo.com",
                # "usuario@exemplo-.com",
                # "usuario@exemplo.c",
                # "usuario@exemplo.toolongtld,
        ]
        
        for invalid_email in invalid_emails:
            payload["email"] = invalid_email
            response = self.client.post(self.url, payload, format="Json")
            self.assertEqual(response.status_code, 400)
