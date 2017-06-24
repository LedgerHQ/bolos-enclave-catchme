"""
*******************************************************************************
*   BOLOS Enclave Samples
*   (c) 2017 Ledger
*
*  Licensed under the Apache License, Version 2.0 (the "License");
*  you may not use this file except in compliance with the License.
*  You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
*  Unless required by applicable law or agreed to in writing, software
*  distributed under the License is distributed on an "AS IS" BASIS,
*  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
*  See the License for the specific language governing permissions and
*  limitations under the License.
********************************************************************************
"""

from ledgerblue.ecWrapper import PublicKey, PrivateKey
import hashlib
import binascii
import sys
import pysodium
import os

ATTESTATION = "04502c2f1660ee9209247271a60f26dedc6b96f298aeda684855a9db1a0fc098fef0d48ac8e512df00b7511f75f9b56bcd52cf5510ccf744a5c113ae314e9f4742".decode('hex')
CODEHASH = "14bd272e704351712ffab3cbe3768d3419245e2b478c803e5731e13d7bda0472".decode('hex')

# 04db4693a6ba5d75cdab1f30fae741bb534e05d1e8a96dbc988579078c9f38ae82ef7525da06ee20a32ff80b16386d08d18ce75243c41183d0dd06e73289acd0a6
SECRET = "7b2afd4370db330399ade4e776a328b9cda43369e9a1f51bf948a8b4430621d2".decode('hex')

data = bytearray(sys.argv[1].decode('hex'))

offset = 0
ephemeralPublic = data[offset : offset + 65]
offset = offset + 65
endorsementKey = data[offset : offset + 65]
offset = offset + 65
endorsementSignatureLength = data[offset + 1] + 2
endorsementSignature = data[offset : offset + endorsementSignatureLength]
offset = offset + endorsementSignatureLength
codeSignatureLength = data[offset + 1] + 2
codeSignature = data[offset : offset + codeSignatureLength]
offset = offset + codeSignatureLength
blob = data[offset:]

m = hashlib.sha256()
m.update(chr(0xFE))
m.update(str(endorsementKey))
digest = m.digest()

publicKey = PublicKey(bytes(ATTESTATION), raw=True)
signature = publicKey.ecdsa_deserialize(bytes(endorsementSignature))
if not publicKey.ecdsa_verify(bytes(digest), signature, raw=True):
	raise Exception("Attestation key signature not verified")

m = hashlib.sha256()
m.update(str(ephemeralPublic))
m.update(CODEHASH)
digest = m.digest()

publicKey = PublicKey(bytes(endorsementKey), raw=True)
signature = publicKey.ecdsa_deserialize(bytes(codeSignature))
if not publicKey.ecdsa_verify(bytes(digest), signature, raw=True):
	raise Exception("Endorsement not verified")

ephemeralPublicKey = PublicKey(bytes(ephemeralPublic), raw=True)
privateKey = PrivateKey()
secret = ephemeralPublicKey.ecdh(bytes(privateKey.serialize().decode('hex')))

nonce = os.urandom(pysodium.crypto_secretbox_NONCEBYTES)
sealed = pysodium.crypto_secretbox(str(SECRET), str(nonce), str(secret))

result = str(blob) + str(privateKey.pubkey.serialize(compressed=False)) + str(nonce) + str(sealed)

print result.encode('hex')

