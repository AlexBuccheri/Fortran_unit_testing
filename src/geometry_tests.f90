!> Module to test geometry functions and routines
!
! Notes:
! Can generate the driver program with:
!   PATH_TO/zofu-driver geometry_tests.f90 geometry_tests_driver.f90
! or if using MPI:
!   PATH_TO/zofu-driver geometry_tests.f90 geometry_tests_driver.f90 --mpi
! But doesn't seem like much point. Just manually write it as so
!
program geometry_tests
    use zofu
    use constants, only: wp
    use geometry, only: distance_matrix

    type(unit_test_type) :: geom_test

    call geom_test%init()
    call geom_test%run(test_distance_matrix, &
            '! Test distance matrix when passing an array of positions')
    call geom_test%summary()

contains

    ! TODO(Alex) Clean this junk up
    subroutine test_distance_matrix(geom_test)
        ! Test distance matrix when passing an array of positions
        class(unit_test_type), intent(inout) :: geom_test

        !real(wp), dimension(4,3) :: positions = [[1._wp, 1._wp, 1._wp,],
        !                                        2._wp, 3._wp, 4._wp]]
!        real(wp), allocatable :: d_transpose(:,:)
!        integer :: n_atoms

        call geom_test%assert(4 == 4,  name = '4 == 4')

!        n_atoms = size(positions)
!        d = distance_matrix(molecule)
!        call geom_test%assert(size(d, 1) == 4,  name = 'size(d, 1) == 4')
!        call geom_test%assert(is_square(d), name = 'is_square(d)')
!
!        allocate(d_transpose(n_atoms, n_atoms))
!        d_transpose = transpose(d)
!        call geom_test%assert(d, d_transpose, name = 'd = d^T')

    end subroutine test_distance_matrix


end program geometry_tests