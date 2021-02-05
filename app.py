import os
from json import dump, load
from flask import Flask, request, redirect


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

    def add_comment(self, comment):
        pass


app = App(__name__)


@app.route('/', methods=['GET'])
def get_root():
    with open('./index.html', 'r') as index_page:
        return index_page.read()


@app.route('/comments/', methods=['GET'])
def get_comments():
    with open('./comments/comments.json', 'r') as comments_file:
        comments = load(comments_file)
    with open('./comments/comment_template.html', 'r') as comment_template:
        template = comment_template.read()
    formatted_comments = [template.format(**comment) for comment in comments]
    joined_comments = '\n'.join(formatted_comments)
    with open('./comments/index.html', 'r') as comments_page:
        comments_content = comments_page.read()
    return comments_content.format(joined_comments)


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


if __name__ == '__main__':
    app.run()
