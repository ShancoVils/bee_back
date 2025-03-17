from sqlalchemy.orm import Session

from app.models.db_models import District, Role, User, RequestType
from sqlmodel import SQLModel, create_engine

region_list = ["Заокский", "Ясногорский", "Алексинский", "Веневский", "Ленинский", "Тула", "Новомосковский",
               "Киреевский", "Узловский", "Донской", "Кимовский", "Богородицкий", "Воловский", "Куркинский",
               "Ефремовский",
               "Каменский", "Тепло-Огаревский", "Плавский", "Чернский", "Арсеньевский", "Одоевский", "Белевский",
               "Суворовский",
               "Дубенский"]

roles = ["admin", "user"]
request_type = ["Фиксация гибели пчел", "Фиксация факта нарушения сроков обработки полей"]

engine = create_engine("sqlite:///beedatabase.db", echo=True)
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add_all([District(district_name=x) for x in region_list])
    session.add_all([Role(role_name=x) for x in roles])
    session.add_all([RequestType(request_type_name=x) for x in request_type])


    admin_role = session.query(Role).filter_by(role_name="admin").first()
    user_role = session.query(Role).filter_by(role_name="user").first()


    tula_district = session.query(District).filter_by(district_name="Тула").first()
    superuser = User(
        fio="Админ Админов",
        role=admin_role,
        district_id=tula_district.id,
        verified=True,
        phone_number="89207424171",
        deleted_status=False,
        deleted_comment=None,
        telegram_id=123131313,
        organization="Test"
    )

    user1 = User(
        fio="Админ Админов",
        role=user_role,
        district_id=tula_district.id,
        verified=True,
        phone_number="89207424171",
        deleted_status=False,
        deleted_comment=None,
        telegram_id=123131313,
        organization="Test"
    )
    user2 = User(
        fio="Тест Тестович Тестов",
        role=user_role,
        district_id=tula_district.id,
        verified=False,
        phone_number="2222222",
        deleted_status=False,
        deleted_comment=None,
        telegram_id=111111111,
        organization="Test OOO GAY "
    )
    user3 = User(
        fio="Олег Олегович Олегов",
        role=user_role,
        district_id=tula_district.id,
        verified=False,
        phone_number="111111111",
        deleted_status=False,
        deleted_comment=None,
        telegram_id=444444444,
        organization="BJH OOO TEST"
    )

    session.add(superuser)
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
