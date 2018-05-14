from app import app
from flask import render_template, jsonify
from flask_restful import reqparse
from app.models import *


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/university')
def university():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser.add_argument('p', 1, type=int)
    parser.add_argument('rpp', 10, type=int)
    args = parser.parse_args()
    query = db.session.query(Universities)
    offset = (args['p'] - 1) * args['rpp']
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    query_result = query.offset(offset).limit(args['rpp'])
    results = []
    for row in query_result:
        results.append(row.name)
    return jsonify(quantity=query.count(), result=results)


@app.route('/rank')
def rank():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser.add_argument('worldRankOp', 'le')
    parser.add_argument('worldRank', None, type=int)
    parser.add_argument('nationalRankOp', 'le')
    parser.add_argument('nationalRank', None, type=int)
    parser.add_argument('scoreOp', 'ge')
    parser.add_argument('score', None, type=float)
    parser.add_argument('yearOp', 'eq')
    parser.add_argument('year', None, type=int)
    parser.add_argument('p', 1, type=int)
    parser.add_argument('rpp', 10, type=int)
    args = parser.parse_args()
    query = db.session.query(Ranks, Universities).filter(Ranks.uni_id == Universities.id)
    offset = (args['p'] - 1) * args['rpp']
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'worldRank': 'world_rank',
        'nationalRank': 'national_rank',
        'score': 'score',
        'year': 'year'
    }
    query = table_query_filter_builder(query, Ranks, args, attribute_to_field)
    query_result = query.offset(offset).limit(args['rpp'])
    results = []
    rank_neglect_fields = ['id', 'uni_id', 'create_date', '_sa_instance_state']
    for uni_rank, uni in query_result:
        rank_copied = vars(uni_rank).copy()
        for field in rank_neglect_fields:
            rank_copied.pop(field)
        rank_copied['university'] = uni.name
        results.append(rank_copied)
    return jsonify(quantity=query.count(), result=results)


@app.route('/enrollment')
def enrollment():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser.add_argument('applicationOp', 'ge')
    parser.add_argument('application', None, type=int)
    parser.add_argument('offerOp', 'ge')
    parser.add_argument('offer', None, type=int)
    parser.add_argument('offerRateOp', 'ge')
    parser.add_argument('offerRate', None, type=float)
    parser.add_argument('yearOp', 'eq')
    parser.add_argument('year', None, type=int)
    parser.add_argument('p', 1, type=int)
    parser.add_argument('rpp', 10, type=int)
    args = parser.parse_args()
    query = db.session.query(Enrollments, Universities).filter(Enrollments.uni_id == Universities.id)
    offset = (args['p'] - 1) * args['rpp']
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'application': 'applications',
        'offer': 'offers',
        'offerRate': 'offer_rates',
        'year': 'year'
    }
    query = table_query_filter_builder(query, Enrollments, args, attribute_to_field)
    query_result = query.offset(offset).limit(args['rpp'])
    results = []
    rank_neglect_fields = ['id', 'uni_id', 'create_date', '_sa_instance_state']
    for uni_enrollment, uni in query_result:
        enrollment_copied = vars(uni_enrollment).copy()
        for field in rank_neglect_fields:
            enrollment_copied.pop(field)
        enrollment_copied['university'] = uni.name
        results.append(enrollment_copied)
    return jsonify(quantity=query.count(), result=results)


@app.route('/completion')
def completions():
    pass


@app.route('/income')
def income():
    pass


@app.route('mashup')
def mashup():
    pass


def table_query_filter_builder(query, table, arguments, accepted_attributes_with_fields):
    for attribute in accepted_attributes_with_fields:
        field = getattr(table, accepted_attributes_with_fields[attribute])
        if arguments[attribute]:
            query = query.filter(getattr(field, f'__{arguments[attribute + "Op"]}__')(arguments[attribute]))
    return query
