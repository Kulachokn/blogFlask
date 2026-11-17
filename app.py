from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)


@app.route('/')
def index():
    with open('data.json', 'r', encoding='utf-8') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        new_author = request.form['author']
        new_title = request.form['title']
        new_content = request.form['content']

        with open('data.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)

        new_entry = {
            "id": str(uuid.uuid4()),
            "author": new_author,
            "title": new_title,
            "content": new_content
        }

        posts.append(new_entry)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<string:id>', methods=['POST'])
def delete_post(id):
    with open('data.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)

        # for post in posts:
        #     if post['id'] == id:
        #         posts.remove(post)
        #         break

    updated_posts = [post for post in posts if post['id'] != id]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(updated_posts, f, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update_post(id):
    with open('data.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    post = next((p for p in posts if str(p['id']) == id), None)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=4)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)

@app.route('/like/<string:id>', methods=['POST'])
def like_post(id):
    with open('data.json', 'r', encoding='utf-8') as f:
        posts = json.load(f)
    post = next((p for p in posts if str(p['id']) == id), None)
    if post is None:
        return "Post not found", 404

    post['likes'] = post.get('likes', 0) + 1

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
