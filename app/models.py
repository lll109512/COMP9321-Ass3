from app import db
from datetime import datetime

class University(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),index=True, unique=True)
    rank = db.relationship('Rank', backref='university', lazy='dynamic')
    enrollments = db.relationship('Enrollments', backref='university', lazy='dynamic')
    research_income = db.relationship('Research_income', backref='university', lazy='dynamic')
    HDR_completions = db.relationship('HDR_completions', backref='university', lazy='dynamic')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)


    def __repr__(self):
        return '<name {}>'.format(self.name)


class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    word_rank = db.Column(db.Integer, index=True)
    national_rank = db.Column(db.Integer,index=True)
    quality_of_education = db.Column(db.Integer)
    alumni_employment = db.Column(db.Integer)
    quality_of_faculty = db.Column(db.Integer)
    publications = db.Column(db.Integer)
    influence = db.Column(db.Integer)
    citations = db.Column(db.Integer)
    broad_impact = db.Column(db.Integer)
    patents = db.Column(db.Integer)
    score = db.Column(db.Float)
    year = db.Column(db.Integer)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<rank for {}>'.format(self.uni_id)


class Enrollments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    applications = db.Column(db.Integer)
    offers = db.Column(db.Integer)
    offer_rates = db.Column(db.Float)
    year = db.Column(db.Integer)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Enrollments for {}>'.format(self.uni_id)


class Research_income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    australian_competitive_grants = db.Column(db.Text())
    other_public_sector_research_funding = db.Column(db.Text())
    industry_and_other_funding = db.Column(db.Text())
    cooperative_research_center_funding = db.Column(db.Text())
    grand_total = db.Column(db.Integer())
    year = db.Column(db.Integer())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Research income for {}>'.format(self.uni_id)

class HDR_completions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('university.id'))
    research_master_hc_non_indigenous = db.Column(db.String(32))
    research_master_lc_non_indigenous = db.Column(db.String(32))
    research_doctorate_hc_non_indigenous = db.Column(db.String(32))
    research_doctorate_lc_non_indigenous = db.Column(db.String(32))
    total_non_indigenous_unweighted = db.Column(db.String(32))
    research_master_hc_indigenous = db.Column(db.String(32))
    research_master_lc_indigenous = db.Column(db.String(32))
    research_doctorate_hc_indigenous = db.Column(db.String(32))
    research_doctorate_lc_indigenous = db.Column(db.String(32))
    total_indigenou_unweighted = db.Column(db.String(32))
    grand_total_non_indigenous_and_indigenous_unweighted = db.Column(db.String(32))
    grand_total_non_indigenous_and_indigenous_weighted = db.Column(db.String(32))
    year = db.Column(db.Integer())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<HDR Completions for {}>'.format(self.uni_id)
