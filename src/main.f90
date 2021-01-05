program main
    use precision, only: dp
    use command_line, only: cmd_line_args_type
    use read, only: read_xyz, len_max_sym
    use geometry, only: distance_matrix
    implicit none

    ! Declarations
    type(cmd_line_args_type) :: args
    real(dp), allocatable :: positions(:, :)
    character(len=len_max_sym), allocatable :: species(:)
    real(dp), allocatable :: d(:, :)
    integer :: i


    ! Main code
    write(*, *) '! Simple demo code that reads in an xyz file and computes a distance matrix'
    call args%parse()
    call read_xyz(args%input_file, positions, species)

    d = distance_matrix(positions)
    call output_distance_matrix(d)


contains

    !> Output distance matrix to stdout
    subroutine output_distance_matrix(d)
        real(dp), intent(in) :: d(:, :)
        integer :: ia, ja

        write(*, *) '! distance matrix output:'
        write(*, *) '! i, j, distance matrix(i,j)'
        do ja = 1, size(d, 2)
            do ia = 1, size(d, 1)
                write(*, *) ia, ja, d(ia, ja)
            end do
        end do

    end subroutine output_distance_matrix


end program
