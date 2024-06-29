"""
Django settings for lpdleshop project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','imenemedjaoui.pythonanywhere.com','lpdl.local']


# Application definition

INSTALLED_APPS = [
    'ecommerce',
    'django_ckeditor_5',
    'phonenumber_field',
    'jazzmin',
    #'admin_black.apps.AdminBlackConfig',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
]

JAZZMIN_SETTINGS = {
    "site_title": "La Pierre de Lune",
    "site_header": "La Pierre de Lune",
    "site_brand": "La Pierre de Lune",
    
    "site_icon": "img/admin_logo.webp",
    "custom_css": "css/jazzmin-dark.css",
    # Add your own branding here
    "site_logo": "img/admin_logo.webp",
    "welcome_sign": "Bienvenue sur La Pierre de Lune",
    # Copyright on the footer
    "copyright": "Batel Technology",
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    # "topmenu_links": [
    #     # Url that gets reversed (Permissions can be added)
    #     {"name": "your_site_name", "url": "accueil", "permissions": ["auth.view_user"]},
    #     # model admin to link to (Permissions checked against model)
    #     {"model": "auth.User"},
    # ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file",
    },
    # # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-arrow-circle-right",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    # Uncomment this line once you create the bootstrap-dark.css file
    # "custom_css": "css/bootstrap-dark.css",
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "slate",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

CRISPY_TEMPLATE_PACK="bootstrap4"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'csp.middleware.CSPMiddleware',
]

# CSP_DEFAULT_SRC = ("'none'",)
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
# CSP_SCRIPT_SRC = ("'self'", "https://maps.googleapis.com")
# CSP_CONNECT_SRC = ("'self'", "https://maps.googleapis.com")
# CSP_IMG_SRC = ("'self'",)
# CSP_REPORT_URI = '/csp-violation-report/'

CORS_ALLOWED_ORIGINS = [
    "https://www.lapierredelune.net",
]

ROOT_URLCONF = 'eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # pour Test Local
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pierre_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',  # Ou l'adresse de votre serveur MySQL
        'PORT': '3306',       # Port MySQL par défaut
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command':"SET sql_mode='STRICT_TRANS_TABLES'" # Pour activer le mode strict de MySQL, c'est une bonne pratique !
        }
    }

    # # pour PythonAnywhere
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'ImeneMedjaoui$pierre_db',
    #     'USER': 'ImeneMedjaoui',
    #     'PASSWORD': 'djangolpdl',
    #     'HOST': 'ImeneMedjaoui.mysql.pythonanywhere-services.com',
    #     'OPTIONS': {
    #         'init_command':"SET sql_mode='STRICT_TRANS_TABLES'" # Pour activer le mode strict de MySQL, c'est une bonne pratique !
    #     }
    # }
}


#AUTH_USER_MODEL = 'auth.User'  # Assurez-vous que le chemin est correct
AUTH_USER_MODEL = 'ecommerce.ClientUser'  # Assurez-vous que le chemin est correct

LOGIN_REDIRECT_URL = 'accueil'  # Replace 'home' with the actual name or path of your home page

DATE_FORMAT = 'd/m/Y'

USE_L10N = False

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/' # A CHANGER LORS DE L'HEBERGEMENT

# Spécifiez le répertoire racine des fichiers statiques
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Spécifiez l'emplacement où les fichiers statiques seront collectés lors du déploiement
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# CKEDITOR 5 SETTINGS

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
        {
                    'color': 'hsl(0, 0%, 0%)',
                    'label': 'Black'
                },
                {
                    'color': 'hsl(0, 0%, 29%)',
                    'label': 'Dim grey'
                },
                {
                    'color': 'hsl(0, 0%, 60%)',
                    'label': 'Grey'
                },
                {
                    'color': 'hsl(0, 0%, 74%)',
                    'label': 'Light grey'
                },
                {
                    'color': 'hsl(0, 0%, 87%)',
                    'label': 'Very light grey'
                },
                {
                    'color': 'hsl(0, 0%, 100%)',
                    'label': 'White'
                },
                {
                    'color': 'hsl(0, 74%, 65%)',
                    'label': 'Red'
                },
                {
                    'color': 'hsl(348, 100%, 54%)',
                    'label': 'Tomato'
                },
                {
                    'color': 'hsl(6, 100%, 67%)',
                    'label': 'Orange'
                },
                {
                    'color': 'hsl(35, 100%, 58%)',
                    'label': 'Orange red'
                },
                {
                    'color': 'hsl(45, 71%, 61%)',
                    'label': 'Gold'
                },
                {
                    'color': 'hsl(48, 100%, 50%)',
                    'label': 'Yellow'
                },
                {
                    'color': 'hsl(75, 100%, 44%)',
                    'label': 'Dark yellow'
                },
                {
                    'color': 'hsl(105, 56%, 52%)',
                    'label': 'Olive'
                },
                {
                    'color': 'hsl(133, 100%, 42%)',
                    'label': 'Lawn green'
                },
                {
                    'color': 'hsl(160, 100%, 38%)',
                    'label': 'Green'
                },
                {
                    'color': 'hsl(186, 100%, 38%)',
                    'label': 'Lime'
                },
                {
                    'color': 'hsl(210, 89%, 43%)',
                    'label': 'Aqua marine'
                },
                {
                    'color': 'hsl(240, 100%, 40%)',
                    'label': 'Turquoise'
                },
                {
                    'color': 'hsl(270, 50%, 45%)',
                    'label': 'Teal'
                },
                {
                    'color': 'hsl(292, 62%, 43%)',
                    'label': 'Light blue'
                },
                {
                    'color': 'hsl(292, 100%, 43%)',
                    'label': 'Dodger blue'
                },
                {
                    'color': 'hsl(317, 100%, 42%)',
                    'label': 'Blue'
                },
                {
                    'color': 'hsl(240, 30%, 50%)',
                    'label': 'Medium blue'
                },
                {
                    'color': 'hsl(273, 53%, 44%)',
                    'label': 'Purple'
                },
                {
                    'color': 'hsl(300, 67%, 56%)',
                    'label': 'Medium purple'
                },
                {
                    'color': 'hsl(326, 56%, 52%)',
                    'label': 'Violet'
                },
                {
                    'color': 'hsl(348, 50%, 50%)',
                    'label': 'Magenta'
                },

    ]

# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
        'language': 'fr',

    },

    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    },

    'newsletter': {
        'toolbar': {
            'items': [
                'heading', '|', 'bold', 'italic', '|', 'fontSize', 'fontFamily', 'fontColor', 'alignment', '|', 'insertImage',  'mediaEmbed', 'link',
                 '|', 'bulletedList', 'numberedList', '|','highlight', 'blockQuote', 'code', '|',
                'fontBackgroundColor', 'indent', 'outdent', '|', 'codeBlock', 'insertTable','|','undo', 'redo'
            ]
        },
        'language': 'fr',
        'image': {
            'toolbar': ['imageTextAlternative', 'imageStyle:inline', 'imageStyle:block', 'imageStyle:side', 'linkImage'],
            'styles': ['full', 'side', 'alignLeft', 'alignRight', 'alignCenter'],
        },


        'heading': {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' },
                { 'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_heading4' },
                { 'model': 'heading5', 'view': 'h5', 'title': 'Heading 5', 'class': 'ck-heading_heading5' },
                { 'model': 'heading6', 'view': 'h6', 'title': 'Heading 6', 'class': 'ck-heading_heading6' }
            ]
        },

        'fontSize': {
            'options': [10, 12, 14, 'default', 18, 20, 22],
            'supportAllValues': True
        },

        'fontFamily': {
            'options': [
                'default',
                'Arial, Helvetica, sans-serif',
                'Courier New, Courier, monospace',
                'Georgia, serif',
                'Lucida Sans Unicode, Lucida Grande, sans-serif',
                'Tahoma, Geneva, sans-serif',
                'Times New Roman, Times, serif',
                'Trebuchet MS, Helvetica, sans-serif',
                'Verdana, Geneva, sans-serif'
            ],
            'supportAllValues': True
        },
        
        'fontColor': {
            'colors': customColorPalette
        },

        'fontBackgroundColor': {
            'colors': customColorPalette
        },

        'highlight': {
            'options': [
                { 'model': 'default', 'title': 'Default', 'class': 'ck-highlight_default' },
                { 'model': 'yellowMarker', 'title': 'Yellow marker', 'class': 'ck-highlight_yellowMarker' }
            ]
        },

        'codeBlock': {
            'languages': [
                { 'language': 'plaintext', 'label': 'Plain text' },
                { 'language': 'html', 'label': 'HTML' },
                { 'language': 'css', 'label': 'CSS' },
                { 'language': 'javascript', 'label': 'JavaScript' },
                { 'language': 'python', 'label': 'Python' }
            ]
        },

        'alignment': {
            'options': ['left', 'center', 'right', 'justify']
        },

        'indent': {
            'options': ['indent', 'outdent']
        },

        'link': {
            'addTargetToExternalLinks': True,
            'defaultProtocol': 'https://'
        },

        'table': {
            'contentToolbar': [
                'tableColumn',
                'tableRow',
                'mergeTableCells',
                'tableProperties',
                'tableCellProperties'
            ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        
        'mediaEmbed': {
            'previewsInData': True
        },

    },

}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

EMAIL_HOST_USER = 'lpdl.help@gmail.com'
EMAIL_HOST_PASSWORD = 'fyre tmmb fxln kezl'
EMAIL_USE_TLS = True
# Replace with the admin email address
EMAIL_RECIPIENT = 'medjaoui.imene@gmail.com'

# Logo Base64 data
LOGO_BASE64 = ''
# Replace with the admin email address
ADRESSE_VOYANCE = 'medjaoui.imene@gmail.com'

DOMAIN_NAME = 'http://127.0.0.1:8000/'

# Replace YOUR_API_KEY with your api key
SMTP_API_KEY = 'your_api_key'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_api_key'

# Stripe settings
STRIPE_API_KEY_PUBLISHABLE = 'your_api_key'
STRIPE_API_SECRET_KEY = 'your_api_key'

# STRIPE_WEBHOOK_SECRET = 'your_webhook_secret'
# STRIPE_WEBHOOK_ENDPOINT = 'https://your-domain.com/webhooks/stripe/'
STRIPE_ENDPOINT_SECRET = 'your_api_key'