from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)
CONFIG_FILE = "config.json"

# 读取配置文件


def read_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# 写入配置文件


def write_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 首页：显示配置列表


@app.route("/")
def index():
    configs = read_config()
    return render_template("index.html", configs=configs)

# 新增配置页面


@app.route("/add", methods=["GET", "POST"])
def add_config():
    print(request.form)
    if request.method == "POST":
        name = request.form.get("name")
        urls = request.form.getlist("url")
        for index in range(len(urls)):
            url = urls[index]
            if "kiosk" not in url and "panelId" not in url:
                urls[index] += "&kiosk"
        if name and urls:
            configs = read_config()
            configs.append({"name": name, "urls": urls})
            write_config(configs)
            return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/delete/<int:config_id>", methods=["GET", "POST"])
def delete_config(config_id):
    configs = read_config()
    del configs[config_id]
    write_config(configs)
    return redirect(url_for("index"))

# 渲染页面


@app.route("/view/<int:config_id>")
def view_config(config_id):
    configs = read_config()
    if config_id < len(configs):
        config = configs[config_id]
        return render_template("render.html", config=config)
    return "Config not found", 404


if __name__ == "__main__":
    app.run(debug=True)
