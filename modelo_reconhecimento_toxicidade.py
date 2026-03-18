'''
Objetivo: reconhecer um texto quando é tóxico ou não. Tóxicos são textos que contém palavras de baixo calão, incentivo a violência, drogas entre outros.
Entrada: texto em português.
Saída: categoria da toxicidade: sim ou não. 
Obs: modelo pré-treinado usado unitary/toxic-bert. O código abaixo contém funções nativas para identificação de textos tóxicos.
Referência: https://huggingface.co/unitary/toxic-bert
Usaremos porém a biblioteca desenvolvida para isso: detoxify
'''
import detoxify



# each model takes in either a string or a list of strings

results = detoxify.Detoxify('portuguese').predict('example text')

#results = detoxify.Detoxify('unbiased').predict(['example text 1','example text 2'])

results = detoxify.Detoxify('multilingual').predict(['example text','exemple de texte','texto de ejemplo','testo di esempio','texto de exemplo','örnek metin','пример текста'])

# optional to display results nicely (will need to pip install pandas)

import pandas as pd

print(pd.DataFrame(results, index=input_text).round(5))
