from app import app, db
from app.models import University, Rank


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'University': University, 'Rank': Rank}

# app.run(debug=True)
