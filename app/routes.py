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
    result_quantity = query.count()
    query_result = query.offset(offset).limit(args['rpp'])
    results = []
    for row in query_result:
        results.append(row.name)
    return jsonify(quantity=result_quantity, result=results)


@app.route('/rank')
def rank():
    parser = reqparse.RequestParser()
    parser.add_argument('uni', '')
    parser.add_argument('year', False, type=int)
    parser.add_argument('p', 1, type=int)
    parser.add_argument('rpp', 10, type=int)
    args = parser.parse_args()
    query = db.session.query(Ranks, Universities).filter(Ranks.uni_id == Universities.id)
    offset = (args['p'] - 1) * args['rpp']
    if args['uni'] != '':
        query = query.filter(Universities.name.like(f"%{args['uni']}%"))
    if args['year']:
        query = query.filter(Ranks.year == args['year'])
    query_result = query.offset(offset).limit(args['rpp'])
    results = []
    rank_neglect_fields = ['id', 'uni_id', 'create_date', '_sa_instance_state']
    for rank, university in query_result:
        rank_copied = vars(rank).copy()
        for field in rank_neglect_fields:
            rank_copied.pop(field)
        rank_copied['university'] = university.name
        results.append(rank_copied)
    return jsonify(result=results)
