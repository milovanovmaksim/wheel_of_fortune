import typing

from aiohttp.web_exceptions import HTTPUnauthorized, HTTPForbidden
from aiohttp_session import Session, get_session

if typing.TYPE_CHECKING:
    from aiohttp.abc import StreamResponse
    from app.store.admin.accessor import AdminAccessor


class AuthRequiredMixin:
    async def _iter(self) -> "StreamResponse":
        session: Session = await get_session(self.request)
        email = session.get("admin")
        if self.request.cookies.get("sessionid") and email is None:
            raise HTTPForbidden
        admin_accessor: "AdminAccessor" = self.request.app.store.admins
        admin = await admin_accessor.get_by_email(email)
        if admin:
            self.request.admin = admin
            return await super(AuthRequiredMixin, self)._iter()
        raise HTTPUnauthorized
