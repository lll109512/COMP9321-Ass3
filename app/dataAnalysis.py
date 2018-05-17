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
    def enrollment_mean_summary():
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
            else:
                record_dict[row.year]['applications'].append(row.applications)
                record_dict[row.year]['offers'].append(row.offers)
                record_dict[row.year]['offer_rates'].append(row.offer_rates)
        for year in sorted(record_dict.keys()):
            summary['labels'].append(year)
            summary['applications_mean'].append(np.mean(record_dict[year]['applications']))
            summary['offers_mean'].append(np.mean(record_dict[year]['offers']))
            summary['offer_rates_mean'].append(np.mean(record_dict[year]['offer_rates']))
        return summary
        


