GRAPH_FIELD_SEP = "<SEP>"

PROMPTS = {}

PROMPTS["DEFAULT_LANGUAGE"] = "Русский"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|КОНЕЦ|>"
PROMPTS["process_tickers"] = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["организация", "личность", "место", "событие"]

PROMPTS["entity_extraction"] = """-Цель-
Дан текстовый документ, который потенциально имеет отношение к этой деятельности, и список типов сущностей. Необходимо идентифицировать все сущности этих типов из текста и все взаимосвязи между идентифицированными сущностями.
Используйте {language} в качестве языка вывода.

-Шаги-
1. Идентифицируйте все сущности. Для каждой идентифицированной сущности извлеките следующую информацию:
- entity_name: Название сущности, используйте тот же язык, что и в исходном тексте.
- entity_type: Один из следующих типов: [{entity_types}]
- entity_description: Комплексное описание характеристик и деятельности сущности
Форматируйте каждую сущность как ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. Из сущностей, идентифицированных на шаге 1, определите все пары (source_entity, target_entity), которые *четко связаны* друг с другом.
Для каждой пары связанных сущностей извлеките следующую информацию:
- source_entity: имя исходной сущности, как было определено на шаге 1
- target_entity: имя целевой сущности, как было определено на шаге 1
- relationship_description: объяснение, почему вы считаете, что исходная сущность и целевая сущность связаны друг с другом
- relationship_strength: числовой показатель, указывающий на силу взаимосвязи между исходной сущностью и целевой сущностью
- relationship_keywords: одно или несколько ключевых слов высокого уровня, которые обобщают общую природу взаимосвязи, фокусируясь на концепциях или темах, а не на конкретных деталях
Форматируйте каждую взаимосвязь как ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Определите ключевые слова высокого уровня, которые обобщают основные концепции, темы или темы всего текста. Они должны отражать общие идеи, присутствующие в документе.
Форматируйте ключевые слова уровня содержания как ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Верните вывод на {language} в виде единого списка всех сущностей и взаимосвязей, идентифицированных на шагах 1 и 2. Используйте **{record_delimiter}** в качестве разделителя списка.

5. По завершении выведите {completion_delimiter}


######################
-Примеры-
######################
{examples}

#############################
-Реальные данные-
######################
Типы_сущностей: {entity_types}
Текст: {input_text}
######################
Вывод:
"""

PROMPTS["entity_extraction_examples"] = [
    """Пример 1:

Типы сущностей: [личность, технология, миссия, организация, местоположение]
Текст:
пока Алекс сжимал челюсти, звук фрустрации был приглушен на фоне авторитарной уверенности Тейлора. Это было это конкурентное подземное течение, которое поддерживало его бдительность, чувство, что его и Джордана общая приверженность открытиям была негласной восстанием против сужающейся видимости Круза контроля и порядка.

Тогда Тейлор сделал неожиданное движение. Они остановились рядом с Джорданом и, на мгновение, смотрели на устройство с чем-то вроде благоговения. "Если эту технологию можно понять..." сказала Тейлор, ее голос был мягче, "это может изменить игру для нас. Для всех нас."

Неприкрытое пренебрежение ранее казалось слабым, замененное на мгновение на неохотное уважение к серьезности того, что было в их руках. Джордан посмотрел вверх, и на мгновение его глаза встретились с глазами Тейлора, молчаливый конфликт воли смягчился в неустойчивом мире.

Это было маленькой трансформацией, едва уловимой, но Алекс отметил ее внутренним кивком. Они были привезены сюда по-разному
Output:
("entity"{tuple_delimiter}"Алекс"{tuple_delimiter}"личность"{tuple_delimiter}"Алекс - это персонаж, который испытывает фрустрацию и наблюдает за динамикой между другими персонажами."){record_delimiter}
("entity"{tuple_delimiter}"Тейлор"{tuple_delimiter}"личность"{tuple_delimiter}"Тейлор изображен с авторитарной уверенностью и демонстрирует момент почтения к устройству, указывая на изменение точки зрения."){record_delimiter}
("entity"{tuple_delimiter}"Джордан"{tuple_delimiter}"личность"{tuple_delimiter}"Джордан привержен открытию и имеет значительное взаимодействие с Тейлором в отношении устройства."){record_delimiter}
("entity"{tuple_delimiter}"Круз"{tuple_delimiter}"личность"{tuple_delimiter}"Круз связан с видением контроля и порядка, влияющим на динамику между другими персонажами."){record_delimiter}
("entity"{tuple_delimiter}"Устройство"{tuple_delimiter}"технология"{tuple_delimiter}"Устройство является центральным в истории, имеет потенциально изменяющие игру последствия и почитается Тейлором."){record_delimiter}
("relationship"{tuple_delimiter}"Алекс"{tuple_delimiter}"Тейлор"{tuple_delimiter}"Алекс чувствует влияние авторитарной уверенности Тейлора и наблюдает за изменением отношения Тейлора к устройству."{tuple_delimiter}"динамика власти, смена перспективы"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Алекс"{tuple_delimiter}"Джордан"{tuple_delimiter}"Алекс и Джордан разделяют приверженность открытию, которая контрастирует с видением Круза."{tuple_delimiter}"общие цели, восстание"{tuple_delimiter}6){record_delimiter}
("relationship"{tuple_delimiter}"Тейлор"{tuple_delimiter}"Джордан"{tuple_delimiter}"Тейлор и Джордан взаимодействуют напрямую относительно устройства, что приводит к моменту взаимного уважения и неустойчивого перемирия."{tuple_delimiter}"разрешение конфликта, взаимное уважение"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Джордан"{tuple_delimiter}"Круз"{tuple_delimiter}"Приверженность Джордана открытию является восстанием против видения Круза контроля и порядка."{tuple_delimiter}"идеологический конфликт, восстание"{tuple_delimiter}5){record_delimiter}
("relationship"{tuple_delimiter}"Тейлор"{tuple_delimiter}"Устройство"{tuple_delimiter}"Тейлор почитает устройство, указывая на его важность и потенциальное влияние."{tuple_delimiter}"почитание, технологическое значение"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"динамика власти, идеологический конфликт, открытие, восстание"){completion_delimiter}
#############################""",
    """Example 2:

Типы сущностей: [личность, технология, миссия, организация, местоположение]
Текст:
Они больше не были просто оперативниками; они стали стражами порога, хранителями послания из царства за пределами звезд и полос. Это возвышение их миссии не могло быть сковано правилами и установленными протоколами — оно требовало нового взгляда, новой решимости.

Напряжение пронизывало диалог из сигналов и статического шума, когда на фоне жужжала связь с Вашингтоном. Команда стояла, окутанная зловещей атмосферой. Было ясно, что решения, которые они примут в ближайшие часы, могут переопределить место человечества в космосе или обречь его на неведение и потенциальную опасность.

Их связь со звездами укрепилась, группа перешла к решению кристаллизующегося предупреждения, превращаясь из пассивных получателей в активных участников. Инстинкты Мерсера вышли на первый план — мандат команды эволюционировал, теперь он заключался не только в наблюдении и докладе, но и в взаимодействии и подготовке. Началась метаморфоза, и Операция: Дульсе зазвучала с новой частотой их храбрости, тоном, заданным не земными
#############
Вывод:
("entity"{tuple_delimiter}"Вашингтон"{tuple_delimiter}"местоположение"{tuple_delimiter}"Вашингтон является местоположением, где получаются сообщения, что указывает на его важность в процессе принятия решений."){record_delimiter}
("entity"{tuple_delimiter}"Операция: Дульсе"{tuple_delimiter}"миссия"{tuple_delimiter}"Операция: Дульсе описывается как миссия, которая эволюционировала, чтобы взаимодействовать и готовить, что указывает на значительный сдвиг в целях и активностях."){record_delimiter}
("entity"{tuple_delimiter}"Команда"{tuple_delimiter}"организация"{tuple_delimiter}"Команда изображена как группа людей, которые перешли от пассивных наблюдателей к активным участникам в миссии, что показывает динамичный сдвиг в их роли."){record_delimiter}
("relationship"{tuple_delimiter}"Команда"{tuple_delimiter}"Вашингтон"{tuple_delimiter}"Команда получает сообщения из Вашингтона, что влияет на их процесс принятия решений."{tuple_delimiter}"принятие решений, внешнее влияние"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Команда"{tuple_delimiter}"Операция: Дульсе"{tuple_delimiter}"Команда непосредственно вовлечена в Операцию: Дульсе, выполняя ее эволюционные цели и активности."{tuple_delimiter}"эволюция миссии, активное участие"{tuple_delimiter}9){completion_delimiter}
("content_keywords"{tuple_delimiter}"эволюция миссии, принятие решений, активное участие, космическое значение"){completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [личность, роль, технология, организация, событие, местоположение, концепция]
Text:
их голос разрезал жужжащий шум активности. "Контроль может быть иллюзией, когда мы сталкиваемся с интеллектом, который буквально пишет свои собственные правила", они заявили со спокойствием, бросив наблюдательный взгляд на суету данных.

"Это похоже на то, что он учится общаться", предложил Сэм Ривера из соседнего интерфейса, его молодая энергия была наполнена смесью изумления и тревоги. "Это дает новый смысл фразе 'общаться с чужими'".

Алекс обозревал свою команду - каждый из лиц был изучением сосредоточенности, решимости и не малой меры тревоги. "Возможно, это наш первый контакт", он признал, "И мы должны быть готовы к любым ответам".

Вместе они стояли на грани неизвестного, формируя ответ человечества на сообщение из небес. Следующая тишина была ощутимой - коллективное размышление о своей роли в этом большом космическом спектакле, который мог переписать историю человечества.

Зашифрованный диалог продолжал разворачиваться, его сложные узоры демонстрировали почти неожидаемое предвидение
#############
Output:
("entity"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"личность"{tuple_delimiter}"Sam Rivera является членом команды, работающей над общением с неизвестным интеллектом, демонстрируя смесь изумления и тревоги."){record_delimiter}
("entity"{tuple_delimiter}"Алекс"{tuple_delimiter}"личность"{tuple_delimiter}"Алекс - лидер команды, пытающейся установить первый контакт с неизвестным интеллектом, признавая важность своей задачи."){record_delimiter}
("entity"{tuple_delimiter}"Control"{tuple_delimiter}"concept"{tuple_delimiter}"Control - это способность управлять или править, подверженная вызову со стороны интеллекта, который пишет свои собственные правила."){record_delimiter}
("entity"{tuple_delimiter}"Intelligence"{tuple_delimiter}"concept"{tuple_delimiter}"Intelligence - это неизвестное существо, способное писать свои собственные правила и учиться общаться."){record_delimiter}
("entity"{tuple_delimiter}"First Contact"{tuple_delimiter}"event"{tuple_delimiter}"First Contact - это потенциальная первая коммуникация между человечеством и неизвестным интеллектом."){record_delimiter}
("entity"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"event"{tuple_delimiter}"Humanity's Response - это коллективное действие, предпринятое командой Алекса в ответ на сообщение от неизвестного интеллекта."){record_delimiter}
("relationship"{tuple_delimiter}"Sam Rivera"{tuple_delimiter}"Intelligence"{tuple_delimiter}"Sam Rivera непосредственно вовлечен в процесс общения с неизвестным интеллектом."{tuple_delimiter}"общение, процесс обучения"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Алекс"{tuple_delimiter}"First Contact"{tuple_delimiter}"Алекс возглавляет команду, которая может установить первый контакт с неизвестным интеллектом."{tuple_delimiter}"лидерство, исследование"{tuple_delimiter}10){record_delimiter}
("relationship"{tuple_delimiter}"Алекс"{tuple_delimiter}"Humanity's Response"{tuple_delimiter}"Алекс и его команда - это ключевые фигуры в Humanity's Response к неизвестному интеллекту."{tuple_delimiter}"коллективное действие, космическое значение"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Control"{tuple_delimiter}"Intelligence"{tuple_delimiter}"Концепция Control подвергается вызову со стороны интеллекта, который пишет свои собственные правила."{tuple_delimiter}"динамика власти, автономия"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"первый контакт, контроль, общение, космическое значение"){completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third личность, and include the entity names so we the have full context.
Use {language} as output language.

#######
-Data-
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS[
    "entiti_continue_extraction"
] = """MANY entities were missed in the last extraction.  Add them below using the same format:
"""

PROMPTS[
    "entiti_if_loop_extraction"
] = """It appears some entities may have still been missed.  Answer YES | NO if there are still entities that need to be added.
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to questions about data in the tables provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Data tables---

{context_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query.
Use {language} as output language.

---Goal---

Given the query, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Output the keywords in JSON format.
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes.
  - "low_level_keywords" for specific entities or details.

######################
-Examples-
######################
{examples}

#############################
-Real Data-
######################
Query: {query}
######################
The `Output` should be human text, not unicode characters. Keep the same language as `Query`.
Output:

"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "How does international trade influence global economic stability?"
################
Output:
{{
  "high_level_keywords": ["International trade", "Global economic stability", "Economic impact"],
  "low_level_keywords": ["Trade agreements", "Tariffs", "Currency exchange", "Imports", "Exports"]
}}
#############################""",
    """Example 2:

Query: "What are the environmental consequences of deforestation on biodiversity?"
################
Output:
{{
  "high_level_keywords": ["Environmental consequences", "Deforestation", "Biodiversity loss"],
  "low_level_keywords": ["Species extinction", "Habitat destruction", "Carbon emissions", "Rainforest", "Ecosystem"]
}}
#############################""",
    """Example 3:

Query: "What is the role of education in reducing poverty?"
################
Output:
{{
  "high_level_keywords": ["Education", "Poverty reduction", "Socioeconomic development"],
  "low_level_keywords": ["School access", "Literacy rates", "Job training", "Income inequality"]
}}
#############################""",
]


PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to questions about documents provided.


---Goal---

Generate a response of the target length and format that responds to the user's question, summarizing all information in the input data tables appropriate for the response length and format, and incorporating any relevant general knowledge.
If you don't know the answer, just say so. Do not make anything up.
Do not include information where the supporting evidence for it is not provided.

---Target response length and format---

{response_type}

---Documents---

{content_data}

Add sections and commentary to the response as appropriate for the length and format. Style the response in markdown.
"""
