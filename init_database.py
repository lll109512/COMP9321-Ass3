from app import loadData as ld
from app import db
avaliable_institution, research_data = ld.load_research_data(
    '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/2015_2016_research_income_and_hdr_completions_data.xlsx')
HDR_data = ld.load_HDR_data(
    '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/2015_2016_research_income_and_hdr_completions_data.xlsx')
cwur_data = ld.load_cwur_data(
    '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/cwurData.csv')
enrollments_data = ld.load_enrollments_data(
    '/Users/lixingyu/Documents/assignment/comp9321/assignment3/data/undergraduate_applications_offers_and_acceptances_2017_appendices_1.xlsm')
ld.insert_data(avaliable_institution, research_data,HDR_data, cwur_data, enrollments_data)