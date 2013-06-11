from flask import Flask, render_template, session, redirect, url_for, abort, request, flash, send_from_directory

import crawl, os, re, urllib

app = Flask(__name__)


@app.route("/", methods=['GET'])
def route_base():

	return render_template("template_home.html")


@app.route("/generate", methods=['POST'])
def route_generate():

	crawl.crawl()

	return redirect(url_for("route_download"))


@app.route("/download", methods=['GET'])
def route_download():

	files = []

	for dirname, dirnames, filenames in os.walk('/reports'):
	    # all filenames.
	    for filename in filenames:
	       	tmp = (filename, urllib.quote_plus(filename))
	       	files.append(tmp)

	files = sorted(files, reverse=True)

	return render_template("template_download.html", files=files)


@app.route("/download/<filename>", methods=['GET'])
def route_download_file(filename):
	return send_from_directory("/reports", filename)


if __name__ == "__main__":
	#presets()

	app.debug = True
	app.run()
