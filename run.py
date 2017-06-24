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

import argparse
import os
import os.path
from bolosenclave.bolosEnclaveLink import BolosEnclaveLink
from bolosenclave.bolosEnclave import BolosEnclave

SCRIPT_FILE = "release/catchme_btc"
SCRIPT_SIGNATURE = "304402202ad8eb93458200c477b2c31b51c4d468079274100a646ff6ae37e67a90e2612b022049f081cc8724f885313717fdcbba3a54cd605c8b487f7acc5fc127086bc196b9".decode('hex')

parser = argparse.ArgumentParser()
parser.add_argument("--debug", help="Display debug information", action='store_true')
parser.add_argument("--debugEnclave", help="Run enclave in debug mode", action='store_true')
parser.add_argument("--enclave", help="Enclave to use")
parser.add_argument("--context", help="Persistent context to use")


args = parser.parse_args()

if args.enclave == None:
	raise Exception("No enclave specified")     
if args.context == None:
	raise Exception("No context specified")


link = BolosEnclaveLink(args.enclave, args.debugEnclave, args.debug)
f = open(args.context, "rb")
ctx = f.read()
f.close()
link.set_persistent_context(ctx)

app = BolosEnclave(link)
app.openSession()

if not os.path.isfile("request.bin") and not os.path.isfile("key.bin"):
	scriptFile = open(SCRIPT_FILE, "rb")
	response = app.loadElf(scriptFile, parameters=chr(01), signature=SCRIPT_SIGNATURE)
	scriptFile.close()
	f = open("request.bin", "wb")
	f.write(response['response'])
	f.close()
	print "Challenge " + str(response['response']).encode('hex')
elif os.path.isfile("request.bin"):
	challengeResponse = raw_input("Enter challenge response (hex encoded): ").decode('hex')	
	scriptFile = open(SCRIPT_FILE, "rb")
	os.remove("request.bin")
	response = app.loadElf(scriptFile, parameters=chr(02) + challengeResponse, signature=SCRIPT_SIGNATURE)
	scriptFile.close()
	f = open("key.bin", "wb")
	f.write(response['response'])
	f.close()

if os.path.isfile("key.bin"):
	f = open("key.bin", "rb")
	key = f.read()
	f.close()
	scriptFile = open(SCRIPT_FILE, "rb")
	response = app.loadElf(scriptFile, parameters=chr(03) + key, signature=SCRIPT_SIGNATURE)
	scriptFile.close()
	print "Bounty address %s" % str(response['response'])

app.closeSession()
link.close()
