from api_crud.models import Like, Post, Basket, Order, Category
from methodism import custom_response, error_messages, MESSAGE


def add_to_basket(request, params):

    if not params.get('product_id'):
        return custom_response(False, message=error_messages.error_params_unfilled('product_id'))

    product = Post.objects.filter(id=params.get('product_id')).first()
    if not product:
        return custom_response(False, message=MESSAGE['NotData'])

    basket, created = Basket.objects.get_or_create(post=product,  user=request.user)

    if created:
        basket.quantity = params.get('quantity', 1)
    else:
        basket.quantity += params.get('quantity', 1)

    basket.save()

    return custom_response(True, message=f'{product.title} qoshildi')


def delete_from_basket(request, params):

    if not params.get('product_id') :
        return custom_response(False, message=error_messages.error_params_unfilled('product_id'))

    basket = Basket.objects.filter(post__id=params['product_id']).first()

    if not basket:
        return custom_response(False, message=MESSAGE['NotData'])

    if not params.get('quantity'):
        basket.delete()

    if params.get('quantity') >= basket.quantity:
        return custom_response(False, message={'Mavjud miqdordan katta raqam kiritildi '})
    else:
        basket.quantity -= params.get('quantity')
        basket.save()

    return custom_response(True, message="Deleted")


def order(request, params):
    baskets = Basket.objects.filter(user=request.user, status=True)

    if not baskets:
        return custom_response(False, message='Baskets mavjud emas')

    order = Order.objects.create(user=request.user)
    order.basket.set(baskets)

    total = 0
    for basket in baskets:
        total += basket.post.price * basket.quantity

    order.price = total
    order.save()

    baskets.delete()


