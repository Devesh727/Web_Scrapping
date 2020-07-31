#CODE TO SCRAP THE DATA 
import requests
import os
import csv
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def clg_location(college):
    data={'Amravati':'1','Aurangabad':'2','Mumbai':'3','Nagpur':'4','Nashik':'5','Pune':'6'}
    url='http://www.dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID='+data[college]+'&RegionName='+college
    headers={'User-Agent':'Mozilla/5.0'}
    response=requests.get(url,headers=headers)
    if(response.status_code!=200):
        print("Error to load the website.")
        return False
    print(college,'-Data is getting scraped' '\n')
    soup=BeautifulSoup(response.content,'html.parser')
    stat_table=soup.find_all('table',class_='DataGrid')
    stat_table=stat_table[0]
    count=0
    with open('folder.txt','w') as r:
        for row in stat_table.find_all('tr'):
            d=[]
            for cell in row.find_all('td'):
                d.append(cell.text)

            
            
            if(len(d)<2):
                continue
            
            elif('technical' in d[2].lower() or 'engineering' in d[2].lower() or 'technological' in d[2].lower()or 'institute of technology' in d[2].lower()):    
                r.write("    ".join(d))
                r.write('\n')
                count+=1
              
        
    return True        

def eng_clg(code):
    url='http://dtemaharashtra.gov.in/frmInstituteSummary.aspx?InstituteCode='+str(code)
    headers={'User-Agent':'Mozilla/5.0'}
    response=requests.get(url,headers=headers)
    if(response.status_code!=200):
        return False
    else:
        soup=BeautifulSoup(response.content,'html.parser')
        stat_table=soup.find_all('table',class_='AppFormTable')

        stat_table=stat_table[0]
        with open('folder1.txt','w') as r:
            for row in stat_table.find_all('tr'):
                for cell in row.find_all('td'):
                    r.write(cell.text.ljust(28))
                r.write('\n')
        file1 = open('folder1.txt','r') 
        Lines = file1.readlines() 
        output=['NULL']*11
        flag=0
        for line in Lines:
            s=list(map(str,line.split()))

            if(len(s)==2 and s[1]=="Code"):
                return False
            if(len(s)<3 ):
                pass
            
            elif(s[1]=="Code"):
                output[0]=s[2]
            elif(s[1]=="Name"):
               output[1]=' '.join(s[2: ])
            elif(s[0]=="Address"):
                output[2]=' '.join(s[1:])
            elif(s[0]=='E-Mail'):
                output[3]=s[2]
            elif(s[0]=='District'):
                output[4]=' '.join(s[1:2])   
            elif(s[0]=='Name' and flag==0):
                output[5]=' '.join(s[1:])
                flag=1
                
            elif(s[0]=="Office"):
                j=0
                for i in range(len(s)):
                    if(j!=1 and s[i].isdigit()and len(s[i])>5):
                        output[6]=s[i]
                        j=1
                    elif(j==1 and s[i].isdigit()and len(s[i])>5):
                        output[7]=s[i]
                
            elif(s[0]=='Name' and flag==1):
                output[8]=' '.join(s[1:])
            elif(s[0]=='Status'):
                for i in range(len(s)):
                    if(s[i]=='Autonomy'):
                        output[9]=s[i+2]
                        break
            elif(s[0]=='Year'):
                output[10]=s[3]
        return output
    

def college_data(college_region):
    if(clg_location(college_region)):
        
        no_of_college=1
        with open('folder.txt', 'r') as f:
            for line in f:
                xy=list(map(str,line.split()))
                if(len(xy)<3):
                    pass
                elif(no_of_college>180):
                    return
                elif(xy[0].isdigit() and xy[1].isdigit() and len(xy)>2):
                    o=eng_clg(xy[1])
                    f=open('folder2.txt','a+',newline='')
                    f.write('$'.join(o))
                    f.write('\n')
                    f.close()
                    no_of_college+=1
                    
                    
        return
    else:
        return None
    
f=open('folder2.txt','w+',newline='')
f.close()
print('\nEntered Website is getting Scrapped \n')
college_data("Amravati")
college_data("Aurangabad")
college_data("Mumbai")
college_data("Nagpur")
college_data("Nashik")
college_data("Pune")
print("Data is getting transferred....")
     
with open('scraped_data.csv','w',newline='') as f1:
    fieldnames=['Sr.No','College_Code','Institue_Name','Address','Email','District','Principal_Name','Office_No','Personal_No','TPO_Name','Autonomy_Status','Year_of_Establishment']
    thewriter=csv.DictWriter(f1,fieldnames=fieldnames)
    thewriter.writeheader()                       
    f1.close()
    
no_of_college=1
file=open('folder2.txt','r')
for f in file:
    o=list(map(str,f.split('$')))
    if(o[0]!='NULL' and o[1]!='NULL' and o[2]!='NULL'and o[3]!='NULL'and o[4]!='NULL'and o[5]!='NULL'and o[6]!='NULL'and o[7]!='NULL'and o[8]!='NULL'and o[9]!='NULL'and o[10]!='NULL'):
        with open('scraped_data.csv','a',newline='') as f1:
            fieldnames=['Sr.No','College_Code','Institue_Name','Address','Email','District','Principal_Name','Office_No','Personal_No','TPO_Name','Autonomy_Status','Year_of_Establishment']
            thewriter=csv.DictWriter(f1,fieldnames=fieldnames)
            thewriter.writerow({'Sr.No':no_of_college,'College_Code':int(o[0]),'Institue_Name':o[1],'Address':o[2],'Email':o[3],'District':o[4],'Principal_Name':o[5],'Office_No':int(o[6]),'Personal_No':int(o[7]),'TPO_Name':o[8],'Autonomy_Status':o[9],'Year_of_Establishment':int(o[10])})
            f1.close()
            no_of_college+=1
file.close()        
os.remove('folder.txt')
os.remove('folder1.txt')
os.remove('folder2.txt')
print("Required data is saved successfully.")



#FOR GRAPHICAL VISUALISATION OF THE DATA
x=[]
y=[]
year=[]

with open('scraped_data.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        y.append(row[5])
        x.append(row[10])
        year.append(row[11])

x.pop(0)
y.pop(0)
year.pop(0)

plt.scatter(y,x,90,marker='o',color='red')

plt.title('District vs Autonomy_Status (Whose all details are fetched completly)')

plt.ylabel('Autonomy Status')
plt.xlabel('District')
plt.xticks(rotation='vertical')
plt.show()

l=sorted(list(set(y)))
r=[]
for i in l:
    r.append(y.count(i))

k=dict.fromkeys(list(set(y)),0)
for i,j in k.items():
    k[i]=y.count(i)

   
plt.bar(l,r,.35,color='yellow')
plt.title('District vs No of colleges (whose all details are fetched completly)')
plt.ylabel('No of colleges')
plt.xlabel('District')
plt.xticks(rotation='vertical')
plt.show()


