# Internet_Data_Collection_and_Processing
Methods for collecting and processing data from the Internet: parsing, scraping, crawling  
Data is collected to the local MongoDB.

Required structure (for proper methods usage):  
<pre> 
Internet_Data_Collection_and_Processing  
│  
├───job_sites_parser  
│   │   .env  
│   │   .gitignore  
│   │   jobs_parser.py  
│   │   parser_global_variables.py  
│   │   parser_template_class.py  
│   │   parser_tests.py  
│   └───README.md  
│  
├───parse_to_mongo  
│   │   filter_on_salary.py  
│   │   mongo_global_variables.py  
│   │   parse_jobs_to_mongo.py  
│   └───to_mongo_tests.py
│
└───news_parser
    │   news_parser.py  
    └───news_parser_tests.py

</pre>
