class BaseConfig(object):
    SECRET_KEY = 'dfes34dfgw4egdfg345#$%@edsfs112~$^ge335'
    INDEX_PER_PAGE = 9

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:Abcd1234@10.6.0.127:3306/flyflask?charset=utf8'


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

