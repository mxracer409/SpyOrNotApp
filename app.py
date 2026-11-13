from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-spy-key")

# Decision Tree Structure
TREE = {
    "id": "root",
    "type": "question",
    "text": "What do you do?",
    "options": [
        {
            "text": "AI",
            "next": {
                "type": "question",
                "text": "Is she a 10?",
                "options": [
                    {"text": "Yes", "next": {"type": "result", "text": "SPY"}},
                    {
                        "text": "No",
                        "next": {
                            "type": "question",
                            "text": "Is your company worth over $100M?",
                            "options": [
                                {
                                    "text": "Yes",
                                    "next": {
                                        "type": "question",
                                        "text": "Is she a good listener?",
                                        "options": [
                                            {
                                                "text": "Yes",
                                                "next": {
                                                    "type": "question",
                                                    "text": "Does she say your GPU is the biggest she's ever seen?",
                                                    "options": [
                                                        {"text": "Yes", "next": {"type": "result", "text": "SPY"}},
                                                        {"text": "No", "next": {"type": "result", "text": "Could still be a spy (keep watching)"}}
                                                    ]
                                                }
                                            },
                                            {"text": "No", "next": {"type": "result", "text": "VC associate (worse)"}}
                                        ]
                                    }
                                },
                                {"text": "No", "next": {"type": "result", "text": "You can relax (for now)"}}
                            ]
                        }
                    }
                ]
            }
        },
        {
            "text": "Not AI",
            "next": {
                "type": "question",
                "text": "Are you in the government?",
                "options": [
                    {
                        "text": "Yes",
                        "next": {
                            "type": "question",
                            "text": "Does she avoid talking about Taiwan?",
                            "options": [
                                {"text": "Yes", "next": {"type": "result", "text": "SPY"}},
                                {"text": "No", "next": {"type": "result", "text": "[REDACTED]"}}
                            ]
                        }
                    },
                    {
                        "text": "No",
                        "next": {
                            "type": "question",
                            "text": "Are you in Crypto?",
                            "options": [
                                {
                                    "text": "Yes",
                                    "next": {
                                        "type": "question",
                                        "text": "Can she say 'Kim Jong Un is a big pig'?",
                                        "options": [
                                            {"text": "No", "next": {"type": "result", "text": "SPY (North Korean)"}},
                                            {
                                                "text": "Yes",
                                                "next": {
                                                    "type": "question",
                                                    "text": "Did you make more than $100k from crypto?",
                                                    "options": [
                                                        {"text": "Yes", "next": {"type": "result", "text": "IRS agent"}},
                                                        {"text": "No", "next": {"type": "result", "text": "Probably not a spy"}}
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                },
                                {"text": "No", "next": {"type": "result", "text": "Probably a normal gf (rare)"}}
                            ]
                        }
                    }
                ]
            }
        }
    ]
}

@app.route('/')
def index():
    session.clear()
    session['current_node'] = TREE
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    node = session.get('current_node')
    if not node or node.get('type') != 'question':
        return redirect(url_for('index'))

    if request.method == 'POST':
        choice_index = int(request.form.get('choice'))
        next_node = node['options'][choice_index]['next']
        session['current_node'] = next_node
        
        if next_node.get('type') == 'result':
            return redirect(url_for('result'))
        return redirect(url_for('question'))

    return render_template('question.html', node=node)

@app.route('/result')
def result():
    node = session.get('current_node')
    if not node or node.get('type') != 'result':
        return redirect(url_for('index'))
    return render_template('result.html', result=node['text'])

if __name__ == '__main__':
    app.run(debug=True)
