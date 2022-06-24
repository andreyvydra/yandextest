from restapi.models import OfferAndCategory


def get_average_price(obj):
    result = {
        'summary': 0,
        'counter': 0
    }
    sum_all_prices_with_count_children(obj, result)
    if result['counter'] == 0:
        return None
    return result['summary'] // result['counter']


def sum_all_prices_with_count_children(obj, result):
    many_children = obj.children.all()
    if many_children:
        for children in many_children:
            if children.children:
                sum_all_prices_with_count_children(children, result)

            if children.price:
                result['summary'] += children.price
                result['counter'] += 1


def change_parents_date(parent_id, update_date):
    parent = OfferAndCategory.objects.filter(uuid=parent_id)[0]
    if parent.date.replace(tzinfo=None) < update_date.replace(tzinfo=None):
        parent.date = update_date
        parent.save()
    if parent.parent_id:
        change_parents_date(parent.parent_id, update_date)
