module maths_utils_tests
    use precision,   only: wp
    use maths_utils, only: set_diagonal, is_square
    use zofu,        only: unit_test_type
    implicit none

    type(unit_test_type) :: maths_test

contains

    subroutine test_is_square(maths_test)
        ! Test is_square
        class(unit_test_type), intent(inout) :: maths_test
        real(wp), dimension(4, 4) :: A
        real(wp), dimension(4, 3) :: B

        call maths_test%assert(is_square(A),  name = 'A is square')
        call maths_test%assert(.not. is_square(B),  name = 'B is not square')

    end subroutine test_is_square


    subroutine test_diagonal(maths_test)
        ! Test setting the diagonal of a square matrix
        class(unit_test_type), intent(inout) :: maths_test
        real(wp), dimension(3, 3) :: A = 1._wp
        integer :: i

        call maths_test%assert(is_square(A),  name = 'A is square')
        call set_diagonal(A, 2._wp)

        do i = 1, size(A, 1)
            call maths_test%assert(A(i,i) == 2._wp,  name = 'Diagonal is 2')
        end do

    end subroutine test_diagonal


end module maths_utils_tests