# Data-analysis ploting results for report about injuries in traffic in Berlin
# by Prenzlverkehr
# Sören Bergmann
# Contact: bergmann@prenzlverkehr.de

import pandas as pd
import sys
import matplotlib.pyplot as plt
import numpy as np
print(sys.version)


def import_pol_data_csv(inj):
    # function import and analyses the police data for accidents.
    # Input:
    #   inj: Int, 0= all Accidents, 1=Accidents with death, 2=Accidents with severely injured people, 3=Accidents with lightly injured people
    # Output:
    #   dfAccMatrix: DataFrame with number of accidents (numeric) for each vehicle tuple. Is organized as square matrix, Index gives the subject, columns the second accident member
    #   dfImportInfo: DataFrame with Information about the import: Total number of accidents, Number of accidents with one/two/three/four members.
    dfAccidentData = pd.read_csv('accidentdata.csv')
    dfAccidentData = dfAccidentData.rename(columns={"IstRad": "Fahrrad", "IstPKW": "PKW", "IstFuss": "Fuss",
                                           "IstGkfz": "GKfz", "IstKrad": "KRad", "IstSonstig": "Sonstige"})
    indcol = ['Fahrrad', 'PKW',   'Fuss', 'KRad', 'GKfz',  'Sonstige']
    dfAccMatrix = pd.DataFrame(0, columns=indcol, index=indcol)
    dfImportInfo = pd.DataFrame(columns=['Name', 'Value'], index=['Total_Number', 'Double', 'Triple', 'Quadrupel'])
    dfImportInfo.loc['Total_Number', 'Value'] = len(dfAccidentData)
    data = []
    if inj > 0:
        dfAccidentData = dfAccidentData[dfAccidentData.loc[:, 'UKATEGORIE'] == inj]

    while True:
        ind = dfAccidentData.first_valid_index()
        t = dfAccidentData.loc[ind, 'Fahrrad':'Sonstige'][dfAccidentData.loc[ind, 'Fahrrad':'Sonstige'] == 1].index
        index = dfAccidentData[(dfAccidentData.loc[:, 'Fahrrad'] == dfAccidentData.loc[ind, 'Fahrrad'])
                               & (dfAccidentData.loc[:, 'PKW'] == dfAccidentData.loc[ind, 'PKW'])
                               & (dfAccidentData.loc[:, 'Fuss'] == dfAccidentData.loc[ind, 'Fuss'])
                               & (dfAccidentData.loc[:, 'KRad'] == dfAccidentData.loc[ind, 'KRad'])
                               & (dfAccidentData.loc[:, 'GKfz'] == dfAccidentData.loc[ind, 'GKfz'])
                               & (dfAccidentData.loc[:, 'Sonstige'] == dfAccidentData.loc[ind, 'Sonstige'])].index
        if len(t) == 1:
            dfAccMatrix.loc[t[0], t[0]] = len(index)
        if len(t) == 2:
            dfAccMatrix.loc[t[0], t[1]] = len(index)
            dfAccMatrix.loc[t[1], t[0]] = len(index)
        else:
            pass
        data.append([t, len(index)])
        dfAccidentData = dfAccidentData.drop(index).reset_index(drop=True)
        if len(dfAccidentData) == 0:
            break

    dfData = pd.DataFrame(data, columns=['Index', 'Count'])
    dfData['Len'] = dfData['Index'].apply(len)
    dfImportInfo = dfData.groupby(['Len'])['Count'].sum()
    # dfAccMatrix.to_csv(filename)
    return dfAccMatrix, dfImportInfo


def aufrebbeln(dfAccMatrix):
    # Input: dfAccMatrix. Dataframe, nxm- Matrix. The result of the accident analysis
    # Output: dfAccList. Dataframe, Each entry of the matrix is separated, the column and index names of the entries are combined to the index name.
    myrows = (len(dfAccMatrix)*(len(dfAccMatrix)+1))/2
    dfAccList = pd.DataFrame([], columns=['VM1', 'VM2', 'Acc'], index=range(0, int(myrows)))
    counter = 0
    for k in range(0, len(dfAccMatrix)):
        for s in range(k, len(dfAccMatrix.columns)):
            dfAccList.iat[counter, 2] = dfAccMatrix.iloc[k, s]
            dfAccList.iat[counter, 0] = dfAccMatrix.index[k]
            dfAccList.iat[counter, 1] = dfAccMatrix.columns[s]
            counter += 1
    return dfAccList


def stacked_bar_horizontal(dfData, x_label, y_label, filename):
    # Generates the graphs fpr the report.
    # Input:
    # dfData: DataFrame, Plotdata
    # x_label: str, Label of X-axis
    # y_label: str, Label of Y-axis
    # filename: Name and path of the resulting file
    # Output: png-file

    print(len(dfData.columns))
    my_width = 0.8       # the width of the bars: can also be len(x) sequence
    colors = [plt.cm.Accent(i/float(len(dfData.columns))) for i in range(0, len(dfData.columns))]
    fig, ax = plt.subplots()
    # ax = fig.add_subplot(axes_class=axisartist.Axes)
    fig.set_figheight(5)
    fig.set_figwidth(8)
    columns = dfData.columns
    index = dfData.index
    sum = np.zeros(len(index))

    for t in range(0, len(columns)):
        rects = ax.barh(index, dfData.iloc[:, t], my_width, left=sum, label=columns[t], color=colors[t], align='center')
        sum = sum+dfData.iloc[:, t]
        # ax.bar_label(rects, label_type='center')

    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.xticks(rotation=0)
    plt.yticks(fontsize=10)
    ax.legend(ncol=len(dfData.columns), bbox_to_anchor=(0, 1),
              loc='lower left')
    # ax.axis["left"].major_ticklabels.set_ha("left")
    fig1 = plt.gcf()
    fig1.tight_layout()
    plt.draw()
    fig1.savefig(filename, dpi=100)


def analysis_results(strPicturePath):
    # creates datasets and plots needed for the report of injuries in Berlin in traffic. With setting the variables at the beginning to "True" you can turn on/off the creation
    # Input: strPicturePath: String with path where the plots should be stored.
    # Output: Depends on settings, tables and graphs.
    plot_abs_severity = False  # stacked bar plot of numbers of accidents with death / severe / lightly injrued for each tupel
    plot_pc_severity = True  # stacked bar plot of percentage of death / severe / lightly injrued for each tupel
    table_pc_severity = True  # table with absolute und percentages of injuries in traffic.

    def tupel_prep():
        # preparation of data for further use: Renaming columns, Combining matrices, dropping irrelevant rows, sorting, rounding, etc.
        dftotal = aufrebbeln(import_pol_data_csv(0)[0])
        dftotal = dftotal.rename(columns={"Acc": "Total"})
        dfdeath = aufrebbeln(import_pol_data_csv(1)[0])
        dfdeath = dfdeath.rename(columns={"Acc": "Tote"})
        dfsevinj = aufrebbeln(import_pol_data_csv(2)[0])
        dfsevinj = dfsevinj.rename(columns={"Acc": "Schwerverletzte"})
        dflightinj = aufrebbeln(import_pol_data_csv(3)[0])
        dflightinj = dflightinj.rename(columns={"Acc": "Leichtverletzte"})
        dfanalysis = dftotal.copy()
        dfanalysis = pd.concat([dfanalysis, dfdeath.Tote, dfsevinj.Schwerverletzte, dflightinj.Leichtverletzte], axis=1)
        dfanalysis['Tupel'] = dfanalysis.VM1+' vs. '+dfanalysis.VM2
        dfanalysis = dfanalysis.drop(columns=['VM1', 'VM2'])
        dfanalysis = dfanalysis[['Tupel', 'Total', 'Tote', 'Schwerverletzte', 'Leichtverletzte']]
        dfanalysis = dfanalysis.set_index('Tupel')
        dfanalysis_percent = dfanalysis[['Tote', 'Schwerverletzte', 'Leichtverletzte']].div(dfanalysis['Total'].values, axis=0)*100
        dfanalysis = dfanalysis.drop(columns='Total').sort_values(by=['Schwerverletzte', 'Leichtverletzte'])
        dfanalysis_percent = dfanalysis_percent.sort_values('Leichtverletzte').dropna().astype(float).round(1)
        return dfanalysis, dfanalysis_percent

    # Creating plots and tables
    if plot_abs_severity is True:
        dfanalysis = tupel_prep()
        print(dfanalysis.to_latex())
        stacked_bar_horizontal(dfanalysis, 'Anzahl', '', strPicturePath+'severity_abs')
        pass

    if plot_pc_severity is True:
        dfanalysis, dfanalysis_percent = tupel_prep()
        print(dfanalysis_percent.to_latex())
        stacked_bar_horizontal(dfanalysis_percent, 'Anteil in %', '', strPicturePath+'severity_percentage')

    if table_pc_severity is True:
        dfanalysis, dfanalysis_percent = tupel_prep()
        dfanalysis = pd.concat([dfanalysis, dfanalysis_percent], axis=1)
        print(dfanalysis.to_latex())


if __name__ == "__main__":
    # main function, calls the analysis functions.
    strPicturePath = '/Users/sorenbergmann/Documents/15_PrenzlVerkehr/15_Alternative_Mobilitätsberichterstattung/Berechnungen/Darstellungen/'
    analysis_results(strPicturePath)
    plt.show()
