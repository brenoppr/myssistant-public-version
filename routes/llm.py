from flask import Blueprint
from utils.llm_chat import reset_llm_chat

llm_bp = Blueprint('llm', __name__)

@llm_bp.route('/reset_chat', methods=['GET'])
def reset_chat():
    reset_llm_chat()
    return "OK", 200
    