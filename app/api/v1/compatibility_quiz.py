from fastapi import APIRouter, Depends
from services import (
    ClientService, get_client_service,
    CompatibilityQuizService, get_compatibility_quiz_service,
    FamalyLoveImageService, get_famaly_love_image_service,
    FamalyLoveQuizService, get_famaly_love_quiz,
    MBTIQuizService, get_mbti_quiz_service,
    SMOLQuizService, get_smol_quiz_service
)
from .models import CompatibilityQuiz, ResultCompatibilityQuiz, StatusProcessingCompatibilityQuizEnum, FamalyLoveImages
from data_acces_layer import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from utils.models.famaly_love_quiz_enum import LeisurePreferencesCoincideEnum, EducationLevelEnum, HousingEnum, ExploreTogetherEnum, ExchangeIdeasEnum
from utils.models import CharacterType, PersonalityType
import numpy as np
import traceback

router = APIRouter()


@router.post(
    path='/',
    # response_model=FamalyLoveQuizId
)
async def send_quiz_famaly_love(
    compatibility_quiz: CompatibilityQuiz,
    client_service: ClientService = Depends(
        get_client_service),
    compatibility_quiz_service: CompatibilityQuizService = Depends(
        get_compatibility_quiz_service),
    famaly_love_image_service: FamalyLoveImageService = Depends(
        get_famaly_love_image_service),
    famaly_love_quiz_service: FamalyLoveQuizService = Depends(
        get_famaly_love_quiz),
    mbti_quiz_service: MBTIQuizService = Depends(
        get_mbti_quiz_service),
    smol_quiz_service: SMOLQuizService = Depends(
        get_smol_quiz_service),
    session: AsyncSession = Depends(get_session)
):
    orm_client = await client_service.create(session=session)
    orm_compatibility_quiz = await compatibility_quiz_service.create(
        orm_client.id,
        is_send_to_email=compatibility_quiz.is_send_to_email,
        email=compatibility_quiz.email,
        session=session
    )
    orm_famaly_love_quiz_service = await famaly_love_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.famaly_love_quiz.dict(),
        session=session
    )
    if not compatibility_quiz.images is None:
        if not compatibility_quiz.images.male_images is None:
            for male_image in compatibility_quiz.images.male_images:
                orm_famaly_love_image = await famaly_love_image_service.create(
                    orm_famaly_love_quiz_service.id,
                    is_male=True,
                    image_path=male_image,
                    session=session
                )
        if not compatibility_quiz.images.female_images is None:
            for female_image in compatibility_quiz.images.female_images:
                orm_famaly_love_image = await famaly_love_image_service.create(
                    orm_famaly_love_quiz_service.id,
                    is_male=False,
                    image_path=female_image,
                    session=session
                )
    orm_mbti_female = await mbti_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.mbti_quiz_female.dict(),
        is_male=False,
        session=session
    )
    orm_mbti_male = await mbti_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.mbti_quiz_male.dict(),
        is_male=True,
        session=session
    )
    orm_smol_female = await smol_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.smol_quiz_female.dict(),
        is_male=False,
        session=session
    )
    orm_smol_male = await smol_quiz_service.create(
        orm_compatibility_quiz.id,
        **compatibility_quiz.smol_quiz_male.dict(),
        is_male=True,
        session=session
    )
    try:
        await session.commit()
        return orm_compatibility_quiz.id
    except IntegrityError as ex:
        await session.rollback()
        raise ex


@router.get(
    path='/{id}/result',
    response_model=ResultCompatibilityQuiz
)
async def get_result(
    id: int,
    compatibility_quiz_service: CompatibilityQuizService = Depends(
        get_compatibility_quiz_service),
    session: AsyncSession = Depends(get_session)
):
    compatibility_quiz = await compatibility_quiz_service.get_by_id(id=id, session=session)

    count_famaly_years = 1
    famaly_love_quiz = compatibility_quiz.famaly_love_quiz
    if famaly_love_quiz.height_difference < -20:
        count_famaly_years -= 3
    elif famaly_love_quiz.height_difference < 0:
        count_famaly_years -= round(
            abs(famaly_love_quiz.height_difference) / 20 * 3)
    elif famaly_love_quiz.height_difference < 12:
        count_famaly_years += round(
            abs(famaly_love_quiz.height_difference) / 12 * 3)
    elif famaly_love_quiz.height_difference < 20:
        count_famaly_years += round(abs(20 -
                                    famaly_love_quiz.height_difference) / 8 * 3)

    if famaly_love_quiz.weight_difference < -20:
        count_famaly_years -= 3
    elif famaly_love_quiz.weight_difference < 0:
        count_famaly_years -= round(
            abs(famaly_love_quiz.weight_difference) / 20 * 3)
    elif famaly_love_quiz.weight_difference < 10:
        count_famaly_years += round(
            abs(famaly_love_quiz.weight_difference) / 10 * 3)
    elif famaly_love_quiz.weight_difference < 15:
        count_famaly_years += round(abs(15 -
                                    famaly_love_quiz.weight_difference) / 5 * 3)

    if famaly_love_quiz.age_difference < -10:
        count_famaly_years -= 2
    elif famaly_love_quiz.age_difference < -7:
        count_famaly_years -= round(abs(10 -
                                    famaly_love_quiz.age_difference) / 3 * 2)
    elif famaly_love_quiz.age_difference < 0:
        count_famaly_years += round(abs(famaly_love_quiz.age_difference) / 7 * 5)
    elif famaly_love_quiz.age_difference < 6:
        count_famaly_years += round(abs(famaly_love_quiz.age_difference) / 6 * 5)
    elif famaly_love_quiz.age_difference < 10:
        count_famaly_years -= round(abs(10 -
                                    famaly_love_quiz.age_difference) / 4 * 3)
    else:
        count_famaly_years -= 3

    if famaly_love_quiz.alcoholism:
        count_famaly_years -= 4
    else:
        count_famaly_years += 4

    if famaly_love_quiz.political_views_difference:
        count_famaly_years -= 2
    else:
        count_famaly_years += 2

    if famaly_love_quiz.leisure_preferences_coincide == LeisurePreferencesCoincideEnum.YES:
        count_famaly_years += 3
    elif famaly_love_quiz.leisure_preferences_coincide == LeisurePreferencesCoincideEnum.NO:
        count_famaly_years -= 3

    if famaly_love_quiz.education_level == EducationLevelEnum.YES:
        count_famaly_years += 3
    else:
        count_famaly_years -= 3

    if famaly_love_quiz.salary_male - famaly_love_quiz.salary_female != 0:
        percent_different_salary = (1 - (famaly_love_quiz.salary_male /
                                         (famaly_love_quiz.salary_male - famaly_love_quiz.salary_female))) * 100
        print(percent_different_salary)
        if percent_different_salary < -30:
            count_famaly_years -= 2
        elif percent_different_salary < -15:
            count_famaly_years -= round(abs(30 -
                                        percent_different_salary) / 15 * 2)
        elif percent_different_salary < 17:
            count_famaly_years += round(
                abs(percent_different_salary - 17) / 32 * 3)
        elif percent_different_salary < 50:
            count_famaly_years += round(
                abs(percent_different_salary - 17) / 33 * 1)
    elif famaly_love_quiz.salary_male == 0:
        count_famaly_years -= 2

    if famaly_love_quiz.housing == HousingEnum.YES:
        count_famaly_years += 4
    elif famaly_love_quiz.housing == HousingEnum.MORTAGE:
        count_famaly_years -= 2
    elif famaly_love_quiz.housing == HousingEnum.NO:
        count_famaly_years += 1

    if famaly_love_quiz.explore_together == ExploreTogetherEnum.YES:
        count_famaly_years += 3
    elif famaly_love_quiz.explore_together == ExploreTogetherEnum.SOMETIMES:
        count_famaly_years += 1
    elif famaly_love_quiz.explore_together == ExploreTogetherEnum.NO:
        count_famaly_years -= 1

    if famaly_love_quiz.exchange_ideas == ExchangeIdeasEnum.YES:
        count_famaly_years += 3
    elif famaly_love_quiz.exchange_ideas == ExchangeIdeasEnum.SOMETIMES:
        count_famaly_years += 1
    elif famaly_love_quiz.exchange_ideas == ExchangeIdeasEnum.NO:
        count_famaly_years -= 2

    flag = False
    for i in famaly_love_quiz.economy_sector_male:
        for j in famaly_love_quiz.economy_sector_female:
            if i == j:
                flag = True
    if flag:
        count_famaly_years += 5

    def get_personality_type(
        is_organizing: bool,
        is_communicability: bool,
        is_practicality: bool,
        is_logicality: bool
    ):
        if not is_organizing and is_communicability and not is_practicality and is_logicality:
            return PersonalityType.ENTP, 'Творческий искатель новых идей, теорий, возможностей. Очень любознателен, широкий спектр интересов. Не рационален, не склонен к самоорганизации. Не любит связывать себя обязательствами. Хороший руководитель нового проекта. Всегда живет как ему хочется. Независим, ограждает себя от обязанностей. Быстро теряет интерес к делу.'
        if not is_organizing and not is_communicability and is_practicality and not is_logicality:
            return PersonalityType.ISFP, 'Прекрасный эстетический вкус. Превосходный дизайнер. Стремление к гармонии пространственных форм, ощущению удобства, самочувствия. Стремление получать удовольствие от жизни во всем и сейчас. Дипломатичен, умеет договориться, найти «общий язык», коммуникативно активен, ориентируется в мотивах людей.'
        if is_organizing and is_communicability and is_practicality and not is_logicality:
            return PersonalityType.ESFJ, 'Человек общения. Обожает поднимать настроение другим, дарить радость. Оптимист. Борец за справедливость. Энтузиаст. Если загорается идеей – остается ей верным до конца. Берется за все подряд. Эмоциональность. Многое делает в состоянии душевного порыва. Теряет тонус, если его не хвалят за хорошую работу. Активен, доброжелателен, оптимистичен, создает гармоничные отношения со всеми. Не склонен продумывать свои действия. Не интересуется новым. Консервативен.'
        if is_organizing and not is_communicability and not is_practicality and is_logicality:
            return PersonalityType.INTJ, 'Аналитик в состоянии борьбы за идею. Выше всего ценит независимость. Стремится во всем найти логику, систему, модель. Не признает авторитетов, уважает интеллектуальных собеседников. Бескомпромиссно отстаивает свою точку зрения. Очень трудолюбив, всегда считается с удобством окружающих. Некоммуникабелен, прямолинеен, постоянно проявляет бескомпромиссность. Руководствуется в своих поступках высокими нравственными нормами. Агрессивно противостоит волевому давлению.'
        
        if is_organizing and is_communicability and not is_practicality and not is_logicality:
            return PersonalityType.ENFJ, 'Видит свое предназначение в том, чтобы исследовать душу человека, увидеть источник его боли и страданий, понять его поступки, показать их. Искусно управляет эмоциями людей, воздействует на окружающих широким диапазоном чувств. Желание повышенного внимания, эгоцентризм. Способен увлечься сам и увлечь других. Руководитель-мотиватор. Хорошо предвидит развитие событий.'
        if is_organizing and not is_communicability and is_practicality and is_logicality:
            return PersonalityType.ISTJ, 'Человек системы, структуры. Стремится все классифицировать и систематизировать, склонен все заорганизовывать. Всегда поддерживает действующую власть, не спорит с начальством. Надежный работник, безжалостный руководитель. Противник дестабилизации. Личному желанию отводит последнее место. Предполагает в поступках людей худшие мотивы.'
        if not is_organizing and not is_communicability and not is_practicality and not is_logicality:
            return PersonalityType.INFP, 'Склонный к сопереживанию поэтический романтик. Не критичен к чужому мнению. Нет собственной инициативы. Склонность к сопереживанию. Развито предчувствие. Обаятелен, элегантен, воспитан, деликатен. Склонен к компромиссам, конформист. Противопоказана любая производственная деятельность.'
        if not is_organizing and is_communicability and is_practicality and is_logicality:
            return PersonalityType.ESTP, 'Организатор, любой ценой достигающий результата. Волевой, мобилизованный, энергичный лидер, на котором держится все дело. Ведет себя резко и часто неэтично, может нарушать взятые на себя обязательства. Не признает правил, ограничивающих его свободу. Стремится заставить других сделать то, что ему нужно. Не допускает свободы выбора своего партнера.'
        
        if not is_organizing and not is_communicability and not is_practicality and is_logicality:
            return PersonalityType.INTP, 'Формирует стратегический прогноз и следует ему. Предвидение дальнейшего развития событий из предшествующих. Человек без эмоций, избирательная работоспособность. Долго «раскачивается». Не склонен менять место работы. Сверхдобросовестен. Не авторитарен, не волевой. Мнителен. Демократичен, стремится реализовать свой потенциал.'
        if not is_organizing and is_communicability and is_practicality and not is_logicality:
            return PersonalityType.ESFP, 'Неудержимое стремление к цели, напористость, уверенность в себе, пробивные способности, лидирующие свойства. Неудержимое стремление быть лучшим из лучших. Способен на любые жертвы ради этого. Все что им нужно, – территория для завоевания и повод для драки. Хороший тактик, никудышный стратег. Суматошный, инициативный. Ориентирован на ближайшие конкретные цели. Не способен работать в одиночестве, правильно распределить обязанности.'
        if is_organizing and is_communicability and not is_practicality and is_logicality:
            return PersonalityType.ENTJ, 'Не боящийся трудностей динамично работающий первопроходец. Настроен на преодоление преград, риск, точно рассчитывает новый проект во времени. Очень спортивен. Демократичен, романтичен, мобилен. Склонен к рационализаторству. Начинает много проектов, но только часть доводит до завершения. Прекрасный менеджер нестабильных участков работы.'
        if is_organizing and not is_communicability and is_practicality and not is_logicality:
            return PersonalityType.ISFJ, 'Строгий хранитель и защитник моральных ценностей: семья, дети, традиции. Руководствуется ведущей идеей о нормах морали. Превыше всего ставит мораль, верность долгу, выполнение взятых на себя обязательств. Слабо разбирается в экономической целесообразности. Тяготеет к знаниям, эрудит. Не умеет соразмерять свои планы со своими возможностями. Не может отделить главное от второстепенного.'
        
        if is_organizing and is_communicability and is_practicality and is_logicality:
            return PersonalityType.ESTJ, 'Одаренный администратор стабильных участков. Исключительно высокая степень личной ответственности за порученное дело, колоссальная работоспособность, способность выполнить дело с максимальным эффектом. Консервативен. Требователен. Соблюдает закон и порядок. Главное – хорошо работать, выполнять свое дело от и до. Все планирует.'
        if is_organizing and not is_communicability and not is_practicality and not is_logicality:
            return PersonalityType.INFJ, 'Стремится быть этическим примером идеалистических отношений, быть чутким к людям, соблюдать нормы нравственности, сопереживать, устанавливать благоприятный психологический климат. Помогает людям расти духовно. Стремится достичь гармонии в отношении с людьми, ищет истинные ценности в мире духовности и нравственности. Неэффективный работник. Нетребовательный, не волевой руководитель.'
        if not is_organizing and is_communicability and not is_practicality and not is_logicality:
            return PersonalityType.ISTP, 'Стремление угадать новую перспективную возможность, находить интересных людей с такими возможностями. Ищет с ними компромисс в ущерб принципам. Поиск всего нового, интересного, новаторского. Руководитель-мотиватор. Не любит долго заниматься одним делом. Мало уважения к принятым нормам поведения и иерархии отношений. Никогда не испытывает неловкости, не чувствует себя побежденным. Не любит кропотливой работы, не уважает сложившейся иерархии и норм поведения.'
        if not is_organizing and not is_communicability and is_practicality and is_logicality:
            return PersonalityType.ENFP, 'Мастер своего дела, получающий удовольствие от хорошо сделанной работы.Работает самостоятельно в небольшом коллективе. Характерно стремление к комфорту, желание оградить себя от неприятных ощущений. Хорошо делает работу своими руками. Не коммуникабелен, равнодушен к другим людям. Стремление выжимать личную пользу. Ищет баланс прекрасного и рационального.'
        
        return PersonalityType.NONE, ''

    male_personality_type, male_personality_desc = get_personality_type(
        sum(compatibility_quiz.mbti_quiz_male.first_organizing) + sum(compatibility_quiz.mbti_quiz_male.second_organizing) < 22,
        sum(compatibility_quiz.mbti_quiz_male.first_communicability) + sum(compatibility_quiz.mbti_quiz_male.second_communicability) < 22,
        sum(compatibility_quiz.mbti_quiz_male.first_practicality) + sum(compatibility_quiz.mbti_quiz_male.second_practicality) < 22,
        sum(compatibility_quiz.mbti_quiz_male.first_logicality) + sum(compatibility_quiz.mbti_quiz_male.second_logicality) < 22
    )
    
    female_personality_type, female_personality_desc = get_personality_type(
        sum(compatibility_quiz.mbti_quiz_female.first_organizing) + sum(compatibility_quiz.mbti_quiz_female.second_organizing) < 22,
        sum(compatibility_quiz.mbti_quiz_female.first_communicability) + sum(compatibility_quiz.mbti_quiz_female.second_communicability) < 22,
        sum(compatibility_quiz.mbti_quiz_female.first_practicality) + sum(compatibility_quiz.mbti_quiz_female.second_practicality) < 22,
        sum(compatibility_quiz.mbti_quiz_female.first_logicality) + sum(compatibility_quiz.mbti_quiz_female.second_logicality) < 22
    )

    def func_sum_true(test, arr):
        count_test = 0
        for a in arr:
            if test.quiz[a - 1]:
                count_test += 1
        return count_test

    def func_sum_false(test, arr):
        count_test = 0
        for a in arr:
            if not test.quiz[a - 1]:
                count_test += 1
        return count_test
    
    character_type = [
        CharacterType.SCHIZOID,
        CharacterType.PARANOID,
        CharacterType.NARCISSISTIC,
        CharacterType.PSYCHOPATHIC,
        CharacterType.COMPULSIVE,
        CharacterType.HYSTERICAL,
        CharacterType.DEPRESSIVE,
        CharacterType.MASOCHISTIC
    ]
    character_desc = [
        'Узость круга вариантов деятельности, увлеченность вариантом улучшения мира, уход во внутренний мир, увлеченность негуманитарной наукой, неприхотливость, хорошая память, утомление от интенсивных контактов, замкнутость, черствость, ненамеренное отступление от социальных норм, отстраненность от практической жизни, нетребовательность, нет честолюбия, упрямство, отпор агрессии.',
        'Подозрительность, ожидание худшего, честолюбие, предрассудки, пренебрежение к другим людям, ревность, неуживчивость, целеустремленность, верность флагу, с легкостью нарушают законы, завышенная самооценка, перекладывают ответствен на других, легко обижаемы, ранимы, уважение проявлениям силы и власти.',
        'Завышенная самооценка, не воспринимают людей как личностей, нет эмпатии, завышенные притязания славы, стремление эксплуатировать чужой труд, высокомерное поведение, требование преклонения, зависть, управленческие способности, эффективность решений, претензии на льготное приоритетное положение.',
        'Антисоциальное поведение, безответственность, агрессивность, раздражительность, лидерские качества, нестабильность отношений, бессердечие, лживость, отсутствие «комплексов», стремление манипулировать другими, поиск острых ощущений, неспособность обучатся на собственном опыте, завышенная самооценка, уверенность в правомерности поведения.',
        'Педантизм, условности; мечтательность, бескомпромиссность, отсутствие чувства юмора, бережливость до скупости, авторитарность, мало друзей; живость общения; работоспособность; приоритет работы над семьей; нерешительность.',
        'Требование внимания, раздражительность, ранимость, внушаемость, эгоизм, завышенная самооценка, честолюбие, энергетичность поведения, поиск возбуждающих эмоций, поверхностность, нестабильность отношений, необходимость помощи в снятии возбуждения.',
        'Не волевой, не может противостоять давлению, нетребователен, мобильность, энергичность, общительность, переключаемость, низкая самооценка, завышенные требования к себе, боязнь одиночества, агрессия, ранимость, деликатность, эмпатия, доброта, неинициативность, медлительность.',
        'Терпимость, вера в лучшее будущее, низкая самооценка, необходимость повышения самооценки, ранимость, некоммуникативность, утомляемость, покорность, безрадостность, избирательность контактов.'
    ]
    
    count_se = func_sum_true(compatibility_quiz.smol_quiz_male, [5, 7, 8, 10, 13, 14,15,16,17, 26, 30, 38, 39, 46, 57, 63, 64, 66]) + func_sum_false(compatibility_quiz.smol_quiz_male, [3, 42])
    percent_se = count_se / 20
    count_pa = func_sum_true(compatibility_quiz.smol_quiz_male, [5, 8, 10, 15, 30, 39, 63, 64, 66, 68]) + func_sum_false(compatibility_quiz.smol_quiz_male, [28, 29, 31, 67])
    percent_pa = count_pa / 14
    count_hy = func_sum_true(compatibility_quiz.smol_quiz_male, [9, 13, 18, 26, 44, 46, 55, 57, 62]) + func_sum_false(compatibility_quiz.smol_quiz_male, [1, 2, 3, 11, 23, 28, 29, 31, 33, 35, 37, 40, 41, 43, 45, 50, 56])
    percent_hy = count_hy / 26
    count_pd = func_sum_true(compatibility_quiz.smol_quiz_male, [7, 10, 13, 14, 15, 16, 22, 27, 52, 58, 71]) + func_sum_false(compatibility_quiz.smol_quiz_male, [3, 28, 34, 35, 41, 43, 50, 65])
    percent_pd = count_pd / 19
    count_hs = func_sum_true(compatibility_quiz.smol_quiz_male, [9, 18, 26, 32, 44, 46, 55, 62, 63]) + func_sum_false(compatibility_quiz.smol_quiz_male, [1, 2, 6, 37, 45])
    percent_hs = count_hs / 14
    count_ma = func_sum_true(compatibility_quiz.smol_quiz_male, [4, 7, 8, 21, 29, 34, 38, 39, 54, 57, 60]) + func_sum_false(compatibility_quiz.smol_quiz_male, [43])
    percent_ma = count_ma / 12
    count_d = func_sum_true(compatibility_quiz.smol_quiz_male, [9, 13, 17, 18, 22, 25, 36, 44]) + func_sum_false(compatibility_quiz.smol_quiz_male, [1, 3, 6, 11, 28, 37, 40, 42, 60, 65, 71])
    percent_d = count_d / 19
    count_pt = func_sum_true(compatibility_quiz.smol_quiz_male, [5, 8, 13, 17, 22, 25, 27, 36, 44, 51, 57, 66, 68]) + func_sum_false(compatibility_quiz.smol_quiz_male, [2, 3, 42])
    percent_pt = count_pt / 16
    male_character_number = np.array([percent_se, percent_pa, percent_hy, percent_pd, percent_hs, percent_ma, percent_d, percent_pt]).argmax(axis=0)
    male_character_type = character_type[male_character_number]
    male_character_desc = character_desc[male_character_number]
    
    
    count_se = func_sum_true(compatibility_quiz.smol_quiz_female, [5, 7, 8, 10, 13, 14,15,16,17, 26, 30, 38, 39, 46, 57, 63, 64, 66]) + func_sum_false(compatibility_quiz.smol_quiz_female, [3, 42])
    percent_se = count_se / 20
    count_pa = func_sum_true(compatibility_quiz.smol_quiz_female, [5, 8, 10, 15, 30, 39, 63, 64, 66, 68]) + func_sum_false(compatibility_quiz.smol_quiz_female, [28, 29, 31, 67])
    percent_pa = count_pa / 14
    count_hy = func_sum_true(compatibility_quiz.smol_quiz_female, [9, 13, 18, 26, 44, 46, 55, 57, 62]) + func_sum_false(compatibility_quiz.smol_quiz_female, [1, 2, 3, 11, 23, 28, 29, 31, 33, 35, 37, 40, 41, 43, 45, 50, 56])
    percent_hy = count_hy / 26
    count_pd = func_sum_true(compatibility_quiz.smol_quiz_female, [7, 10, 13, 14, 15, 16, 22, 27, 52, 58, 71]) + func_sum_false(compatibility_quiz.smol_quiz_female, [3, 28, 34, 35, 41, 43, 50, 65])
    percent_pd = count_pd / 19
    count_hs = func_sum_true(compatibility_quiz.smol_quiz_female, [9, 18, 26, 32, 44, 46, 55, 62, 63]) + func_sum_false(compatibility_quiz.smol_quiz_female, [1, 2, 6, 37, 45])
    percent_hs = count_hs / 14
    count_ma = func_sum_true(compatibility_quiz.smol_quiz_female, [4, 7, 8, 21, 29, 34, 38, 39, 54, 57, 60]) + func_sum_false(compatibility_quiz.smol_quiz_female, [43])
    percent_ma = count_ma / 12
    count_d = func_sum_true(compatibility_quiz.smol_quiz_female, [9, 13, 17, 18, 22, 25, 36, 44]) + func_sum_false(compatibility_quiz.smol_quiz_female, [1, 3, 6, 11, 28, 37, 40, 42, 60, 65, 71])
    percent_d = count_d / 19
    count_pt = func_sum_true(compatibility_quiz.smol_quiz_female, [5, 8, 13, 17, 22, 25, 27, 36, 44, 51, 57, 66, 68]) + func_sum_false(compatibility_quiz.smol_quiz_female, [2, 3, 42])
    percent_pt = count_pt / 16
    female_character_number= np.array([percent_se, percent_pa, percent_hy, percent_pd, percent_hs, percent_ma, percent_d, percent_pt]).argmax(axis=0)
    female_character_type = character_type[female_character_number]
    female_character_desc = character_desc[female_character_number]
    
    def calc_compatibility_points_on_personality_type(
        first_type: PersonalityType,
        second_type: PersonalityType
    ):
        points = 0
        positive_points = 0
        negative_points = 0
        
        if first_type.name[0] == 'E' and second_type.name[0]  == 'E':
            points -= 1
            negative_points += 1
        elif first_type.name[0] == 'E' and second_type.name[0]  == 'I':
            points += 1
            positive_points += 1
        elif first_type.name[0] == 'I' and second_type.name[0]  == 'E':
            points += 1
            positive_points += 1
        elif first_type.name[0] == 'I' and second_type.name[0]  == 'I':
            points -= 1
            negative_points += 1
        
        if first_type.name[1] == 'S' and second_type.name[1] == 'S':
            points -= 1
            negative_points += 1
        elif first_type.name[1] == 'S' and second_type.name[1] == 'N':
            points += 1
            positive_points += 1
        elif first_type.name[1] == 'N' and second_type.name[1] == 'S':
            points += 1
            positive_points += 1
        elif first_type.name[1] == 'N' and second_type.name[1] == 'N':
            points -= 1
            negative_points += 1
        
        if first_type.name[2] == 'T' and second_type.name[2] == 'T':
            points -= 1
            negative_points += 1
        elif first_type.name[2] == 'T' and second_type.name[2] == 'F':
            points += 1
            positive_points += 1
        elif first_type.name[2] == 'F' and second_type.name[2] == 'T':
            points += 1
            positive_points += 1
        elif first_type.name[2] == 'F' and second_type.name[2] == 'F':
            points -= 1
            negative_points += 1
        
        if first_type.name[3] == 'J' and second_type.name[3] == 'J':
            points += 1
            positive_points += 1
        elif first_type.name[3] == 'J' and second_type.name[3] == 'P':
            points -= 1
            negative_points += 1
        elif first_type.name[3] == 'P' and second_type.name[3] == 'J':
            points -= 1
            negative_points += 1
        elif first_type.name[3] == 'P' and second_type.name[3] == 'P':
            points += 1
            positive_points += 1
        
        print(first_type, second_type, positive_points, negative_points, 1000 * ((positive_points - negative_points) / 4))
        
        return 1000 * ((positive_points - negative_points) / 4)
    
    def calc_business_points_on_personality_type(
        first_type: PersonalityType,
        second_type: PersonalityType
    ):
        points = 0
        positive_points = 0
        negative_points = 0
        
        if first_type.name[0] == 'E' and second_type.name[0]  == 'E':
            points -= 1
            negative_points += 1
        elif first_type.name[0] == 'E' and second_type.name[0]  == 'I':
            points += 1
            positive_points += 1
        elif first_type.name[0] == 'I' and second_type.name[0]  == 'E':
            points += 1
            positive_points += 1
        elif first_type.name[0] == 'I' and second_type.name[0]  == 'I':
            points -= 1
            negative_points += 1
        
        if first_type.name[1] == 'S' and second_type.name[1] == 'S':
            points += 1
            positive_points += 1
        elif first_type.name[1] == 'S' and second_type.name[1] == 'N':
            points -= 1
            negative_points += 1
        elif first_type.name[1] == 'N' and second_type.name[1] == 'S':
            points -= 1
            negative_points += 1
        elif first_type.name[1] == 'N' and second_type.name[1] == 'N':
            points += 1
            positive_points += 1
        
        if first_type.name[2] == 'T' and second_type.name[2] == 'T':
            points -= 1
            negative_points += 1
        elif first_type.name[2] == 'T' and second_type.name[2] == 'F':
            points += 1
            positive_points += 1
        elif first_type.name[2] == 'F' and second_type.name[2] == 'T':
            points += 1
            positive_points += 1
        elif first_type.name[2] == 'F' and second_type.name[2] == 'F':
            points -= 1
            negative_points += 1
        
        if first_type.name[3] == 'J' and second_type.name[3] == 'J':
            points -= 1
            negative_points += 1
        elif first_type.name[3] == 'J' and second_type.name[3] == 'P':
            points += 1
            positive_points += 1
        elif first_type.name[3] == 'P' and second_type.name[3] == 'J':
            points += 1
            positive_points += 1
        elif first_type.name[3] == 'P' and second_type.name[3] == 'P':
            points -= 1
            negative_points += 1
        
        print(positive_points, negative_points, 1000 * ((positive_points - negative_points) / 4))
        
        return 1000 * ((positive_points - negative_points) / 4)

    compatibility_points = calc_compatibility_points_on_personality_type(male_personality_type, female_personality_type)
    
    business_points = calc_business_points_on_personality_type(male_personality_type, female_personality_type)

    def calc_compatibility_points_on_character_type(
        first_type: CharacterType,
        second_type: CharacterType
    ):
        first_number = 0
        second_number = 0
        arr = [
            [-90.9, -455, 400, -556, 466.7, -800, 0, -200],
            [-455, -333, -556, -143, -143, -750, -143, -500],
            [-400, -556, -667, -429, 0, -455, 66.7, 111],
            [-556, -143, -429, -714, -333, 0, 111.1, 0],
            [466.7, -143, 0, -333, -231, 250, 0, 250],
            [-800, -750, -455, 0, 250, -333, 333.3, 400],
            [0, -143, 167, 111.1, 0, 333.3, -429, 00],
            [-200, -500, -111, 0, 250, 400, 0, 600],
        ]
        return arr[first_number][second_number]
    character_points = calc_compatibility_points_on_character_type(male_character_type, female_character_type)
    print(character_points)
    compatibility_points += character_points
    business_points += character_points
    
    def calc_years(
        points: int
    ):
        try:
            top = [
                1466.7,
                1400,
                1333.3,
                1250,
                1111.1,
                1111,
                1066.7,
                1000,
                966.7,
                909.1,
                900,
                889,
                857,
                833.3,
                833,
                800,
                769,
                750,
                667,
                611.1,
                611,
                600,
                571,
                566.7,
                545,
                500,
                466.7,
                444,
                409.1,
                400,
                389,
                357,
                333.3,
                333,
                300,
                286,
                269,
                250,
                200,
                167,
                111.1,
                111,
                100,
                71,
                66.7,
                45,
                0,
                0,
                -33.3,
                -56,
                -90.9,
                -100,
                -111,
                -143,
                -166.7,
                -167,
                -200,
                -214,
                -231,
                -250,
                -300,
                -333,
                -388.9,
                -389,
                -400,
                -429,
                -433.3,
                -455,
                -500,
                -533.3,
                -556,
                -590.9,
                -600,
                -611,
                -643,
                -666.7,
                -667,
                -700,
                -714,
                -731,
                -750,
                -800,
                -833,
                -888.9,
                -889,
                -900,
                -929,
                -933.3,
                -955,
                -1000,
                -1056,
                -1090.9,
                -1100,
                -1111,
                -1143,
                -1167,
                -1200,
                -1214,
                -1231,
                -1250,
                -1300,
                -1333,
                -1400,
                -1429,
                -1455,
                -1500,
                -1556,
                -1600,
                -1667,
                -1714,
                -1750,
                -1800,
            ]
            top = top.index(points) + 1
        except:
            traceback.print_exc()
            top = 128
        print(points)
        return int(-1.1159 * top + 75.71)
    count_famaly_years = calc_years(compatibility_points) + count_famaly_years
    years_business = calc_years(business_points) + count_famaly_years
    count_famaly_years = count_famaly_years if 0 < count_famaly_years else 0
    years_business = years_business if 0 < years_business else 0

    print(
        male_personality_type,
        male_character_type,
        female_personality_type,
        female_character_type
    )

    return ResultCompatibilityQuiz(
        status=StatusProcessingCompatibilityQuizEnum.OK,
        male_personality_type=male_personality_type,
        male_personality_desc=male_personality_desc,
        male_character_type=male_character_type,
        male_character_desc=male_character_desc,
        female_personality_type=female_personality_type,
        female_personality_desc=female_personality_desc,
        female_character_type=female_character_type,
        female_character_desc=female_character_desc,
        years_compatibility_str=f'{count_famaly_years} лет',
        years_business_str=f'{years_business} лет'
    )
    
    # return ResultCompatibilityQuiz(
    #     status=StatusProcessingCompatibilityQuizEnum.OK,
    #     male_personality_type=person_type[male_personality_number],
    #     male_personality_desc=person_desc[male_personality_number],
    #     male_character_type=male_character_type,
    #     male_character_desc=male_character_desc,
    #     female_personality_type=person_type[female_personality_number],
    #     female_personality_desc=person_desc[female_personality_number],
    #     female_character_type=female_character_type,
    #     female_character_desc=female_character_desc,
    #     years_compatibility_str=f'{count_famaly_years} лет',
    #     years_business_str=f'{years_business} лет'
    # )


@router.get(
    path='/{id}/images',
    response_model=FamalyLoveImages
)
async def get_client_images(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return FamalyLoveImages(
        male_images=[
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWBAMAAADOL2zRAAAAG1BMVEUAAAv///+fn6NfX2YfHyk/P0h/f4W/v8Lf3+CfzlVWAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABAElEQVRoge3SMW+DMBiE4YsxJqMJtHOTITPeOsLQnaodGImEUMZEkZhRUqn92f0MaTubtfeMh/QGHANEREREREREREREtIJJ0xbH299kp8l8FaGtLdTQ19HjofxZlJ0m1+eBKZcikd9PWtXC5DoDotRO04B9YOvFIXmXLy2jEbiqE6Df7DTleA5socLqvEFVxtJyrpZFWz/pHM2CVte0lS8g2eDe6prOyqPglhzROL+Xye4tmT4WvRcQ2/m81p+/rdguOi8Hc5L/8Qk4vhZzy08DduGt9eVQyP2qoTM1zi0/uf4hvBWf5c77e69Gf798y08L7j0RERERERERERH9P99ZpSVRivB/rgAAAABJRU5ErkJggg=='
        ],
        female_images=[
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWBAMAAADOL2zRAAAAG1BMVEUAAAv///+fn6NfX2YfHyk/P0h/f4W/v8Lf3+CfzlVWAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABAElEQVRoge3SMW+DMBiE4YsxJqMJtHOTITPeOsLQnaodGImEUMZEkZhRUqn92f0MaTubtfeMh/QGHANEREREREREREREtIJJ0xbH299kp8l8FaGtLdTQ19HjofxZlJ0m1+eBKZcikd9PWtXC5DoDotRO04B9YOvFIXmXLy2jEbiqE6Df7DTleA5socLqvEFVxtJyrpZFWz/pHM2CVte0lS8g2eDe6prOyqPglhzROL+Xye4tmT4WvRcQ2/m81p+/rdguOi8Hc5L/8Qk4vhZzy08DduGt9eVQyP2qoTM1zi0/uf4hvBWf5c77e69Gf798y08L7j0RERERERERERH9P99ZpSVRivB/rgAAAABJRU5ErkJggg=='
        ]
    )


@router.put(
    path='/{id}/images'
)
async def reinit_images(
    id: int,
    images: FamalyLoveImages,
    session: AsyncSession = Depends(get_session)
):
    return id, images
