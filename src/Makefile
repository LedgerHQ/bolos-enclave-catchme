all:	catchme_btc	

%:	%.c
	moxiebox-gcc -O2 -mel $< -I$(BOLOS_SGX_SDK)/api -L$(BOLOS_SGX_SDK)/runtime -lbolos -o $@

clean:
	rm -rf catchme_btc


