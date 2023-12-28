from django.shortcuts import redirect


def table_manager(request, table_id):
    request.session['table_id'] = table_id
    return redirect('index')