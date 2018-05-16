from app import app
from flask import render_template, jsonify
from flask_restful import reqparse
from app.models import *
import json


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
    for uni_rank, uni in query_result:
        rank_copied = vars(uni_rank).copy()
        for field in neglect_fields:
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
    for uni_enrollment, uni in query_result:
        enrollment_copied = vars(uni_enrollment).copy()
        for field in neglect_fields:
            enrollment_copied.pop(field)
        enrollment_copied['university'] = uni.name
        results.append(enrollment_copied)
    return jsonify(quantity=query.count(), result=results)


@app.route('/completion')
def completions():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser.add_argument('totalUnweightedOp', 'ge')
    parser.add_argument('totalUnweighted', None, type=int)
    parser.add_argument('totalWeightedOp', 'ge')
    parser.add_argument('totalWeighted', None, type=int)
    parser.add_argument('yearOp', 'eq')
    parser.add_argument('year', None, type=int)
    parser.add_argument('p', 1, type=int)
    parser.add_argument('rpp', 10, type=int)
    args = parser.parse_args()
    query = db.session.query(HDR_completions, Universities).filter(HDR_completions.uni_id == Universities.id)
    offset = (args['p'] - 1) * args['rpp']
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'totalUnweighted': 'grand_total_non_indigenous_and_indigenous_unweighted',
        'totalWeighted': 'grand_total_non_indigenous_and_indigenous_weighted',
        'year': 'year'
    }
    query = table_query_filter_builder(query, HDR_completions, args, attribute_to_field)
    query_result = query.offset(offset).limit(args['rpp'])
    results = []
    for uni_completion, uni in query_result:
        completion_copied = vars(uni_completion).copy()
        for field in neglect_fields:
            completion_copied.pop(field)
        completion_copied['university'] = uni.name
        results.append(completion_copied)
    return jsonify(quantity=query.count(), result=results)


@app.route('/income')
def income():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser.add_argument('acgOp', 'ge')
    parser.add_argument('acg', None, type=int)
    parser.add_argument('opsrfOp', 'ge')
    parser.add_argument('opsrf', None, type=int)
    parser.add_argument('iaofOp', 'ge')
    parser.add_argument('iaof', None, type=int)
    parser.add_argument('crcfOp', 'ge')
    parser.add_argument('crcf', None, type=int)
    parser.add_argument('totalOp', 'ge')
    parser.add_argument('total', None, type=int)
    parser.add_argument('yearOp', 'eq')
    parser.add_argument('year', None, type=int)
    parser.add_argument('p', 1, type=int)
    parser.add_argument('rpp', 10, type=int)
    args = parser.parse_args()
    query = db.session.query(Research_incomes, Universities).filter(Research_incomes.uni_id == Universities.id)
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'total': 'grand_total',
        'year': 'year'
    }
    query = table_query_filter_builder(query, Research_incomes, args, attribute_to_field)
    query_result = query.all()
    results = []
    for uni_income, uni in query_result:
        acg = json.loads(uni_income.australian_competitive_grants)
        opsrf = json.loads(uni_income.other_public_sector_research_funding)
        iaof = json.loads(uni_income.industry_and_other_funding)
        crcf = json.loads(uni_income.cooperative_research_center_funding)

        if (args['acg'] is None or (args['acg'] is not None and getattr(acg['Sub Total'], f'__{args["acgOp"]}__')(args['acg']))) and \
            (args['opsrf'] is None or (args['opsrf'] is not None and getattr(opsrf['Sub Total.1'], f'__{args["opsrfOp"]}__')(args['opsrf']))) and \
            (args['iaof'] is None or (args['iaof'] is not None and getattr(iaof['Sub Total.2'], f'__{args["iaofOp"]}__')(args['iaof']))) and \
            (args['crcf'] is None or (args['crcf'] is not None and getattr(crcf['Sub Total.3'], f'__{args["crcfOp"]}__')(args['crcf']))):
            row = {
                'university': uni.name,
                'year': uni_income.year,
                'australian_competitive_grants': acg,
                'other_public_sector_research_funding': opsrf,
                'industry_and_other_funding': iaof,
                'cooperative_research_center_funding': crcf,
                'grand_total': uni_income.grand_total
            }
            results.append(row)
    return jsonify(quantity=len(results), result=results)


@app.route('/mashup')
def mashup():
    pass


def table_query_filter_builder(query, table, arguments, accepted_attributes_with_fields):
    for attribute in accepted_attributes_with_fields:
        field = getattr(table, accepted_attributes_with_fields[attribute])
        if arguments[attribute]:
            query = query.filter(getattr(field, f'__{arguments[attribute + "Op"]}__')(arguments[attribute]))
    return query
