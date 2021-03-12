import sys
sys.path.insert(0, '..')

from abc import ABC, abstractmethod

class Parser(ABC):
    '''
    Template class for job aggregation sites parsing
    '''
    def __init__(self, job_title, number_of_pages, verbose = False):
        '''
        
        Parameters
        ----------
        job_title : str
            string with list of job titles to parse.
            Accepted in the following format: "'Analyst' or 'Data Scientist' or
             'Аналитик данных'"
        number_of_pages : int
            Number of pages to parse.
        verbose : Boolean, optional
        The default is False.
        '''
        self.__debug = False
        self.verbose = verbose
        self.job_title = job_title
        self.number_of_pages = number_of_pages
     
    def save(self, name, format = 'csv'):
        '''
        Save table with parsed data in specified format

        Parameters
        ----------
        name : str
            Name of file.
        format : str, optional
            Format of saved file. Either of the following:
                - 'csv'
                - 'excel'
                - 'pickle'
                - 'json'
            The default is 'csv'.

        Returns
        -------
        Saves file in specified format.

        '''
        if format == 'csv':
            return self.df.to_csv(name + '.csv')
        
        elif format == 'excel':
            return self.df.to_excel(name + '.xlsx')
        
        elif format == 'pickle':
            return self.df.to_pickle(name + '.pkl')
        
        elif format == 'json':
            return self.df.to_json(name + '.json')


    @abstractmethod
    def parse_site(self):
        pass


    @abstractmethod
    def preprocess(self):
        pass

