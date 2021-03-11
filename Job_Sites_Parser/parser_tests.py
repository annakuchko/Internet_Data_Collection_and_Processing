from jobs_parser import job_parser, HHParser


#df = job_parser(save=True, format='csv')

hh_parser = HHParser("'Data Analyst' or 'Data Scientist'", 5, verbose = True)
hh_parser.parse_site()
df_hh = hh_parser.preprocess()
hh_parser.save('dataanalyst_datascientist_hh', 'excel')

