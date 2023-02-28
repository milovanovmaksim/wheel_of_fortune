from typing import Optional

from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import docs, request_schema, response_schema
from aiohttp_session import new_session, Session

from admin_api.web.app import View
from store.admin.models import Admin
from admin_api.web.utils import json_response
from admin_api.admin.schemes import AdminResponseSchema, AdminLoginRequestSchema
from admin_api.web.mixins import AuthRequiredMixin


class AdminLoginView(View):
    @docs(tags=["admin"], summary="Login")
    @request_schema(AdminLoginRequestSchema)
    @response_schema(AdminResponseSchema, 200)
    async def post(self):
        email = self.data["email"]
        password = self.data["password"]
        admin_accessor = self.store.admin_accessor
        admin: Optional[Admin] = await admin_accessor.get_by_email(email)
        if admin:
            if admin.check_password(password):
                await self.set_new_session()
                return json_response(data={'data': admin}, schema=AdminResponseSchema)
        raise HTTPForbidden(reason="incorrect email or password")

    async def set_new_session(self) -> Session:
        session = await new_session(self.request)
        session["admin"] = self.data["email"]
        return session


class AdminCurrentView(AuthRequiredMixin, View):
    async def get(self):
        admin = self.request.admin
        return json_response(data={'data': admin}, schema=AdminResponseSchema)
