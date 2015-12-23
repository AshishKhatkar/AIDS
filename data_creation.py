from random import uniform, randint
pincode_file = open('distinct_pincode.csv', 'r')
with open('distinct_pincode.csv') as pincode_file, open('training_data.csv', 'w') as output_file:
	for idx, data in enumerate(pincode_file):
		if idx == 1000:
			break
		pincode = data.rstrip()
		pincode_success_rate = uniform(0, 1)
		for i in range(100):
			theft = randint(0, 1)
			online_or_cod = randint(0, 1)
			success_rate = uniform(0, 1)
			transaction_amt = randint(1, 10000)
			successful_transaction = randint(1, 100)
			if theft == 1:
				deliver = 0
			num = uniform(0, 1)
			if success_rate >= 0.2 and online_or_cod == 1:
				deliver = (num >= 0.1)
			elif success_rate >= 0.5:
				deliver = (num >= 0.3)
			else:
				deliver = (num >= 0.8)

			output = str(pincode) + ','
			output += str(pincode_success_rate) + ','
			output += str(theft) + ','
			output += str(online_or_cod) + ','
			output += str(success_rate) + ','
			output += str(transaction_amt) + ','
			output += str(successful_transaction) + ','
			output += str(int(deliver)) + '\n'
			output_file.write(output)
