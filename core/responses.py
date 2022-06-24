from rest_framework import response


def error_invalid_schema_of_document_or_data():
    return response.Response(
        status=400,
        data={
            'code': 400,
            'message': 'Validation Failed',
            'description': 'Невалидная схема документа или входные данные не верны.'
        }
    )


def error_item_not_found():
    return response.Response(
        status=404,
        data={
            'code': 404,
            'message': 'Item not found',
            'description': 'Категория/товар не найден.'
        }
    )


def success_delete():
    return response.Response(
        status=200,
        data={
            'code': 200,
            'message': 'Success delete',
            'description': 'Удаление прошло успешно.'
        }
    )


def success_import():
    return response.Response(
        status=200,
        data={
            'code': 200,
            'message': 'Success import',
            'description': 'Вставка или обновление прошли успешно.'
        }
    )
