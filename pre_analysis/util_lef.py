import os
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split ,cross_val_score, cross_validate
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from feature_engine.selection import DropCorrelatedFeatures


def ppp():
    print('u found me')

def explore_df_fillNAs_dropRrows(df):
    print('looking for NANs')
    print(df.isna().sum()) #183 NA in each column EXCEPT pp,blok, condition and timestamp
    df = df.dropna()
    print(df.isna().sum())
    print(df.shape) #(2956, 45)

    print('\n checking distribution of labels')
    Counter(df['Condition']) #{'I'nterruption: 959(32.44%), 'N'eutral: 941 (31,83%), 'T'ime pressure: 655 (22,16%), 'R'elax: 401 (13.57%)})
    (df['Condition'].value_counts()/df.shape[0]).plot(kind='bar', xlabel= 'labels', ylabel='counts')
    plt.ylabel('percentage')
    plt.title('distribution of labels')


    print('\n COrrelation matrix and cluster map: ')
    sns.clustermap(df.corr(), cmap="rocket_r")

    print('current shape: '+str(df.shape))
    df = df.loc[df['Condition'] !='R']
    
    print('new shape after dropping R rows: '+str(df.shape))
    return df 

    


#below function not checked/tested when dropping R rows!!
def prep_df_4clf(df, label_col, cols_2_drop, num_classes):
    df2 = df.copy()

    df2 = df2.dropna()
    
    df2 = df2.loc[df[label_col] !='R']
    print('number of R rows dropped: '+str(df.shape[0]-df2.shape[0]))
    
    
    if num_classes == 3:
        labels = df2[label_col].replace(["N", "I", "T"], ["N", "S1", "S2"])
    elif num_classes == 2:
        labels = df2[label_col].replace(["N", "I", "T"], ["N", "N", "S", "S"])
        

    df2 = df2.drop(columns=cols_2_drop)
    print(df2.shape) 

    
    #standardizing float columns (mean 0 and std 1)
    df2 = zScore_float_cols(df2)

    return df2,labels




def prep_df_4regr(df, label_col, cols_2_drop, num_classes):
    df2 = df.copy()
    print('original shape: ' +str(df.shape))

    df2 = df2.dropna()
    
    df2 = df2.loc[df[label_col] !='R']
    print('number of R rows dropped: '+str(df.shape[0]-df2.shape[0]))

    print('changing labels to numerical - number classes= '+ str(num_classes))
    if num_classes == 3:
        labels = df2[label_col].replace(["N", "I", "T"], [0, 1, 2])    
    elif num_classes == 2:
        labels = df2[label_col].replace(["N", "I", "T"], [0, 1, 1])

    print('dropping cols 2 drop')
    df2 = df2.drop(columns=cols_2_drop)
    print('new shape: ' +str(df2.shape))

    #removing characters from PP column to  be able to be handled by SVM
    #df2['PP'] = df2['PP'].str.replace(r"[a-zA-Z]",'')
    
    print('standardizing float columns (mean 0 and std 1)')
    df2 = zScore_float_cols(df2)
    print("DONE")

    return df2,labels




def zScore_float_cols(df):
    for col in  df.select_dtypes(include=[float]).columns:
        df[col] = (df[col]- df[col].mean())/df[col].std()
        # print('mean and std')
        # print(df[col].mean(), df[col].std())
    return df




def svm_cv (df, labels, shuffle, trainOnFullData):
    clf = svm.SVC(kernel='rbf', random_state=42)

    x_train, x_test, y_train, y_test = train_test_split(df, labels, test_size=0.20, shuffle=shuffle, random_state=42)

    scores = cross_val_score(clf, x_train, y_train, cv=10)
    print(scores)
    print("standard 10fold CV of SVM on shuffle="+str(shuffle)+" data gives accuracy of %f +- %f" %(scores.mean(), scores.std()))
    print('labels are: '+str(set(labels)))
    if trainOnFullData:
        print('now training on full data and predicting on test set(never seen before)')
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        print('\n classification  report on full data (run only once!)')
        print(classification_report(y_test, y_pred))
        print('\n confusion matrix on full data (run only once!)')
        print(confusion_matrix(y_test, y_pred))

        #GETTING FEAUTRE IMPORTANCE OF (trained) SVM with rbf kernel:
        importance = permutation_importance(clf, x_test, y_test, random_state=42)
        sorted_idx = importance.importances_mean.argsort()
        plt.barh(np.array(df.columns)[sorted_idx], importance.importances_mean[sorted_idx])
        #plt.xticks(rotation=90)
        plt.xlabel('permutation importance')
        plt.show()
        print("\n feature importance in increasing order:")
        print(np.array(df.columns)[sorted_idx])
    return scores, clf



#each row is 1 min. will increase window size sequentially and add this as a feature
#cols_list are the cols on which the rolling avg will be computed.
#CURRENTLY WRONG-SHOULD DO IT PER pp!
def make_movingAvg_col(df, row_window, cols_lst ):
    out_df = df.copy()
    #print((cols_lst))
    for col_name in cols_lst:
        #print(col_name)
        
        new_col = col_name + '_avg'+ str(row_window)+'rows'
        
        #print(out_df.columns)

        out_df[new_col] = out_df[col_name].rolling(row_window).mean()

        #print(out_df.columns)
        #print('for window size of %f, total NAs detected: %f' %(row_window, out_df.isna().sum().sum()))
    out_df = out_df.dropna()
    return out_df

#x axis is a list of x values(rolling window for example) and
#acc_lst is a list of lists: 1st inner list contains the 10fold CV for the 1st element of x axis, etc
def plot_CV_accuracies(acc_lst, xaxis):
     #getting avg and std over the 10fold CV
    avg = np.array([x.mean() for x in acc_lst])
    std = np.array([x.std() for x in acc_lst])

    plt.subplot(111)
    plt.plot(xaxis, avg)
    plt.fill_between(xaxis, (avg+std), (avg-std), alpha = 0.2)
    plt.xlabel('window size') ; plt.ylabel('accuracy')
    plt.show()


def replace_correlatedCols_with_their_mean(df):
    df2 = df.copy()
    dropper = DropCorrelatedFeatures(method='pearson', threshold=0.8)
    dfcorr = dropper.fit_transform(df2) #dfcorr has removed all but 1 from each correlated col set

    corr_sets = dropper.correlated_feature_sets_
    #making avg of correlated columns and dropping them
    for colset in corr_sets:
        print('dealing with correlated columns: '+str(colset))
        new_name = 'avg_'+'+'.join(x for x in colset)
        df2[new_name] = df[list(colset)].mean(axis=1)
        df2 = df2.drop(list(colset), axis =1)
    return df2

