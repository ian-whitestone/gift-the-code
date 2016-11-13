library(RPostgreSQL)
library(data.table)
library(magrittr)
library(lubridate)
library(ggplot2)
library(DT)
source('dlin.R')

options(datatable.print.nrows=1000, width=120)

drv = dbDriver('PostgreSQL')
conn = dbConnect(drv, dbname='postgres')
d = dbReadTable(conn, 'data') %>% setDT
postal = dbReadTable(conn, 'postal') %>% setDT

d[, date := parse_date_time(date, '%Y-%m-%d')]
d[, arrive := ymd_hms(paste(date, arrive, sep=' '))]
d[, depart := ymd_hms(paste(date, depart, sep=' '))]

d[, .( Perishable = sum(bread + baked + dairy + produce + protein + prepared + bev_juice + bev_other + snack) / 
    sum(bread + baked + dairy + produce + protein + prepared + bev_juice + bev_other + snack + non_perish + non_food),
    `High Nutrient` = sum(dairy + produce + protein) / 
      sum(bread + baked + dairy + produce + protein + prepared + bev_juice + bev_other + snack + non_perish + non_food)), 
  by=floor_date(date, unit='quarter')] %>% melt(id.vars = 1, measure.vars = 2:3) %>% 
  ggplot(aes(x = floor_date, y = value, col = variable)) + geom_line() + geom_point() + 
  labs(title = 'Ratios', col = NULL, x = 'Month', y = NULL) + theme_dlin()

top_types = dmelt[stop_type == 'Delivery', sum(amount), by=food_type][
  ,V2 := V1 / sum(V1)][order(-V1)][, value := V1 * 2.5 / 1e6]

top_types[, food_type := as.character(food_type)]
top_types[, high_nutrient := FALSE]
top_types[food_type %in% c('dairy','protein','produce'), high_nutrient := TRUE]

ggplot(top_types, aes(x = food_type, weight = value, fill = high_nutrient)) + 
  geom_bar() + theme_dlin() + scale_x_discrete(limits = top_types$food_type) +
  geom_text(aes(y = value / 2, label = sprintf('$%.1fM\n(%.1f%%)', value, V2 * 100))) + 
  theme(axis.text.x=element_text(angle=45, vjust=1, hjust=1)) + 
  labs(x = 'Type of Food', y = 'Value of Donations ($M)', title = 'Types of Food Donated',
       fill = 'High Nutrient')


#### SURVEY STUFF
survey = dbReadTable(conn, 'survey') %>% setDT
setkey(survey, donor_id)
setkey(d, donor_id)
setkey(dmelt, donor_id)
nps_names = c("nps_office", "nps_driver", "nps_agency", "nps_workshop", "crucial_to_success", "healthy_and_nutritious", "diverse", "expanded_programs", "more_opportunities")

survey[d,nomatch=0] ##merge survey data


##Survey Data - Graphs and Charts

nps_table=survey[, list(var = colnames(.SD), lapply(.SD, mean)), .SDcols = nps_names]
nps_table[,survey_score:=round(as.numeric(V2)*100,0)]
nps_table[,V2:=NULL]

ggplot(nps_table,aes(x=var,y=survey_score)) +
  geom_bar(stat = "identity") + theme_dlin() + theme(axis.text.x=element_text(angle=45, vjust=1, hjust=1)) +
  labs(x = 'Survey Variable', y = 'Customer Survey Results', title = 'Second Harvest Survey Results')

survey[,total:=clients*perc_provided]
survey[,children:=total*children_perc]
survey[,youth:=total*youth_perc]
survey[,men:=total*men_perc]
survey[,women:=total*women_perc]
survey[,seniors:=total*senior_perc]

dfr=survey[order(-total)][1:10,.(donor_id,total,children,youth,men,women,seniors)]
mdfr=melt(dfr[,.(donor_id,children,youth,men,women,seniors)], id.vars = "donor_id")
setnames(mdfr,old=c('variable','value'),new=c('demographic','count'))

survey_table=survey[,.(donor_id,total,children,youth,men,women,seniors)][order(-total)]
survey_table[,(colnames(survey_table)) := round(.SD,0), .SDcols=colnames(survey_table)]

##sortable table showing the number of clients reliant on second harvest for each donor
datatable(survey_table) 


# ##basic bar chart showing total clients
# ggplot(dfr,aes(x = factor(donor_id), y = total)) + scale_x_discrete(limits = as.character(survey_top_reliance$donor_id)) +
#   geom_bar(stat = "identity") + theme_dlin() + theme(axis.text.x=element_text(angle=45, vjust=1, hjust=1)) + 
#   labs(x = 'Donor ID', y = '# of Clients', title = 'Who Needs Second Harvest the Most?')

##stacked bar chart with demographic splits
ggplot(mdfr,aes(x = factor(donor_id), y = count,fill=demographic)) + scale_x_discrete(limits = as.character(survey_top_reliance$donor_id)) +
  geom_bar(stat = "identity") + theme_dlin() + theme(axis.text.x=element_text(angle=45, vjust=1, hjust=1)) + 
  labs(x = 'Donor ID', y = '# of Clients', title = 'Who Needs Second Harvest the Most?')

