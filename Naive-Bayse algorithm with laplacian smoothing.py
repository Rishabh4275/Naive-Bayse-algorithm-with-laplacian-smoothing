#py2.7
import pandas as pd
import sys
import csv
tennis = pd.read_csv('Q2-tennis.csv')

def prob(wth):
    yprob=1
    nprob=1
    probab= dict()
    for x in tennis.columns:
        if x!='Play':
            probab = probvar(x,wth)
            yprob= yprob*float(probab['yes'])
            nprob= nprob*float(probab['no'])
    table = pd.crosstab(index = 'count',columns = tennis['Play'])
    noprob= (float(table['no'].sum())+float(wth['k']))/(float(table['yes'].sum()+table['no'].sum())+(2.0*float(wth['k'])))
    yesprob= (float(table['yes'].sum())+float(wth['k']))/(float(table['yes'].sum()+table['no'].sum())+(2.0*float(wth['k'])))
    typrob = yesprob*yprob
    tnprob= noprob*nprob
    typprob=typrob*100/(typrob+tnprob)
    tnpprob=tnprob*100/(typrob+tnprob)
    print typprob
    print tnpprob
    if typprob>tnpprob:
        wth['Play']='Yes'
        print 'Will Play today'
    else:
        wth['Play']="No"
        print "Won't Play today"
    wth['yes']=typprob
    wth['no']=tnpprob
    pr=[wth['Outlook'],wth['Temp.'],wth['Humidity'],wth['Windy'],wth['yes'],wth['no'],wth['Play']]
    return pr

def probvar(x,wth):
    table = pd.crosstab(index=tennis[x],columns=tennis['Play'],margins=True)
    nume=float(table.at[wth[x],'yes']) + float(wth['k'])
    if x in "Outlook" or "Temp.":
        c=3
    else:
        c=2
    c=float(c)*float(wth['k'])
    denom=float(table.at['All','yes']) + c
    ind = dict()
    ind['yes'] = nume/denom
    nume=float(table.at[wth[x],'no']) + float(wth['k'])
    denom=float(table.at['All','no']) + c
    ind['no'] = nume/denom
    return ind


def ch(wth):
    wth['Outlook']=wth['Outlook'].lower()
    wth['Temp.']=wth['Temp.'].lower()
    wth['Humidity']=wth['Humidity'].lower()
    wth['Windy']=wth['Windy'].lower()
    wth['Outlook'].strip()
    wth['Temp.'].strip()
    wth['Humidity'].strip()
    wth['Windy'].strip()
    if  not (wth['Outlook'] in "sunny" or "overcast" or "rainy"):
        print "Faulty data entered"
        sys.exit()
    if  not (wth['Temp.'] in "hot" or "mild" or "cool"):
        print "Faulty data entered"
        sys.exit()
    if  not (wth['Humidity'] in "high" or "normal"):
        print "Faulty data entered"
        sys.exit()
    if  not (wth['Windy'] in "true" or "false"):
        print "Faulty data entered"
        sys.exit()
    try:
        complex(wth['k'])
    except:
        print "Invalid value for k"
        sys.exit()
    if wth['Windy']=="true":
        wth['Windy']="true "
    if wth['Windy']=="false":
        wth['Windy']="false "
    return wth


wth=dict()
read=raw_input("If you want to enter test data through csv file with extension .csv else type No")
try:
    with open(read, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)

        with open('Result.csv', 'wb') as outfile:
            spamwriter = csv.writer(outfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["Outlook","Temp.","Humidity","Windy","Yes","No","Play"])
                

            
            for row in reader:
                wth['Outlook']=row['Outlook']
                wth['Temp.']=row['Temp.']
                wth['Humidity']=row['Humidity']
                wth['Windy']=row['Windy']
                try:
                    wth['k']=row['k']
                except:
                    wth['k']=raw_input("Enter the value of k for laplacian smoothing")
                wth=ch(wth)
                pr=prob(wth)
                spamwriter.writerow(pr)


    
except IOError:
    wth['Outlook']=raw_input("Enter the outlook as sunny or overcast or rainy")
    wth['Temp.']=raw_input("Enter the outlook as hot or mild or cool")
    wth['Humidity']=raw_input("Enter the outlook as high or normal")
    wth['Windy']=raw_input("Enter the outlook as true or false")
    wth['k']=raw_input("Enter the value of k for laplacian smoothing")
    wth=ch(wth)
    prob(wth)
    

