import sys
sys.path.insert(0, '..')

import numpy as np
import pandas as pd
import requests
import warnings
warnings.filterwarnings('ignore')
from parser_global_variables import TAGS_HH, HH_URL, HH_AREA, SUPERJOB_AREA,\
    DATE_FROM, DATE_TO, PER_PAGE, TAGS_SUPERJOB, SUPERJOB_URL, SUPERJOB_SECRET
from parser_template_class import Parser



def enter_specs():
    '''
    Function for manually enter job titles to search for and number of pages 
    to parse
    
    Returns
    -------
    job_title : string with job titles "or" separated
    
    number_of_pages : integer, number of pages to parse
    '''
    
    job_title = "' or '".join(input('Enter comma separated list of job names'
                                    ' to search for: ').split(','))
    job_title = f"'{job_title}'"
    if all('' == s for s in [job_title]):
        raise ValueError('List of job titles is not specified')
    
    number_of_pages = (input('Enter number of pages to scrap or press Enter '
                             'to evaluate all pages available: '))
    if not number_of_pages:
        number_of_pages = 100500
    else:
        number_of_pages = int(number_of_pages)
    
    return job_title, number_of_pages


        
class HHParser(Parser):
    
    def parse_site(self, area = HH_AREA, date_from = DATE_FROM, 
                   date_to = DATE_TO, per_page = PER_PAGE):
        '''
        Function to parse hh.ru job posts

        Parameters
        ----------
        area : str, optional
            hh.ru area code. The default is '113' (Russia).
        
        date_from : datetime, optional
            Date to start searching from in format '2020-09-12'. 
            The default is 6 months ago.
        
        date_to : datetime, optional
            Date to end searching to in format '2020-09-12'.
            The default is today.
        
        per_page : int, optional
            Number of vacancies per page. The default is 100.

        Returns
        -------
        Data Frame of raw job vacancies info.
        '''
 
        datf = []
        debug = self._Parser__debug
        verbose = self.verbose
        number_of_pages = self.number_of_pages
        job_title = self.job_title

        if verbose:
            print('List of job titles to parse:', job_title)

        data=[]
        try:
            for i in range(1, number_of_pages+1):
                if verbose:
                    print(f'Evaluating page {i}')
                url = HH_URL
                par = {
                    'text':job_title,
                    'area':area,
                    'per_page': per_page,
                    'page':i,
                    'date_from':date_from,
                    'date_to': date_to
                    }
                r = requests.get(url, params=par)
                if debug:
                    print(r.url)
                e = r.json()
                data.append(e)
                for d in range(len(data)):
                    for j in range(len(data[d]['items'])):
                        datf.append(data[d]['items'][j])
        
        except:
            if verbose:
                print(f'Page limit reached. Last page {i}')
                print('Number of collected samples: ', len(datf))
    
        past_df = pd.DataFrame(datf)
        # keep only unique jobs posts
        if verbose:
            print(past_df.columns)
        past_df = past_df[past_df['id'].duplicated() == False]

        v =[]
        for i in range(past_df.shape[0]):
            if verbose:
                if i%10 == 0:
                    print(f'Downloaded {i} vacancies')
            r = requests.get(np.array(past_df['url'])[i])
            info = r.json()
            v.append(info)
        self.v = v
        return pd.DataFrame(v)
    
    def preprocess(self, tags = TAGS_HH):
        '''
        Function to preprocess data downloaded from hh.ru

        Parameters
        ----------
        tags : list, optional
            List of tags to keep. The default is TAGS_HH.

        Returns
        -------
        df : Data Frame of preprocessed data.
        '''
        
        #keep only required fields
        df = pd.DataFrame(self.v)[tags]
        
        # tackle nans to parse dicts
        df['salary']= df.salary.fillna(
            "{'from': None, 'to': None, 'currency': None, 'gross': False}"
            )
        df['experience']= df.experience.fillna("{'id': None, 'name': None}")
        df['address'] = df['address'].fillna(
            "{'city': None, 'street': None, 'building': None,"
            " 'description': None, 'lat': None, 'lng': None,"
            " 'raw': None, 'metro': {'station_name': 'None',"
            " 'line_name': None, 'station_id': None, "
            "'line_id': None, 'lat': None, 'lng': None},"
            " 'metro_stations': [{'station_name': None, "
            "'line_name': None, 'station_id': None,"
            " 'line_id': None, 'lat': None, 'lng': None}]}")
        df['employer'] = df.description.fillna(
            "{'id': None, 'name': None, 'url': None, "
            "'alternate_url': None,'logo_urls': "
            "{'90': None, 'original': None, '240': None}, "
            "'vacancies_url': None, 'trusted': None}"
            )
        df["employment"] = df.employment.fillna(
            "{'id': None, 'name': None}"
            )
        df['site'] = df.site.fillna(
            "{'id': None, 'name': None}"
            )
        df['type'] = df.type.fillna(
            "{'id': None, 'name': None}"
            )
        sals_from = []
        sals_to = []
        exp = []
        for i in range(df.shape[0]):
            sal_from = eval(str(np.array(df['salary'])[i]))['from']
            sals_from.append(sal_from)
            sal_to = eval(str(np.array(df['salary'])[i]))['to']
            sals_to.append(sal_to)
            e = eval(str(np.array(df['experience'])[i]))['name']
            exp.append(e)
            
        df['payment_from'] = sals_from
        df['payment_to'] = sals_to
        df['experience'] = exp
        df['site'] = 'hh.ru'
        
        df.rename(columns = {
            'alternate_url':'url',
            'name':'job_name',
            'date_published':'published_at',
            'vacancyRichText':'description',
            'firm_name':'employer',
            'employment':'employment_type',
            'candidat':'skills',
            'type':'is_closed',
            'key_skills':'skills',
            'specializations':'specialisation',
            'archived':'is_archived'
            },
            inplace = True)

        self.df = df
        return df
    
    

class SuperjobParser(Parser):

    def parse_site(self, area = SUPERJOB_AREA, date_published_from = DATE_FROM,
                   date_published_to = DATE_TO,
                   per_page = PER_PAGE):
        '''
        Function to parse superjob.ru job posts

        Parameters
        ----------
        area : str, optional
            superjob.ru area code. The default is '1' (Russia).
        
        date_published_from : datetime, optional
            Date to start searching from in format '2020-09-12'. 
            The default is 6 months ago.
        
        date_published_to : datetime, optional
            Date to end searching to in format '2020-09-12'.
            The default is today.
        
        per_page : int, optional
            Number of vacancies per page. The default is 100.
        
        Returns
        -------
        past_df : Data Frame of raw job vacancies info.
        '''
        
        datf = []
        debug = self._Parser__debug
        verbose = self.verbose
        number_of_pages = self.number_of_pages
        job_title = self.job_title

        if verbose:
            print('List of job titles to parse:', job_title)
        
        data = []
        for i in range(1, number_of_pages + 1):
            try:
                if verbose:
                    print(f'Evaluating page {i}')
                url = SUPERJOB_URL
                secret = SUPERJOB_SECRET
                headers = {
                    'Host': 'api.superjob.ru',
                    'X-Api-App-Id': secret,
                    'Authorization': 'Bearer r.000000010000001.example.'
                    'access_token',
                    'Content-Type': 'application/x-www-form-urlencoded'
                    }
                par = {
                    'keywords_skwc':job_title,
                    'countries':area,
                    'count': per_page,
                    'page':i,
                    'date_published_from':date_published_from
                    }
                r = requests.get(url, headers = headers, params = par)
                if debug:
                    print(r.url)
                e=r.json()['objects']
                
                if len(e)==0:
                    print(f'Page limit reached. Last page {i}')
                    break
                
                else:
                    data.append(e)
                
                datf = []
                for d in range(len(data)):
                    for j in range(len(data[d])):
                        datf.append(data[d][j])
                  
            except:
                if verbose:
                    print(f'Page limit reached. Last page {i}')
                    print('number of collected samples: ', len(datf))
    
            past_df = pd.DataFrame(datf)
            past_df = past_df[past_df['id'].duplicated() == False]
            self.past_df = past_df

        return past_df

    def preprocess(self):
        '''
        Function to preprocess data downloaded from superjob.ru

        Parameters
        ----------
        tags : list, optional
            List of tags to keep. The default is TAGS_SUPERJOB.

        Returns
        -------
        df : Data Frame of preprocessed data.
        '''
        
        past_df = self.past_df
        past_df = past_df[TAGS_SUPERJOB]
        past_df['site'] ='superjob.ru'
        past_df.rename(columns = {
            'link':'url',
            'profession':'job_name',
            'date_published':'published_at',
            'vacancyRichText':'description',
            'firm_name':'employer',
            'type_of_work':'employment_type',
            'candidat':'skills',
            'catalogues':'specialisation',
            'is_archive':'is_archived'
            },
            inplace = True)
        
        return past_df
        
def job_parser(hh = True, superjobs = True, verbose = False, save = True, 
               format = 'csv'):
    '''
    Function to parse the vacancies info from two sites: hh.ru and superjob.ru

    Parameters
    ----------
    hh : boolean, optional
        Whether to parse data from hh.ru. The default is True.
    
    superjobs : boolean, optional
        Whether to parse data from superjob.ru. The default is True.
    
    verbose : boolean, optional
        Whether to print status of parsing. The default is False.
    
    save : boolean, optional
        Whether to save the output dataframe to file. The default is False.
    
    format : Format to save file. Either of the following:
        - 'csv'
        - 'excel'
        - 'pickle'
        - 'json'
        The default is 'csv'.

    Returns
    -------
    Data Frame of parsed vacancies data from specified sites.
    '''
    
    job_title, number_of_pages = enter_specs()
    
    if hh:
        hh_pars = HHParser(job_title, number_of_pages, verbose = verbose)
        hh_pars.parse_site()
        hh_df = hh_pars.preprocess()
    else:
        hh_df = pd.DataFrame(None)
    print(hh_df.shape)
    print(hh_df.columns)
    
    if superjobs:
        superjobs_pars = SuperjobParser(job_title, number_of_pages, 
                                        verbose = verbose)
        superjobs_pars.parse_site()
        superjobs_df = superjobs_pars.preprocess()
    else:
        superjobs_df = pd.DataFrame(None)
    print(superjobs_df.shape)
    print(superjobs_df.columns)
    
    df = pd.concat([hh_df, superjobs_df])
    
    if save:
        name = 'vacancies'
        if format == 'csv':
            df.to_csv(name + '.csv')
        
        elif format == 'excel':
            df.to_excel(name + '.xlsx')
        
        elif format == 'pickle':
            df.to_pickle(name + '.pkl')
        
        elif format == 'json':
            df.to_json(name + '.json')
    
    return df
