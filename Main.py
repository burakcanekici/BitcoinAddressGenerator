import hashlib,base58,binascii,ecdsa, codecs

# Step1: Generate ECDSA Private Key")
ecdsaPrivateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
print("ECDSA Private Key: ", ecdsaPrivateKey.to_string().hex())
print("------------------------------------------------------")
# Step2: Generate ECDSA Public Key from value at Step#1
ecdsaPublicKey = '04' +  ecdsaPrivateKey.get_verifying_key().to_string().hex()
print("ECDSA Public Key: ", ecdsaPublicKey)
print("------------------------------------------------------")
# Step3: SHA256(value at Step#2)
hash256FromECDSAPublicKey = hashlib.sha256(binascii.unhexlify(ecdsaPublicKey)).hexdigest()
print("SHA256(ECDSA Public Key): ", hash256FromECDSAPublicKey)
print("------------------------------------------------------")
# Step4: RIDEMP160(value at Step#3)
ridemp160FromHash256 = hashlib.new('ripemd160', binascii.unhexlify(hash256FromECDSAPublicKey))
print("RIDEMP160(SHA256(ECDSA Public Key)): ", ridemp160FromHash256.hexdigest())
print("------------------------------------------------------")
# Step5: Prepend 00 as network byte to value at Step#4
prependNetworkByte = '00' + ridemp160FromHash256.hexdigest()
print("Prepend Network Byte to RIDEMP160(SHA256(ECDSA Public Key)): ", prependNetworkByte)
print("------------------------------------------------------")
# Step6: Apply SHA256 to value at Step#5 at 2 times to generate Checksum
hash = prependNetworkByte
for x in range(1,3):
    hash = hashlib.sha256(binascii.unhexlify(hash)).hexdigest()
    print("\t|___>SHA256 #", x, " : ", hash)
print("------------------------------------------------------")
# Step7: Get first 4 bytes of value at Step#6 as Checksum
cheksum = hash[:8]
print("Checksum(first 4 bytes): ", cheksum)
print("------------------------------------------------------")
# Step8: Append Checksum to value at Step#5
appendChecksum = prependNetworkByte + cheksum
print("Append Checksum to RIDEMP160(SHA256(ECDSA Public Key)): ", appendChecksum)
print("------------------------------------------------------")
# Step9: Generate Bitcoin Address with apply Base58 Encoding to value at Step#8
bitcoinAddress = base58.b58encode(binascii.unhexlify(appendChecksum))
print("Bitcoin Address: ", bitcoinAddress.decode('utf8'))
