

# Dynamic path for FileField


def upload_path_menu(instance, filename):
    file = filename.rfind(".")
    formatt = filename[file:]
    name = instance.name + formatt
    return "{0}/category/{1}/{2}".format(
        instance.restaurant.name, instance.category.name, name
    )


def upload_path_rest(instance, file):
    return "{0}/backgroud/{1}".format(instance.name, file)


def upload_logo_rest(instance, file):
    return "{0}/logo/{1}".format(instance.name, file)