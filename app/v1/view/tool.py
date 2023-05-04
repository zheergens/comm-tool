from app.v1.view import template
from flask import  render_template, request
import hashlib



def get_md5(s: str):
    return hashlib.md5(s.encode()).hexdigest().upper()


@template.route('/tool', methods=['GET', 'POST'])
def tool():
    title = "工具页"
    view_obj = {
        "md5_list": [],
        "s": ""
    }
    s = request.form.get("md5_list", "")
    if len(s) > 0:
        s_list = s.split(",")
        view_obj["md5_list"] = [(k, get_md5(k)) for k in s_list]
        view_obj["s"] = s

    return render_template("v1_tool.html", title=title, view_obj=view_obj)
