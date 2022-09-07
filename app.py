from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
import Constants
from Data_Collection import get_channel_Ids, get_playlist_ids, get_video_details, get_comments, download_video

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.secret_key = "faiz"


@app.route("/home")
def home():
    return render_template("index.html", GitHubLink=Constants.GitHubLink)


@app.route("/check", methods=["POST", "GET"])
def check():
    try:
        youtube_url = str(request.form['youtube_url'])
        session['username'] = youtube_url.split('/')[4]
        if len(youtube_url) != 0:
            session['channelId'] = get_channel_Ids.get_channel_Ids(youtube_url)
            if session['channelId'] == 'INVALID':
                return redirect(url_for("home"))
            else:
                return render_template("index.html", GitHubLink=Constants.GitHubLink,
                                       status_comments="channelId found: " + session['channelId'])
        else:
            return redirect(url_for("home"))
    except Exception as e:
        print(e)
        return redirect(url_for("home"))



@app.route("/submit", methods=["POST", "GET"])
def submit():
    if session['channelId'] == 'INVALID':
        return redirect(url_for("home"))
    else:
        session['playlistId'] = get_playlist_ids.get_playlist_ids(session['channelId'])
        if session['playlistId'] == 'INVALID':
            session['channelId'] = 'INVALID'
            return redirect(url_for("home"))
        else:
            session['videoCountRequest'] = int(request.form['videoCountRequest'])
            session['video_data'], channelTitle = get_video_details.get_video_details(session['playlistId'], session['username'],
                                                                               maxResults=session['videoCountRequest'])
            if session['video_data'] is None:
                session['channelId'] = 'INVALID'
                session['playlistId'] = 'INVALID'
                return redirect(url_for("home"))
            else:
                return render_template("index_table.html", tables=[session['video_data'].to_html(escape=False,
                                                                                          formatters=dict(thumbnail = path_to_image_html,
                                                                                                          Comments = convert_comment_link,
                                                                                                          VideoTitle = convert_title_link,
                                                                                                          DownloadLink=create_download_urls
                                                                                                          ),
                                                                                          render_links=True,
                                                                                          bold_rows=True,
                                                                                          justify='center',
                                                                                          index_names=False,
                                                                                          columns=['thumbnail',
                                                                                                   'VideoTitle',
                                                                                                   'publishedAt',
                                                                                                   'viewCount',
                                                                                                   'likeCount',
                                                                                                   'Comments',
                                                                                                   'DownloadLink'
                                                                                                   ]
                                                                                          )
                                                                   ],
                                       titles=[''],
                                       channelTitle=channelTitle)


@app.route("/comments", methods=["POST", "GET"])
def comments():
    videoId = request.args.get('videoId')
    video_data = session['video_data']
    videotitle = video_data[video_data['videoId'] == videoId]['title'].values[0]
    comments_data = get_comments.get_comments(videoId, videotitle)
    return jsonify(comments_data)

@app.route("/download", methods = ["POST", "GET"])
def download():
    videoId = request.args.get('videoId')
    file = download_video.download_video(videoId)
    return file


def path_to_image_html(path):
    return f'''
                <a>
                            <img src = "{path}" alt = "thumbnail"
                             width= "200" height="150" align = "left"/>
                        </a>
                '''


def convert_comment_link(var):
    videoId, commentCount = var.split('#SPLIT#')
    return f'''
            <a target="_blank" href="/comments?videoId={videoId}"> {commentCount} </a>
            '''

def convert_title_link(var):
    title, videoLink = var.split('#SPLIT#')
    return f'''
            <a target="_blank" href="{videoLink}"> {title} </a>
            '''

def create_download_urls(videoId):
    return f'''
            <a target="_blank" href="/download?videoId={videoId}"> Download </a>
            '''

@app.route('/')
def go_to_home():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=False)
