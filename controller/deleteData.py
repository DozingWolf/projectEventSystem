from crypt import methods
from flask import Blueprint,current_app,request,session
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from time import strftime,localtime
from traceback import print_exc
from model import db
from tool.responseGenerator import responseStructures
from tool.sqlGenerator import updateSqlGenerator
from controller.dataTraceRecorder import queryTracerLog
from controller.errorlist import PostNoParaError,PostParaEmptyError,AuthNoPermissionError,SqlBuilderError
from auth.authManager import isLoginCheck,isPermissionCheck

deleteDataBP = Blueprint('deleteData',__name__)
