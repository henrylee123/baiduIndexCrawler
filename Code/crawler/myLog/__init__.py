
import logging
from functools import wraps
from setting import  log_conf
import copy


def defalut_log_decorator(myloger):
    def decorater(f):
        def add_log_method(*l, **d):
            myloger.info('start ' + f.__name__)
            try:
                result = f(*l, **d)
                return result
            except Exception as e:
                myloger.error(f.__name__ + str(e))
                raise e
            finally:
                myloger.info('end ' + f.__name__)

        return add_log_method
    return decorater


class MyLoger():
    def __new__(cls, conf: dict, file_name: str):
        """
        :param file_name: input __name__
        """
        level = getattr(logging, conf.get('level', 'DEBUG'))
        tmp_conf = copy.deepcopy(conf)
        tmp_conf['level'] = level
        logging.basicConfig(**tmp_conf)
        return logging.getLogger(file_name)


# 类log装饰器
def Add_Log(file_name, method_decorator=None, conf=log_conf):
    """
    一个类装饰器(它用来给类的所有成员函数添加一个日志装饰器)
    装上它的类有某一个方法出错后都能执行异常处理并输出日志到文本中
    :param method_decorator: 准备应用于类中所有方法的日志装饰器
    """
    myloger = MyLoger(conf, file_name)
    if method_decorator is None:
        method_decorator = defalut_log_decorator

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

        def rebuild__init__(decorator=method_decorator(myloger),
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
