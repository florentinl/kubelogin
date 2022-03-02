import datetime
import base64
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization


cert = open("ca.crt", "rb")
key = open("ca.key", "rb")
root_key = load_pem_private_key(key.read(), None, default_backend())
root_cert = x509.load_pem_x509_certificate(cert.read(), default_backend())

# Now we want to generate a cert from that root


def get_cert_and_key(username):
    cert_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    new_subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, username),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "viarezo")
    ])

    certificate = x509.CertificateBuilder().subject_name(
        new_subject
    ).issuer_name(
        root_cert.issuer
    ).public_key(
        cert_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=90)
    ).add_extension(
        x509.SubjectAlternativeName(
            [x509.DNSName(u"kube-master-1.test.viarezo.fr")]),
        critical=False,
    ).sign(root_key, hashes.SHA256(), default_backend())

    key = cert_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    cert = certificate.public_bytes(
        encoding=serialization.Encoding.PEM,
    )

    ca = root_cert.public_bytes(
        encoding=serialization.Encoding.PEM,
    )
    def prepare(string):
        return base64.encodebytes(string).decode("utf-8").replace("\n", "")
    return prepare(key), prepare(cert), prepare(ca)
