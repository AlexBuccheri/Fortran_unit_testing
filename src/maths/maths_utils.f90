!> TODO(Alex) Write a bunch of maths utils
module maths_utils
    use precision, only: wp
    implicit none
    private

    interface norm
        module procedure norm_wp_1d
    end interface

    interface set_diagonal
        module procedure set_diagonal_wp
    end interface

    interface is_square
        module procedure is_square_wp
    end interface is_square

    public :: norm, set_diagonal, is_square

contains
    !> @ Norm
    real(wp) function norm_wp_1d(a) result(norm_of_a)
        real(wp), intent(in) :: a(:)
        norm_of_a = sqrt(dot_product(a, a))
    end function norm_wp_1d

    !> Set the diagonal of a matrix with a scalar value
    subroutine set_diagonal_wp(a, value)
        real(wp), intent(inout) :: a(:,:)
        real(wp), intent(in) :: value
        integer :: i
        ! assert(size(a,1) == size(a,2))
        do i = 1, size(a, 1)
            a(i,i) = value
        end do
    end subroutine set_diagonal_wp

    logical function is_square_wp(A) result(square)
        real(wp), intent(in) :: A(:,:)
        square = size(A, 1) == size(A, 2)
    end function is_square_wp


end module maths_utils