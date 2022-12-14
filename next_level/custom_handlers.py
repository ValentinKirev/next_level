import logging

from django.shortcuts import render


def bad_request(request, exception):

    context = {'user': request.user}

    response = render(request, "errors/bad-request.html", context=context)
    response.status_code = 400

    logging.error(f'Error occurred with status code {response.status_code}')
    logging.critical(f'Critical error occurred with status code {response.status_code}')

    return response


def permission_denied(request, exception):

    context = {'user': request.user}

    response = render(request, "errors/permission_denied.html", context=context)
    response.status_code = 403

    logging.error(f'Error occurred with status code {response.status_code}')
    logging.critical(f'Critical error occurred with status code {response.status_code}')

    return response


def page_not_found(request, exception):

    context = {'user': request.user}

    response = render(request, "errors/page-not-found.html", context=context)
    response.status_code = 404

    logging.error(f'Error occurred with status code {response.status_code}')
    logging.critical(f'Critical error occurred with status code {response.status_code}')

    return response


def internal_server_error(request):

    response = render(request, "errors/internal_server_error.html")
    response.status_code = 500

    logging.error(f'Error occurred with status code {response.status_code}')
    logging.critical(f'Critical error occurred with status code {response.status_code}')

    return response
