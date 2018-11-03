"""Locale cache module. author: Joseph Vithayathil"""
from django.db import models
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class CacheExceptionClass(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, error):
        """Initialization."""
        super(CacheExceptionClass, self).__init__(
            "ERROR: CacheExceptionClass: " + error)
        self.error = error


class CachedModelManager(models.Manager):
    """Model manager of static models wich can be cached."""

    def cache_filter(self, model_objs=None, **kwargs):
        """To filter a list of model objects."""
        model_name = self.model
        if model_objs is None:
            model_objs = get_model_from_cache(model_name)
        model_filter_objs = []
        if list(model_objs) == []:  # When the query object list is empty.
            return model_filter_objs

        """For formating the query input."""
        for key in list(kwargs):
            if key not in model_objs[0].__dict__.keys():
                field_not_in_model = True
                if "__" in key:
                    foreing_key = key.split("__")[0]
                    if model_name._meta.get_field(foreing_key).get_internal_type() == "ForeignKey":
                        foreingkey_model = model_name._meta.get_field(foreing_key).rel.to
                        f_kwargs = {key[len(foreing_key) + 2:]: kwargs[key]}
                        try:
                            f_objects = foreingkey_model.objects.cache_filter(**f_kwargs)
                            f_objects_value = []
                            for f_object in f_objects:
                                f_objects_value.append(f_object.id)
                            kwargs[foreing_key + '_id'] = f_objects_value
                            del kwargs[key]
                        except CacheExceptionClass as exception:
                            raise exception
                        field_not_in_model = False
                elif model_name._meta.get_field(key).get_internal_type() == "ForeignKey":
                    """Query condition that is passed is foreignkey."""
                    try:
                        kwargs[key + '_id'] = kwargs[key].id
                    except:
                        raise CacheExceptionClass("Expected a object.")
                    del kwargs[key]
                    field_not_in_model = False
                if field_not_in_model:
                    """Inputed a worng field in query condition."""
                    raise CacheExceptionClass(
                        "Field \"" + key + "\"not in the Model.")

        """Filtering the query objects based on the condition passed as parameters."""
        for model_obj in model_objs:
            """Iterating throug each query object from the list of query objects."""
            flag = True
            for key in kwargs:
                if isinstance(kwargs[key], (list, tuple)):
                    list_item_flag = False
                    for val in kwargs[key]:
                        if check_equality(model_obj.serializable_value(key), val):
                            list_item_flag = True
                    if not list_item_flag:
                        flag = False
                        break
                elif not check_equality(model_obj.serializable_value(key), kwargs[key]):
                    """Current query object 'model_obj' doesn't satisfy the condition."""
                    flag = False
                    break
            if flag is True:
                """Current query object 'model_obj' satisfies the condition."""
                model_filter_objs.append(model_obj)
        return model_filter_objs


    def cache_get(self, pk=None, **kwargs):
        """To get a single model object."""
        model_name = self.model
        model_objs = get_model_from_cache(model_name)
        model_get_obj = None
        model_obj_list = []
        # If the query condition is based on id(or pk) it will be a direct query.
        if pk is not None:
            for model_obj in model_objs:
                if pk == model_obj.pk:
                    model_obj_list = [model_obj]
                    break
        else:
            model_obj_list = self.cache_filter(
                model_objs, **kwargs)

        model_obj_list_len = len(model_obj_list)
        if model_obj_list_len == 1:
            model_get_obj = model_obj_list[0]
        elif model_obj_list_len == 0:
            raise ObjectDoesNotExist
        else:
            raise MultipleObjectsReturned
        return model_get_obj


def check_equality(value1, value2):
    """Function to check equality."""
    try:
        if str(value1) == str(value2):
            return True
        else:
            return False
    except Exception:
        if value1 == value2:
            return True
        else:
            return False


def get_model_from_cache(model_name):
    """Get the object from cache or query it from db if not in cache."""
    table_name = model_name._meta.object_name
    model_objs = cache.get(table_name)  # Get the query object from the cache.
    if not model_objs:  # If the corresponding query object is not present in the cache or not.
        # Query the objects from the correspondin model.
        foreignkey_fields = []
        for field in model_name._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                foreignkey_fields.append(field.name)
        model_objs = model_name.objects.select_related(
            *foreignkey_fields).filter(is_deleted=False)
        # Set the query objects in cache with the name as model name.
        cache.set(table_name, model_objs)
    return model_objs


class CustomCacheModelClass(models.Model):
    """Custom cache model class."""

    objects = CachedModelManager()

    def save(self, *args, **kwargs):
        """Custom save fuction to override default save fuction to clear data in cache."""
        table_name = self._meta.object_name
        cache.delete(table_name)
        super(CustomCacheModelClass, self).save(*args, **kwargs)

    class Meta:
        """Meta class."""
        abstract = True  # To tell django that this is not a acutal model.
