from django.urls import resolve



def Here2HelpMCMiddleware(get_response):

    def middleware(request):
        response = get_response(request)

        print('namespace:name (to add to STRONGHOLD_PUBLIC_NAMED_URLS) ', resolve(request.path_info).view_name)

        return response

    return middleware


