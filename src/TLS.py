
import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
from resources import *
import multiprocessing as mp

CPUS = 10
assert CPUS < mp.cpu_count() - 1


def allAucWrapper(self:PairwiseCorrMatrix,  yColumnNameList:list[str], label:str, proxyColumnList:list[str], ascendingList:list[bool], filepath:str = None ):

    self.aucsCalculator(yColumnNameList= yColumnNameList, label= label, proxyColumnList=proxyColumnList, ascendingList = ascendingList, filepath = filepath)

glsCorrs:PairwiseCorrMatrix = read(PATH + '/datasetsTese/glsPairwiseCorr.pickle.gz')
pearsonCorrs:PairwiseCorrMatrix = read(PATH + '/datasetsTese/baseModelFiltered.pickle.gz') # R
pearsonCorrs.data=pearsonCorrs.data.rename(columns= {'globalCorrelation': 'pearsonR'})
vaeGLSCorrs:PairwiseCorrMatrix = read(PATH + '/datasetsTese/VAEGLSPairCorr.pickle.gz') # gls + vae
vaeGLSCorrs.data=vaeGLSCorrs.data.rename(columns= {'glsCoefficient': 'beta'})
vaePearsonCorrs:PairwiseCorrMatrix = read(PATH + '/datasetsTese/VAEPearsonPairCorr.pickle.gz') # R + vae

print('Loading Completed')

#Add all aucs
pairwiseCorrs = [glsCorrs, pearsonCorrs, vaeGLSCorrs, vaePearsonCorrs]
yColumnLists = [['corum', 'corum'],['corum', 'corum'],['corum', 'corum'],['corum', 'corum']]
proxyColumnLists = [['pValue', 'beta'],['pValue', 'pearsonR'],['pValue', 'beta'],['pValue', 'pearsonR']]
ascendingLists = [[True, False],[True, 'pearsonR'],[True, False],[True, False]]
labels = ['gls', 'pearson', 'VAE-GLS', 'VAE-pearson']
filepaths= [PATH + '/datasetsTese/glsPairwiseCorr.pickle.gz', PATH + '/datasetsTese/baseModelFiltered.pickle.gz', PATH + '/datasetsTese/VAEGLSPairCorr.pickle.gz', PATH + '/datasetsTese/VAEPearsonPairCorr.pickle.gz']

with mp.Pool(CPUS) as process:
    process.starmap(allAucWrapper, zip(pairwiseCorrs, yColumnLists, labels, proxyColumnLists, ascendingLists, filepaths)) 



# glsCorrs.aucCalculator('corum', 'gls','pValue', True)
# glsCorrs.aucCalculator('corum', 'gls','beta', False)
# print(glsCorrs)
# glsCorrs.write(PATH + '/datasetsTese/glsPairwiseCorr.pickle.gz')

# pearsonCorrs.aucCalculator('corum', 'pearson','pValue', True)
# pearsonCorrs.aucCalculator('corum', 'pearson','beta', False)
# print(pearsonCorrs)
# pearsonCorrs.write(PATH + '/datasetsTese/baseModelFiltered.pickle.gz')

# vaeGLSCorrs.aucCalculator('corum', 'VAE-GLS','pValue', True)
# vaeGLSCorrs.aucCalculator('corum', 'VAE-GLS','beta', False)
# print(vaeGLSCorrs)
# vaeGLSCorrs.write(PATH + '/datasetsTese/VAEGLSPairCorr.pickle.gz')

# vaePearsonCorrs.aucCalculator('corum', 'VAE-pearson','pValue', True)
# vaePearsonCorrs.aucCalculator('corum', 'VAE-pearson','beta', False)
# print(vaePearsonCorrs)
# vaePearsonCorrs.write(PATH + '/datasetsTese/VAEPearsonPairCorr.pickle.gz')





# tlsResidualsMatrix = proteomics.tlsResidues(glsPairwise)
# print(glsPairwise.data.loc[glsPairwise.data['p-value'] > 0])
# print(tlsResidualsMatrix.data.shape)
# print(tlsResidualsMatrix.data.isna().sum().sum())

