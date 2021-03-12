import os
from json import dump, load
from flask import Flask, request, redirect, render_template


class App(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def check_for_file(path, l=False):
            if not os.path.isfile(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as wfile:
                    wfile.write(('[]' if l else'{}'))
                return False
            return True

        check_for_file('./comments/comments.json', l=True)


app = App(__name__)


@app.route('/', methods=['GET'])
def get_root():
    return render_template('main.html')


@app.route('/comments/', methods=['GET'])
def get_comments():
    with open('./comments/comments.json', 'r') as comments_file:
        comments = load(comments_file)
    with open('./templates/comment_template.html', 'r') as comment_template:
        template = comment_template.read()
    formatted_comments = [template.format(**comment) for comment in comments]
    joined_comments = '\n'.join(formatted_comments)
    return render_template('comments.html', comments=joined_comments)


@app.route('/comments/post/', methods=['POST'])
def post_comment():
    data = dict(request.form)
    if 'name' not in data or 'comment' not in data:
        return 'Missing Parameter'

    with open('./comments/comments.json', 'r') as comments_file:
        comments = load(comments_file)
    comments.append(data)
    with open('./comments/comments.json', 'w') as comments_file:
        dump(comments, comments_file)

    return redirect('/comments/', code=302)


@app.route('/comments/reset/', methods=['POST'])
def post_reset():
    with open('./comments/comments.json', 'w') as comments_file:
        comments_file.write('[]')
    return redirect('/comments/', code=302)


@app.route('/search/', methods=['GET'])
def get_search():
    search = request.args.get('search')
    if search:
        return render_template('search.html', search=search)
    return render_template('search.html', search='')


@app.route('/login', methods=['POST'])
def post_login():
    data = dict(request.form)
    pass


if __name__ == '__main__':
    app.run()
