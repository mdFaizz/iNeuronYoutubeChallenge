from flask import Flask, render_template, request, flash, redirect, url_for
import Constants
from Data_Collection import get_channel_Ids, get_playlist_ids, get_video_details

app = Flask(__name__)
app.secret_key = "faiz"

app.channelId = 'INVALID'
app.playlistId = 'INVALID'
app.video_data = 'INVALID'
app.username = None

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
            app.video_data = get_video_details.get_video_details(app.playlistId, app.username)
            if app.video_data is None:
                app.channelId = 'INVALID'
                app.playlistId = 'INVALID'
                return redirect(url_for("home"))
            else:
                return render_template("index_table.html", tables=[app.video_data.to_html()], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)
