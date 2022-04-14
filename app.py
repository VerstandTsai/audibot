from flask import Flask, send_file

app = Flask(__name__)

@app.route('/downloads/<string:file_id>')
def download(file_id):
    return send_file(f'./downloads/{file_id}.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')