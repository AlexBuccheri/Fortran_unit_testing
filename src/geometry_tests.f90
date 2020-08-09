!> Module to test geometry functions and routines
module geometry_tests
    use zofu
    use constants, only: wp
    use geometry, only: distance_matrix
    private

    !> Test object
    type(unit_test_type) :: geom_test


contains

    ! TODO(Alex) Clean this junk up
    !
    !    subroutine test_distance_matrix(geom_test)
!        ! Test distance matrix when passing an array of positions
!        class(unit_test_type), intent(inout) :: geom_test
!
!        real(wp), dimension(4,3) :: positions = [[1._wp, 1._wp, 1._wp,],
!                                                2._wp, 3._wp, 4._wp]]
!        real(wp), allocatable :: d_transpose(:,:)
!        integer :: n_atoms
!
!        n_atoms = size(positions)
!        d = distance_matrix(molecule)
!        call geom_test%assert(size(d, 1) == 4,  name = 'size(d, 1) == 4')
!        call geom_test%assert(is_square(d), name = 'is_square(d)')
!
!        allocate(d_transpose(n_atoms, n_atoms))
!        d_transpose = transpose(d)
!        call geom_test%assert(d, d_transpose, name = 'd = d^T')
!
!    end subroutine test_distance_matrix


end module geometry_tests