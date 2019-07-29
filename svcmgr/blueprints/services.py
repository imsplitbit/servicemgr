from flask import Blueprint, request, jsonify

from svcmgr.models import Service


services = Blueprint('services', __name__, url_prefix='/api/v0')


def fetch_service(svcname):
    return Service.query.filter_by(name=svcname).first()


@services.route('/services/<string:svcname>', methods=('POST',))
def service_create(svcname):
    service = Service(name=svcname)
    service.save()
    response = jsonify(
        {
            'id': service.id,
            'name': service.name,
            'created': service.date_created,
            'modified': service.date_modified
        }
    )
    response.status_code = 201
    return response

@services.route('/services/<string:svcname>', methods=('GET',))
def service_list(svcname):
    service = fetch_service(svcname)
    if not service:
        response = jsonify({
            'error': 'Service {} not found'.format(svcname)
        })
        response.status_code = 404
        return response
    else:
        response = jsonify(
            {
                'id': service.id,
                'name': service.name,
                'created': service.date_created,
                'modified': service.date_modified
            }
        )
        response.status_code = 200
        return response


@services.route('/services/<string:svcname>', methods=('DELETE',))
def service_delete(svcname):
    pass
