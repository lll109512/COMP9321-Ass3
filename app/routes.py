from app import app
from flask import render_template, jsonify, redirect, url_for
from flask_restful import reqparse
from app.models import *
from app.dataAnalysis import Enrollments_Analysis as ea
import json


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('raw_data'))


@app.route('/raw', methods=['GET'])
def raw_data():
    return render_template('raw.html', style={'raw': 'active', 'analysis': ''})


@app.route('/analysis', methods=['GET'])
def analysis():
    return render_template('analysis.html', style={'raw': '', 'analysis': 'active'})


@app.route('/mapTest', methods=['GET'])
def map_test():
    return render_template('googleMapTest.html')


@app.route('/chartsTest', methods=['GET'])
def charts_test():
    return render_template('chatsTest.html')

@app.route('/get_uni_list', methods=['POST'])
def get_uni_list():
    unis = Universities.query.all()
    data = []
    for uni in unis:
        data.append({
            'id':uni.id,
            'label':uni.name
        })
    return jsonify(result=data),200


@app.route('/analysis_enrollments', methods=['POST'])
def analysis_enrollments():
    parser = reqparse.RequestParser()
    parser.add_argument('uni','')
    parser.add_argument('methods','')
    args = parser.parse_args()
    if args['methods'] == 'by_uni_name':
        data = ea.get_enrollment_data_by_name(args['uni'])
        if not data['applications']:
            return jsonify(error=1),400
    elif args['methods'] == 'all_mean_summary':
        data = ea.enrollment_mean_summary()
    elif args['methods'] == 'state_mean_summary':
        data = ea.enrollment_mean_summary_by_state()
    else:
        return jsonify(error=1),400
    return jsonify(result=data),200



@app.route('/university', methods=['GET'])
def university():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    args = parser.parse_args()
    query = db.session.query(Universities)
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    query_result = query.all()
    results = []
    for row in query_result:
        results.append(row.name)
    return jsonify(result=results)


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
    parser.add_argument('order', None)
    parser.add_argument('desc', False, type=bool)
    args = parser.parse_args()
    query = db.session.query(Ranks, Universities).filter(Ranks.uni_id == Universities.id)
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'worldRank': 'world_rank',
        'nationalRank': 'national_rank',
        'score': 'score',
        'year': 'year'
    }
    query = table_query_filter_builder(query, Ranks, args, attribute_to_field)
    query_result = query.all()
    results = []
    for uni_rank, uni in query_result:
        rank_copied = without_unnecessary_fields(vars(uni_rank).copy())
        rank_copied['university'] = uni.name
        results.append(rank_copied)
    return jsonify(result=results)


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
    parser.add_argument('order', None)
    parser.add_argument('desc', True, type=bool)
    args = parser.parse_args()
    query = db.session.query(Enrollments, Universities).filter(Enrollments.uni_id == Universities.id)
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'application': 'applications',
        'offer': 'offers',
        'offerRate': 'offer_rates',
        'year': 'year'
    }
    query = table_query_filter_builder(query, Enrollments, args, attribute_to_field)
    query_result = query.all()
    results = []
    for uni_enrollment, uni in query_result:
        enrollment_copied = without_unnecessary_fields(vars(uni_enrollment).copy())
        enrollment_copied['university'] = uni.name
        results.append(enrollment_copied)
    return jsonify(result=results)


@app.route('/completion', methods=['GET'])
def completions():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser = argument_adder(parser, [
        'totalUnweighted',
        'totalWeighted',
        ('year', 'eq')
    ])
    parser.add_argument('order', None)
    parser.add_argument('desc', True, type=bool)
    args = parser.parse_args()
    query = db.session.query(HDR_completions, Universities).filter(HDR_completions.uni_id == Universities.id)
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    attribute_to_field = {
        'totalUnweighted': 'grand_total_non_indigenous_and_indigenous_unweighted',
        'totalWeighted': 'grand_total_non_indigenous_and_indigenous_weighted',
        'year': 'year'
    }
    query = table_query_filter_builder(query, HDR_completions, args, attribute_to_field)
    query_result = query.all()
    results = []
    for uni_completion, uni in query_result:
        completion_copied = without_unnecessary_fields(vars(uni_completion).copy())
        completion_copied['university'] = uni.name
        results.append(completion_copied)
    return jsonify(result=results)


@app.route('/income', methods=['GET'])
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
    parser.add_argument('order', None)
    parser.add_argument('desc', True, type=bool)
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

        if (args['acg'] is None or
            args['acg'] is not None and
            getattr(acg['Sub Total'], f'__{args["acgOp"]}__')(args['acg'])) and \
                (args['opsrf'] is None or
                 args['opsrf'] is not None and
                 getattr(opsrf['Sub Total.1'], f'__{args["opsrfOp"]}__')(args['opsrf'])) and \
                (args['iaof'] is None or
                 args['iaof'] is not None and
                 getattr(iaof['Sub Total.2'], f'__{args["iaofOp"]}__')(args['iaof'])) and \
                (args['crcf'] is None or
                 args['crcf'] is not None and
                 getattr(crcf['Sub Total.3'], f'__{args["crcfOp"]}__')(args['crcf'])):
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
    return jsonify(result=results)


@app.route('/mashup')
def mashup():
    final = {}
    delete_fields = ['uni_id', 'year', 'create_date', '_sa_instance_state']
    # create all universities
    universities = db.session.query(Universities).all()
    university_name = {}
    for university in universities:
        final[university.name] = {
            'id': university.id,
            'rank': {},
            'enrollment': {},
            'income': {},
            'completion': {}
        }
        university_name[university.id] = university.name
    # rank data
    ranks = db.session.query(Ranks).all()
    for rank in ranks:
        year_rank = without_unnecessary_fields(vars(rank).copy(), delete_fields)
        final[university_name[rank.uni_id]]['rank'][rank.year] = year_rank
    # enrollment data
    enrollments = db.session.query(Enrollments).all()
    for enrollment in enrollments:
        year_enrollment = without_unnecessary_fields(vars(enrollment).copy(), delete_fields)
        final[university_name[enrollment.uni_id]]['enrollment'][enrollment.year] = year_enrollment
    # research income
    incomes = db.session.query(Research_incomes).all()
    for income in incomes:
        year_income = without_unnecessary_fields(vars(income).copy(), delete_fields)
        for field in ['australian_competitive_grants', 'other_public_sector_research_funding',
                      'industry_and_other_funding', 'cooperative_research_center_funding']:
            year_income[field] = json.loads(year_income[field])
        final[university_name[income.uni_id]]['income'][income.year] = year_income
    # completion
    completions = db.session.query(HDR_completions).all()
    for completion in completions:
        year_completion = without_unnecessary_fields(vars(completion).copy(), delete_fields)
        final[university_name[completion.uni_id]]['completion'][completion.year] = year_completion
    return jsonify(result=final)


def table_query_filter_builder(query, table, arguments, accepted_attributes_with_fields):
    for attribute in accepted_attributes_with_fields:
        field = getattr(table, accepted_attributes_with_fields[attribute])
        if arguments[attribute]:
            query = query.filter(getattr(field, f'__{arguments[attribute + "Op"]}__')(arguments[attribute]))
    print(arguments['desc'])
    if arguments['order'] is not None:
        field = getattr(table, accepted_attributes_with_fields[arguments['order']])
        if arguments['desc']:
            field = field.desc()
        query = query.order_by(field)
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
                elif type(argument[key]) == type:
                    argument_type = argument[key]
            parser.add_argument(field + 'Op', operator)
            parser.add_argument(field, None, type=argument_type)
    return parser


def without_unnecessary_fields(inputs, fields_to_delete=None):
    if fields_to_delete is None:
        fields_to_delete = neglect_fields
    for field in fields_to_delete:
        inputs.pop(field)
    return inputs
