from rest_framework import permissions

from diploma.apps.works.models import Work


class IsMasterPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		return bool(request.user.is_master)

