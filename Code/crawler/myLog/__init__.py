import logging


class MyLoger():
    def __new__(cls, conf: dict, file_name: str=__name__):
        """
        :param file_name: input __name__
        """
        level = getattr(logging, conf.get('level', 'DEBUG'))
        conf['level'] = level
        logging.basicConfig(**conf)
        return logging.getLogger(file_name)


def method_add_log(f):
    def add_log_method(*l, **d):
        try:
            result = f(*l, **d)
            return result
        except Exception as e:
            print(str(e))
            raise ValueError
    return add_log_method


def Add_Log(log_decorator):
    """
    一个类装饰器(它用来给类的所有成员函数添加一个日志装饰器)
    装上它的类有某一个方法出错后都能执行异常处理并输出日志到文本中
    :param log_decorator: 准备应用于类中所有方法的日志装饰器
    """
    def Decorator(obj):
        def decorator_method_connector(self, decorator):
            """
            重写self里每一个成员方法，连接上日志装饰器
            :self: 类中的字典
            :param decorator: 接收到的日志装饰器
            :return:
            """
            for property_name in dir(self):
                if not property_name.startswith('__') and  not property_name.endswith('__'):
                    property_object = getattr(self, property_name)
                    if callable(property_object):
                        well_done_method = decorator(property_object)
                        well_done_method.__name__ = property_name
                        setattr(self, property_name, well_done_method)

        def rebuild__init__(decorator=log_decorator,
                            handle_decorator=decorator_method_connector,
                            origin__init__=obj.__init__):
            """
            重写类的初始化方法，重写__init__方法,
            在__init__开头植入decorator_method_connector日志连接器
            效果是当类在实例化的同时，能顺带启动被植入的“日志连接器”把log_decorator装饰器
                                                                                    加到每一个成员函数里（其实是重写方法）
            :param decorator: 接收到的日志装饰器
            :param decorator_method_connector: 连接器：把日志装饰器与每一个类方法粘连
            :param origin__init__: 源初始化方法
            :return:
            """
            def __init__(self, *l, **d):
                handle_decorator(self, decorator)
                origin__init__(self, *l, **d)
            setattr(obj, '__init__', __init__)

        rebuild__init__()
        return obj
    return Decorator

#
# logger = MyLoger(__name__)
# logger.error('This is a log info')
# logger.debug('Debugging')
# logger.warning('Warning exists')
# logger.info('Finish')
# logger.info('This is a log info')
# logger.debug('Debugging')
# logger.warning('Warning exists')
# logger.info('Finish')