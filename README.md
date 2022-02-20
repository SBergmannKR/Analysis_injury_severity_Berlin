# Analysis_injury_severity_Berlin

Automated analyses of the official accident data from 2019 of the "Bundesamtes für Statistik"
**************Functions*************************
"analysis_script_injuries_SB.py":
- Reads "accidentdata.csv" and "Personenkm_Berlin.csv."
- makes various operations based on this Data
- Outputs tabular and graphical analysis results

********************Data***************************

"accidentdata.csv": Dataset of the "Bundesamtes für Statistik"
(https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Verkehrsunfaelle/_inhalt.html, https://unfallatlas.statistikportal.de/_opendata2021.html).Eine For more information about the data see the file "Info_DSB_Unfallatlas.pdf" in this repo.

"Personenkm_Berlin.csv": Contains the transportation service (people) for each vehicle type in Berlin (Fahrrad, Auto, etc.), the dimension is [km / a]. The data was aggregated from the StV. For more information about this data see the file "Artikel_Verkehrsleistung_Bergmann.pdf" (German) in this repo.
**************************************
