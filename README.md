# covid-vaccin-finder
Latest vaccine availability as per CoWin

No need to login to CoWin/ArogyaSetu to find vaccine availability. All you need a python3 environment with pandas. 
(Environment set will be addressed in future check-ins). 

# sample output
```
C:\Users\AbhishekJog> python3 .\cowin_avail.py
          date  available_capacity  min_age_limit  pincode                            name   state_name district_name block_name fee_type
9   03-05-2021                   0             18   411057       Maan PHC (18 To 44 Years)  Maharashtra          Pune     Mulshi     Free 
21  03-05-2021                   0             18   411026             New Bhosari (18-44)  Maharashtra          Pune     Haveli     Free 
27  03-05-2021                   0             18   411001  Pune Cantonment (18 To 44 Yrs)  Maharashtra          Pune     Haveli     Free 
33  03-05-2021                   0             18   411028      Villoo Poonawalla Hospital  Maharashtra          Pune     Haveli     Paid 
46  03-05-2021                   0             18   411033     Premlok Park Disp- 2(18-44)  Maharashtra          Pune     Haveli     Free 
57  03-05-2021                   0             18   411011    Kamla Nehru PMC 1 (18 To 44)  Maharashtra          Pune     Haveli     Free 
58  03-05-2021                   0             18   411017  New Jijamata Hospital-2(18-44)  Maharashtra          Pune     Haveli     Free 
91  03-05-2021                   0             18   411006    Rajiv Gandhi Hosp (18 To 44)  Maharashtra          Pune     Haveli     Free 
```

# Future work:
1. make command-line driven
2. filter on vaccine (will be required for 2nd shot)

Contributions are welcome!
