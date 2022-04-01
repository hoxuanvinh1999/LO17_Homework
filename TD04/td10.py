from wsd import wsdData

data = wsdData('wsd-data1.txt',['NN','NNS','NNP','NNPS'],'resistance')
instances = data.getInstances()
for i in instances:
  print(i)
