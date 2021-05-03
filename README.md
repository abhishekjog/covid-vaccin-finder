# covid-vaccin-finder
Latest vaccine availability as per CoWin

No need to login to CoWin/ArogyaSetu to find vaccine availability. All you need a python3 environment with pandas. 
(Environment set will be addressed in future check-ins). 

# sample output: default date and age
```
C:\Users\AbhishekJog> python3 .\vaccine_avail.py --state Maharashtra --district Pune
          date  available_capacity  min_age_limit  pincode                            name   state_name district_name block_name fee_type
20  03-05-2021                   0             18   411026             New Bhosari (18-44)  Maharashtra          Pune     Haveli     Free 
26  03-05-2021                   0             18   411001  Pune Cantonment (18 To 44 Yrs)  Maharashtra          Pune     Haveli     Free 
32  03-05-2021                   0             18   411028      Villoo Poonawalla Hospital  Maharashtra          Pune     Haveli     Paid 
44  03-05-2021                   0             18   411033     Premlok Park Disp- 2(18-44)  Maharashtra          Pune     Haveli     Free 
53  03-05-2021                   0             18   411011    Kamla Nehru PMC 1 (18 To 44)  Maharashtra          Pune     Haveli     Free 
54  03-05-2021                   0             18   411017  New Jijamata Hospital-2(18-44)  Maharashtra          Pune     Haveli     Free 
86  03-05-2021                   0             18   411006    Rajiv Gandhi Hosp (18 To 44)  Maharashtra          Pune     Haveli     Free 
```
# Usage
```
C:\Users\AbhishekJog> python3 .\vaccine_avail.py --h
usage: vaccine_avail.py [-h] [--age {18,45}] [--pincodes PINCODES] [--pinrange PINRANGE] [--state STATE] [--district DISTRICT]
                        [--vaccine {Covaxin,Covishield}] [--date DATE]

optional arguments:
  -h, --help            show this help message and exit
  --age {18,45}         Age group : 18 or 45
  --pincodes PINCODES   Comma separate list of pincodes
  --pinrange PINRANGE   hyphen separate range of pincodes
  --state STATE         State name (first letter caps)
  --district DISTRICT   District name (first letter caps)
  --vaccine {Covaxin,Covishield}
                        Name of the vaccine
  --date DATE           Select from date in dd-mm-yyyy format
```  

# Future work:
1. make command-line driven
2. filter on vaccine (will be required for 2nd shot)

Contributions are welcome!
