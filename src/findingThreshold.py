import pandas as pd
import seaborn as sb
import numpy as np
from sklearn.metrics import auc
import matplotlib.pyplot as plt
import utils
from sklearn.metrics import auc
from classes import ppiDataset


from env import PATH
RANDOMSTATE = 42

proteinsData = pd.read_csv(PATH+'/datasetsTese/proteomicsDataTrans.csv', index_col='modelID')

# pairwiseCorrData = pd.read_csv(PATH+'/datasetsTese/BaseModelPairwise.csv', index_col='PPI')


# What Professor Pedro did not ask For :( 

def getAUCvsThresholdPlot(pairwiseCorrData:pd.DataFrame) -> None:

    # find the best count threshold n
    best = True
    previousAUC = 0
    threshold = 2
    aucList=[]
    thresholdList =[]
    while threshold < 101:
        
        queriedPairCorrData = pairwiseCorrData.query('counts > @threshold')
        corrCumSum = np.cumsum(queriedPairCorrData['Corum']) / np.sum(queriedPairCorrData['Corum'])
        indexes = np.array(queriedPairCorrData.reset_index().index) / queriedPairCorrData.shape[0]
        currentAUC = auc(indexes, corrCumSum)
        #Update Lists for Curve plot
        aucList.append(currentAUC)
        thresholdList.append(threshold)
        
        
        if best and currentAUC < previousAUC:
            bestPairwuiseFrequency = threshold-1
            best = False
            print('The limit threshold of interactions were we start to lose information after increasing it is: ' + str(threshold-1) + '\n with an auc of ' + str(previousAUC))
        # print(str(currentAUC) + '>=' + str(previousAUC) + '\n' + str(best))
        threshold += 1
        previousAUC = currentAUC


    # make chart with auc per n threshold

    _, ax = plt.subplots(1, 1, figsize=(4, 3), dpi=600)
    ax.plot(
        thresholdList,
        aucList,
        c='green',
    )
    ax.plot([0,100],[0.78,0.78], "r--", label='AUC == 0.78',lw=0.7)
    ax.plot([bestPairwuiseFrequency,bestPairwuiseFrequency],[0,1], "b--", label='max n==' + str(bestPairwuiseFrequency),lw=0.6)

    ax.legend(loc="lower right", frameon=False)
    ax.set_ybound(lower=0.6, upper=0.9)
    ax.set_ylabel("Area Under the Curve")
    ax.set_xlabel("Minimum interaction threshold")
    ax.set_title('AUC vs sample frequency of PPI threshold')
    ax.grid(True, axis="both", ls="-", lw=0.1, alpha=1.0, zorder=0)

    plt.savefig("thresholdVSAUC.png",
                bbox_inches="tight")
    

# getAUCvsThresholdPlot(pairwiseCorrData)

    # What Professor Pedro Asked For :)
def randomSubSamplingAUC(proteinsData: pd.DataFrame, subsampleSizes: list[int], repeats: int):
    import time

    proteinsData:pd.DataFrame = proteinsData.copy()
    corum = ppiDataset(filename=PATH + '/externalDatasets/corumPPI.csv.gz')
    corum = corum.getPPIs(True)
    allAUC = pd.DataFrame()
    
    
    # Random Sampling
    for sampleNum in subsampleSizes:

        iteration = 0
        aucList = list()
        while iteration < repeats:
            print(str(iteration) + ' - Iteration')
            print(str(repeats) + ' - repeats')

            proteinsDatSample = proteinsData.sample(n = sampleNum, axis=0, random_state=RANDOMSTATE)
            pairwiseCorr = utils.getPairwiseCorrelation(
                proteinsDatSample, None, str(sampleNum) + ' samples', False)
            del proteinsDatSample
            start =time.time()
            pairwiseCorr = utils.addGroundTruth(corum, pairwiseCorr.iloc[100000:120000], 'corum', None)
            end = time.time()
            print(end-start)
            

            corrCumSum = np.cumsum(pairwiseCorr['corum']) / np.sum(pairwiseCorr['corum'])
            indexes = np.array(pairwiseCorr.reset_index().index) / pairwiseCorr.shape[0]
            AUC = auc(indexes, corrCumSum)
            aucList.append(AUC)
            del pairwiseCorr
            iteration += 1
        
        print(aucList)
        allAUC[str(sampleNum)] = aucList

    # Plot each AUC in the various boxplot chart
    ax = allAUC.plot(kind='box')
    ax.plot([0, 100], [0.70, 0.70], label= 'AUC == 0.7')
    ax.plot([0, 100], [0.76, 0.76], label='Baseline Model, 0.76')
    ax.set_ylabel("AUC")
    ax.set_xlabel("Sampling Number") 
        
    plt.savefig("aucPerSamplingNumber.png",
                bbox_inches="tight")
        


randomSubSamplingAUC(proteinsData, [5], 5)
