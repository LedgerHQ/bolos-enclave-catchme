# Ledger BOLOS Enclave bounty

A small game to motivate people to break an SGX [BOLOS Enclave](https://github.com/ledgerhq/bolos-enclave) - obtain a private key encrypted for your CPU loaded with BTC, and see if you can extract it.

The bounty is reasonably small to keep the hacks on the software side, feel free to contribute to it if you like it though.

# How to play 

 * Install [BOLOS Enclave](https://github.com/ledgerhq/bolos-enclave) (requires Intel Core CPU, Skylake or above)
 * Perform an attestation of the enclave against Ledger servers for key 1

On Linux :

```
python -m bolosenclave.endorsementSetupLedger --enclave linux/BolosSGX_signed.so --script scripts/endorsement_init.bin --key 1 --output key1Context.bin
```

On Windows :

```
python -m bolosenclave.endorsementSetupLedger --enclave windows/BolosSGX_signed.dll --script scripts/endorsement_init.bin --key 1 --output key1Context.bin
```
  * Run the bounty script to obtain your challenge

On Linux :

```
python run.py --enclave linux/BolosSGX_signed.so --context key1Context.bin
```

On Windows :

```
python run.py --enclave windows/BolosSGX_signed.dll --context key1Context.bin
```

  * Submit your challenge on [Ledger Slack](http://slack.ledger.co), channel #enclave and get a response - if you want to train on your own first, you can use remote/catchme_btc.py instead
  * Run the bounty script again to send the response and see the Bitcoin address associated to the bounty
  * Hax ?
  * Profit ? (please share a post mortem)  

## Contact

Developer Slack : http://slack.ledger.co in the #enclave channel

Mail : hello@ledger.fr
