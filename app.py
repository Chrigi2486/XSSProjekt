import os
import random
from json import dump, load
from flask import Flask, request, redirect, render_template


class App(Flask):  # Backend for the interactive part of our website
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def check_for_file(path, l=False):  # Checks for critical files and creates them if they're non existent
            if not os.path.isfile(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as wfile:
                    wfile.write(('[]' if l else'{}'))
                return False
            return True

        check_for_file('./comments/comments.json', l=True)

        self.neon_colors = ['blue', 'green', 'purple', 'pink', 'yellow', 'red']


app = App(__name__)


@app.route('/', methods=['GET'])
def get_root():
    return render_template('main.html')  # returns main.html at the root URL


@app.route('/comments/', methods=['GET'])
def get_comments():
    with open('./comments/comments.json', 'r') as comments_file:
        comments = load(comments_file)
    with open('./templates/comment_template.html', 'r') as comment_template:
        template = comment_template.read()
    formatted_comments = [template.format(color=random.choice(app.neon_colors), position=('right' if index % 2 else 'left'), **comment) for index, comment in enumerate(comments)]
    joined_comments = '\n'.join(formatted_comments)
    return render_template('comments.html', comments=joined_comments)  # returns comments.html formatted with the comments at root/comments/


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

    return redirect('/comments/', code=302)  # Creates a new comment and redirects to root/comments/


@app.route('/comments/reset/', methods=['POST'])
def post_reset():
    with open('./comments/comments.json', 'w') as comments_file:
        comments_file.write('[]')
    return redirect('/comments/', code=302)  # removes all the comments and redirects to root/comments/


@app.route('/search/', methods=['GET'])
def get_search():
    search = request.args.get('search')
    if search:
        return render_template('search.html', search=search)  # returns search.html formatted with the search word at root/search/
    return render_template('search.html', search='')


if __name__ == '__main__':
    app.run()
