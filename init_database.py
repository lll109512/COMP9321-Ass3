from app import loadData as ld

available_institution, research_data = ld.load_research_data(
    './data/2015_2016_research_income_and_hdr_completions_data.xlsx')
HDR_data = ld.load_HDR_data(
    './data/2015_2016_research_income_and_hdr_completions_data.xlsx')
cwur_data = ld.load_cwur_data(
    './data/cwurData.csv')
enrollments_data = ld.load_enrollments_data(
    './data/undergraduate_applications_offers_and_acceptances_2017_appendices_1.xlsm')
ld.insert_data(available_institution, research_data, HDR_data, cwur_data, enrollments_data)
