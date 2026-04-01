from house import models

def profile_image(request):

    email = request.session.get('semail')

    if email:
        try:
            user = models.Register.objects.get(email=email)
            return {'profile_image': user.profile_image}
        except:
            return {'profile_image': None}

    return {'profile_image': None}
