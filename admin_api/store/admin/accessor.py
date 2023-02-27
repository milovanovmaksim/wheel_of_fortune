import typing
from typing import Optional
from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.sql.expression import Select

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin, AdminModel
from app.web.config import AdminConfig


if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):

    async def connect(self, app: "Application"):
        admin_config: AdminConfig = self.app.config.admin
        admin: Optional[Admin] = await self.get_by_email(admin_config.email)
        if not admin:
            await self.create_admin(password=admin_config.password, email=admin_config.email)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        query: Select = select(AdminModel).where(AdminModel.email == email)
        async with self.app.database.session() as session:
            result: Result = await session.execute(query)
        admin_model: AdminModel = result.scalar_one_or_none()
        if admin_model:
            return Admin(**admin_model.to_dict())
        return None

    async def create_admin(self, email: str, password: str) -> Admin:
        password = sha256(password.encode()).hexdigest()
        admin_model = AdminModel(email=email, password=password)
        async with self.app.database.session() as session:
            session.add(admin_model)
            await session.commit()
        return Admin(**admin_model.to_dict())
