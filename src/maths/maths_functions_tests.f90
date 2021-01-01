module maths_functions_tests
    use zofu,        only: unit_test_type
    use precision,   only: wp
    !> Module being tested
    use maths_functions, only: sgn

    implicit none
    private

    public :: test_sgn_function

contains

     subroutine test_sgn_function(tester)
        ! Test sgn function for x = positive, negative and zero
        class(unit_test_type), intent(inout) :: tester

        call tester%assert(sgn(2.1_wp) == 1._wp, name = 'sgn(2.1) /= 1')
        call tester%assert(sgn(-3.4_wp) == -1._wp, name = 'sgn(-3.4) /= -1')
        call tester%assert(sgn(0._wp) == 0._wp, name = 'sgn(0) /= 0')
        call tester%assert(sgn(1._wp) == 1._wp, name = 'sgn(1) /= 1')
        call tester%assert(sgn(-1._wp) == -1._wp, name = 'sgn(-1) /= -1')

    end subroutine test_sgn_function

end module maths_functions_tests