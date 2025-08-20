```python
import polars as pl
from shapely.geometry import Point, Polygon
```

### Description

An extensive data set containing over 94,000 charted, uncharted, live and dead wrecks and obstructions from around the world. Updated on a quarterly basis, this data set is made available free of charge under an Open Government Licence, which can be accessed here: https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
Updated April 2024

### Terms of Use

No special restrictions or limitations on using the item's content have been provided.


```python
# https://data.admiralty.co.uk/portal/home/item.html?id=60c0908526b844a68494c038a457e1a7
df = pl.read_csv(
    'data/wrecks.tsv', separator='\t', quote_char='"', encoding='latin1', infer_schema_length=10000000,  null_values=[""] )
print(df.schema)

```

    Schema({'wreck_id': Int64, 'wreck_category': String, 'obstruction_category': String, 'status': String, 'classification': String, 'position': String, 'latitude': String, 'longitude': String, 'horizontal_datum': String, 'limits': String, 'position_method': String, 'depth': Float64, 'height': Float64, 'depth_method': String, 'depth_quality': String, 'depth_accuracy': Float64, 'water_depth': Int64, 'water_level_effect': String, 'vertical_datum': String, 'reported_year': String, 'name': String, 'type': String, 'flag': String, 'length': Float64, 'width': Float64, 'draught': Float64, 'sonar_length': Float64, 'sonar_width': Float64, 'shadow_height': Float64, 'orientation': Float64, 'tonnage': Int64, 'tonnage_type': String, 'cargo': String, 'conspic_visual': String, 'conspic_radar': String, 'date_sunk': String, 'non_sub_contact': Int64, 'bottom_texture': String, 'scour_dimensions': String, 'debris_field': String, 'original_sensor': String, 'last_sensor': String, 'original_detection_year': String, 'last_detection_year': String, 'original_source': String, 'markers': String, 'circumstances_of_loss': String, 'surveying_details': String, 'general_comments': String, 'last_amended_date': Int64})



```python
for col in ["general_comments", "surveying_details", "circumstances_of_loss"]:
    #strip and replace with na if empty afterwards
    df = df.with_columns(pl.col(col).str.strip_chars().replace("", None))
```


```python
df["wreck_category"].value_counts(sort=True)
```




<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (6, 2)</small><table border="1" class="dataframe"><thead><tr><th>wreck_category</th><th>count</th></tr><tr><td>str</td><td>u32</td></tr></thead><tbody><tr><td>null</td><td>32991</td></tr><tr><td>&quot;dangerous wreck&quot;</td><td>29703</td></tr><tr><td>&quot;non-dangerous wreck&quot;</td><td>24159</td></tr><tr><td>&quot;wreck showing any portion of h…</td><td>12127</td></tr><tr><td>&quot;distributed remains of wreck&quot;</td><td>913</td></tr><tr><td>&quot;wreck showing mast/masts&quot;</td><td>602</td></tr></tbody></table></div>




```python
df["status"].value_counts(sort=True)
```




<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (17, 2)</small><table border="1" class="dataframe"><thead><tr><th>status</th><th>count</th></tr><tr><td>str</td><td>u32</td></tr></thead><tbody><tr><td>null</td><td>64842</td></tr><tr><td>&quot;dead&quot;</td><td>31289</td></tr><tr><td>&quot;lifted&quot;</td><td>2709</td></tr><tr><td>&quot;Not Fully Surveyed&quot;</td><td>712</td></tr><tr><td>&quot;historic&quot;</td><td>631</td></tr><tr><td>&hellip;</td><td>&hellip;</td></tr><tr><td>&quot;historic, existence doubtful&quot;</td><td>1</td></tr><tr><td>&quot;UNKNOWN&quot;</td><td>1</td></tr><tr><td>&quot;Removed&quot;</td><td>1</td></tr><tr><td>&quot;Not Fully Surveyed, historic&quot;</td><td>1</td></tr><tr><td>&quot;existence doubtful, dead&quot;</td><td>1</td></tr></tbody></table></div>




```python
df["depth"].describe()
```




<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (9, 2)</small><table border="1" class="dataframe"><thead><tr><th>statistic</th><th>value</th></tr><tr><td>str</td><td>f64</td></tr></thead><tbody><tr><td>&quot;count&quot;</td><td>39549.0</td></tr><tr><td>&quot;null_count&quot;</td><td>60946.0</td></tr><tr><td>&quot;mean&quot;</td><td>29.250057</td></tr><tr><td>&quot;std&quot;</td><td>57.541481</td></tr><tr><td>&quot;min&quot;</td><td>-21.0</td></tr><tr><td>&quot;25%&quot;</td><td>7.17</td></tr><tr><td>&quot;50%&quot;</td><td>16.2</td></tr><tr><td>&quot;75%&quot;</td><td>35.0</td></tr><tr><td>&quot;max&quot;</td><td>4513.0</td></tr></tbody></table></div>




```python
df["original_source"].value_counts(sort=True)
```




<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (25, 2)</small><table border="1" class="dataframe"><thead><tr><th>original_source</th><th>count</th></tr><tr><td>str</td><td>u32</td></tr></thead><tbody><tr><td>&quot;national HO/authority charts&quot;</td><td>27256</td></tr><tr><td>&quot;national HO/authority notice t…</td><td>25215</td></tr><tr><td>&quot;other&quot;</td><td>9853</td></tr><tr><td>&quot;survey vessel&quot;</td><td>9741</td></tr><tr><td>&quot;Lloyd&#x27;s and Marine Underwriter…</td><td>7360</td></tr><tr><td>&hellip;</td><td>&hellip;</td></tr><tr><td>&quot;research vessel&quot;</td><td>80</td></tr><tr><td>&quot;published other losses&quot;</td><td>34</td></tr><tr><td>&quot;yacht&quot;</td><td>20</td></tr><tr><td>&quot;national HO/authority files&quot;</td><td>15</td></tr><tr><td>&quot;geodetic survey reports or cha…</td><td>1</td></tr></tbody></table></div>




```python
df.filter(pl.col("general_comments").is_not_null()).select("general_comments").sample(10).to_series().to_list()
```




    ['TURBULENT UPWELLING OF DISCOLOURED WATER. Amended from WRECKS to OBSTRN 18.02.2019 to be consistent with wk_idn 90497 close NW.',
     'AREA OF LARGE BROKEN DEBRIS',
     'REP(2004)',
     'AREA OF BROKEN WRECKAGE, THIS IS THE POSN ON ONE TURBINE',
     'INTACT, UPRIGHT, MAST INTACT, BOWS SE',
     'SINGLE PIECE OF WRECKAGE',
     'INTACT, BOWS S',
     'HIGHLY DEGRADED BROKEN WK',
     'BADLY BROKEN UP, 2 MAIN SECTIONS',
     'BADLY DEGRADED, NO VISABLE FEATURES.']




```python
df.filter(pl.col("surveying_details").is_not_null()).select("surveying_details").sample(10).to_series().to_list()
```




    ['2.2.72   WK IN 563930N, 112830E [EUR]. CONDITION UNKNOWN OR UNTOUCHED. THOUGHT TO BE 2 WKS. (DANISH WK RECORD NO 639128). FOR FILING ONLY. NCA.     SEP 2016/000132285   30.8.16   WK NOT SHOWN ON DK4KATGS (EDN 48.6) AND DANISH 102 (EDN 13, COR TO 27.5.16). AMEND TO DEAD.',
     'H342/31   22.1.31   WK IN 362445N, 051915W. (AUTHORITY NOT STATED). NCA. POSN TOO VAGUE TO CHART.     H342/31   18.5.31   WK REMOVED. (AUTHORITY NOT STATED). AMEND TO LIFT. NCA.',
     'HH440/180/01      4.9.90      HH440/180/01 4.9.90 WELLHEAD "KC-2" IN 041441.4N, 071719E IN GEN DEPTH 18.6MTRS [MSL]. (NPA LISTING, DA LAGOS) INS AS WH USC 12.8MTRS. NE 1863.          HH432/351/01      27.12.90      HH432/351/01 27.12.90 WELLHEAD REMOVED. (NPA NM 52/66) BY HNC4, TO BE DELETED AS NPA LISTING ABOVE IS OF ALL KNOWN POSNS, & HAS NOT BEEN UPDATED FOR ANY SUBSEQUENT REMOVALS. AMENDED TO DEAD.',
     'H04213/45   10.9.45   INFORMATION ON WRECKS IN MANILA BAY IN 142500N, 1203000E APPROX. (ADMIRALTY). NCA.',
     '2.4.75   NDW SHOWN IN 544810N, 061905E [EUR] ON NETHERLANDS 1032 & GERMAN 50 [1974 EDNS]. BR STD.     H1271/82   17.8.82   SHOWN AS WK 38MTRS ON GERMAN 50D [1982 EDN]. AMEND WK 21FMS. BR STD.        12.12.86   AMEND WK 38MTRS. NE 2182B.        24.10.13   SHOWN AS WK 37MTRS IN 5448.27N, 0618.93E [WGD] ON GERMAN 50 [2013 EDN]. NE 1432.     SEP 2015/000158093    15.1.16    SHOWN AS SW 37MTRS IN 5448.271N, 0619.007E [WGD] ON DE221000 [ED7.0, DTD 10.07.15]. AMEND TO SW 37MTRS IN REVISED POSN.',
     '7.1.76      7.1.76 OB SHOWN IN 552957N, 000501E [EUR]. POSN BY DECCA. (KINGFISHER CHART KE 155-1A, MAY 1970 EDN). NCA, RECORDED AS FISHERMENS FASTENER.',
     'H2088/77   20.2.80   2ND CLASS MOORING C6 IN 554524N, 045324W [OGB]. (AUTHORITY NOT STATED) INS AS FOUL. NE 1907 & 2491.     H2885/83   12.5.86   NOT INVESTIGATED DURING SURVEY. NMSD, FAIRLIE ADMINISTER THIS MOORING. THEIR QUOTED POSN IS 554524N, 045324W [OGB]. (HMSML GLEANER, HI 165C). NCA.        27.10.00   AMEND POSN. BR STD.     HH274/440/06   21.2.02   MATERIAL HAS BEEN RECOVERED. FOUL MAY BE REMOVED. (SALMO (NORTH), HN DTD 13.2.02). AMENDED LIFT. DELETE. BR STD.',
     "H3076/77   16.4.85   WK 68MTRS, LIES 144.3DEGS, 3.66M FROM CAPO D'OTRANTO LIGHT. (GENOA NM 3.9/85). CHART AS WK 37FMS IN 400318N, 183408E. SUBNAVMED 001/85 ISSUED. BR STD.        6.4.93   NDW SHOWN IN 400324N, 183357E ON ITALIAN 920 [1992 EDN]. BR STD.     HH180/300/06   13.7.00   RETAINED AS WK 68MTRS ON BA NM BLOCK 2741/00. SHOWN AS NDW ON  ITALIAN 920 [CORRECT TO 7/16/2000, SCALE 1: 250,000] BUT STILL SHOWN AS WK 68MTRS ON LARGEST SCALE ITALIAN 28 [LATEST EDN HELD 1993].        25.5.12   [WGD] POSN: 4003.433N, 1833.982E.",
     'HH650/350/02      19.9.90      HH650/350/02 19.9.90 SUNK IN 394048S, 620300W. MARKED BY SMALL BUOYS. (ARG NM 119T/89). INS AS DW. BR STD.                22.7.10      22.7.10 SHOWN IN 3940.737S, 6203.053W [WGD] ON ARGENTINIAN 213 [EDN 2 DTD 2008, 1:150,000].',
     'SEP 2016/000028552    24.3.16    SHOWN AS WK 98.7MTRS IN 5831.129N, 2118.524E [WGD] ON EE4C3521 [ED1.5, DTD 25.1.16]. INS NDW 98MTRS.']




```python
df.filter(pl.col("circumstances_of_loss").is_not_null()).select("circumstances_of_loss").sample(10).to_series().to_list()
```




    ['3300KG ANCHOR LOST BY MT TOBA PEGASSO.',
     "EX-ROSA. BUILT IN 1875 BY GOOLE ENGINEERING & SHIPBUILDING CO LTD, GOOLE. OWNED AT TIME OF LOSS BY BIRD'S SHIPPING CO LTD. ONE BOILER, COMPOUND EXPANSION ENGINE OF 80HP, SINGLE SHAFT. PASSAGE NEWCASTLE-UPON-TYNE FOR DUNKIRK. TORPEDOED AND SUNK BY GERMAN SEAPLANE. (WW1SL & SIBI).",
     'VESSEL, BUILT 1961 BY CLELANDS SHIPBUILDING CO., LTD. OWNED AT TIME OF LOSS BY EUROMAR CHARTERING & SHIPPING CO LTD. ON PASSAGE FROM ANTWERP TO TRIPOLI. RAN AGROUND OFF RAS EL KORAN, ABOUT 19M FROM BIZERTE. FIRE SUBSEQUENTLY BROKE OUT IN ENGINE-ROOM CAUSING EXTENSIVE DAMAGE. VESSEL DECLARED CONSTRUCTIVE TOTAL LOSS. (MSD).',
     "BUILT IN 1905 BY A STEPHENS & SONS, GLASGOW. OWNED AT TIME OF LOSS BY BRITISH & AFRICAN STEAM NAVIGATION CO. TWO BOILERS, TRIPLE EXPANSION ENGINE OF 424NHP FOR 11.5 KNOTS, SINGLE SHAFT. PASSAGE PLYMOUTH FOR LE HAVRE WITH 806 OFFICERS AND MEN OF AN AFRICAN LABOUR BATALLION EMBARKED AND 88 CREW. WHILE STEAMING DEAD SLOW IN DENSE FOG WITH NO NAVIGATION LIGHTS, BUT SOUNDING THE CORRECT FOG SIGNAL, WAS STRUCK ON STBD SIDE BY THE LINER 'DARRO' WHICH WAS ALSO STEAMING WITHOUT LIGHTS. SANK WITH LOSS OF 607 MEN OF THE REGIMENT AND 29 CREW. DARRO DID NOT STOP TO PICK UP SURVIVORS OWING TO THE DANGER FROM ENEMY SUBMARINES. (DODS, WW1SL & SIBI).",
     "VESSEL, SANK FOLLOWING COLLISION WITH RUSSIAN OCEANOGRAPHIC RESEARCH VESSEL 'BEREZEN'. FOUR CREW RESCUED. (LLOYDS VOL.212).",
     'BUILT IN 1972 BY MITSUI SHIPBUILDING & ENGINEERING CO., ICHIHARA. OWNED AT TIME OF LOSS BY PAN OCEAN SHIPPING CO., LTD. ON PASSAGE SEPETIBA FOR POHANG. DIVERTED TO CAPE TOWN FOR REPAIRS. DRAGGED ANCHOR IN A GALE AND STRANDED ON WHALE ROCK, BREAKING IN TWO. ALL 28 CREW SAFELY RESCUED. DECLARED A CONSTRUCTIVE TOTAL LOSS. (MSD).',
     "BUILT IN 1920. OWNED AT TIME OF LOSS BY SOC NAVALE DE L'OUEST. PASSAGE TAKORADI FOR FREETOWN. TORPEDOED BY U 547. (DODS, WW2SL, LL WW2, AXIS SUBMARINE SUCCESSES).",
     "BUILT IN 1913 BY R DUNCAN & CO., WITH TRIPLE EXPANSION ENGINE OF 475NHP. OWNED AT TIME OF LOSS BY BABA SHOJI K K, UNDER COMMAND OF THE JAPANESE ARMY. PASSAGE TANDJUNG PRIOK FOR PADANG. FITTED WITH EXTRA DECKS CONSTRUCTED OF BAMBOO, SUBDIVIDED INTO CAGES OF THE SAME MATERIAL. TORPEDOED AND SUNK BY HM SUBMARINE 'TRADEWIND' OFF INDRAPURA, SUMATERA. ON BOARD WERE 4,860 JAVANESE WORKERS AND OVER 2000 PRISONERS OF WAR; 1377 DUTCH, 64 BRITISH AND AUSTRALIAN AND 8 AMERICAN. 5620 LOST. 723 SURVIVORS RESCUED, ONLY TO BE PUT TO WORK IN DEADLY CONDITIONS. (DODS, SEA BREEZES AUG. 1983, AMERICAN SUBMARINE SUCCESSES WWII & WILKIPEIDIA).",
     'EX-VENTROUS, EX-VENTUROUS. BUILT IN 1998 BY JONES BUCKIE SLIP. OWNED AT TIME OF LOSS BY PHEALAN & PRESCOTT, NEWRY, CO DOWN. OIL ENGINE OF 500BHP, SINGLE SHAFT. SUFFERED FIRE WHICH COULD NOT BE CONTAINED. CREW ABANDONED. LAST SEEN VISUALLY AND ON RADAR ON FIRE IN THICK FOG. PRESUMED SUNK. (LL).',
     'VESSEL, SUNK BY A MINE DURING THE SPANISH CIVIL WAR. (KELVIN HUGHES SURVEY, 1964-65).']




```python
df["position"]
```




<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (100_495,)</small><table border="1" class="dataframe"><thead><tr><th>position</th></tr><tr><td>str</td></tr></thead><tbody><tr><td>&quot;26 13.93 N,56 13.8 E&quot;</td></tr><tr><td>&quot;58 3.06 N,1 46.86 W&quot;</td></tr><tr><td>&quot;6 8.439 N,108 26.078 E&quot;</td></tr><tr><td>&quot;49 48.948 N,0 1.505 W&quot;</td></tr><tr><td>&quot;49 43.479 N,0 0.6 W&quot;</td></tr><tr><td>&hellip;</td></tr><tr><td>&quot;22 10.873 N,114 31.599 E&quot;</td></tr><tr><td>&quot;22 11.389 N,114 30.871 E&quot;</td></tr><tr><td>&quot;22 8 N,114 28 E&quot;</td></tr><tr><td>&quot;22 9.481 N,114 34.036 E&quot;</td></tr><tr><td>&quot;22 9.24 N,114 41.27 E&quot;</td></tr></tbody></table></div>




```python
df["latitude"]
```




<div><style>
.dataframe > thead > tr,
.dataframe > tbody > tr {
  text-align: right;
  white-space: pre-wrap;
}
</style>
<small>shape: (100_495,)</small><table border="1" class="dataframe"><thead><tr><th>latitude</th></tr><tr><td>str</td></tr></thead><tbody><tr><td>&quot;26 13.93 N&quot;</td></tr><tr><td>&quot;58 3.06 N&quot;</td></tr><tr><td>&quot;6 8.439 N&quot;</td></tr><tr><td>&quot;49 48.948 N&quot;</td></tr><tr><td>&quot;49 43.479 N&quot;</td></tr><tr><td>&hellip;</td></tr><tr><td>&quot;22 10.873 N&quot;</td></tr><tr><td>&quot;22 11.389 N&quot;</td></tr><tr><td>&quot;22 8 N&quot;</td></tr><tr><td>&quot;22 9.481 N&quot;</td></tr><tr><td>&quot;22 9.24 N&quot;</td></tr></tbody></table></div>




```python
import json

with open('data/iho88.json', 'r') as f:
    iho88_data = json.load(f)

coords = iho88_data['features'][0]['geometry']['coordinates'][0][0]

polygon = Polygon(coords)


# degrees minutes direction to signed decimal degree
def parse_coord(coord_str):
    if coord_str is None:
        return None
    parts = coord_str.strip().split()
    if len(parts) != 3:
        return None
    
    degrees = float(parts[0])
    minutes = float(parts[1])
    direction = parts[2].upper()
    
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal = -decimal
    
    return decimal

df_with_coords = df.with_columns([
    pl.col("latitude").map_elements(parse_coord, return_dtype=pl.Float64).alias("lat"),
    pl.col("longitude").map_elements(parse_coord, return_dtype=pl.Float64).alias("lon")
])

# Filter for points inside the polygon
df_inside = (
    df_with_coords
    .with_columns(
        pl.struct(["lon", "lat"])
          .map_elements(lambda row: polygon.contains(Point(row["lon"], row["lat"])), return_dtype=pl.Boolean)
          .alias("inside")
    )
    .filter(pl.col("inside"))
    .drop("inside")
)

print(f"Total records: {len(df)}")
print(f"Records inside IHO S-88 polygon: {len(df_inside)}")
print(f"\nFiltered DataFrame shape: {df_inside.shape}")
```

    Total records: 100495
    Records with valid coordinates: 100495
    Records inside IHO S-88 polygon: 21357
    
    Filtered DataFrame shape: (21357, 52)

