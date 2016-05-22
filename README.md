虚拟机管理系统整体分为两个模块：web模块和脚本模块

脚本模块

主要功能：虚拟机的创建与销毁
子模块：
1、参数解析
使用argparse库，将管理员输入的参数转化为参数字典
2、image创建
复制已有的image模版，以输入dst_disk的参数命名新的image
3、生成Xml模版文件
使用xmltree库解析模版Xml文件，将虚拟机的cpu，memory，diskpath，
4、虚拟机创建与销毁
硬盘和xml文件准备好后，使用os.system()调用virsh define以及virsh create命令定义和创建虚拟机
销毁虚拟机使用virsh undefine命令，同时从数据库删除该虚拟机的纪录
5、数据库操作
使用sqlalchemy库，实现vmtools_vm这个表与VM类的映射
当参数为创建虚拟机时，将虚拟机的信息插入到数据库中
当参数为删除虚拟机时，将虚拟机信息从数据库中删除

web模块
主要功能：实现用户对虚拟机的开关机以及申请操作
子模块：
1、视图模块
子功能：
注册：调用Django的UserCreationForm()类，将表单中的注册信息存入数据库，实现注册
认证：调用Django的authenticate()函数将表单中的认证数据与数据库中用户信息进行对比
申请：在前台页面申请表单中的参数传到视图中处理申请虚拟机的函数，将申请消息存入数据库
2、模型模块
models.py：使用sqlalchemy库，实现数据库表与python类的映射
3、控制模块
url.py：处理url与视图函数的映射。
