from django.http import JsonResponse
from django.shortcuts import redirect

from app.utils.poster import poster


def product_view(request, product_id):
    # product = poster.get_product(product_id)
    # print(product)
    # similar_products = poster.get_products(category_id=int(product['menu_category_id']))
    # return render(request, 'app/product.html',
    #               {'product': product, 'similar_products': similar_products[:5]})
    return redirect('index')


def product_info_json(request, product_id):
    product = poster.get_product(product_id)
    # print(product)
    if "modifications" in product:
        modifications = product['modifications']
        return JsonResponse({"type": "ProductModifications", "modifications": modifications})
    elif "group_modifications" in product:
        if len(product['group_modifications']) == 1:
            if product['group_modifications'][0]['type'] == 1:
                modifications = product['group_modifications'][0]['modifications']
                return JsonResponse({"type": "DishModifications", "modifications": modifications})
            else:
                if product["group_modifications"][0]["num_max"] == product["group_modifications"][0]["num_min"]:
                    modifications = product['group_modifications'][0]['modifications']
                    return JsonResponse({"type": "Combo", "modifications": modifications})
                else:
                    modifications = product['group_modifications'][0]['modifications']
                    return JsonResponse({"type": "DishModifications", "modifications": modifications})
        else:
            modifications = product['group_modifications']
            return JsonResponse({"type": "Combo_Set", "modifications": modifications})
