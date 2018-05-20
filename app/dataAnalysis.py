from app import db
from app.models import Universities, Enrollments, HDR_completions, Research_incomes
import numpy as np
import json

class Enrollments_Analysis:
    @staticmethod
    def get_enrollment_data_by_name(uniName):
        data = {}
        data['applications'] = []
        data['offers'] = []
        data['offer_rates'] = []
        labels = []
        
        uni = Universities.query.filter_by(name=uniName).first()
        for record in uni.enrollment.order_by(Enrollments.year).all():
            labels.append(record.year)
            data['applications'].append(record.applications)
            data['offers'].append(record.offers)
            data['offer_rates'].append(record.offer_rates)
        data['labels'] = labels
        return data

    @staticmethod
    def get_all_enrollments_data():
        allData = {}
        for uni in Universities.query.all():
            data = {}
            data['applications'] = []
            data['offers'] = []
            data['offer_rates'] = []
            labels = []
            for record in uni.enrollment.order_by(Enrollments.year).all():
                labels.append(record.year)
                data['applications'].append(record.applications)
                data['offers'].append(record.offers)
                data['offer_rates'].append(record.offer_rates)
            data['labels'] = labels
            allData[uni.name] = data
        return allData
        
    @staticmethod
    def enrollment_mean_summary_by_uni():
        record_dict = {}
        summary = {}
        summary['labels'] = []
        summary['applications_mean'] = []
        summary['offers_mean'] = []
        summary['offer_rates_mean'] = []
        for row in Enrollments.query.all():
            if row.year not in record_dict:
                record_dict[row.year] = {}
                record_dict[row.year]['applications'] = []
                record_dict[row.year]['offers'] = []
                record_dict[row.year]['offer_rates'] = []
            record_dict[row.year]['applications'].append(row.applications)
            record_dict[row.year]['offers'].append(row.offers)
            record_dict[row.year]['offer_rates'].append(row.offer_rates)
        for year in sorted(record_dict.keys()):
            summary['labels'].append(year)
            summary['applications_mean'].append(
                np.mean(record_dict[year]['applications']).round(2))
            summary['offers_mean'].append(
                np.mean(record_dict[year]['offers']).round(2))
            summary['offer_rates_mean'].append(
                np.mean(record_dict[year]['offer_rates']).round(2))
        return summary

    @staticmethod
    def enrollment_mean_summary_by_state():
        summary = {}
        for uni,erl in db.session.query(Universities,Enrollments).filter(Universities.id == Enrollments.uni_id).all():
            if uni.state not in summary:
                summary[uni.state] = {}
            if erl.year not in summary[uni.state]:
                summary[uni.state][erl.year] = {}
                summary[uni.state][erl.year]['applications'] = []
                summary[uni.state][erl.year]['offers'] = []
                summary[uni.state][erl.year]['offer_rates'] = []
            summary[uni.state][erl.year]['applications'].append(erl.applications)
            summary[uni.state][erl.year]['offers'].append(erl.offers)
            summary[uni.state][erl.year]['offer_rates'].append(erl.offer_rates)
        mean_summary = {}
        for state,value in summary.items():
            state_summary = {}
            state_summary['labels'] = []
            state_summary['applications_mean'] = []
            state_summary['offers_mean'] = []
            state_summary['offer_rates_mean'] = []
            for year in sorted(value.keys()):
                state_summary['labels'].append(year)
                state_summary['applications_mean'].append(np.mean(value[year]['applications']).round(2))
                state_summary['offers_mean'].append(np.mean(value[year]['offers']).round(2))
                state_summary['offer_rates_mean'].append(np.mean(value[year]['offer_rates']).round(2))
            mean_summary[state] = state_summary
        return mean_summary



class HDR_Income_Analysis:
    @staticmethod
    def HDR_state_summary():
        summary = {}
        states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
        results = HDR_completions.query.join(Universities).add_columns(Universities.name,Universities.state).all()
        for row in results:
            if row.state not in summary:
                summary[row.state] = {}
            year = row[0].year
            if year not in summary[row.state]:
                summary[row.state][year] = {}
                summary[row.state][year]['grand_total_Non_I_and_I_weighted'] = []
            summary[row.state][year]['grand_total_Non_I_and_I_weighted'].append(
                float(row[0].grand_total_non_indigenous_and_indigenous_weighted))

        mean_summary = {}
        for state, value in summary.items():
            if state not in mean_summary:
                mean_summary[state] = {}
            for year, sub_value in value.items():
                if year not in mean_summary[state]:
                    mean_summary[state][year] = {}
                mean_summary[state][year]['mean_grand_total_Non_I_and_I_weighted'] = np.mean(
                    sub_value['grand_total_Non_I_and_I_weighted']).round(2)
        return mean_summary

    @staticmethod
    def Income_state_summary():
        summary = {}
        states = ['ACT', 'NSW', 'NT', 'QLD', 'SA', 'TAS', 'VIC', 'WA']
        item = ['australian_competitive_grants',
                'other_public_sector_research_funding', 
                'industry_and_other_funding', 
                'cooperative_research_center_funding']
        results = Research_incomes.query.join(Universities).add_columns(
            Universities.name, Universities.state).all()
        for row in results:
            if row.state not in summary:
                summary[row.state] = {}
            year = row[0].year
            if year not in summary[row.state]:
                summary[row.state][year] = {}
                summary[row.state][year]['grand_total'] = []
                for i in item:
                    summary[row.state][year][i] = []
            summary[row.state][year]['grand_total'].append(row[0].grand_total)
            for index,i in enumerate(item):
                summary[row.state][year][i].append(json.loads(getattr(row[0],i))['Sub Total' + (index!=0) * f'.{index}'])
        
        mean_summary = {}
        for state, value in summary.items():
            if state not in mean_summary:
                mean_summary[state] = {}
            for year, sub_value in value.items():
                if year not in mean_summary[state]:
                    mean_summary[state][year] = {}
                mean_summary[state][year]['grand_total'] = np.mean(sub_value['grand_total']).round(2)
                for index, i in enumerate(item):
                    mean_summary[state][year][i] = np.mean(sub_value[i]).round(2)
        return mean_summary


    def all_uni_HDR():
        summary = {}
        for uni,hdr in db.session.query(University, HDR_completions).filter(
            University.id == HDR_completions.uni_id).all():
            if uni.name not in summary:
                summary[uni.name] = {}
            summary[uni.name][hdr.year] = hdr.grand_total_non_indigenous_and_indigenous_weighted
        return summarys
    
    def all_uni_Income():
        summary = {}
        item = ['australian_competitive_grants',
                'other_public_sector_research_funding',
                'industry_and_other_funding',
                'cooperative_research_center_funding']
        for uni, income in db.session.query(University, Research_incomes).filter(
                University.id == Research_incomes.uni_id).all():
            if uni.name not in summary:
                summary[uni.name] = {}
            if income.year not in summary[uni.name]:
                summary[uni.name][income.year] = {}
            for index, i in enumerate(item):
                summary[uni.name][income.year][i] = json.loads(
                    getattr(income, i))['Sub Total' + (index != 0) * f'.{index}']
            summary[uni.name][income.year]['grand_total'] = income.grand_total
        return summary
