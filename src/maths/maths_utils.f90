! TODO(Alex) Write a bunch of maths utils
! Also worth adopting a bunch of these: http://hornekyle.github.io/CommonModules/

!> Maths utilities
module maths_utils
    use precision, only: wp
    use asserts,   only: assert
    implicit none
    private

    !> @brief A generic interface for computing the Euclidean norm of a vector
    interface norm
        module procedure norm_wp_1d
    end interface

    !> A generic interface for setting the diagonal elements of a two-dimensional array
    interface set_diagonal
        module procedure set_diagonal_wp, set_diagonal_with_vector_wp
    end interface

    !> A generic interface for checking if a two-dimensional array is square
    interface is_square
        module procedure is_square_wp
    end interface is_square

    public :: norm, set_diagonal, is_square

contains

    !> @brief Check if a two-dimensional array is square
    !>
    !> @param A Two-dimensional array
    logical function is_square_wp(A) result(square)
        real(wp), intent(in) :: A(:,:)
        square = size(A, 1) == size(A, 2)
    end function is_square_wp


    !> @brief Compute the Euclidean norm of a vector
    !>
    !> @param a One-dimensional vector of arbitrary length
    real(wp) function norm_wp_1d(a) result(norm_of_a)
        real(wp), intent(in) :: a(:)
        norm_of_a = sqrt(dot_product(a, a))
    end function norm_wp_1d


    !> Set the diagonal of a 2D matrix with a scalar value
    !>
    !> @param a Two-dimensional matrix
    !> @param value Scalar value for all diagonal elements
    subroutine set_diagonal_wp(a, value)
        real(wp), intent(inout) :: a(:,:)
        real(wp), intent(in) :: value
        integer :: i
        call assert(is_square_wp(a), "array is not square")
        do i = 1, size(a, 1)
            a(i,i) = value
        end do
    end subroutine set_diagonal_wp


    !> Set the diagonal of a 2D matrix with a vector
    !>
    !> @param a Two-dimensional matrix
    !> @param x One-dimensional vector
    subroutine set_diagonal_with_vector_wp(a, x)
        real(wp), intent(inout) :: a(:,:)
        real(wp), intent(in) :: x(:)
        integer :: i

        call assert(is_square_wp(a), "array is not square")
        call assert(size(a, 1) == size(x), "diagonal of a and length of x differ in size")

        do i = 1, size(a, 1)
            a(i,i) = x(i)
        end do

    end subroutine set_diagonal_with_vector_wp

end module maths_utils