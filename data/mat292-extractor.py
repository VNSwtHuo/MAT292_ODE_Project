import re

sql_statements = """
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3804,436,-5.14850594922925,7.33857045318782,null,null,null,null,-5.1485,8.53322,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3805,436,-4.22500174830415,11.4618506472815,null,null,null,null,-4.225,13.32773,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3806,436,-2.24224502232834,14.1331778119889,null,null,null,null,-2.24224,16.43392,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3807,436,-1.21871784369162,15.9256955457551,null,null,null,null,-1.21871,18.51825,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3808,436,-0.18156388303346,21.5636287088493,null,null,null,null,-0.18156,25.07398,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3809,436,0.0545271087045496,18.2449785707554,null,null,null,null,0.05452,21.21509,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3810,436,0.73414787655973,13.1254870562869,null,null,null,null,0.73414,15.26219,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3811,436,1.86117466057924,14.7826402217098,null,null,null,null,1.86117,17.18911,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3812,436,3.87705925252505,9.32832642342063,null,null,null,null,3.87705,10.84689,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3813,436,5.8889477207109,7.37354155140766,null,null,null,null,5.88894,8.57388,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3814,436,7.8044496838067,3.67267989461719,null,null,null,null,7.80444,4.27055,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3815,436,11.8568788275372,1.93205879338644,null,null,null,null,11.85687,2.24657,null,null,null);
insert into `conc_time_values`(`id`,`fk_series_id`,`time_original`,`conc_original`,`conc_sd_original`,`conc_lower_bound_original`,`conc_upper_bound_original`,`no_conc_val_type`,`time_hr`,`conc`,`conc_sd`,`conc_lower_bound`,`conc_upper_bound`) values (3816,436,17.9911685664905,1.18056545941388,null,null,null,null,17.99116,1.37275,null,null,null);
"""

columns = ["id","fk_series_id","time_original","conc_original","conc_sd_original",
    "conc_lower_bound_original","conc_upper_bound_original","no_conc_val_type",
    "time_hr","conc","conc_sd","conc_lower_bound","conc_upper_bound"]

column_to_extract = "conc"
col_index = columns.index(column_to_extract) 

values = re.findall(r"values\s*\((.*?)\);",sql_statements, flags=re.IGNORECASE|re.DOTALL)

excel_column = "\n".join([v.split(",")[col_index] for v in values])

print(excel_column)