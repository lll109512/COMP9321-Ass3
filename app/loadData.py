# from app.models import University,Rank,Enrollments,Research_income,HDR_completions
# from app import db
import pandas as pd
import re

def load_cwur_data(file_path):
    df = pd.read_csv(file_path,index_col=1)
    audf = df.loc[df['country'] == 'Australia']
    audf = audf.loc[:, audf.columns != 'country']
    dicted_data = audf.to_dict('index')
    cwur_data = []
    for key,value in dicted_data.items():
        name = re.sub(r'\(Australia\)','',key)
        name = name.strip()
        print(name)
        value['institution'] = name
        cwur_data.append(value)
    return cwur_data



def load_research_data(file_path):
    sub_header = [[1, 5, 'Australian Competitve Grants'],
                  [5, 9, 'Other Public Sector Research Funding'],
                  [9,17, 'Industry and Other Funding for Research'],
                  [17,21, 'Cooperative Research Center Funding']]
    research_data = []
    for sheet,year in [(1,2016),(2,2015)]:
        df = pd.read_excel(file_path, sheet, skiprows=6,skip_footer=2, index_col=0)
        df = df.rename(columns=lambda x: x.strip())
        df = df.rename(columns=lambda x: re.sub(r'[ ]+', ' ', x))
        avaliable_institution = df.index.tolist()
        for institution in avaliable_institution:
            temp_inst_data = {}
            df_inst = df.loc[institution]
            for i,j,header_name in sub_header:
                temp_inst_data[header_name] = df_inst.iloc[i:j].to_dict()
            temp_inst_data['Grand Total'] = df_inst.iloc[21]
            temp_inst_data['year'] = year
            temp_inst_data['institution'] = institution
            research_data.append(temp_inst_data)       
    return avaliable_institution, research_data


def load_HDR_data(file_path):
    HDR_data = []
    for sheet,year in [(3,2016),(4,2015)]:
        df = pd.read_excel(file_path, sheet, skiprows=4, skip_footer=2,index_col=0)
        df = df.rename(columns=lambda x: x.strip())
        df = df.rename(columns=lambda x: re.sub(r'\n', ' ', x))
        df = df.rename(columns=lambda x: re.sub(r'[ ]+', ' ', x))
        dicted_data = df.iloc[:, 1:].to_dict('index')
        for key,value in dicted_data.items():
            value['institution'] = key
            value['year'] = year
            HDR_data.append(value)
    return HDR_data


def load_enrollments_data(file_path):
    enrollments_data = []
    df = pd.read_excel(file_path, 10, skiprows=4, skip_footer=5,index_col=0)
    df = df.dropna(how='any')
    years = list(range(2010,2018))
    years_pair = [[year,f'{year}.1',f'{year}.2'] for year in years]
    for year_pair in years_pair:
        dicted_data = df[year_pair].to_dict('index')
        for key,value in dicted_data.items():
            temp = {}
            for sub_key,sub_value in value.items():
                if sub_key == year_pair[0]:
                    temp['Applications'] = sub_value
                elif sub_key == year_pair[1]:
                    temp['Offers'] = sub_value
                else:
                    temp['Offer rates'] = sub_value
            temp['year'] = year_pair[0]
            temp['institution'] = key
            enrollments_data.append(temp)
    return enrollments_data

            
            




# def insert_data(avaliable_institution,reserch_data,HDR_data,cwur_data,enrollments_data):
    
if __name__ == '__main__':
    # avaliable_institution, research_data = load_research_data(
    #     '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/2015_2016_research_income_and_hdr_completions_data.xlsx')
    # print(avaliable_institution)
    # print(research_data)
    # HDR_data = load_HDR_data(
    #     '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/2015_2016_research_income_and_hdr_completions_data.xlsx')
    # print(HDR_data)
    # cwur_data = load_cwur_data(
    #     '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/cwurData.csv')
    # print(cwur_data)
    enrollments_data = load_enrollments_data(
        '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/undergraduate_applications_offers_and_acceptances_2017_appendices_1.xlsm')
    print(enrollments_data)
    pass
