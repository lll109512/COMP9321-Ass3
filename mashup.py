from app import app, db
from app.models import Universities, Ranks


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'University': Universities, 'Rank': Ranks}


if __name__ == '__main__':
    app.run(debug=True,processes=3)
