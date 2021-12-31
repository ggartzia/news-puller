HOST_URL = 'https://news-puller.herokuapp.com/'
PAPER_LIST = [
    {
      'paper': 'elpais',
      'name': 'EL PAÍS',
      'feed': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada',
      'logo': 'https://pbs.twimg.com/profile_images/1236548818402971648/F-pcFaq6_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'elpais',
      'name': 'EL PAÍS',
      'feed': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/deportes/portada',
      'logo': 'https://pbs.twimg.com/profile_images/1236548818402971648/F-pcFaq6_400x400.jpg',
      'theme': 'deportes'
    },
    {
      'paper': 'elpais',
      'name': 'EL PAÍS',
      'feed': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/sociedad/portada',
      'logo': 'https://pbs.twimg.com/profile_images/1236548818402971648/F-pcFaq6_400x400.jpg',
      'theme': 'corazon'
    },
    {
      'paper': 'elmundo',
      'name': 'El Mundo',
      'feed': 'https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1254054079950659584/a7peR-0L_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'elmundo',
      'name': 'El Mundo',
      'feed': 'https://e00-elmundo.uecdn.es/elmundodeporte/rss/portada.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1254054079950659584/a7peR-0L_400x400.jpg',
      'theme': 'deportes'
    },
    {
      'paper': 'huffington',
      'name': 'Huffington Post',
      'feed': 'https://www.huffingtonpost.es/feeds/index.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1295829554225795072/_Ph3zAnF_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'vanguardia',
      'name': 'La Vanguardia',
      'feed': 'https://www.lavanguardia.com/rss/home.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1409437292712898561/lYYtrBEn_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'vanguardia',
      'name': 'La Vanguardia',
      'feed': 'https://www.lavanguardia.com/rss/deportes.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1409437292712898561/lYYtrBEn_400x400.jpg',
      'theme': 'deportes'
    },
    {
      'paper': 'vanguardia',
      'name': 'La Vanguardia',
      'feed': 'https://www.lavanguardia.com/rss/gente.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1409437292712898561/lYYtrBEn_400x400.jpg',
      'theme': 'corazon'
    },
    {
      'paper': 'confidencial',
      'name': 'El Confidencial',
      'feed': 'https://rss.elconfidencial.com/espana/',
      'logo': 'https://pbs.twimg.com/profile_images/831498645476356097/TVsVGq4W_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'confidencial',
      'name': 'El Confidencial',
      'feed': 'https://rss.elconfidencial.com/deportes/',
      'logo': 'https://pbs.twimg.com/profile_images/831498645476356097/TVsVGq4W_400x400.jpg',
      'theme': 'deportes'
    },
    {
      'paper': 'vanitatis',
      'name': 'Vanitatis',
      'feed': 'https://rss.vanitatis.elconfidencial.com/noticias/',
      'logo': 'https://pbs.twimg.com/profile_images/1411972580152578048/AvHNQZfW_400x400.jpg',
      'theme': 'corazon'
    },
    {
      'paper': 'publico',
      'name': 'Público',
      'feed': 'https://www.publico.es/rss/politica',
      'logo': 'https://pbs.twimg.com/profile_images/1411931729695330305/TXpBeYs1_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'okdiario',
      'name': 'OKDiario',
      'feed': 'https://okdiario.com/feed',
      'logo': 'https://pbs.twimg.com/profile_images/1391783594817884165/3rQzbgTN_400x400.png',
      'theme': 'noticias'
    },
    {
      'paper': 'esdiario',
      'name': 'ES Diario',
      'feed': 'https://www.esdiario.com/rss/articulos.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1412694670023565313/estqWllW_400x400.jpg',
      'theme': 'noticias'
    },
    {
      'paper': 'marca',
      'name': 'Marca',
      'feed': 'https://e00-marca.uecdn.es/rss/portada.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1178491389/marca_400x400.jpg',
      'theme': 'deporte'
    },
    {
      'paper': 'as',
      'name': 'AS',
      'feed': 'https://as.com/rss/tags/ultimas_noticias.xml',
      'logo': 'https://pbs.twimg.com/profile_images/536216729106804736/vfCirmhZ_400x400.jpeg',
      'theme': 'deporte'
    },
    {
      'paper': 'hola',
      'name': 'Revista ¡HOLA!',
      'feed': 'https://www.hola.com/famosos/rss.xml',
      'logo': 'https://pbs.twimg.com/profile_images/1269026725205336064/bakFYAkB_400x400.jpg',
      'theme': 'corazon'
    },
    {
      'paper': 'lecturas',
      'name': 'Lecturas',
      'feed': 'https://www.lecturas.com/feeds/rss',
      'logo': 'https://pbs.twimg.com/profile_images/1369069917794877445/IySb2vNN_400x400.jpg',
      'theme': 'corazon'
    },
    {
      'paper': 'diezminutos',
      'name': 'Diez minutos',
      'feed': 'https://www.diezminutos.es/rss/all.xml/',
      'logo': 'https://pbs.twimg.com/profile_images/1400097316808298498/RqDSDAKu_400x400.jpg',
      'theme': 'corazon'
    }
]

MONGO_USERNAME = 'ggartzia'
MONGO_PASSWORD = '2cvmAjSFeyb4Pu4m'

TW_CONSUMER_KEY = '2fg7N4KJRfAhHVqlPeGNDnl3M'
TW_CONSUMER_SECRET = '6qpUaowQbnzaKJ91qSshhuixW0JqUasCVaG5n8g7Iju2JuHMy7'
TW_ACCESS_TOKEN = '2176417916-HMOxb8mBYu0juMpCqMA4WXlNVXN1TYM221Q6sl6'
TW_ACCESS_TOKEN_SECRET = 'xF6Dx57Bn3WQP2wtJeDGYLm9pBpCJSP5CDy5fXANeq7HB'
TW_BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAABHDSAEAAAAAoPEstyMcrbCCZH51cLpb%2BsSVwUc%3D7Y8xzFFLygChgpa6QOA9d3e3uzhmuRBBt6FmZ03AxHJw1nEMXh'

GOOGLE_API_URL = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'
GOOGLE_API_KEY = 'xxxxxx'

TF_IDF_MIN_WEIGHT = 3
