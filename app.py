from flask import Flask, render_template, request, session, redirect, url_for
import os
import random

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-spy-key")

# Mapping results to local image paths (relative to 'static' folder)
IMAGE_MAP = {
    "spy": ["images/spy/spy1.png", "images/spy/spy2.png", "images/spy/spy3.png"],
    "vc": ["images/vc/vc1.png"],
    "irs": ["images/irs/IRS1.png"],
    "default": ["images/default/default1.png"]
}

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
    session['history'] = []
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    node = session.get('current_node')
    history = session.get('history', [])
    
    if not node or node.get('type') != 'question':
        return redirect(url_for('index'))

    if request.method == 'POST':
        choice_index = int(request.form.get('choice'))
        selected_option = node['options'][choice_index]
        
        # Add decision to history
        history.append(selected_option['text'])
        session['history'] = history
        
        next_node = selected_option['next']
        session['current_node'] = next_node
        
        if next_node.get('type') == 'result':
            return redirect(url_for('result'))
        return redirect(url_for('question'))

    return render_template('question.html', node=node, history=history)

@app.route('/result')
def result():
    node = session.get('current_node')
    history = session.get('history', [])
    
    if not node or node.get('type') != 'result':
        return redirect(url_for('index'))
    
    result_text = node['text'].lower()
    
    # Robust keyword-based lookup
    if "spy" in result_text:
        image_list = IMAGE_MAP["spy"]
    elif "vc" in result_text:
        image_list = IMAGE_MAP["vc"]
    elif "irs" in result_text:
        image_list = IMAGE_MAP["irs"]
    else:
        image_list = IMAGE_MAP["default"]
    
    random_path = random.choice(image_list)
    image_url = url_for('static', filename=random_path)
    
    return render_template('result.html', result=node['text'], image_url=image_url, history=history)

if __name__ == '__main__':
    app.run(debug=True)
