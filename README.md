# CSL_Shanghai_LivingLine_Data_Analysis

The codes of visualization part are all in visualization demo, but some can not be send because the data need to be secret

## Introduction of each Python file 
City Science Lab Shanghai - LivingLine Project - Data Analysis

### Wi-Fi AP connection-oriented data analysis
0812_second version for processing stay point (combine 1 day)  
cleanData to csv for processing clean data to a csv file  
toJSON for processing raw data to a json file  

### User Device-oriented data analysis
exploreWifiLL for comparing the raw data with the clean data to get the valid macs and the individual connection records in one peoriod
individual xy coordinates for getting the staypoints  
to_graph_csv for getting 10 minutes data to visualize
0824 interval tree.py and 0906_individual_xy coordinates.py  for using Interval Tree and Hyperbola to define the accurate location of each individual 

## Rhino Grasshopper Visualization

All Rhino Grasshopper source code is under "RH_GH" folder. 

### Wi-Fi AP connection number visualization
1. Sample viz of AP connection - raw data  
result video  
https://drive.google.com/open?id=15XojIVYzIk6O_PPsK_gQTrlWsvjuQSpS  
data used (processed anonymous data, team access only)  
shared gdrive folder: LivingLine Data\Wi-Fi Data\Data Sample\180731_reformat for viz_Weiting\rawdata_2018_06_19.csv  
  
2. Sample viz of AP connection - clean data  
result video  
https://drive.google.com/open?id=17l6p-ebcfchp48siHpVclDYYibS_sxfN  
data used (processed anonymous data, team access only)  
shared gdrive folder: LivingLine Data\Wi-Fi Data\Data Sample\180731_reformat for viz_Weiting\cleandata_2018_06_19.csv  
  
### User Device to Wi-Fi AP connectin path
1. Sample viz of device path - detailed viz of a device with min connection  
result video  
https://drive.google.com/open?id=1okseFWYsrJYcgWzIMc4QCHZb9y75XbhW  
data used (processed anonymous data, team access only)  
shared gdrive folder: LivingLine Data\Wi-Fi Data\Data Sample\180812_csv for viz_Weiting\16_freq_0728vis.csv  
  
2. Sample viz of device path - non-detailed viz of a device with max connection (first 500 data points)  
result video  
https://drive.google.com/open?id=1sQlhtg6_sgunRxopRwKr_Z6bs-CokCo5  
data used (processed anonymous data, team access only)  
shared gdrive folder: LivingLine Data\Wi-Fi Data\Data Sample\180812_csv for viz_Weiting\max24094_freq_0728vis.csv  

## visualization demo
timestay.html visualized the amount of the staypoints divided by how long do they last. 
spacial staypoints.html visualized the spacial of the stay-points in each time period, but it is not workable now because the spacial data of the staypoints is not correct enough. However, I still upload the staypoints data on drive: https://drive.google.com/open?id=1miPacbr410zlpAgCXtwoUa8G1Bbv5kt_, with this you can run the html code(put them in a same folder)
