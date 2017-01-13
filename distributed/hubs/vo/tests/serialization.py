__author__ = 'civa'

from jsonweb.encode import dumper

from hubs.vo.model.observation_data import *
from hubs.vo.model.test_object import TestObject


def main():
    test = TestObject()
    # test.add_simple_part(SimpleItem('TestSingle',   Values(
    #                                    'TestValue',
    #                                    'TestValue'
    #                                 )))
    test.add_simple_part(SimpleItem('TestSingle2',
                                        SimpleValue('TestValue2'),
                                        SimpleValue('TestValue2')
    ))

    test.add_complex_part(ComplexItem(
        'TestSingleValue1', ComplexValue(
            'TestValue', 'm', '+3.6'
        ),
        ComplexValue(
            'TestValue', 'm', '+3.6'
        )
    ))

    test.add_complex_part(ComplexItem(
        'TestSingleValue2', ComplexValue(
            'TestValue', 'm', '-3.6'
        ),
        ComplexValue(
            'TestValue', 'm', '+3.6'
        )
    ))

    # test.add_complex_part(ComplexItem(
    #     'TestSingleValue3', ComplexValue(
    #         'TestValue', 'm', '+3.6'
    #     )
    # ))

    # test.add_composite_part(CompositeItem(
    #     "Composite",
    #     SimpleItem("TestComposite1", "TestCompVal1"),
    #     SimpleItem("TestComposite1", "TestCompVal1")
    #     # CompositeParts(
    #     #     SinglePart('TestComposite3', 'TestValue3', 'm3'),
    #     #     SinglePart('TestComposite4', 'TestValue4', 'm4')
    #     # )
    # ))

    test.add_multi_part(MultiItem(
        'TestMulti1',
                SimpleValue('MultiValue1'),
                SimpleValue('MultiValue2'),
                SimpleValue('MultiValue3')
        )
        # 'TestMulti1',
        #     SimpleValue('MultiValue1'),
        #     SimpleValue('MultiValue2'),
        #     SimpleValue('MultiValue3')
        # )
        # 'TestMulti1', MultiValue(
        #     'MultiValue1',
        #     'MultiValue2',
        #     'MultiValue3'
        # )
    )

    print dumper(test, indent=2)
    # cel_obj = CelestialObjectEx(
    #     DataPart('test1', 'testval1', 'km'),
    #     DataPart('test2', 'testval2', 'm'),
    #     DataPart('test3', 'testval3', 'km/s')
    # )
#
    #print dumper(cel_obj)
    #parts = []
##
    #part = DataPart('test1', 'testval1', 'km')
    #part2 = DataPart('test2', 'testval2', 'm')
    #part3 = DataPart('test3', 'testval3', 'km/s')
##
    #parts.append(part)
    #parts.append(part2)
    #parts.append(part3)
#
    #cel_obj = CelestialObjectEx(parts)

    #print dumper(cel_obj)

if __name__ == "__main__":
    main()
