from app import db
from datetime import datetime


class Universities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    state = db.Column(db.String(8))
    rank = db.relationship('Ranks', backref='universities', lazy='dynamic')
    enrollment = db.relationship('Enrollments', backref='universities', lazy='dynamic')
    research_income = db.relationship('Research_incomes', backref='universities', lazy='dynamic')
    HDR_completion = db.relationship('HDR_completions', backref='universities', lazy='dynamic')
    geo_info = db.relationship('Geo_info', backref='universities', lazy='dynamic')
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<University#{self.id} {self.name}>'


class Ranks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    world_rank = db.Column(db.Integer, index=True)
    national_rank = db.Column(db.Integer, index=True)
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
        return f'<Rank for {self.uni_id}>'


class Enrollments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    applications = db.Column(db.Integer)
    offers = db.Column(db.Integer)
    offer_rates = db.Column(db.Float)
    year = db.Column(db.Integer)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<Enrollment for {self.uni_id}>'


class Research_incomes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    australian_competitive_grants = db.Column(db.Text())
    other_public_sector_research_funding = db.Column(db.Text())
    industry_and_other_funding = db.Column(db.Text())
    cooperative_research_center_funding = db.Column(db.Text())
    grand_total = db.Column(db.Integer())
    year = db.Column(db.Integer())
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'<Research income for {self.uni_id}>'


class HDR_completions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
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
        return f'<HDR Completion for {self.uni_id}>'

class Geo_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.Integer, db.ForeignKey('universities.id'))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    create_date = db.Column(db.DateTime(), default=datetime.utcnow)


neglect_fields = ['id', 'uni_id', 'create_date', '_sa_instance_state']
