dictionary = {'а':'a',
              'б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'ch','ш':'sh','щ':'sch','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ya', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'YO',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CH','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}

future_db = {'город': '',
             'поиск': '',
             'мин': '',
             'макс': '',
             'ссылка': ''}

full_db = {}

cities = ['абакан', 'азов', 'александров', 'алексин', 'альметьевск', 'анапа', 'ангарск', 'анжеро-судженск', 'апатиты', 'арзамас', 'армавир', 'арсеньев', 'артем', 'архангельск', 'асбест', 'астрахань', 'ачинск', 'балаково', 'балахна', 'балашиха', 'балашов', 'барнаул', 'батайск', 'белгород', 'белебей', 'белово', 'белогорск (амурская область)', 'белорецк', 'белореченск', 'бердск', 'березники', 'березовский (свердловская область)', 'бийск', 'биробиджан', 'благовещенск (амурская область)', 'бор', 'борисоглебск', 'боровичи', 'братск', 'брянск', 'бугульма', 'буденновск', 'бузулук', 'буйнакск', 'великие луки', 'великий новгород', 'верхняя пышма', 'видное', 'владивосток', 'владикавказ', 'владимир', 'волгоград', 'волгодонск', 'волжск', 'волжский', 'вологда', 'вольск', 'воркута', 'воронеж', 'воскресенск', 'воткинск', 'всеволожск', 'выборг', 'выкса', 'вязьма', 'гатчина', 'геленджик', 'георгиевск', 'глазов', 'горно-алтайск', 'грозный', 'губкин', 'гудермес', 'гуково', 'гусь-хрустальный', 'дербент', 'дзержинск', 'димитровград', 'дмитров', 'долгопрудный', 'домодедово', 'донской', 'дубна', 'евпатория', 'егорьевск', 'ейск', 'екатеринбург', 'елабуга', 'елец', 'ессентуки', 'железногорск (красноярский край)', 'железногорск (курская область)', 'жигулевск', 'жуковский', 'заречный', 'зеленогорск', 'зеленодольск', 'златоуст', 'иваново', 'ивантеевка', 'ижевск', 'избербаш', 'иркутск', 'искитим', 'ишим', 'ишимбай', 'йошкар-ола', 'казань', 'калининград', 'калуга', 'каменск-уральский', 'каменск-шахтинский', 'камышин', 'канск', 'каспийск', 'кемерово', 'керчь', 'кинешма', 'кириши', 'киров (кировская область)', 'кирово-чепецк', 'киселевск', 'кисловодск', 'клин', 'клинцы', 'ковров', 'когалым', 'коломна', 'комсомольск-на-амуре', 'копейск', 'королев', 'кострома', 'котлас', 'красногорск', 'краснодар', 'краснокаменск', 'краснокамск', 'краснотурьинск', 'красноярск', 'кропоткин', 'крымск', 'кстово', 'кузнецк', 'кумертау', 'кунгур', 'курган', 'курск', 'кызыл', 'лабинск', 'лениногорск', 'ленинск-кузнецкий', 'лесосибирск', 'липецк', 'лиски', 'лобня', 'лысьва', 'лыткарино', 'люберцы', 'магадан', 'магнитогорск', 'майкоп', 'махачкала', 'междуреченск', 'мелеуз', 'миасс', 'минеральные воды', 'минусинск', 'михайловка', 'михайловск (ставропольский край)', 'мичуринск', 'москва', 'мурманск', 'муром', 'мытищи', 'набережные челны', 'назарово', 'назрань', 'нальчик', 'наро-фоминск', 'находка', 'невинномысск', 'нерюнгри', 'нефтекамск', 'нефтеюганск', 'нижневартовск', 'нижнекамск', 'нижний новгород', 'нижний тагил', 'новоалтайск', 'новокузнецк', 'новокуйбышевск', 'новомосковск', 'новороссийск', 'новосибирск', 'новотроицк', 'новоуральск', 'новочебоксарск', 'новочеркасск', 'новошахтинск', 'новый уренгой', 'ногинск', 'норильск', 'ноябрьск', 'нягань', 'обнинск', 'одинцово', 'озерск (челябинская область)', 'октябрьский', 'омск', 'орел', 'оренбург', 'орехово-зуево', 'орск', 'павлово', 'павловский посад', 'пенза', 'первоуральск', 'пермь', 'петрозаводск', 'петропавловск-камчатский', 'подольск', 'полевской', 'прокопьевск', 'прохладный', 'псков', 'пушкино', 'пятигорск', 'раменское', 'ревда', 'реутов', 'ржев', 'рославль', 'россошь', 'ростов-на-дону', 'рубцовск', 'рыбинск', 'рязань', 'салават', 'сальск', 'самара', 'санкт-петербург', 'саранск', 'сарапул', 'саратов', 'саров', 'свободный', 'севастополь', 'северодвинск', 'северск', 'сергиев посад', 'серов', 'серпухов', 'сертолово', 'сибай', 'симферополь', 'славянск-на-кубани', 'смоленск', 'соликамск', 'солнечногорск', 'сосновый бор', 'сочи', 'ставрополь', 'старый оскол', 'стерлитамак', 'ступино', 'сургут', 'сызрань', 'сыктывкар', 'таганрог', 'тамбов', 'тверь', 'тимашевск', 'тихвин', 'тихорецк', 'тобольск', 'тольятти', 'томск', 'троицк', 'туапсе', 'туймазы', 'тула', 'тюмень', 'узловая', 'улан-удэ', 'ульяновск', 'урус-мартан', 'усолье-сибирское', 'уссурийск', 'усть-илимск', 'уфа', 'ухта', 'феодосия', 'фрязино', 'хабаровск', 'ханты-мансийск', 'хасавюрт', 'химки', 'чайковский', 'чапаевск', 'чебоксары', 'челябинск', 'черемхово', 'череповец', 'черкесск', 'черногорск', 'чехов', 'чистополь', 'чита', 'шадринск', 'шали', 'шахты', 'шуя', 'щекино', 'щелково', 'электросталь', 'элиста', 'энгельс', 'южно-сахалинск', 'юрга', 'якутск', 'ялта', 'ярославль']