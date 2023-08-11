import subprocess as sp
import pandas as pd

artigos = pd.read_csv("artigos_etica.csv",header=None) #lista csv com apenas doi
bibs = []

for a in artigos[0]:
	resultado = sp.getoutput('doi2bib '+ a)
	bib = "@"+resultado.split("@")[1]
	bibs.append(bib)
	
artigos[1] = bibs
artigos.to_csv("etica.csv", index=False)
