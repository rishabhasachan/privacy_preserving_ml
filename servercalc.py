from linmodel import LinModel
import phe as paillier
import json

# GET THE ENCRYPTED DATA SEND BY THE CUSTOMER
def getData():
	with open('data.json', 'r') as file: 
		d=json.load(file)
	data=json.loads(d)
	return data

# PERFORM CALCUALTION BASED ON THE MODEL COFFIENTS CALCULATED FROM THE MODEL
def computeData():
	data=getData()
	mycoef=LinModel().getCoef()
	pk=data['public_key']
	pubkey= paillier.PaillierPublicKey(n=int(pk['n']))
	enc_nums_rec = [paillier.EncryptedNumber(pubkey, int(x[0], int(x[1]))) for x in data['values']]
	results=sum([mycoef[i]*enc_nums_rec[i] for i in range(len(mycoef))])
	return results, pubkey

# DUMP THE PUBLIC KEY AND RESULT
def serializeData():
	results, pubkey = computeData()
	encrypted_data={}
	encrypted_data['pubkey'] = {'n': pubkey.n}
	encrypted_data['values'] = (str(results.ciphertext()), results.exponent)
	serialized = json.dumps(encrypted_data)
	return serialized

#print(sum([data[i]*mycoef[i] for i in range(len(data))]))

# SAVE THE RESULT AND PUCLIC KEY INTO THE FILE (SENT BACK TO THE CUSTOMER)
def main():
	datafile=serializeData()
	with open('answer.json', 'w') as file:
		json.dump(datafile, file)

if __name__=='__main__':
	main()

