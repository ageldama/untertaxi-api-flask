# -*- coding: utf-8; -*-
"""
Untertaxi API v1
"""
from flask import Blueprint, jsonify, make_response, request
from validate_email import validate_email

from ...auth import auth
from ...db import (Member, MemberAddress, MemberType, RideRequest,
                   RideRequestStatus, db)

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
    member = Member(email, password, member_type)
    db.session.add(member)
    db.session.commit()
    #
    resp = make_response()
    resp.status_code = 201  # CREATED
    return resp


@BP.route('/member/<member_id>', methods=['GET'])
@auth.login_required
def member_get(member_id):
    """회원 정보 `GET /member/<id>`"""
    member = Member.query.get(member_id)
    if member is None:
        raise APIException(u'사용자 없음', 400)
    else:
        return jsonify(member.to_dict())

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


@BP.route('/address/<address_id>', methods=['GET'])
@auth.login_required
def address_get(address_id):
    """주소 정보 `GET /address/<id>`"""
    address = MemberAddress.query.get(address_id)
    if address is None:
        raise APIException(u'주소없음', 400)
    else:
        return jsonify(address.to_dict())


@BP.route('/address/<address_id>', methods=['DELETE'])
@auth.login_required
def address_deactivate(address_id):
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


@BP.route('/ride_request', methods=['POST'])
@auth.login_required
def ride_request_new():
    """배차요청 `POST /ride_request`"""
    member = Member.find_first_by_email(auth.username())
    req_json = request.json
    address_id = req_json['address_id']
    address = MemberAddress.query.get(address_id)
    if address is None:
        raise APIException(u'주소 찾을수없음', 400)
    #
    ride_req = RideRequest(member, address)
    db.session.add(ride_req)
    db.commit()
    #
    return jsonify({'id': ride_req.id})


@BP.route('/ride_request', methods=['GET'])
@auth.login_required
def ride_request_list():
    """배차요청 목록 `GET /ride_request`"""
    return jsonify(rq.to_dict() for rq in RideRequest.find_all())


@BP.route('/ride_request/<ride_request_id>', methods=['DELETE'])
@auth.login_required
def ride_request_deactivate(ride_request_id):
    """배차요청 취소 `DELETE /ride_request/:id`"""
    #
    ride_request = RideRequest.query.get(ride_request_id)
    if ride_request is None:
        raise APIException(u'배차요청없음', 400)
    # 요청자 자신의 ride_request?
    email = auth.username()
    passenger = Member.query.get(ride_request.passenger_id)
    if passenger is None or passenger.email != email:
        raise APIException(u'배차요청자의 배차요청 아님', 401)
    #
    RideRequest.deactivate(ride_request.id)
    #
    resp = make_response()
    resp.status_code = 204  # NO CONTENT
    return resp


@BP.route('/ride_request/<ride_request_id>/accept', methods=['POST'])
@auth.login_required
def ride_request_accept(ride_request_id):
    """배차 `POST /ride_request/:id/accept`"""
    # 내가 driver?
    driver = Member.find_first_by_email(auth.username())
    if driver is None or driver.member_type != MemberType.DRIVER:
        raise APIException(u'기사인 회원만 배차요청 승인가능', 401)
    #
    ride_request = RideRequest.query.get(ride_request_id)
    if ride_request is None:
        raise APIException(u'배차요청없음', 400)
    # 내가 만든 배차요청인가?
    if ride_request.passenger_id == driver.id:
        raise APIException(u'기사 본인이 만든 배차요청은 본인이 배차 받을수없음.', 401)
    #
    ride_request.driver_id = driver.id
    ride_request.status = RideRequestStatus.ACCEPTED
    db.session.add(ride_request)
    db.session.commit()
    #
    resp = make_response()
    resp.status_code = 204  # NO CONTENT
    return resp


@BP.route('/ride_request/<ride_request_id>/arrive', methods=['POST'])
@auth.login_required
def ride_request_arrive(ride_request_id):
    """도착통지 `POST /ride_request/:id/arrive`"""
    # 내가 driver?
    driver = Member.find_first_by_email(auth.username())
    if driver is None or driver.member_type != MemberType.DRIVER:
        raise APIException(u'기사인 회원만 배차요청 도착확인 가능.', 401)
    #
    ride_request = RideRequest.query.get(ride_request_id)
    if ride_request is None:
        raise APIException(u'배차요청없음.', 400)
    #
    if ride_request.driver_id != driver.id:
        raise APIException(u'내가 승인한 배차요청이 아님.', 401)
    #
    ride_request.status = RideRequestStatus.ARRIVED
    db.session.add(ride_request)
    db.session.commit()
    #
    resp = make_response()
    resp.status_code = 204  # NO CONTENT
    return resp


# EOF.
