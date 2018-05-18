from app import db
from app.models import Universities, Enrollments
import numpy as np

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
            summary['applications_mean'].append(np.mean(record_dict[year]['applications']))
            summary['offers_mean'].append(np.mean(record_dict[year]['offers']))
            summary['offer_rates_mean'].append(np.mean(record_dict[year]['offer_rates']))
        return summary

    @staticmethod
    def enrollment_mean_summary_by_state():
        summary = {}
        states = ['ACT','NSW','NT','QLD','SA','TAS','VIC','WA']
        for state in states:
            year_record = {}
            state_unis = Universities.query.filter_by(state=state).all()
            for uni in state_unis:
                uni_enrollments = uni.enrollment.order_by(Enrollments.year).all()
                for enrollment in uni_enrollments:
                    if enrollment.year not in year_record:
                        year_record[enrollment.year] = {}
                        year_record[enrollment.year]['applications'] = []
                        year_record[enrollment.year]['offers'] = []
                        year_record[enrollment.year]['offer_rates'] = []
                    year_record[enrollment.year]['applications'].append(enrollment.applications)
                    year_record[enrollment.year]['offers'].append(enrollment.offers)
                    year_record[enrollment.year]['offer_rates'].append(enrollment.offer_rates)
            sub_summary = {}
            sub_summary['labels'] = []
            sub_summary['applications_mean'] = []
            sub_summary['offers_mean'] = []
            sub_summary['offer_rates_mean'] = []
            for year in sorted(year_record.keys()):
                sub_summary['labels'].append(year)
                sub_summary['applications_mean'].append(np.mean(year_record[year]['applications']))
                sub_summary['offers_mean'].append(np.mean(year_record[year]['offers']))
                sub_summary['offer_rates_mean'].append(np.mean(year_record[year]['offer_rates']))
            summary[state] = sub_summary
        return summary






