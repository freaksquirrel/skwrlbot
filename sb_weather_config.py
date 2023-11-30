# -*- coding: utf-8 -*-
import os.path

## URL and request format related definitions
# Weather info graph related configs
aux_path = "<your path to the directory where the graphs folder is stored>"
graph_path = os.path.join(aux_path, "graphs/ACODE/YYYY/MM/")
graphs_file_ext = '.png'
graph_generic_fname = 'graph_scatter_amedas_'
graph_comp_fname = 'comp_'
graph_simple_fname   = f"{graph_generic_fname}VALUE_YYYY-MM-DD{graphs_file_ext}"
graph_datecomp_fname = f"{graph_generic_fname}VALUE_{graph_comp_fname}yyyy-mm-ddvsYYYY-MM-DD{graphs_file_ext}"
graph_areacomp_fname = f"{graph_generic_fname}VALUE_-AREAA-VS-AREAB-_YYYY-MM-DD{graphs_file_ext}"
graph_allareascomp_fname = f"{graph_generic_fname}VALUE_{graph_comp_fname}AllAreasVS_YYYY-MM-DD{graphs_file_ext}"

replace_target_value = "VALUE_"    # does this needs to be VALUE instead of VALUE_ ??
replace_target_date = "YYYY-MM-DD"
replace_target_date_cmp = "yyyy-mm-dd"
replace_target_year="YYYY"
replace_target_month="MM"
replace_target_areacode="ACODE"
replace_target_acodeA = "-AREAA-"
replace_target_acodeB = "-AREAB-"

ndays_timedelta_lst = 1
ndays_timedelta_prv = 8

area_code_def = '40201'    #I use "Mito" as default but you can change it to whatever area you want
area_code_comp_def = '44132'    #I use "Mito" as default but you can change it to whatever area you want

#post texts format  (you may want to adjust these messages...)
weather_simple_post_text = 'Graphs about the weather today @ Mito, Ibaraki, Japan. \n (Info acquired from AMeDAS, Japan Meteorological Agency)\n #weatherSQuirreL'
weather_ondate_post_text = f"Graphs about the weather on {replace_target_date} @ Mito, Ibaraki, Japan. \n (Info acquired from AMeDAS, Japan Meteorological Agency)\n #weatherSQuirreL"
weather_ondate_post_single_text = f"Graph of the {replace_target_value} on {replace_target_date} @ Mito, Ibaraki, Japan. \n (Info acquired from AMeDAS, Japan Meteorological Agency)\n #weatherSQuirreL"
weather_comp_post_text = f"Graphs comparing the weather of {replace_target_date_cmp} vs {replace_target_date}  @ Mito, Ibaraki, Japan. \n (Info acquired from AMeDAS, Japan Meteorological Agency)\n #weatherSQuirreL"
weather_comparea_post_text = f"Graphs comparing the weather @ {replace_target_acodeA} vs {replace_target_acodeB} on {replace_target_date}. \n (Info acquired from AMeDAS, Japan Meteorological Agency)\n #weatherSQuirreL"
weather_compareas_post_text = f"Graphs comparing weather info of different areas on {replace_target_date}. \n (Info acquired from AMeDAS, Japan Meteorological Agency)\n #weatherSQuirreL"

#temporarly took this from the weathersquirrel configs
## info for plots   value (json format)       Name                           Axis title          filename
graph_amedas_dic = {"temp":             ['Temperature'                     ,'Temp [°C]'          ,'01_temp_'              ],
                    "humidity":         ['Humidity'                        ,'Humidity [%]'       ,'02_humidity_'          ],
                    "snow":             ['Snow'                            ,'Snow [cm]'          ,'06_snow_'              ],
                    "pressure":         ['Sea level pressure'              ,'Sea level pressure' ,'05_pressure_'          ],
                    "sun10m":           ['Sunlight per Hour (prev 10 min)' ,'Sun time / 1hr'     ,'07_sunper10min_'       ],
                    "sun1h":            ['Sunlight per Hour (prev 1 hour)' ,'Sun time / 1hr'     ,'07_sunperhour_'        ],
                    "precipitation10m": ['Precipitation (prev 10min)'      ,'Precipitation [mm]' ,'03_precipitacion10min_'],
                    "precipitation1h":  ['Precipitation (prev 1 hr)'       ,'Precipitation [mm]' ,'03_precipitacion1h_'   ],
                    "precipitation3h":  ['Precipitation (prev 3 hr)'       ,'Precipitation [mm]' ,'03_precipitacion3h_'   ],
                    "precipitation24h": ['Precipitation (prev 24hr)'       ,'Precipitation [mm]' ,'03_precipitacion24h_'  ],
                    "windDirection":    ['Wind direction'                  ,'16 directions'      ,'04_windirection_'      ],
                    "wind":             ['Wind'                            ,'Wind [m/s]'         ,'04_wind_'              ] }
##            CODE      Area name          Area short name         Area name in japanese
area_info = {'40201': {'name':'Mito'   , 'short_name':'mito'   , 'japanese_name':'水戸（ミト）'},
             '44132': {'name':'Tokyo'  , 'short_name':'tokyo'  , 'japanese_name':'東京（トウキョウ）'},
             '14163': {'name':'Sapporo', 'short_name':'sapporo', 'japanese_name':'札幌（サッポロ）'},
             '62078': {'name':'Osaka'  , 'short_name':'osaka'  , 'japanese_name':'大阪(オオサカ)'},
             '82182': {'name':'Fukuoka', 'short_name':'fukuoka', 'japanese_name':'福岡（フクオカ）'},
             '91197': {'name':'Naha'   , 'short_name':'naha'   , 'japanese_name':'那覇（ナハ）'},
             'common':{'name':'_'      , 'short_name':'comm'   , 'japanese_name':'_'}                 }
