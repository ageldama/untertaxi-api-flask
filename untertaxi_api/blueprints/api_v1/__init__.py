# -*- coding: utf-8; -*-
"""
Untertaxi API v1
"""
from flask import Blueprint, jsonify, make_response, request
from validate_email import validate_email

from ...auth import auth
from ...db import Member, MemberAddress, MemberType, db

BP = Blueprint('api-v1', __name__,
               url_prefix='/v1',
               template_folder='templates')

# ---- API Exception ----


class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@BP.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


# ---- 회원가입 ----


@BP.route('/member', methods=['PUT'])
def member_signup():
    req_json = request.json
    email = req_json['email']
    password = req_json['password']
    member_type = None
    # validations
    if not validate_email(email, check_mx=False, verify=False):
        raise APIException(u'잘못된 이메일 형식', 400)
    if Member.count_by_email(email) > 0:
        raise APIException(u'이미 가입된 이메일', 400)
    if len(password) < 4:
        raise APIException(u'비밀번호가 4글자 이하', 400)
    try:
        member_type = MemberType(request.form['member_type'])
    except ValueError as exc:
        raise APIException(u'잘못된 회원타입', 400)
    #
    m = Member(email, password, member_type)
    db.session.add(m)
    db.session.commit()
    #
    resp = make_response()
    resp.status_code = 201  # CREATED
    return resp

# ---- 배차 요청 ----


@BP.route('/address', methods=['GET'])
@auth.login_required
def address_list():
    """주소 목록 `GET /address`"""
    return MemberAddress.find_all_by_email(auth.username())


@BP.route('/address', methods=['PUT'])
@auth.login_required
def address_new():
    """주소 등록 `PUT /address`"""
    member = Member.find_first_by_email(auth.username())
    req_json = request.json
    address = req_json['address']
    # validation
    if member is None:
        raise APIException(u'사용자를 찾을수없음', 401)
    if address is None or len(address) < 1:
        raise APIException(u'주소가 입력안됨.', 400)
    if len(address) > 100:
        raise APIException(u'주소가 100자 이상임.', 400)
    #
    address = MemberAddress(member, address)
    db.session.add(address)
    db.session.commit()
    # response
    return jsonify({'id': address.id})
    
@BP.route('/address/<address_id>', methods=['DELETE'])
@auth.login_required
def address_delete(address_id):
    """주소 삭제 `DELETE /address/:id`"""
    member = Member.find_first_by_email(auth.username())
    address = MemberAddress.query.get(address_id)
    if address is None:
        raise APIException(u'주소 없음', 400)
    if address.member_id != member.id:
        raise APIException(u'사용자 권한없음', 401)
    #
    MemberAddress.deactivate(address.id)
    #
    resp = make_response()
    resp.status_code = 204  # NO CONTENT
    return resp

# TODO: 배차요청 `POST /ride_request`

# TODO: 배차요청 목록 `GET /ride_request`

# TODO: 배차요청 취소 `DELETE /ride_request/:id`

# TODO: 배차 `POST /ride_request/:id/accept`

# TODO: 도착통지 `POST /ride_request/:id/arrived`

# EOF.
