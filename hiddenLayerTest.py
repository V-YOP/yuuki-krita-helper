from krita import Krita

Krita.instance().activeDocument().dynamicPropertyNames()
for node in Krita.instance().activeDocument().topLevelNodes():

    print(f"{node.name()=}")
    print(f"{node.objectName()=}")
    print(f"{node.uniqueId()=}")
    print(f"{node.hasExtents()=}")
    print(f"{node.type()=}")
    print(f"{node.childNodes()=}")
    print(f"{node.index()=}")
    print(f"{node.dynamicPropertyNames()=}")
    print(f"{node.metaObject()=}")
    print(f"{node.staticMetaObject=}")
    print(f"{node.metaObject().propertyCount()=}")
    print(f"{node.staticMetaObject.propertyCount()=}")
    print(f"{node.__class__=}")
    for i in range(0, node.metaObject().propertyCount()):
        prop = node.metaObject().property(i)
        print(f"{prop.name()=}, {prop.type()=}, {prop.read(node)=}")

    for i in range(0, node.staticMetaObject.propertyCount()):
        prop = node.staticMetaObject.property(i)
        print(f"{prop.name()=}, {prop.type()=}, {prop.read(node)=}")

    print(f"{Krita.instance().activeDocument().dynamicPropertyNames()=}")
    print('---')

