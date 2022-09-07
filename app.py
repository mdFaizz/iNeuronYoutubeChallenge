from flask import Flask, render_template, request, redirect, url_for, jsonify
import Constants
from Data_Collection import get_channel_Ids, get_playlist_ids, get_video_details, get_comments

app = Flask(__name__)
app.secret_key = "faiz"

app.channelId = 'INVALID'
app.playlistId = 'INVALID'
app.video_data = 'INVALID'
app.username = None
app.videoCountRequest = 5


@app.route("/home")
def home():
    return render_template("index.html", GitHubLink=Constants.GitHubLink)


@app.route("/check", methods=["POST", "GET"])
def check():
    try:
        youtube_url = str(request.form['youtube_url'])
        app.username = youtube_url.split('/')[4]
        if len(youtube_url) != 0:
            app.channelId = get_channel_Ids.get_channel_Ids(youtube_url)
            if app.channelId == 'INVALID':
                return redirect(url_for("home"))
            else:
                return render_template("index.html", GitHubLink=Constants.GitHubLink,
                                       status_comments="channelId found: " + app.channelId)
        else:
            return redirect(url_for("home"))
    except Exception as e:
        print(e)
        return redirect(url_for("home"))


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if app.channelId == 'INVALID':
        return redirect(url_for("home"))
    else:
        app.playlistId = get_playlist_ids.get_playlist_ids(app.channelId)
        if app.playlistId == 'INVALID':
            app.channelId = 'INVALID'
            return redirect(url_for("home"))
        else:
            app.videoCountRequest = int(request.form['videoCountRequest'])
            app.video_data, channelTitle = get_video_details.get_video_details(app.playlistId, app.username,
                                                                               maxResults=app.videoCountRequest)
            if app.video_data is None:
                app.channelId = 'INVALID'
                app.playlistId = 'INVALID'
                return redirect(url_for("home"))
            else:
                return render_template("index_table.html", tables=[app.video_data.to_html(escape=False,
                                                                                          formatters=dict(thumbnail = path_to_image_html,
                                                                                                          Comments = convert_comment_link,
                                                                                                          VideoTitle = convert_title_link
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
                                                                                                   'Comments'
                                                                                                   ]
                                                                                          )
                                                                   ],
                                       titles=[''],
                                       channelTitle=channelTitle)


@app.route("/comments", methods=["POST", "GET"])
def comments():
    videoId = request.args.get('videoId')
    videotitle = app.video_data[app.video_data['videoId'] == videoId]['title'].values[0]
    comments_data = get_comments.get_comments(videoId, videotitle)
    return jsonify(comments_data)


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


@app.route('/')
def go_to_home():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run()
