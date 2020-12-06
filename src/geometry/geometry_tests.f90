!> Module to test geometry functions and routines
!
! Notes:
! Can generate the driver program with:
!   PATH_TO/zofu-driver geometry_tests.f90 geometry_tests_driver.f90
! or if using MPI:
!   PATH_TO/zofu-driver geometry_tests.f90 geometry_tests_driver.f90 --mpi
! But doesn't seem like much point. Just manually write it as so
!
module geometry_tests
    use zofu,        only: unit_test_type
    use precision,   only: wp
    use asserts,     only: assert
    use maths_utils, only: is_square

    !> Module being tested
    use geometry,  only: distance_matrix

    implicit none

    type(unit_test_type) :: geom_test


!    call geom_test%init()
!    call geom_test%run(test_distance_matrix, &
!            '! Test distance matrix when passing an array of positions')
!    call geom_test%summary()

contains

    subroutine test_distance_matrix(geom_test)
        ! Test distance matrix when passing an array of positions
        class(unit_test_type), intent(inout) :: geom_test

        !> Number of atoms
        integer, parameter :: n_atoms = 4

        !> Atomic coordinates, written row-wise but stored columnwise
        real(wp), dimension(3, n_atoms) :: positions = &
        reshape([1._wp, 1._wp, 1._wp, &
                 2._wp, 2._wp, 2._wp, &
                 3._wp, 3._wp, 3._wp, &
                 4._wp, 4._wp, 4._wp], [3, n_atoms])

        !> Distance matrix
        real(wp), allocatable :: d(:,:)


        d = distance_matrix(positions)
        call assert(.not. allocated(d), &
                message = "d is allocated (deliberate so one can check the assertion)")

        call geom_test%assert(all(positions(:, 1) == [1._wp, 1._wp, 1._wp]), &
            name = 'Atomic positions not stored per column')
        call geom_test%assert(n_atoms == 4, name = 'n_atoms /= 4')
        call geom_test%assert(size(d, 2) == 4,  name = 'size(d, 2) /= 4')
        call geom_test%assert(is_square(d), name = 'd is not square')
        call geom_test%assert(d, transpose(d), name = 'd is not square (d /= d^T)')

    end subroutine test_distance_matrix


end module geometry_tests