from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user



app = Flask(__name__)