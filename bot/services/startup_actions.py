import random
import string

from bot.db.postgresql import Repo
from bot.db.postgresql.model.models import Cocktail, Promocode, LevelPrise

COCKTAILS = [
    'Calabria',
    'Kampania',
    'Lombardia',
    'Sardegna',
    'Sicilia',
    'Toscana',
    'Aperetivo Spritz',
    'Bitter Spritz',
    'Lemon Drop',
    'Strawberry Spritz',
    'Peach Spritz',
    'Limoncello Spritz',
]

leve_prise_dict = {
    1: 'Вітаємо, гра розпочалась✨',
    2: 'КЛАС, ПРОДОВЖУЙ 🔥',
    3: 'ТИ ВЕЛИКИЙ МОЛОДЕЦЬ! ☺️',
    4: ('<b>ВІТАЄМО!\nВи отримали свій перший приз- БЕЗКОШТОВНИЙ ЛІТРОВИЙ GAMONDI🍹</b>\n\nНасолоджуйтесь! Та '
        'пам’ятайте,'
        'що це лише початок😉\n\n<i>Для того щоб його отримати - покажіть це повідомлення офіціанту</i>'),
    5: 'ЧУДОВО, ТАК ТРИМАТИ 😍',
    6: 'ЗАЛИШИЛОСЬ ЩЕ ТРІШКИ ДО ПЕРЕМОГИ🤩',
    7: 'НЕ ЗВОЛІКАЙ, ПРОДОВЖУЙ🔥',
    8: '<b>ВІТАЄМО, ТИ МОЛОДЕЦЬ!\nОсь твій другий приз - БРЕНДОВАНИЙ БОКАЛ ВІД TUTTI☺️</b>\n\n'
       '<i>Для того щоб його отримати - покажіть це повідомлення офіціанту</i>',
    9: 'ТИ СПРАВЖНІЙ ФАНАТ ШПРИЦІВ🤤',
    10: 'СУПЕР, СКОРО СТАНЕШ СПРАВЖНІМ ЧЕМПІОНОМ❤️‍🔥',
    11: 'ЗАЛИШИВСЯ ОДИН ШПРИЦ ДО ФІНАЛЬНОГО ПРИЗУ🔥',
    12: ('<b>ВІТАЄМО ІЗ ЗАКІНЧЕННЯМ ГРИ😍</b>\n'
         'Дякуємо за участь, ти успішно пройшов усі етапи та отримав <b>ГОЛОВНИЙ ПОДАРУНОК - унікальна статуетка з '
         'твоїм'
         'іменем❤️</b>\n\n<i>Для того щоб його отримати - покажіть це повідомлення офіціанту</i>')

}


async def add_default_objects(db_factory):
    async with db_factory() as session:
        repo = Repo(session=session)
        cocktails = await repo.user_repo.get_cocktails()
        if not cocktails:
            for i in COCKTAILS:
                cocktail_model = Cocktail(
                    title=i,
                    code=i[0:2].upper()
                )
                cocktail_model = await repo.add_one(cocktail_model,
                                                    commit=False)

                promo_model = Promocode( 
                    
                    promocode=f'{cocktail_model.code}{"".join(random.choices(string.ascii_letters + string.digits, k=5))}',
                    cocktail_id=cocktail_model.id
                )
                await repo.add_one(promo_model, commit=False)
            for i in range(1, 13):
                level_model = LevelPrise(
                    level=i,
                    prise=leve_prise_dict[i]
                )
                await repo.add_one(level_model, commit=False)

            await session.commit()
