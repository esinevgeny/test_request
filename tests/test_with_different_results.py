import sys
import pytest


@pytest.mark.skip("JI: ###; Description")
def test_fails():
    """
    Skipped test
    :return: None
    """
    assert 0 == 1


# def test_real_failed():
#     """
#     Failed test
#     :return: None
#     """
#     assert 0 == 1


@pytest.mark.skipif(sys.version_info <= (2, 7), reason=f"Test is supported only for versions <= 2.7."
                                                       f"Current: {sys.version_info}")
def test_check_skip():
    """
    This test should not be performed if os version is '7.0.0'
    :return: None
    """
    assert 0 == 0


@pytest.mark.skipif(sys.version_info >= (2, 7), reason=f"Test is supported only for versions >= 2.7."
                                                       f"Current: {sys.version_info}")
def test_check_not_skip(return_test_data):
    """
    This test should be performed if os version is not '7.0.0'
    :return: None
    """
    print(return_test_data)
    assert return_test_data == range(3, 90, 2)


if __name__ == '__main__':
    pytest.main()
