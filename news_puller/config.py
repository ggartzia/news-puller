HOST_URL = 'https://news-puller.herokuapp.com/'
PAPER_LIST = [
    {
      'paper': 'elpais',
      'name': 'EL PAÍS',
      'feed': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada',
      'theme': 'noticias'
    },
    {
      'paper': 'elpais',
      'name': 'EL PAÍS',
      'feed': 'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/deportes/portada',
      'theme': 'deportes'
    },
    {
      'paper': 'infocorazon',
      'name': 'Info Corazón',
      'feed': 'http://www.infocorazon.com/feed/',
      'theme': 'corazon'
    },
    {
      'paper': 'elmundo',
      'name': 'El Mundo',
      'feed': 'https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml',
      'theme': 'noticias'
    },
    {
      'paper': 'elmundo',
      'name': 'El Mundo',
      'feed': 'https://e00-elmundo.uecdn.es/elmundodeporte/rss/portada.xml',
      'theme': 'deportes'
    },
    {
      'paper': 'huffington',
      'name': 'Huffington Post',
      'feed': 'https://www.huffingtonpost.es/feeds/index.xml',
      'theme': 'noticias'
    },
    {
      'paper': 'vanguardia',
      'name': 'La Vanguardia',
      'feed': 'https://www.lavanguardia.com/rss/home.xml',
      'theme': 'noticias'
    },
    {
      'paper': 'vanguardia',
      'name': 'La Vanguardia',
      'feed': 'https://www.lavanguardia.com/rss/deportes.xml',
      'theme': 'deportes'
    },
    {
      'paper': 'vanguardia',
      'name': 'La Vanguardia',
      'feed': 'https://www.lavanguardia.com/rss/gente.xml',
      'theme': 'corazon'
    },
    {
      'paper': 'confidencial',
      'name': 'El Confidencial',
      'feed': 'https://rss.elconfidencial.com/espana/',
      'theme': 'noticias'
    },
    {
      'paper': 'confidencial',
      'name': 'El Confidencial',
      'feed': 'https://rss.elconfidencial.com/deportes/',
      'theme': 'deportes'
    },
    {
      'paper': 'vanitatis',
      'name': 'Vanitatis',
      'feed': 'https://rss.vanitatis.elconfidencial.com/noticias/',
      'theme': 'corazon'
    },
    {
      'paper': 'publico',
      'name': 'Público',
      'feed': 'https://www.publico.es/rss/politica',
      'theme': 'noticias'
    },
    {
      'paper': 'okdiario',
      'name': 'OKDiario',
      'feed': 'https://okdiario.com/feed',
      'theme': 'noticias'
    },
    {
      'paper': 'esdiario',
      'name': 'ES Diario',
      'feed': 'https://www.esdiario.com/rss/articulos.xml',
      'theme': 'noticias'
    },
    {
      'paper': 'marca',
      'name': 'Marca',
      'feed': 'https://e00-marca.uecdn.es/rss/portada.xml',
      'theme': 'deporte'
    },
    {
      'paper': 'as',
      'name': 'AS',
      'feed': 'https://as.com/rss/tags/ultimas_noticias.xml',
      'theme': 'deporte'
    },
    {
      'paper': 'hola',
      'name': 'Revista ¡HOLA!',
      'feed': 'https://www.hola.com/famosos/rss.xml',
      'theme': 'corazon'
    },
    {
      'paper': 'lecturas',
      'name': 'Lecturas',
      'feed': 'https://www.lecturas.com/feeds/rss',
      'theme': 'corazon'
    },
    {
      'paper': 'diezminutos',
      'name': 'Diez minutos',
      'feed': 'https://www.diezminutos.es/rss/all.xml/',
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
