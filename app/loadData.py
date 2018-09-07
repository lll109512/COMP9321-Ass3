from app.models import Universities, Ranks, Enrollments, Research_incomes, HDR_completions
from app import db
import pandas as pd
import re
import json


def process_university_name(name):
    name = re.sub(r'^(The|the)', '', name)
    name = name.strip()
    name = re.sub(r'\n', ' ', name)
    name = re.sub(r'[ ]+', ' ', name)
    if 'RMIT' in name:
        name = 'Royal Melbourne Institute of Technology'
    if 'Federation' in name:
        name = 'Federation University Australia'
    return name


def load_cwur_data(file_path):
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    audf = df.loc[df['country'] == 'Australia']
    audf = audf.loc[:, audf.columns != 'country']
    cwur_data = []
    for i in audf.index:
        dicted = json.loads(audf.loc[i].to_json())
        name = re.sub(r'\(Australia\)', '', dicted['institution'])
        name = name.strip()
        dicted['institution'] = name
        cwur_data.append(dicted)
    return cwur_data


def load_research_data(file_path):
    sub_header = [[1, 5, 'Australian Competitve Grants'],
                  [5, 9, 'Other Public Sector Research Funding'],
                  [9, 17, 'Industry and Other Funding for Research'],
                  [17, 21, 'Cooperative Research Center Funding']]
    research_data = []
    for sheet, year in [(1, 2016), (2, 2015)]:
        df = pd.read_excel(file_path, sheet, skiprows=6, skip_footer=2, index_col=0)
        df = df.rename(columns=lambda x: x.strip())
        df = df.rename(columns=lambda x: re.sub(r'\n', ' ', x))
        df = df.rename(columns=lambda x: re.sub(r'[ ]+', ' ', x))
        available_institution = df.index.tolist()
        formatted_institution = [process_university_name(i) for i in available_institution]
        for institution in available_institution:
            temp_inst_data = {}
            df_inst = df.loc[institution]
            for i, j, header_name in sub_header:
                temp_inst_data[header_name] = df_inst.iloc[i:j].to_json()
            temp_inst_data['Grand Total'] = int(df_inst.iloc[21])
            temp_inst_data['year'] = int(year)
            temp_inst_data['institution'] = institution
            research_data.append(temp_inst_data)
    return formatted_institution, research_data


def load_HDR_data(file_path):
    HDR_data = []
    for sheet, year in [(3, 2016), (4, 2015)]:
        df = pd.read_excel(file_path, sheet, skiprows=4, skip_footer=2, index_col=0)
        df = df.rename(columns=lambda x: x.strip())
        df = df.rename(columns=lambda x: re.sub(r'\n', ' ', x))
        df = df.rename(columns=lambda x: re.sub(r'[ ]+', ' ', x))
        dicted_data = df.iloc[:, 1:].to_dict('index')
        for key, value in dicted_data.items():
            value['institution'] = key
            value['year'] = year
            HDR_data.append(value)
    return HDR_data


def load_university_state(file_path):
    df = pd.read_excel(file_path, 1, skiprows=6, skip_footer=2, index_col=0)
    df = df.rename(columns=lambda x: x.strip())
    df = df.rename(columns=lambda x: re.sub(r'\n', ' ', x))
    df = df.rename(columns=lambda x: re.sub(r'[ ]+', ' ', x))
    df = df.rename(columns=lambda x: process_university_name(x))
    available_institution = df.index.tolist()
    formatted_institution = [process_university_name(i) for i in available_institution]
    values = df.iloc[:, 0].to_dict().values()
    uni_state = dict(zip(formatted_institution, values))
    return uni_state


def load_enrollments_data(file_path):
    enrollments_data = []
    df = pd.read_excel(file_path, 10, skiprows=4, skip_footer=5, index_col=0)
    df = df.dropna(how='any')
    years = list(range(2010, 2018))
    years_pair = [[year, f'{year}.1', f'{year}.2'] for year in years]
    for year_pair in years_pair:
        dicted_data = df[year_pair].to_dict('index')
        for key, value in dicted_data.items():
            temp = {}
            for sub_key, sub_value in value.items():
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


def insert_data(available_institution, research_data, HDR_data, cwur_data, enrollments_data, uni_state):
    for institution in available_institution:
        u = Universities(name=institution, state=uni_state[institution])
        db.session.add(u)
    for item in research_data:
        u = Universities.query.filter(Universities.name.contains(process_university_name(item['institution']))).first()
        if u:
            ri = Research_incomes(
                australian_competitive_grants=item['Australian Competitve Grants'],
                other_public_sector_research_funding=item['Other Public Sector Research Funding'],
                industry_and_other_funding=item['Industry and Other Funding for Research'],
                cooperative_research_center_funding=item['Cooperative Research Center Funding'],
                grand_total=item['Grand Total'],
                year=item['year']
            )
            u.research_income.append(ri)
        else:
            print(f"missing university:{item['institution']}")
    for item in HDR_data:
        u = Universities.query.filter(Universities.name.contains(process_university_name(item['institution']))).first()
        if u:
            hdr = HDR_completions(
                research_master_hc_non_indigenous=item['Research Masters High Cost non-Indigenous'],
                research_master_lc_non_indigenous=item['Research Masters Low Cost non-Indigenous'],
                research_doctorate_hc_non_indigenous=item['Research Doctorate High Cost non-Indigenous'],
                research_doctorate_lc_non_indigenous=item['Research Doctorate Low Cost non-Indigenous'],
                total_non_indigenous_unweighted=item['Total non-Indigenous (Unweighted)'],
                research_master_hc_indigenous=item['Research Masters High Cost Indigenous'],
                research_master_lc_indigenous=item['Research Masters Low Cost Indigenous'],
                research_doctorate_hc_indigenous=item['Research Doctorate High Cost Indigenous'],
                research_doctorate_lc_indigenous=item['Research Doctorate Low Cost Indigenous'],
                total_indigenou_unweighted=item['Total Indigenous (Unweighted)'],
                grand_total_non_indigenous_and_indigenous_unweighted=item[
                    'Grand Total Non-Indigenous and Indigenous (Unweighted)'],
                grand_total_non_indigenous_and_indigenous_weighted=item[
                    'Grand Total Non-Indigenous and Indigenous (Weighted)'],
                year=item['year']
            )
            u.HDR_completion.append(hdr)
        else:
            print(f"missing university:{item['institution']}")
    for item in cwur_data:
        u = Universities.query.filter(Universities.name.contains(process_university_name(item['institution']))).first()
        if u:
            rank = Ranks(
                world_rank=item['world_rank'],
                national_rank=item['national_rank'],
                quality_of_education=item['quality_of_education'],
                alumni_employment=item['alumni_employment'],
                quality_of_faculty=item['quality_of_faculty'],
                publications=item['publications'],
                influence=item['influence'],
                citations=item['citations'],
                broad_impact=item['broad_impact'],
                patents=item['patents'],
                score=item['score'],
                year=item['year']
            )
            u.rank.append(rank)
        else:
            print(f"missing university:{item['institution']}")
    for item in enrollments_data:
        u = Universities.query.filter(Universities.name.contains(process_university_name(item['institution']))).first()
        if u:
            enrol = Enrollments(
                applications=item['Applications'],
                offers=item['Offers'],
                offer_rates=item['Offer rates'],
                year=item['year']
            )
            u.enrollment.append(enrol)
        else:
            print(f"missing university:{item['institution']}")
    db.session.commit()
