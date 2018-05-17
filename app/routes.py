from app import app
from flask import render_template, jsonify
from flask_restful import reqparse
from app.models import *
import json


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/maptest', methods=['GET'])
def maptest():
    return render_template('googleMapTest.html')

@app.route('/chartsTest', methods=['GET'])
def chartsTest():
    return render_template('chatsTest.html')

@app.route('/route_name', methods=['POST'])
def get_all():
   pass


@app.route('/university',methods=['GET'])
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


@app.route('/rank', methods=['GET'])
def rank():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser = argument_adder(parser, [
        ('worldRank', 'le'),
        ('nationalRank', 'le'),
        ('score', float),
        ('year', 'eq')
    ])
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


@app.route('/enrollment', methods=['GET'])
def enrollment():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser = argument_adder(parser, [
        'application',
        'offer',
        ('offerRate', float),
        ('year', 'eq')
    ])
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


@app.route('/completion',methods=['GET'])
def completions():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser = argument_adder(parser, [
        'totalUnweighted',
        'totalWeighted',
        ('year', 'eq')
    ])
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


@app.route('/income',methods=['GET'])
def income():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser = argument_adder(parser, [
        'acg',
        'opsrf',
        'iaof',
        'crcf',
        'total',
        ('year', 'eq')
    ])
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


def argument_adder(parser, to_add):
    for argument in to_add:
        if type(argument) == str:
            parser.add_argument(argument + 'Op', 'ge')
            parser.add_argument(argument, None, type=int)
        elif type(argument) == tuple:
            field = argument[0]
            operator = 'ge'
            argument_type = int
            for key in range(1, len(argument)):
                if type(argument[key]) == str:
                    operator = argument[key]
                else:
                    argument_type = argument[key]
            parser.add_argument(field + 'Op', operator)
            parser.add_argument(field, None, type=argument_type)
    return parser
