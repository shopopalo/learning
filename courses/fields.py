from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
	# переопределение конструктора класса-родителя
	def __init__(self, for_fields=None, *args, **kwargs):
		self.for_fields = for_fields
		# явно вызываем конструктор родителя
		# вызвать можно и так super().__init__(*args, **kwargs)
		super(OrderField, self).__init__(*args, **kwargs)

	def pre_save(self, model_instance, add):
		# проверка наличия значения атрибута attname в экземпляре модели
		if getattr(model_instance, self.attname) is None:
			try:
				queryset = self.model.objects.all()
				# если явно указано поля для которых .......
				# order будет расчитано относительно указанных полей
				if self.for_fields:
					query = {field: getattr(model_instance, field) for field in self.for_fields}
					queryset = queryset.filter(**query)
				# ищем объект с самым большим значением order(self.attname)
				# если объект не будет найден, будет вызвано исключение ObjectDoesNotExist
				# это значит что объект находится первым в списке
				last_item = queryset.latest(self.attname)
				# если объект найден, то увеличиваем значение
				value = last_item.order + 1
			except ObjectDoesNotExist:
				value = 0
			# для изменения знчаения нужно обязательно обновить атрибут модели
			setattr(model_instance, self.attname, value)
			# также обязательно нужно вернуть новое значение атрибута модели
			return value
		else:
			# если значение для этого атрибута уже указано, то нужно вызвать метод родителя
			return super(OrderField, self).pre_save(model_instance, add)

